import streamlit as st
from streamlit_mic_recorder import speech_to_text

# Título de la aplicación
st.title("Dictado por Voz")
st.write("Presiona el botón, permite el uso del micrófono y empieza a hablar.")

# Versión simplificada del componente
texto_dictado = speech_to_text(
    start_prompt="Click para grabar",
    stop_prompt="Detener",
    language='es',
    key='dictado'
)

# Mostrar el texto si se detecta algo
if texto_dictado:
    st.success("¡Texto detectado!")
    st.text_area("Resultado:", value=texto_dictado, height=200)
