from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from operator import itemgetter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from chunk_semantically import semantic_retriever

app = Flask(__name__)

def prompt_return(query):
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    chunks = semantic_retriever('file.txt')
    vectorstore = FAISS.from_texts(
        chunks, embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k" : 5})  # Specifying the value of "k"
    template = """<human>: craft efficient prompt based on {question}, 
                    make sure to generate very EFFECTIVE and 
                    PRACTICAL, the prompt should be clear and
                    concise and strategic as well. 


    ### CONTEXT
    {context}

    ### QUESTION
    Question: {question}

    \n

    <bot>:
    """

    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(temperature=0.75)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)

@app.route('/prompt_return_endpoint', methods=['POST'])
def prompt_return_endpoint():
    try:
        # Assuming the input is a JSON object with a "query" field
        data = request.json
        input_string = data.get("query", "")

        # Call your modified function with the input string
        result = prompt_return(input_string)

        # Return the result as a JSON response
        return jsonify({"result": result})
    except Exception as e:
        # Handle any exceptions and return an error response if necessary
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5522)

