import sys
sys.path.append('back_end')
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from back_end.chunk_semantically import semantic_retriever

chunks = semantic_retriever('file.txt')
vectorstore = FAISS.from_texts(
    chunks, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever(search_kwargs={"k" : 5}) # Specifying the value of "k" 
relevant_docs = retriever.get_relevant_documents("What are the challenges in evaluating Retrieval Augmented Generation pipelines?")
