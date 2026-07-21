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

## Historial de Decisiones de Arquitectura (ADR)

### Refactorización de Embeddings y LLM (21 de Julio 2026)

**Contexto del Problema:** 
Durante la fase inicial de desarrollo y vectorización de los manuales de cultivo, el SDK nativo de Google (`google-genai`) presentó problemas de compatibilidad de versiones y errores internos recurrentes de formato (`NOT_FOUND`, `unexpected model name format`) al intentar integrarse con las últimas versiones de LangChain.

**Decisión Técnica:** 
Para garantizar la escalabilidad, la estabilidad del entorno Linux y mantener los costos operativos estrictamente en cero, se reestructuró el pipeline RAG reemplazando por completo el ecosistema de Google por alternativas de código abierto y alta disponibilidad.

**Cambios Implementados y Justificación:**
1. **Embeddings Locales con HuggingFace (`all-MiniLM-L6-v2`):** 
   * Sustituye a la API de vectorización de Google. 
   * *Justificación:* Al ejecutar el modelo de forma 100% local, eliminamos la dependencia de una conexión a internet para el procesamiento de PDFs, esquivamos los límites de peticiones (rate limits) y aseguramos una compatibilidad absoluta con FAISS sin generar ningún costo para el proyecto.
2. **Motor de Inferencia con Groq y Llama 3 (Meta):** 
   * Sustituye a Gemini como el cerebro conversacional del agente.
   * *Justificación:* Groq es un motor de inferencia diseñado específicamente para maximizar la velocidad. Ofrece una capa gratuita sumamente estable para desarrolladores y el modelo Llama-3-8B garantiza respuestas técnicas inmediatas y precisas para los operarios de Nigredo, con una integración impecable en LangChain.
