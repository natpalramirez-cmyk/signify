# Configuración centralizada de la aplicación Signify
# Este archivo contiene todas las variables de configuración
# que se utilizan en toda la aplicación
import os

class Config:
    """
    Clase de configuración principal.
    Contiene todos los parámetros ajustables de la aplicación.
    """
    
    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Clave secreta para Flask (cambiar en producción)
    
    # Gestión de archivos
    UPLOAD_FOLDER = 'fotos'  # Carpeta donde se guardan las imágenes
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Tamaño máximo de archivo: 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas
    
    # Configuración de MediaPipe (detección de manos)
    MIN_DETECTION_CONFIDENCE = 0.5  # Confianza mínima para detectar mano (0.0-1.0)
    MIN_TRACKING_CONFIDENCE = 0.5   # Confianza mínima para seguir mano (0.0-1.0)
    # Valores más altos = más precisión pero menos sensibilidad
    
    # Configuración de reconocimiento de gestos
    GESTURE_HOLD_TIME = 2.0  # Segundos que se debe mantener un gesto para registrarlo
    # Tiempo mayor = menos errores pero más lento
    
    # Configuración de cámara
    CAMERA_WIDTH = 640   # Ancho deseado de la cámara (píxeles)
    CAMERA_HEIGHT = 480  # Alto deseado de la cámara (píxeles)
    # Resolución balanceada para buen rendimiento y calidad
    
    # Mapeo extendido de gestos a letras
    # Relaciona el número de dedos extendidos con letras del alfabeto
    GESTURE_MAP = {
        0: 'A',   # Puño cerrado (0 dedos)
        1: 'B',   # 1 dedo levantado
        2: 'C',   # 2 dedos levantados
        3: 'D',   # 3 dedos levantados
        4: 'E',   # 4 dedos levantados
        5: 'F',   # 5 dedos levantados (mano abierta)
        6: 'G',   # Combinación específica de 6 dedos (no posible, pero mantenido para extensibilidad)
        7: 'H',   # Combinación específica
        8: 'I',   # Combinación específica
        9: 'K',   # Combinación específica
        10: 'L',  # Combinación específica
        11: 'M',  # Combinación específica
        12: 'N',  # Combinación específica
        13: 'O',   # Combinación específica
        14: 'P',  # Combinación específica
        15: 'Q',  # Combinación específica
        16: 'R',  # Combinación específica
        17: 'S',  # Combinación específica
        18: 'T',  # Combinación específica
        19: 'U',  # Combinación específica
        20: 'V',  # Combinación específica
        21: 'W',  # Combinación específica
        22: 'X',  # Combinación específica
        23: 'Y'   # Combinación específica
        # Nota: J y Z requieren movimiento, no están implementadas aún
    }
    
    # Constantes adicionales para futuras expansiones
    DEBUG_MODE = True  # Modo depuración (más logs y mensajes)
    LOG_LEVEL = 'INFO'  # Nivel de logging: DEBUG, INFO, WARNING, ERROR
    ENABLE_VOICE_RECOGNITION = True  # Habilitar reconocimiento de voz
    ENABLE_GESTURE_DETECTION = True  # Habilitar detección de gestos
