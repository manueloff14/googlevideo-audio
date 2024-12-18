from flask import Flask, jsonify
import yt_dlp
import re

app = Flask(__name__)

# Función para validar una URL de YouTube
def es_url_valida(url):
    """Verifica si la URL tiene un formato válido de YouTube."""
    patron = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    return re.match(patron, url)

# Función para obtener la URL del audio
def obtener_audio_url(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    if not es_url_valida(video_url):
        return {"error": "La URL proporcionada no es válida."}, 400

    try:
        # Configuración de yt-dlp
        opciones = {
            'quiet': True,
            'no_check_certificate': True,
            'allow_unplayable_formats': True,
            'format': 'bestaudio[ext=webm]/bestaudio',
            'noplaylist': True,
            'cookiefile': 'cookies.txt',  # Usa el archivo de cookies
        }

        # Extraer la URL de audio
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url'] if 'url' in info else None

            if audio_url:
                return {"audio_url": audio_url, "title": info.get('title', 'No disponible')}, 200
            else:
                return {"error": "No se pudo encontrar una URL de audio."}, 404

    except yt_dlp.utils.DownloadError as e:
        return {"error": f"Error de descarga: {str(e)}"}, 500
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}, 500

# Ruta de la API
@app.route('/streaming/<id>', methods=['GET'])
def streaming(id):
    """Ruta para obtener la URL del audio del video."""
    resultado, status = obtener_audio_url(id)
    return jsonify(resultado), status

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
