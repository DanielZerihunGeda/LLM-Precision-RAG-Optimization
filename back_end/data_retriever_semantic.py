import re
import combine_sentences
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.vectorstores import Chroma
oaiembeds = OpenAIEmbeddings()

def semantic_retriever(file,query):
    with open(file) as file:
        essay = file.read()
    
    single_sentences_list = re.split(r'(?<=[.?!])\s+', essay) # split the texts based on "(?<=[.?!])\s+" to stage the splitting
    sentences = [{'sentence': x, 'index' : i} for i, x in enumerate(single_sentences_list)]
    combine_sentences(sentences)
    embeddings = oaiembeds.embed_documents([x['combined_sentence'] for x in sentences])
    for i, sentence in enumerate(sentences):
        embeddings[i] = sentence['combined_sentence_embedding']
    db = Chroma.from_documents(embeddings, OpenAIEmbeddings())

    query = query
    retriever = db.as_retriever(
    search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.65, "k": 5}
)
    docs = retriever.get_relevant_documents(query)
    # Print each output individually
    for i in range(min(4, len(docs))):  # Avoid index out of range if there are less than 4 results
        print(docs[i].page_content)
    
    return None
