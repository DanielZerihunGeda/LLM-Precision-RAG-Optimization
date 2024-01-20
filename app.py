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
template = """<human>: rate the relevance of retrieved context to the user {question} on scale of 1-10':
Example:

<human>: "who is jessica james?"

<bot>:"the score of context is 7.5"


### CONTEXT
{context}

### QUESTION
Question: {question}

\n

<bot>:
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
chain.invoke("what was the first program I wrote?")