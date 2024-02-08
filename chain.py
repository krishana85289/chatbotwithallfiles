# qa_api_blueprint.py
from flask import Blueprint, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from shared_db import db

import boto3
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
llama = LlamaAPI("LL-rue4yBAEM6QIKlDyRI4klfII3cWnZ7KzyR8OsH9HhuZ9L2il2p0AvOuXSvvTUBO5")
qa_api_blueprint = Blueprint('qa_api', __name__)
llm = ChatLlamaAPI(client=llama)  

load_dotenv()
os.getenv("GOOGLE_API_KEY")
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="semantic_similarity")
#vectorstore = FAISS.load_local("faiss_index", bedrock_embeddings)
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import Chroma

print(db)
vector=Chroma(persist_directory="./chroma_db", embedding_function=bedrock_embeddings)
def retriever(query):
    
    retriever = vector.as_retriever(
    search_type="similarity", search_kwargs={"k": 2}
)
    docs = retriever.get_relevant_documents(query)
    return docs
#llm=Bedrock(model_id="amazon.titan-text-lite-v1",client=bedrock,)

prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n just say i dont know
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)


@qa_api_blueprint.route('/qa', methods=['POST'])
def question_answering():
    data = request.get_json()

    query = data.get("query")
    docs = retriever(query)

    response=chain(
        {"input_documents":docs, "question": query}
        , return_only_outputs=False)
    result=response["output_text"]

    print(str(result))


    return jsonify({'answer': result})

