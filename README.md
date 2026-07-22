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

### Actualización del Motor y Sintaxis (Julio 2026)

**Contexto del Problema:** 
1. El módulo clásico `langchain.chains` fue marcado como obsoleto en la versión más reciente del framework.
2. El modelo inicial de Groq (`llama3-8b-8192`) fue retirado de sus servidores (decommissioned).

**Decisión Técnica:**
1. **Migración a LCEL (LangChain Expression Language):** Se reescribió el flujo del agente usando la sintaxis moderna de LangChain (tuberías modulares) para garantizar compatibilidad futura y un código más limpio.
2. **Actualización a Llama 3.1:** Se cambió el motor de inferencia a `llama-3.1-8b-instant`, asegurando el acceso a la última y más eficiente versión del modelo gratuito de Meta.

## Interfaces de Usuario (Fase 4)

El ecosistema cuenta con dos interfaces para interactuar con el motor RAG de Inteligencia Artificial ("Fungiagente"), diseñadas para adaptarse al entorno de trabajo en oficina y en el área de cultivo.

### 1. Interfaz Web (Streamlit)
Aplicación web de escritorio con la identidad visual corporativa de Nigredo, ideal para consultas extensas.

**Ejecución:**
1. Asegurarse de que el servidor FastAPI esté corriendo: `uvicorn app.main:app --reload`
2. En una nueva terminal, activar el entorno virtual y ejecutar: `streamlit run app/ui.py`
3. La interfaz se abrirá automáticamente en `http://localhost:8501`.

### 2. Integración Móvil (Bot de Telegram)
Canal de comunicación ágil para consultas operativas directamente desde dispositivos móviles en la zona de producción.

**Configuración y Ejecución:**
1. Obtener un token a través de BotFather en Telegram.
2. Añadir el token al archivo `.env` en la raíz del proyecto: `TELEGRAM_BOT_TOKEN="tu_token"`.
3. Con el servidor FastAPI corriendo, iniciar el puente de Telegram en una nueva terminal ejecutando: `python app/telegram_bot.py`

