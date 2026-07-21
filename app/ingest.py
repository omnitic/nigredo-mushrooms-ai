import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def procesar_manuales():
    pdf_path = "../data/manual_hongos.pdf"
    print(f"Cargando el documento: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    documentos = loader.load()

    print("Dividiendo el texto en fragmentos (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"El manual se dividió en {len(chunks)} fragmentos.")

    print("Descargando/Generando embeddings locales con HuggingFace...")
    # Este modelo corre localmente, es gratis y no genera errores de API
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("../faiss_index")
    
    print("Base de datos vectorial guardada exitosamente en 'faiss_index'.")

if __name__ == "__main__":
    procesar_manuales()
