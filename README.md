# Proyecto de Visión por Computadora para la Detección de Enfermedades en Plantas

Este proyecto utiliza YOLOv8 para la detección de enfermedades en plantas, con la segmentación realizada mediante Roboflow. La aplicación web está construida con Flask y muestra los resultados en una página local.

## Enlaces Importantes

- [Modelo preentrenado y fine-tuned](https://universe.roboflow.com/usfx-xqsnn/peach-diseasesusfx-cy77o)
- [Descargar el modelo entrenado](https://drive.google.com/file/d/15omldH2jnwooS_Eo67ImRpGxeS3yC8mP/view?usp=sharing)

## Instrucciones de Uso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/jafernandezm/peach-yolov8-seg
cd flask

pip install -r requirements.txt


python app.py

```

<video width="720" height="340" controls>
  <source src="videos/video_9.mp4" type="video/mp4">
  Tu navegador no soporta el elemento de video.
</video>