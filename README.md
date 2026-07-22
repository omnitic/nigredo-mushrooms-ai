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

### Refactorización de Embeddings y LLM 

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

### Actualización del Motor y Sintaxis

**Contexto del Problema:** 
1. El módulo clásico `langchain.chains` fue marcado como obsoleto en la versión más reciente del framework.
2. El modelo inicial de Groq (`llama3-8b-8192`) fue retirado de sus servidores (decommissioned).

**Decisión Técnica:**
1. **Migración a LCEL (LangChain Expression Language):** Se reescribió el flujo del agente usando la sintaxis moderna de LangChain (tuberías modulares) para garantizar compatibilidad futura y un código más limpio.
2. **Actualización a Llama 3.1:** Se cambió el motor de inferencia a `llama-3.1-8b-instant`, asegurando el acceso a la última y más eficiente versión del modelo gratuito de Meta.

## Interfaces de Usuario 

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

### Gestión de Conocimiento y Comportamiento del Agente (Fungiagente)

El sistema ha sido refinado para ofrecer una experiencia de usuario natural y precisa:

* **Actualización Dinámica de la Base Vectorial:** El sistema permite la actualización del manual de operaciones central (`data/manual_hongos.pdf`). Al reemplazar el archivo físico y re-ejecutar el script de ingesta, FAISS reescribe los vectores automáticamente, permitiendo que la IA absorba nuevo conocimiento sin alterar la arquitectura del código.
* **Procesamiento de Lenguaje Natural (NLP) Empático:** El `system_prompt` está diseñado con instrucciones de enrutamiento lógico. Fungiagente es capaz de distinguir entre interacciones sociales (saludos, agradecimientos) y consultas operativas complejas. Esto evita respuestas robóticas o errores de búsqueda, manteniendo un tono colaborativo alineado con la filosofía de transformación y sostenibilidad del proyecto.

### Ajustes Finales de Producción (Fase 6 - Estabilización)

Para garantizar la correcta ejecución del contenedor en cualquier entorno, se implementaron las siguientes correcciones estructurales:

*   **Inyección de Variables de Entorno:** El servicio de Telegram requiere la inyección explícita de credenciales durante el arranque. Se modificó el comando de despliegue para incluir `--env-file .env`, asegurando que todos los procesos internos tengan acceso a los tokens de seguridad.
*   **Integración de Base Vectorial:** Se actualizó el `Dockerfile` para incluir la copia de la carpeta `faiss_index/` al interior del contenedor, y se normalizaron las rutas relativas en `app/main.py` (eliminando prefijos `../`) para que la lectura de datos coincida con la raíz del espacio de trabajo de Docker.
*   **Mantenimiento de la Interfaz:** Se actualizaron los parámetros visuales en `app/ui.py` reemplazando el atributo obsoleto `use_container_width` por `width="stretch"`, asegurando compatibilidad con futuras versiones del motor Streamlit (post-2025).
*   **Coherencia Omnicanal:** Se normalizó el mensaje de bienvenida estructurado para que sea exactamente idéntico tanto en la interfaz gráfica web (Streamlit) como en el bot de Telegram. Esto unifica la voz de Fungiagente y mantiene la coherencia corporativa en todos los puntos de contacto.

**Comando final de despliegue en producción:**
\`\`\`bash
sudo docker run -d -p 8000:8000 -p 8501:8501 --env-file .env --name fungiagente-app fungiagente:v1
\`\`\`
