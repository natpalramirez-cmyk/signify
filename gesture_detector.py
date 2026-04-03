# Importaciones necesarias para el detector de gestos
import cv2  # OpenCV para procesamiento de imágenes y visión por computadora
import mediapipe as mp  # MediaPipe para detección de manos y puntos clave
import time  # Para manejar temporizadores y control de tiempo
import logging  # Para registrar eventos y errores
from config import Config  # Configuración centralizada

# Configurar el sistema de logging específico para este módulo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GestureDetector:
    """
    Clase principal para detectar gestos de manos y convertirlos en letras.
    Utiliza MediaPipe para detectar puntos clave de la mano y OpenCV para
    procesamiento de imágenes.
    """
    
    def __init__(self):
        """
        Inicializa el detector de gestos.
        Configura MediaPipe Hands y establece variables de estado.
        """
        try:
            # Inicializar soluciones de MediaPipe para detección de manos
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,  # Confianza mínima para detección
                min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE   # Confianza mínima para seguimiento
            )
            # Utilidades para dibujar landmarks y conexiones
            self.mp_drawing = mp.solutions.drawing_utils
            
            # Variables de estado para seguimiento
            self.current_letter = ""  # Letra actualmente detectada
            self.word = ""            # Palabra formada hasta ahora
            self.last_time = time.time()  # Timestamp del último cambio
            
            logger.info("Gesture detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize gesture detector: {e}")
            raise

    def count_fingers(self, hand_landmarks):
        """
        Cuenta el número de dedos extendidos en una mano.
        
        Args:
            hand_landmarks: Puntos clave de la mano detectada por MediaPipe
            
        Returns:
            int: Número de dedos extendidos (0-5)
            
        Lógica:
        - Pulgar: Compara posición del dedo con el nudillo
        - Otros dedos: Compara posición de la punta con el nudillo
        """
        try:
            fingers = []  # Lista para almacenar estado de cada dedo (0=cerrado, 1=abierto)
            
            # Detectar pulgar (dedo 0)
            # El pulgar se detecta comparando coordenada X (horizontal)
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                fingers.append(1)  # Pulgar extendido
            else:
                fingers.append(0)  # Pulgar cerrado
            
            # Detectar otros cuatro dedos (índice, medio, anular, meñique)
            # Se detectan comparando coordenada Y (vertical)
            finger_tips = [8, 12, 16, 20]    # Puntas de los dedos
            finger_pips = [6, 10, 14, 18]    # Nudillos de los dedos
            
            for tip, pip in zip(finger_tips, finger_pips):
                # Si la punta está arriba del nudillo, el dedo está extendido
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    fingers.append(1)  # Dedo extendido
                else:
                    fingers.append(0)  # Dedo cerrado
            
            return sum(fingers)  # Total de dedos extendidos
            
        except Exception as e:
            logger.error(f"Error counting fingers: {e}")
            return 0  # Retornar 0 en caso de error

    def detect_gesture(self, frame):
        """
        Detecta gestos de manos en un frame de video.
        
        Args:
            frame: Imagen capturada por la cámara (formato OpenCV)
            
        Returns:
            tuple: (frame_procesado, letra_detectada, palabra_actual)
            
        Proceso:
        1. Convierte frame a RGB (MediaPipe requiere RGB)
        2. Procesa con MediaPipe para detectar manos
        3. Para cada mano detectada:
           - Dibuja landmarks y conexiones
           - Cuenta dedos extendidos
           - Mapea a letra usando GESTURE_MAP
        4. Actualiza palabra si se mantiene el gesto suficiente tiempo
        5. Dibuja información en el frame
        """
        try:
            # Convertir frame de BGR (OpenCV) a RGB (MediaPipe)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb_frame)
            
            detected_letter = ""  # Letra detectada en este frame
            
            # Procesar todas las manos detectadas
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    # Dibujar puntos clave y conexiones en el frame
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Contar dedos y mapear a letra
                    finger_count = self.count_fingers(hand_landmarks)
                    detected_letter = Config.GESTURE_MAP.get(finger_count, "")
                    
                    # Actualizar letra actual si es diferente a la anterior
                    if detected_letter and detected_letter != self.current_letter:
                        self.current_letter = detected_letter
                        self.last_time = time.time()  # Reiniciar temporizador
            
            # Agregar letra a la palabra si se mantiene el gesto el tiempo suficiente
            current_time = time.time()
            if (self.current_letter and 
                current_time - self.last_time > Config.GESTURE_HOLD_TIME):
                self.word += self.current_letter  # Agregar letra a la palabra
                self.last_time = current_time     # Actualizar timestamp
                logger.info(f"Added letter '{self.current_letter}' to word. Current word: '{self.word}'")
            
            # Dibujar información en el frame
            cv2.putText(frame, f"Letra: {self.current_letter}", (30, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)  # Verde para letra
            cv2.putText(frame, f"Palabra: {self.word}", (30, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)  # Azul para palabra
            
            return frame, detected_letter, self.word
            
        except Exception as e:
            logger.error(f"Error detecting gesture: {e}")
            return frame, "", self.word  # Retornar valores por defecto en caso de error

    def process_image(self, image_path):
        """
        Procesa una imagen estática para detección de gestos.
        
        Args:
            image_path: Ruta al archivo de imagen a procesar
            
        Returns:
            tuple: (letra_detectada, palabra_actual)
            
        Uso:
        - Se llama desde Flask cuando se sube una foto
        - Carga la imagen con OpenCV
        - Aplica detección de gestos
        - Retorna resultados para enviar al frontend
        """
        try:
            # Cargar imagen desde el archivo
            frame = cv2.imread(image_path)
            if frame is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Aplicar detección de gestos al frame
            frame, detected_letter, word = self.detect_gesture(frame)
            return detected_letter, word
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return "", ""  # Retornar vacío en caso de error

    def reset_word(self):
        """
        Reinicia la palabra actual y la letra detectada.
        
        Uso:
        - Se llama cuando el usuario presiona el botón "Reiniciar"
        - Limpia el estado para comenzar una nueva palabra
        """
        self.word = ""            # Limpiar palabra
        self.current_letter = ""   # Limpiar letra actual
        logger.info("Word reset")  # Registrar el reinicio

    def __del__(self):
        """
        Destructor de la clase.
        Se ejecuta cuando el objeto es eliminado.
        Libera recursos de MediaPipe de forma segura.
        """
        try:
            # Cerrar la solución de manos de MediaPipe
            if hasattr(self, 'hands'):
                self.hands.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
