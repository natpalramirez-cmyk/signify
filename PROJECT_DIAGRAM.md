# 📊 Diagrama del Proyecto Signify

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NAVEGADOR WEB (Frontend)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Cámara Web   │  │   Micrófono    │  │   Interfaz     │ │
│  │   (getUserMedia)│  │ (Speech API)   │  │   Bootstrap    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP Requests (JSON)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    SERVIDOR FLASK (Backend)                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    app.py                              │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│     │
│  │  │   Route /   │  │ Route /foto │  │Route /reset ││     │
│  │  │   (index)   │  │   (POST)    │  │  (POST)     ││     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘│     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                │                              │
│                                │                              │
│                                ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │               gesture_detector.py                        │     │
│  │  ┌─────────────────────────────────────────────────────┐ │     │
│  │  │           CLASE GESTUREDETECTOR                │ │     │
│  │  │  ┌─────────────┐  ┌─────────────┐            │ │     │
│  │  │  │  MediaPipe   │  │   OpenCV    │            │ │     │
│  │  │  │   Hands      │  │ Processing  │            │ │     │
│  │  │  └─────────────┘  └─────────────┘            │ │     │
│  │  └─────────────────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                │                              │
│                                ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                  config.py                            │     │
│  │  • GESTURE_MAP (Mapeo de gestos)                   │     │
│  │  • Configuración de MediaPipe                        │     │
│  │  • Configuración de cámara                           │     │
│  │  • Límites y permisos                               │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                │                              │
│                                ▼                              │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                 SISTEMA DE ARCHIVOS                     │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│     │
│  │  │   fotos/    │  │ templates/  │  │   logs/     ││     │
│  │  │ (Imágenes)  │  │ (HTML/CSS)  │  │ (Eventos)   ││     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘│     │
│  └─────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

### 1. Detección de Gestos con Lenguaje de Señas

```
Usuario hace gesto → Cámara captura → JavaScript envía foto → Flask recibe → 
MediaPipe detecta mano → Cuenta dedos → Mapea a letra → 
Guarda en palabra → Devuelve JSON → Frontend muestra resultado
```

### 2. Dictado por Voz

```
Usuario habla → Micrófono captura → Web Speech API procesa → 
Convierte a texto → Frontend muestra resultado
```

## 📁 Estructura de Archivos

```
signify/
├── 📄 app.py                    # Servidor web principal
│   ├── 🌐 Rutas HTTP (/, /foto, /reset_word, /health)
│   ├── 📤 Manejo de archivos subidos
│   └── 🔗 Conexión con detector de gestos
│
├── 🤖 gesture_detector.py        # Lógica de IA
│   ├── 📸 Procesamiento de imágenes (OpenCV)
│   ├── 🤲 Detección de manos (MediaPipe)
│   ├── 👆 Conteo de dedos
│   └── 🔤 Mapeo gesto → letra
│
├── ⚙️ config.py                # Configuración
│   ├── 🗺️ GESTURE_MAP (0-23 dedos → A-Y)
│   ├── 📷 Configuración de cámara
│   └── 🔐 Seguridad y permisos
│
├── 📋 requirements.txt          # Dependencias
│   ├── Flask (servidor web)
│   ├── OpenCV (procesamiento imagen)
│   ├── MediaPipe (detección manos)
│   └── NumPy, Pillow (utilidades)
│
├── 🎨 templates/
│   └── 📄 index.html           # Interfaz de usuario
│       ├── 📹 Cámara web
│       ├── 🎤 Micrófono
│       ├── 🎨 Bootstrap 5 UI
│       └── 📱 JavaScript interactivo
│
├── 📸 fotos/                   # Imágenes capturadas
└── 📖 README.md               # Documentación
```

## 🎯 Componentes Principales

### Frontend (Navegador)
- **Cámara Web**: Acceso a `getUserMedia()` para capturar video
- **Canvas**: Convierte frames a imágenes para enviar al servidor
- **Voice Recognition**: Web Speech API para dictado
- **UI/UX**: Bootstrap 5 con diseño responsivo
- **AJAX**: Fetch API para comunicación asíncrona

### Backend (Servidor Flask)
- **Rutas**: Endpoints para diferentes funcionalidades
- **Manejo de Archivos**: Guardado y validación de imágenes
- **JSON API**: Comunicación estructurada con frontend
- **Error Handling**: Manejo robusto de errores
- **Logging**: Registro de eventos para depuración

### IA (Gesture Detector)
- **MediaPipe Hands**: Detección de 21 puntos clave por mano
- **OpenCV**: Procesamiento de imágenes y visualización
- **Algoritmo**: Conteo de dedos basado en posiciones relativas
- **Mapeo**: Conversión de número de dedos a letras

## 🔧 Tecnologías por Capa

```
┌─────────────────────────────────────────────────────────────────┐
│                 PRESENTACIÓN (Frontend)                     │
│  • HTML5/CSS3 (Estructura y estilo)                      │
│  • Bootstrap 5 (Framework CSS)                              │
│  • JavaScript ES6+ (Lógica cliente)                        │
│  • Web APIs (getUserMedia, Speech Recognition)               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 APLICACIÓN (Backend)                         │
│  • Flask (Framework web)                                   │
│  • Python 3.8+ (Lenguaje principal)                      │
│  • JSON (Formato de comunicación)                           │
│  • Logging (Registro de eventos)                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 INTELIGENCIA (IA/ML)                        │
│  • MediaPipe (Detección de manos)                          │
│  • OpenCV (Procesamiento de imágenes)                     │
│  • NumPy (Operaciones numéricas)                           │
│  • Algoritmos personalizados (Conteo de dedos)               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 DATOS (Almacenamiento)                       │
│  • Sistema de archivos (Imágenes)                            │
│  • Configuración (Variables de entorno)                      │
│  • Logs (Eventos y errores)                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Flujo de Ejecución

1. **Inicio**: `python app.py` → Servidor Flask en puerto 5001
2. **Acceso**: Navegador → `http://localhost:5001`
3. **Carga**: Flask sirve `index.html` con todos los assets
4. **Interacción**: Usuario interactúa con la interfaz
5. **Procesamiento**: JavaScript envía datos a Flask
6. **IA**: Flask procesa con MediaPipe/OpenCV
7. **Respuesta**: Resultados devueltos como JSON
8. **Actualización**: Frontend muestra resultados en tiempo real

## 🎛️ Configuración Clave

### gesture_detector.py
```python
# Sensibilidad de detección
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Tiempo para mantener gesto
GESTURE_HOLD_TIME = 2.0 segundos

# Mapeo extendido (0-23 dedos → A-Y)
GESTURE_MAP = {0: 'A', 1: 'B', ..., 23: 'Y'}
```

### app.py
```python
# Límites de seguridad
MAX_CONTENT_LENGTH = 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Estructura de carpetas
UPLOAD_FOLDER = 'fotos'
templates_folder = 'templates'
```

Este diagrama muestra cómo todos los componentes trabajan juntos para crear una aplicación completa de traducción de lenguaje de señas! 🎯

## 📦 requirements.txt - Gestión de Dependencias

### ¿Qué es requirements.txt?
```
Flask==2.3.3              # Servidor web framework
opencv-python==4.8.1.78     # Procesamiento de imágenes
mediapipe==0.10.7           # Detección de manos (IA)
streamlit==1.28.1            # Interfaz alternativa
streamlit-mic-recorder==0.0.8  # Micrófono para Streamlit
numpy==1.24.3                # Operaciones matemáticas
Pillow==10.0.1               # Manipulación de imágenes
```

### ¿Por qué es necesario?

**🎯 Propósito Principal:**
- **Reproducibilidad**: Asegura que todos usen las mismas versiones
- **Colaboración**: Evita conflictos entre desarrolladores
- **Despliegue**: Facilita instalación en producción

**📋 Funciones Específicas:**
- **Flask**: Framework web para crear servidor HTTP
- **OpenCV**: Biblioteca de visión por computadora para procesar imágenes
- **MediaPipe**: Biblioteca de Google para detección de manos en tiempo real
- **NumPy**: Soporte matemático para operaciones con arrays (imágenes)
- **Pillow**: Manipulación y conversión de formatos de imagen

**🔄 Instalación Automática:**
```bash
pip install -r requirements.txt
```
Esto instala todas las dependencias con las versiones exactas especificadas.

---

## 🐍 Virtual Environment (venv) - Entorno Virtual

### ¿Qué es un Entorno Virtual?
Un **entorno virtual** es un espacio aislado con sus propias dependencias Python.

**🏗️ Analogía:**
- **Sin venv**: Como una casa donde todos comparten el mismo baño (conflictos)
- **Con venv**: Como apartamentos separados, cada uno con sus propias instalaciones

### ¿Por qué es necesario?

**🛡️ Aislamiento de Dependencias:**
- Evita conflictos entre versiones de paquetes
- Proyecto A usa Flask 2.0, Proyecto B usa Flask 1.0 → Sin conflictos
- Cada proyecto tiene sus propias bibliotecas

**🔐 Seguridad:**
- Las dependencias del proyecto no afectan al sistema global
- Evita contaminar el Python del sistema operativo

**📦 Gestión Limpia:**
- Fácil desinstalar: basta borrar la carpeta venv
- Sin residuos en el sistema

### Creación y Uso:
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (macOS/Linux)
source venv/bin/activate

# 2. Activar (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
python app.py

# 5. Desactivar (cuando termines)
deactivate
```

**📁 Estructura con venv:**
```
signify/
├── venv/                    # Entorno virtual aislado
│   ├── bin/               # Ejecutables del entorno
│   ├── lib/               # Bibliotecas instaladas
│   └── pyvenv.cfg        # Configuración del entorno
├── app.py                 # Tu aplicación
├── requirements.txt        # Dependencias del proyecto
└── ...                    # Otros archivos del proyecto
```

---

## 🐍 Python (.py) - Backend del Sistema

### ¿Por qué .py es Backend?

**🎯 Rol de Servidor:**
- **Python (.py)**: Se ejecuta en el servidor, procesa lógica del lado del servidor
- **HTML/CSS/JS**: Se ejecutan en el navegador (cliente), manejan la interfaz

**🔄 Arquitectura Cliente-Servidor:**
```
┌─────────────────┐    HTTP Request    ┌─────────────────┐
│   NAVEGADOR   │ ──────────────────→ │   SERVIDOR      │
│   (Frontend)   │                  │   Python (.py)   │
│                 │ ←───────────────── │                 │
│  - HTML/CSS/JS │    HTTP Response   │  - Lógica de IA  │
│  - Interfaz    │                  │  - Base de datos  │
│  - Usuario ve   │                  │  - Procesamiento  │
└─────────────────┘                  └─────────────────┘
```

### ¿Qué hace el Backend Python?

**🌐 Servidor Web (Flask):**
- Recibe peticiones HTTP del navegador
- Procesa archivos subidos (fotos)
- Devuelve respuestas JSON
- Maneja rutas: `/`, `/foto`, `/reset_word`, `/health`

**🤖 Inteligencia Artificial:**
- **MediaPipe**: Detecta puntos clave de manos en imágenes
- **OpenCV**: Procesa imágenes, convierte formatos
- **Algoritmos personalizados**: Convierte gestos en letras

**💾 Gestión de Datos:**
- Guarda archivos de imágenes en carpeta `fotos/`
- Maneja configuración desde `config.py`
- Registra eventos con `logging`

### Flujo de Trabajo Backend:
```
1. 🚀 Inicio: python app.py → Servidor Flask arranca
2. 📡 Escucha: Servidor espera peticiones en puerto 5001
3. 📸 Procesa: Recibe foto → MediaPipe detecta mano
4. 🔢 Analiza: Cuenta dedos → Mapea a letra
5. 💬 Responde: Devuelve JSON con letra y palabra
6. 🔄 Repite: Espera siguiente petición
```

### Ventajas de Python como Backend:

**🚀 Rendimiento:**
- Python es rápido para procesamiento de datos
- MediaPipe está optimizado para Python
- Manejo eficiente de imágenes con NumPy

**🛠️ Ecosistema:**
- Flask: Framework web ligero y flexible
- OpenCV: Biblioteca madura de visión artificial
- MediaPipe: Tecnología de Google para detección

**📚 Facilidad de Desarrollo:**
- Sintaxis clara y legible
- Gran cantidad de bibliotecas disponibles
- Comunidad activa y documentación

**🔧 Integración:**
- Fácil integración con bases de datos
- Soporte para APIs externas
- Despliegue sencillo en múltiples plataformas

Esta arquitectura separa claramente las responsabilidades:
- **Frontend (HTML/JS)**: Interfaz de usuario
- **Backend (Python)**: Lógica de negocio e IA
- **Comunicación**: HTTP/JSON entre ambos
