import streamlit as st
from streamlit_mic_recorder import speech_to_text

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(page_title="Dictado por Voz", layout="centered")

# -------------------------------
# Estado de la app
# -------------------------------
if "texto" not in st.session_state:
    st.session_state.texto = ""

# -------------------------------
# UI
# -------------------------------
st.title("🎙️ Dictado por Voz")
st.write("Presiona el botón, permite el micrófono y comienza a hablar.")

# -------------------------------
# Grabación de voz
# -------------------------------
texto_dictado = speech_to_text(
    start_prompt="🎤 Iniciar grabación",
    stop_prompt="⏹️ Detener",
    language="es",
    key="dictado"
)

# -------------------------------
# Procesamiento
# -------------------------------
if texto_dictado:
    st.session_state.texto += " " + texto_dictado

# -------------------------------
# Mostrar resultado
# -------------------------------
if st.session_state.texto:
    st.success("Texto detectado:")
    
    st.text_area(
        "Resultado:",
        value=st.session_state.texto,
        height=200
    )

# -------------------------------
# Botón para limpiar
# -------------------------------
if st.button("🧹 Limpiar texto"):
    st.session_state.texto = ""
