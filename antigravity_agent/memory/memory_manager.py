from langchain_core.documents import Document
from memory.vector_store import ChromaStore
from datetime import datetime
import json


class MemoryManager:

    def __init__(self):
        self.store = ChromaStore()

    def store_raw_results(self, results, query=None, iteration=0):

        documents = []

        for content in results:
            metadata = {
                "type": "raw_research",
                "query": query,
                "iteration": iteration,
                "timestamp": str(datetime.utcnow())
            }

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

        self.store.add_documents(documents)

    def store_compressed_context(self, context, iteration=0):

        metadata = {
            "type": "compressed_context",
            "iteration": iteration,
            "timestamp": str(datetime.utcnow())
        }

        doc = Document(
            page_content=json.dumps(context),
            metadata=metadata
        )

        self.store.add_documents([doc])

    def store_reflection(self, reflection_data, iteration=0):

        metadata = {
            "type": "reflection_note",
            "iteration": iteration,
            "timestamp": str(datetime.utcnow())
        }

        doc = Document(
            page_content=json.dumps(reflection_data),
            metadata=metadata
        )

        self.store.add_documents([doc])

    def retrieve(self, query, top_k=3, memory_type=None):

        results = self.store.similarity_search(query, k=top_k)

        if memory_type:
            results = [
                doc for doc in results
                if doc.metadata.get("type") == memory_type
            ]

        return [doc.page_content for doc in results]
