# Signify - Traductor de Lenguaje de Señas

Una aplicación web que ayuda a桥梁 la brecha de comunicación entre usuarios de lenguaje de señas y personas que no conocen LSM (Lenguaje de Señas Mexicano).

## 🎯 Objetivo del Proyecto

Este proyecto fue desarrollado como parte de un programa educativo para adolescentes interesados en tecnología y codificación. Los objetivos principales son:

- **Aprender a codificar**: Desarrollar habilidades prácticas de programación
- **Trabajo en equipo**: Colaborar para resolver un problema social
- **Impacto social**: Crear una herramienta que ayude a la comunicación inclusiva

## 🚀 Características

### 🤲 Traductor de LSM a Texto
- Detección de gestos de manos en tiempo real usando MediaPipe
- Reconocimiento de 24 letras del alfabeto (A-Y, excepto J y Z)
- Interfaz visual con cámara web integrada
- Construcción de palabras letra por letra

### 🎤 Dictado por Voz a Texto
- Reconocimiento de voz usando Web Speech API
- Soporte para español
- Transcripción en tiempo real

### 🎨 Interfaz Moderna
- Diseño responsivo con Bootstrap 5
- Retroalimentación visual en tiempo real
- Guías interactivas para usuarios
- Indicadores de estado del sistema

## 🛠️ Tecnología

### Backend
- **Flask**: Framework web para Python
- **OpenCV**: Procesamiento de imágenes y visión por computadora
- **MediaPipe**: Detección de manos y puntos clave
- **NumPy**: Operaciones numéricas eficientes

### Frontend
- **HTML5/CSS3**: Estructura y estilo
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript**: Lógica del lado del cliente
- **Web Speech API**: Reconocimiento de voz nativo

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Safari)
- Cámara web y micrófono

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/signify.git
cd signify
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
```bash
python app.py
```

### 5. Acceder a la Aplicación
Abre tu navegador web y visita:
```
http://localhost:5001
```

## 📖 Uso de la Aplicación

### Modo LSM a Texto
1. **Permite el acceso a la cámara** cuando el navegador lo solicite
2. **Posiciona tu mano** frente a la cámara
3. **Usa los gestos** según la guía:
   - **A**: Puño cerrado (0 dedos)
   - **B**: 1 dedo levantado
   - **C**: 2 dedos levantados
   - **D**: 3 dedos levantados
   - **E**: 4 dedos levantados
   - **F-Y**: Más combinaciones de dedos
4. **Haz clic en "Capturar Seña"** para detectar el gesto
5. **La letra detectada** aparecerá en pantalla
6. **Continúa formando palabras** letra por letra
7. **Usa "Reiniciar"** para comenzar una nueva palabra

### Modo Voz a Texto
1. **Haz clic en "Iniciar Dictado"**
2. **Permite el acceso al micrófono**
3. **Habla claramente** en español
4. **El texto aparecerá** automáticamente en tiempo real
5. **Haz clic en "Detener Dictado"** cuando termines

## 🤝 Cómo Contribuir

¡Este es un proyecto educativo y valoramos las contribuciones!

### Para Estudiantes
1. **Explora el código** y trata de entender cómo funciona
2. **Identifica áreas de mejora** (UI, nuevos gestos, etc.)
3. **Propón cambios** discutiéndolos con el equipo
4. **Implementa mejoras** con ayuda de mentores

### Para Mentores
1. **Guía a los estudiantes** en el proceso de desarrollo
2. **Fomenta buenas prácticas** de codificación
3. **Ayuda a resolver problemas técnicos**
4. **Promueve el trabajo en equipo**

## 📁 Estructura del Proyecto

```
signify/
├── app.py                 # Aplicación Flask principal
├── config.py             # Configuración de la aplicación
├── gesture_detector.py   # Lógica de detección de gestos
├── requirements.txt      # Dependencias de Python
├── templates/
│   └── index.html       # Interfaz web principal
├── fotos/               # Carpeta para imágenes capturadas
├── prueba/              # Archivos de experimentación
└── README.md           # Este archivo
```

## 🔧 Configuración

Puedes personalizar la aplicación modificando `config.py`:

- `GESTURE_HOLD_TIME`: Tiempo para mantener un gesto antes de registrarlo
- `MIN_DETECTION_CONFIDENCE`: Sensibilidad de detección de manos
- `CAMERA_WIDTH/HEIGHT`: Resolución de la cámara
- `GESTURE_MAP`: Mapeo de gestos a letras

## 🐛 Solución de Problemas

### Problemas Comunes

**Cámara no funciona:**
- Asegúrate de que ningún otro programa esté usando la cámara
- Revisa los permisos del navegador
- Intenta recargar la página

**Reconocimiento de gestos impreciso:**
- Asegúrate de tener buena iluminación
- Mantén la mano bien visible y centrada
- Evita movimientos rápidos

**Error al instalar dependencias:**
- Actualiza pip: `pip install --upgrade pip`
- Usa un entorno virtual
- Verifica la versión de Python (3.8+)

## 🚀 Mejoras Futuras

### Características Planeadas
- [ ] Soporte para números y símbolos
- [ ] Modo de práctica con retroalimentación
- [ ] Base de datos para guardar progreso
- [ ] Soporte para otros idiomas de señas
- [ ] Aplicación móvil
- [ ] Modo offline

### Mejoras Técnicas
- [ ] Pruebas unitarias automatizadas
- [ ] Optimización de rendimiento
- [ ] Sistema de logging avanzado
- [ ] Despliegue en la nube


---

**¡Recuerda**: Este proyecto es más que código - es una herramienta para hacer el mundo más inclusivo! 🌍💙