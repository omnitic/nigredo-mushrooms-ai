import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
# Importamos las herramientas modernas de LCEL
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class QueryRequest(BaseModel):
    pregunta: str

class QueryResponse(BaseModel):
    respuesta: str

app = FastAPI(
    title="Nigredo Cultivos AI",
    description="Microservicio RAG para consulta de manuales de cultivo.",
    version="1.0.0"
)

rag_chain = None

# Función auxiliar para extraer el texto de los documentos encontrados
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@app.on_event("startup")
async def startup_event():
    global rag_chain
    print("Cargando la base de datos vectorial local...")
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    
    print("Conectando con el cerebro LLM de Groq (Llama 3)...")
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    
    system_prompt = (
        "Eres el agente técnico de cultivo de hongos para el personal de Nigredo. "
        "Utiliza exclusivamente los siguientes fragmentos de contexto recuperado para responder a la pregunta. "
        "Si no sabes la respuesta basada en el contexto, di simplemente 'No tengo información en los manuales actuales'. "
        "Sé conciso y directo.\n\n"
        "Contexto:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # ---------------------------------------------------------
    # Nueva Arquitectura LCEL (Reemplaza a langchain.chains)
    # ---------------------------------------------------------
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("El agente de IA está en línea y listo para responder.")

@app.post("/api/v1/consultar", response_model=QueryResponse)
async def consultar_manual(request: QueryRequest):
    if not rag_chain:
        raise HTTPException(status_code=503, detail="El motor de IA aún está inicializando.")
    
    try:
        # En la sintaxis moderna, pasamos el string directamente al invoke
        response = rag_chain.invoke(request.pregunta)
        return QueryResponse(respuesta=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
