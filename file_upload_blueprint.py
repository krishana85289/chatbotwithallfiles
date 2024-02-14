from flask import Blueprint, request, jsonify
from flask import Flask, request, jsonify
from methods import handle_file_upload, is_allowed_file
import comtypes.client 
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
import json
import os
import sys
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from shared_db import db
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import boto3
import shutil

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="semantic_similarity")
bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)

ALLOWED_EXTENSIONS = {'pdf','text','docx','doc','csv','xlsx'}
db_path = "./chroma_db"

# Check if the file exists
"""if os.path.exists(db_path):
    # Delete the file
    shutil.rmtree(db_path, ignore_errors=True)
    # Print a message
    print(f"Deleted {db_path}")"""
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
file_upload_blueprint = Blueprint('file_upload', __name__)

@file_upload_blueprint.route('/upload-files', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No selected files'}), 400
    extracted_texts, error_message = handle_file_upload(files)
    text_splitter = CharacterTextSplitter(separator = "\n\n",chunk_size = 250,chunk_overlap  = 20)
    docs = text_splitter.create_documents([extracted_texts])
    print(docs)
    db = Chroma.from_documents(documents=docs, embedding=bedrock_embeddings,persist_directory="./chroma_db")
    print(db)
    return jsonify({"Message":"Data base is created"})

