import streamlit as st
import requests
import os

# 1. Configuración de la página del navegador
st.set_page_config(
    page_title="Fungiagente | Nigredo",
    page_icon="🍄",
    layout="centered"
)

# 2. Inyección de CSS (Tipografías y Ajustes Finos)
st.markdown("""
    <style>
    /* Importar tipografías corporativas */
    @import url('https://fonts.googleapis.com/css2?family=Aladin&family=Athiti:wght@400;600&display=swap');
    
    /* Aplicar tipografía a todos los textos */
    html, body, [class*="css"], p, div, span {
        font-family: 'Athiti', sans-serif !important;
    }
    
    /* Aplicar tipografía a los títulos */
    h1, h2, h3 {
        font-family: 'Aladin', cursive !important;
        color: #C08937 !important; /* Dorado Nigredo */
    }
    
    /* Personalización del área de mensajes del usuario */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(192, 137, 55, 0.15) !important;
        border-radius: 10px;
        border-left: 4px solid #C08937 !important;
    }
    
    /* Personalización del área de mensajes del Fungiagente (IA) */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(142, 42, 1, 0.15) !important;
        border-radius: 10px;
        border-left: 4px solid #8E2A01 !important;
    }

    /* Asegurar que el texto dentro del chat sea Crema Nigredo */
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
        color: #FEFADF !important;
    }
    
    /* Ocultar header flotante de Streamlit */
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado de la interfaz con Imágenes
# Alineamos los elementos verticalmente para que el logo no quede flotando
col1, col2 = st.columns([1, 4], vertical_alignment="center")

logo_path = "../pictures/logo_nigredo_blanco.png"
if os.path.exists(logo_path):
    with col1:
        # CORRECCIÓN: use_container_width en lugar del obsoleto use_column_width
        st.image(logo_path, use_container_width=True)
else:
    with col1:
        st.write("🍄") 

with col2:
    st.title("Fungiagente")
    st.markdown("**Asistente Operativo de Nigredo Cultivos**")

banner_path = "../pictures/cultivo_hongos.png"
if os.path.exists(banner_path):
    # CORRECCIÓN: use_container_width en lugar del obsoleto use_column_width
    st.image(banner_path, use_container_width=True)

st.divider()

# 4. Inicializar el historial de conversación en la memoria
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"rol": "assistant", "contenido": "¡Hola, equipo Nigredo! Soy Fungiagente. ¿En qué parámetro del manual o proceso de cultivo te puedo asistir hoy?"}]

# 5. Renderizar los mensajes previos en pantalla con Avatares Personalizados
for mensaje in st.session_state.mensajes:
    # Asignamos un hongo a la IA y una silueta al usuario
    icono = "🍄" if mensaje["rol"] == "assistant" else "👤"
    with st.chat_message(mensaje["rol"], avatar=icono):
        st.markdown(mensaje["contenido"])

# 6. Capturar la consulta del usuario
pregunta = st.chat_input("Escribe tu consulta técnica aquí...")

if pregunta:
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta)
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

    # 7. Conectar con el microservicio RAG
    with st.chat_message("assistant", avatar="🍄"):
        indicador = st.empty()
        indicador.markdown("*Consultando los archivos de Nigredo...*")
        
        try:
            respuesta_api = requests.post(
                "http://127.0.0.1:8000/api/v1/consultar",
                json={"pregunta": pregunta}
            )
            
            if respuesta_api.status_code == 200:
                respuesta_texto = respuesta_api.json()["respuesta"]
                indicador.markdown(respuesta_texto)
                st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta_texto})
            else:
                indicador.error(f"Error de conexión con el motor IA: Código {respuesta_api.status_code}")
                
        except Exception as e:
            indicador.error(f"El servidor central está desconectado. Detalle: {e}")
