# main.py

import os
import gradio as gr
from urllib.parse import urlparse
from loader import DocumentLoader
from retrieval_chain import RetrievalChainHandler
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def main_app(sitemap, query):
    parsed_uri = urlparse(sitemap)
    domain = parsed_uri.netloc

    persist_directory = os.path.join("db", domain)

    documents = None
    if not os.path.exists(persist_directory):
        document_loader = DocumentLoader(sitemap)
        document = document_loader.load_document()

        text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
        documents = text_splitter.split_documents(document)

        retrieval_chain_handler = RetrievalChainHandler(documents, persist_directory)
        retrieval_chain_handler.generate_vectorstore() # generamos y guardamos el vectorstore
    else:
        retrieval_chain_handler = RetrievalChainHandler(None, persist_directory)

    vectorstore = retrieval_chain_handler.get_vectorstore()

    answer = retrieval_chain_handler.execute_chain(vectorstore, query)
    return answer

if __name__ == "__main__":
    main_app(input("Añade tu sitemap: "), input("Añade tu pregunta: "))