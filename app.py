# Importaciones necesarias para la aplicación web
from flask import Flask, render_template, request, jsonify, send_from_directory  # Flask y componentes para manejar HTTP
import os  # Para interactuar con el sistema de archivos
import logging  # Para registrar eventos y errores
from datetime import datetime  # Para generar timestamps únicos
from gesture_detector import GestureDetector  # Nuestra clase de detección de gestos
from config import Config  # Configuración centralizada de la aplicación

# Configurar el sistema de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de la aplicación Flask
app = Flask(__name__)
# Cargar configuración desde la clase Config
app.config.from_object(Config)

# Inicializar el detector de gestos
gesture_detector = None
try:
    # Crear instancia del detector de gestos
    gesture_detector = GestureDetector()
    logger.info("Gesture detector initialized successfully")
except Exception as e:
    # Registrar error si no se puede crear la instancia
    logger.error(f"Failed to initialize gesture detector: {e}")

# Crear carpeta para subir archivos si no existe
# Esta carpeta almacenará las imágenes capturadas por la cámara
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Función para verificar si un archivo tiene una extensión permitida
def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida según la configuración.
    Args:
        filename: Nombre del archivo a verificar
    Returns:
        bool: True si la extensión está permitida, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal - muestra la página de inicio
@app.route("/")
def index():
    """
    Página principal de la aplicación.
    Renderiza el template index.html que contiene la interfaz de usuario.
    Returns:
        HTML: Página principal con la interfaz de la aplicación
    """
    return render_template("index.html")

# Ruta para procesar fotos capturadas - método POST
@app.route("/foto", methods=["POST"])
def foto():
    """
    Procesa la foto capturada por la cámara.
    Recibe el archivo de imagen, lo guarda, procesa para detectar gestos
    y devuelve los resultados en formato JSON.
    Returns:
        JSON: Con información sobre el procesamiento y detección
    """
    try:
        # Verificar si se ha enviado un archivo
        if 'foto' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        # Obtener el archivo enviado desde el formulario
        file = request.files['foto']
        
        # Verificar si se ha seleccionado un archivo
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Verificar si el archivo tiene una extensión permitida
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed"}), 400
        
        # Generar nombre de archivo único con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gesture_{timestamp}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Guardar el archivo en el disco
        file.save(filepath)
        logger.info(f"Photo saved to {filepath}")
        
        # Procesar imagen para detección de gestos
        if gesture_detector:
            detected_letter, current_word = gesture_detector.process_image(filepath)
            
            return jsonify({
                "success": True,
                "filename": filename,
                "detected_letter": detected_letter,
                "current_word": current_word
            })
        else:
            return jsonify({
                "success": True,
                "filename": filename,
                "message": "Gesture detector not available"
            })
            
    except Exception as e:
        # Registrar error y devolver respuesta de error
        logger.error(f"Error processing photo: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Ruta para reiniciar la palabra actual
@app.route("/reset_word", methods=["POST"])
def reset_word():
    """
    Reinicia la palabra actual en el detector de gestos.
    Permite al usuario comenzar a formar una nueva palabra.
    Returns:
        JSON: Confirmación del reinicio o mensaje de error
    """
    try:
        if gesture_detector:
            # Reiniciar la palabra en el detector
            gesture_detector.reset_word()
            return jsonify({"success": True, "message": "Word reset successfully"})
        else:
            return jsonify({"error": "Gesture detector not available"}), 500
    except Exception as e:
        logger.error(f"Error resetting word: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Ruta para verificar el estado del servidor
@app.route("/health")
def health_check():
    """
    Endpoint de salud para monitoreo del sistema.
    Permite verificar si el servidor y el detector de gestos están funcionando.
    Returns:
        JSON: Estado del servidor y componentes
    """
    return jsonify({
        "status": "healthy",
        "gesture_detector": gesture_detector is not None
    })

# Punto de entrada principal de la aplicación
# Se ejecuta solo cuando el script se corre directamente (no cuando se importa)
if __name__ == "__main__":
    """
    Inicia el servidor de desarrollo de Flask.
    - debug=True: Activa el modo depuración (recarga automática, mensajes de error detallados)
    - host='0.0.0.0': Permite acceso desde cualquier IP en la red local
    - port=5001: Puerto donde se ejecutará el servidor
    """
    app.run(debug=True, host='0.0.0.0', port=5001)
    

