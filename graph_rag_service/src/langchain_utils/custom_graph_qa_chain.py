"""Custom question answering over a graph."""

from __future__ import annotations

import logging
import random
import re
from typing import Any, Dict, List, Optional

from langchain.chains.base import Chain
from langchain.chains.graph_qa.prompts import CYPHER_GENERATION_PROMPT, CYPHER_QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate

from src.database.neo4j import neo4j_async_driver
from src.database.queries import get_graph_view

INTERMEDIATE_STEPS_KEY = "intermediate_steps"


def construct_schema(triplets: List[Dict[str]]) -> str:
    """Filter the schema based on included or excluded types"""

    relations = []
    schema = ""

    logging.info(f"Triplets: {len(triplets)}")
    
    if len(triplets) > 250:
        schema += f"Showing only 250 of {len(triplets)}, rerun tool to see more."
        triplets = random.sample(triplets, 250)
        
    for triplet in triplets:
        relation = (
            f'({triplet["n.name"]})-[{triplet["relationship"]}]->({triplet["m.name"]})'
        )
        relations.append(relation)

    schema += ",".join(relations)
    return schema


async def extract_cypher(text: str) -> str:
    """Extract Cypher code from a text.

    Args:
        text: Text to extract Cypher code from.

    Returns:
        Cypher code extracted from the text.
    """
    # The pattern to find Cypher code enclosed in triple backticks
    pattern = r"```(.*?)```"

    # Find all matches in the input text
    matches = re.findall(pattern, text, re.DOTALL)

    return matches[0] if matches else text


async def parse_list(input: str) -> List[str]:
    try:
        # This pattern matches items enclosed in single or double quotes
        # It allows for quotes inside the items as long as they are not at the edges.
        pattern = re.compile(r'(?<!\\)["\']([^"\']+?)["\'](?!\\)')
        # Find all non-greedy matches that are not preceded or followed by a backslash
        # This avoids capturing escaped quotes
        matches = pattern.findall(input)
        results = [match.strip().lower() for match in matches[:5]]
        return results
    except Exception as e:
        # Log the error or handle it as needed
        print(f"An error occurred while parsing the list: {e}")
        return []


class CustomGraphCypherQAChain(Chain):
    """Chain for question-answering against a graph by generating Cypher statements.

    *Security note*: Make sure that the database connection uses credentials
        that are narrowly-scoped to only include necessary permissions.
        Failure to do so may result in data corruption or loss, since the calling
        code may attempt commands that would result in deletion, mutation
        of data if appropriately prompted or reading sensitive data if such
        data is present in the database.
        The best way to guard against such negative outcomes is to (as appropriate)
        limit the permissions granted to the credentials used with this tool.

        See https://python.langchain.com/docs/security for more information.
    """

    cypher_generation_chain: LLMChain
    qa_chain: LLMChain
    graph_schema: str
    input_key: str = "query"  #: :meta private:
    output_key: str = "result"  #: :meta private:
    graph_kb_name: Optional[str] = None
    """Number of results to return from the query"""
    return_intermediate_steps: bool = False
    """Whether or not to return the intermediate steps along with the final answer."""
    return_direct: bool = False
    """Whether or not to return the result of querying the graph directly."""

    @property
    def input_keys(self) -> List[str]:
        """Return the input keys.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Return the output keys.

        :meta private:
        """
        _output_keys = [self.output_key]
        return _output_keys

    @property
    def _chain_type(self) -> str:
        return "graph_cypher_chain"

    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        *,
        graph_kb_name: Optional[str] = None,
        qa_prompt: Optional[BasePromptTemplate] = None,
        cypher_prompt: Optional[BasePromptTemplate] = None,
        cypher_llm: Optional[BaseLanguageModel] = None,
        qa_llm: Optional[BaseLanguageModel] = None,
        exclude_types: List[str] = [],
        include_types: List[str] = [],
        qa_llm_kwargs: Optional[Dict[str, Any]] = None,
        cypher_llm_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> CustomGraphCypherQAChain:
        """Initialize from LLM."""

        if not cypher_llm and not llm:
            raise ValueError("Either `llm` or `cypher_llm` parameters must be provided")
        if not qa_llm and not llm:
            raise ValueError("Either `llm` or `qa_llm` parameters must be provided")
        if cypher_llm and qa_llm and llm:
            raise ValueError(
                "You can specify up to two of 'cypher_llm', 'qa_llm'"
                ", and 'llm', but not all three simultaneously."
            )
        if cypher_prompt and cypher_llm_kwargs:
            raise ValueError(
                "Specifying cypher_prompt and cypher_llm_kwargs together is"
                " not allowed. Please pass prompt via cypher_llm_kwargs."
            )
        if qa_prompt and qa_llm_kwargs:
            raise ValueError(
                "Specifying qa_prompt and qa_llm_kwargs together is"
                " not allowed. Please pass prompt via qa_llm_kwargs."
            )
        use_qa_llm_kwargs = qa_llm_kwargs if qa_llm_kwargs is not None else {}
        use_cypher_llm_kwargs = (
            cypher_llm_kwargs if cypher_llm_kwargs is not None else {}
        )
        if "prompt" not in use_qa_llm_kwargs:
            use_qa_llm_kwargs["prompt"] = (
                qa_prompt if qa_prompt is not None else CYPHER_QA_PROMPT
            )
        if "prompt" not in use_cypher_llm_kwargs:
            use_cypher_llm_kwargs["prompt"] = (
                cypher_prompt if cypher_prompt is not None else CYPHER_GENERATION_PROMPT
            )

        qa_chain = LLMChain(llm=qa_llm or llm, **use_qa_llm_kwargs)  # type: ignore[arg-type]

        cypher_generation_chain = LLMChain(
            llm=cypher_llm or llm,  # type: ignore[arg-type]
            **use_cypher_llm_kwargs,  # type: ignore[arg-type]
        )

        if exclude_types and include_types:
            raise ValueError(
                "Either `exclude_types` or `include_types` "
                "can be provided, but not both"
            )

        graph_view = get_graph_view(db_name=graph_kb_name)
        graph_schema = construct_schema(triplets=graph_view)

        logging.info(graph_schema)
        
        return cls(
            graph_schema=graph_schema,
            graph_kb_name=graph_kb_name,
            qa_chain=qa_chain,
            cypher_generation_chain=cypher_generation_chain,
            **kwargs,
        )

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError()

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Generate Cypher statement, use it to look up in db and answer question."""
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        question = inputs[self.input_key]

        intermediate_steps: List = []

        nodes_string = self.cypher_generation_chain.run(
            {"question": question, "schema": self.graph_schema}, callbacks=callbacks
        )

        nodes = await parse_list(nodes_string)
        logging.info(nodes)

        generated_cyphers = [
            f"MATCH (a)-[r]-(b) WHERE a.name = '{node.lower()}' RETURN r"
            for node in nodes
        ]

        await _run_manager.on_text("Generated Cypher:", end="\n", verbose=self.verbose)
        await _run_manager.on_text(
            generated_cyphers, color="green", end="\n", verbose=self.verbose
        )

        # Retrieve the results
        if generated_cyphers:
            results = []
            context = []
            for generated_cypher in generated_cyphers:
                try:
                    result = [
                        {
                            "document_id": record["r"]["document_id"],
                            "document_name": record["r"]["document_name"] if record["r"]["document_name"] else None,
                            "information": record["r"]["information"],
                        }
                        for record in (
                            await neo4j_async_driver.execute_query(
                                query_=generated_cypher, database_=self.graph_kb_name
                            )
                        ).records
                    ]
                    
                    results.append(result)
                    context.extend([context["information"] for context in result])
                except Exception as e:
                    logging.error(e)
            
            # Deduplicate context (a list of strings) for LLM input
            context = list(set(context))
        else:
            results = []
            context = []

        if self.return_direct:
            final_result = context
        else:
            await _run_manager.on_text("Full Context:", end="\n", verbose=self.verbose)
            await _run_manager.on_text(
                str(context), color="green", end="\n", verbose=self.verbose
            )

            for generated_cypher, results in zip(generated_cyphers, results):
                intermediate_steps.append(
                    {"query": generated_cypher, "results": results}
                )

            result = self.qa_chain(
                {"question": question, "context": context},
                callbacks=callbacks,
            )
            final_result = result[self.qa_chain.output_key]

        chain_result: Dict[str, Any] = {self.output_key: final_result}
        if self.return_intermediate_steps:
            chain_result[INTERMEDIATE_STEPS_KEY] = intermediate_steps

        return chain_result
