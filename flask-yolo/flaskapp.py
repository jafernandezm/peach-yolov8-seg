from flask import Flask, render_template, Response,jsonify,request,session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os
import cv2
from YOLO_Video import video_detection
import json
# Crea una instancia de la aplicación Flask
app = Flask(__name__)
# Configuración de la aplicación
app.config['SECRET_KEY'] = 'muhammadmoin'
app.config['UPLOAD_FOLDER'] = 'static/files'
# Inicializa una lista para almacenar las tuplas (img, detections)
global_detections_list = []
ubicaciones=[]
# Define un formulario para subir archivos de video
class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Run")
# Función para generar fotogramas a partir de detecciones de video
def generate_frames(path_x=''):
    global_detections_list.clear()
    for img, detections in video_detection(path_x):
        ref, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
       
        global_detections_list.append(detections)
        
# Función para generar fotogramas web a partir de detecciones de video
def generate_frames_web(path_x):
    for img, detections in video_detection(path_x):
        ref, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        global_detections_list.append(detections)
       
        
# Ruta principal, renderiza la página de inicio
@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('indexproject.html')
# Ruta para renderizar la página de la webcam
@app.route("/webcam", methods=['GET','POST'])
def webcam():
    session.clear()
    return render_template('ui.html')
# Ruta para renderizar la página con el formulario para subir archivos de video
@app.route('/FrontPage', methods=['GET','POST'])
def front():
    # Upload File Form: Create an instance for the Upload File Form
    form = UploadFileForm()
    if form.validate_on_submit():
        # Our uploaded video file path is saved here
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # Then save the file
        # Use session storage to save video file path
        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
    return render_template('videoprojectnew.html', form=form)
# Ruta para obtener el video y mostrarlo en el navegador
@app.route('/video')
def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')


# Ruta para mostrar los fotogramas en la página web
@app.route('/webapp')
def webapp():
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_data')
def get_data():
    # Obtén los datos que deseas mostrar en la tabla (puedes cambiar esto según tus necesidades)
    for detections in global_detections_list:
        data = detections
    return jsonify(data)

@app.route('/table')
def table():
    for detections in global_detections_list:
        data = detections
    return render_template('table.html', detections=data)

@app.route('/api/prueba', methods=['GET'])
def prueba():
    # Lógica de prueba
    global_detections_list
    return jsonify(global_detections_list)

@app.route('/api/ubicacion', methods=['POST'])
def recibir_ubicacion():
    # Obtener datos de latitud y longitud del cuerpo de la solicitud
    datos = request.get_json()

    if 'ubicacion' in datos and len(datos['ubicacion']) == 2:
        latitud = datos['ubicacion'][0]
        longitud = datos['ubicacion'][1]
        # Agregar a la lista global_detections_list
            
        ubicaciones.append(datos['ubicacion'])
        # Aquí puedes realizar la lógica con los datos de latitud y longitud
        resultado = {"mensaje": f"Ubicación recibida - Latitud: {latitud}, Longitud: {longitud}"}

        return jsonify(resultado)
    else:
        return jsonify({"error": "Datos de ubicación incorrectos"}), 400
    
# Si este script es el principal, ejecuta la aplicación
if __name__ == '__main__':
    # Escuchar en todas las interfaces de red (0.0.0.0)
    #app.run(host='192.168.100.34', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)