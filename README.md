# Nigredo Mushrooms AI - Sistema RAG

API REST basada en Inteligencia Artificial (Gemini 1.5) para la consulta automatizada de manuales de cultivo de hongos dela Empresa Nigredo SAS.

## Arquitectura
- **Framework AI:** LangChain
- **LLM y Embeddings:** Google Gemini (gemini-1.5-flash / text-embedding-004)
- **Vector Store:** FAISS
- **Procesamiento de PDF:** PyPDF
- **API Backend:** FastAPI + Uvicorn

## Configuración Local
1. Clonar el repositorio.
2. Crear y activar entorno virtual: `python3 -m venv venv && source venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Configurar el archivo `.env` con la variable `GOOGLE_API_KEY`.
5. Ejecutar la API: `uvicorn app.main:app --reload`
