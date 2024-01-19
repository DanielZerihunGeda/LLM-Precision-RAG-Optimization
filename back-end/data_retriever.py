from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
def data_retriever(file, query):
    # Load the document, split it into chunks, embed each chunk, and load it into the vector store.
    raw_documents = TextLoader(file).load()
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
    documents = text_splitter.split_documents(raw_documents)
    
    # Assuming OpenAIEmbeddings is properly initialized and available as `embeddings`
    db = Chroma.from_documents(documents, OpenAIEmbeddings())
    
    query = query
    docs = db.similarity_search(query)
    
    # Print each output individually
    for i in range(min(4, len(docs))):  # Avoid index out of range if there are less than 4 results
        print(docs[i].page_content)
    
    return None
