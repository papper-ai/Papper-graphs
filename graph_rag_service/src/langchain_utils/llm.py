import asyncio
import logging
from typing import Any, List, Mapping, Optional

import aiohttp
import httpx
import langchain
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM, BaseLLM
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_community.llms.gigachat import GigaChat
from langchain_openai import ChatOpenAI

'''
class С4aiLLM(BaseLLM):
    llm_url: str = "http://host.docker.internal:8088/generate"

    def _llm_type(self) -> str:
        return "C4AI 4bit"

    def _generate(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        raise NotImplementedError()

    async def _agenerate(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # if stop is not None:
        #    raise ValueError("stop kwargs are not permitted.")

        logging.info(f"prompt: {prompt[0]}")
        payload = {"prompt": prompt[0], "max_tokens": 48}

        headers = {"accept": "application/json", "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.llm_url,
                json=payload,
                headers=headers,  # ssl=False
            ) as response:
                logging.info(f"HTTP Status Code: {response.status}")
                result = await response.json()

        logging.info(result)

        return (
            result["generated_text"]
            .split("<|CHATBOT_TOKEN|>")[-1]
            .replace("<|END_OF_TURN_TOKEN|>", "")
        )

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"llm_url": self.llm_url}

llm = С4aiLLM()'''

llm = GigaChat()

langchain.debug = True
llm = ChatOpenAI(
    base_url="http://host.docker.internal:8001/v1/",
    api_key="sk-no-key-required",
    verbose=True,
)
