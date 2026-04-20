import streamlit as st
from streamlit_mic_recorder import speech_to_text

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(page_title="Voice dictation", layout="centered")

# -------------------------------
# Estado de la app
# -------------------------------
if "texto" not in st.session_state:
    st.session_state.texto = ""

if "limpiar" not in st.session_state:
    st.session_state.limpiar = False

# -------------------------------
# Sidebar (anuncio fijo)
# -------------------------------
with st.sidebar:
    st.info("The interface of this page is in english, but the writing works in spanish.")

# -------------------------------
# UI principal
# -------------------------------
st.title("🎙️ Voice dictation")
st.write("Press the button, allows the microphone and start talking.")

# -------------------------------
# Botón limpiar (ANTES del procesamiento)
# -------------------------------
if st.button("🧹 Clean text"):
    st.session_state.texto = ""
    st.session_state.limpiar = True
    st.rerun()

# -------------------------------
# Grabación de voz
# -------------------------------
texto_dictado = speech_to_text(
    start_prompt="🎤 Start recording",
    stop_prompt="⏹️ Stop",
    language="es",
    key="dictado"
)

# -------------------------------
# Procesamiento controlado
# -------------------------------
if texto_dictado and not st.session_state.limpiar:
    st.session_state.texto += " " + texto_dictado

# Reset bandera
st.session_state.limpiar = False

# -------------------------------
# Mostrar resultado
# -------------------------------
if st.session_state.texto:
    st.success("Text detected:")
    
    st.text_area(
        "Resultado:",
        value=st.session_state.texto,
        height=200
    )

    # Contador de palabras (extra pro)
    palabras = len(st.session_state.texto.split())
    st.write(f"📝 Palabras: {palabras}")
    