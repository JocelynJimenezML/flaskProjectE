from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Configura tu única clave de API (asegúrate de que tenga acceso a ambas API)
api_key = "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"

def generar_descripcion_imagen(descripcion, num_imagenes):
    openai.api_key = api_key

    # Genera una descripción para la imagen usando ChatGPT
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Genera una descripción para una imagen: {descripcion}",
        max_tokens=50
    )
    descripcion_generada = respuesta.choices[0].text.strip()

    # Llama a la función para crear imágenes con DALL-E
    imagenes = crear_imagenes(descripcion_generada, num_imagenes)

    return descripcion_generada, imagenes

def crear_imagenes(descripcion, num_imagenes):
    # Utiliza la misma clave de API para DALL-E si es aplicable
    openai.api_key = api_key

    # Llama a la función para crear imágenes con DALL-E
    # (asegúrate de que la clave de API tenga acceso a DALL-E)
    respuestas = []
    for _ in range(num_imagenes):
        respuesta = openai.Image.create(
            prompt=descripcion,
            n=1,  # Generar una imagen a la vez
            size='512x512'
        )
        respuestas.append(respuesta["data"][0]["url"])
    return respuestas

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        descripcion = data["descripcion"]
        numero_imagenes = int(data["numeroImagenes"])
        try:
            descripcion_generada, imagenes = generar_descripcion_imagen(descripcion, numero_imagenes)
            return jsonify({"descripcion_generada": descripcion_generada, "imagenes": imagenes})
        except openai.error.APIError as e:
            return jsonify({"error": str(e)})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
