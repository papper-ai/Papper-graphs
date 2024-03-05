from src.utils.spacy import nlp
import logging


class KB:
    def __init__(self):
        self.relations = []

    async def relations_equal(self, relation1, relation2):
        return all(
            relation1[attr] == relation2[attr] for attr in ["head", "type", "tail"]
        )

    async def relation_exists(self, r1):
        return any([await self.relations_equal(r1, r2) for r2 in self.relations])

    async def add_relation(self, relation, document_id):
        logging.info(relation)
        relation["meta"]["document_id"] = document_id
        if not await self.relation_exists(relation):
            self.relations.append(relation)

    async def lemmatize(self, text):
        doc = nlp(text)
        return " ".join([token.lemma_ for token in doc])

    async def filter_relations(self):
        seen_head_type_pairs = set()
        seen_head_tail_pairs = set()
        filtered_relations = []

        for entry in self.relations:
            # Lemmatize head and tail in place
            entry["head"] = (
                (await self.lemmatize(entry["head"])).strip().replace("- ", "")
            )
            entry["tail"] = (
                (await self.lemmatize(entry["tail"])).strip().replace("- ", "")
            )

            # Skip entry if head is equal to tail
            if entry["head"] == entry["tail"]:
                continue

            # Create pairs for checking
            head_type_pair = (entry["head"], entry["type"])
            head_tail_pair = (entry["head"], entry["tail"])

            # Check if we've seen this head with this type before
            if head_type_pair not in seen_head_type_pairs:
                seen_head_type_pairs.add(head_type_pair)

                # Check if we've seen this head-tail pair before
                if head_tail_pair not in seen_head_tail_pairs:
                    seen_head_tail_pairs.add(head_tail_pair)
                    filtered_relations.append(entry)

        unwanted_types = [
            "изучается в",
            "испытал влияние от",
            "тематически относится к",
            "противоположно",
            "не путать с",
        ]
        filtered_relations = [
            r for r in filtered_relations if r.get("type") not in unwanted_types
        ]

        self.relations = filtered_relations

    async def generate_cypher_statements(self):
        cypher_statements = []

        data = self.relations

        # Create all unique nodes without any properties
        unique_nodes = set(item["head"] for item in data) | set(
            item["tail"] for item in data
        )
        for node in unique_nodes:
            cypher_statements.append(f"MERGE (:Node {{name: '{node}'}})")

        # Create all relationships with `meta`
        for item in data:
            head = item["head"]
            relation_type = item["type"]
            tail = item["tail"]
            meta = item["meta"]

            # Build the meta string
            meta_parts = []
            for k, v in meta.items():
                value = str(v).replace("'", "\\'")
                meta_parts.append(f"{k}: '{value}'")
            meta_str = ", ".join(meta_parts)

            # Create the relationship with the meta data
            statement = (
                f"MATCH (h:Node {{name: '{head}'}}), (t:Node {{name: '{tail}'}}) "
                f"MERGE (h)-[:`{relation_type}` {{{meta_str}}}]->(t)"
            )
            cypher_statements.append(statement)

        return cypher_statements

    def print(self):
        print(f"Total number of relations: {len(self.relations)}\n")
        print("Relations:")
        for r in self.relations:
            print(f"  {r}")
