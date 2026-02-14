from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os
class ChromaStore:

    def __init__(self, persist_directory="memory/chroma_db"):

        self.persist_directory = persist_directory

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model
        )

    def add_documents(self, documents):
        if not documents:
            return
        self.vectorstore.add_documents(documents)
        # self.vectorstore.persist() # Deprecated in Chroma 0.4.x

    def similarity_search(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)