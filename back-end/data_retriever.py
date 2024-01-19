from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

def data_retriever(file, query):
# Load the document, split it into chunks, embed each chunk and load it into the vector store.
    raw_documents = TextLoader(file).load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    db = Chroma.from_documents(documents, OpenAIEmbeddings())
    query = query
    docs = db.similarity_search(query)
    for i in range(0,4):
        outputs = print(docs[i].page_content)
    return outputs   