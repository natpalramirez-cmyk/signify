from flask import Flask, render_template, request 
import os 

# 🔥 importar tu función de IA
from mano import procesar_imagen

# 🔥 correcto
app = Flask(__name__)

# crear carpeta para guardar fotos
if not os.path.exists("fotos"):
    os.makedirs("fotos")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/foto", methods=["POST"])
def foto():
    archivo = request.files['foto']
    
    nombre = "fotos/foto.jpg"
    archivo.save(nombre)

    print("Foto guardada en", nombre)

    # 🔥 procesar imagen con MediaPipe
    resultado = procesar_imagen(nombre)

    return resultado

# 🔥 CORREGIDO
if __name__ == "__main__":
    app.run(debug=True, port=5001)
    