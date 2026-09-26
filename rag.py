# import os library
import os
# PyPDFLoader load pdf from the langchain
from langchain_community.document_loaders import PyPDFLoader
# RecursiveCharacterTextSplitter splits text from pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
# HuggingFaceEmbeddings will embed data [convert data into numbers]
from langchain_huggingface import HuggingFaceEmbeddings
# 'FAISS' stores the data [also known as database]
from langchain_community.vectorstores import FAISS

# pdf present in the data folder 
PDF_file="Data/nutrition.pdf"

# load the pdf 'nutrition' from the data folder
def create_rag():
    if not os.path.exists(PDF_file):
        raise FileNotFoundError("File Not Found")
    else:
        # make document
        document=PyPDFLoader(PDF_file).load()
        # split the word from data
        splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        # connect 'splitter' in 'document'
        chunks=splitter.split_documents(document)
        # "model name present in the apis.txt" and it convert data into numbers
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # create database
        db=FAISS.from_documents(chunks,embedding)
        # save database locally ( in vector_database folder )
        db.save_local("Vector_database")
        return len(chunks)


def load_rag():
    # "model name present in the apis.txt" and it convert data into numbers
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # load database locally ( in vector_database folder )
    db=FAISS.load_local("Vector_database",embedding,allow_dangerous_deserialization=True)
    return db