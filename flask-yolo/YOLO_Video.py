from ultralytics import YOLO
import cv2
import math

def video_detection(path_x):
    video_capture = path_x
    #Create a Webcam Object
    cap=cv2.VideoCapture(video_capture)
    frame_width=int(cap.get(3))
    frame_height=int(cap.get(4))
    model=YOLO("../YOLO-Weights/bestNyolo.pt")
    detections = []
    classNames  = ["ManchaBaterial", "Roya", "Taphrina"]
    while True:
        success, img = cap.read()
        frame = cv2.resize(img, (640, 480))

        results=model.predict(frame, imgsz=640, conf=0.40)
        # Mostramos resultados
        anotaciones = results[0].plot()
        print(anotaciones)
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                print(x1,y1,x2,y2)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                detections.append({
                    "clase": class_name,
                    "confianza": conf,
                    "x1": x1,
                    "y1": y2,
                    "x2": x2,
                    "y2": y2
                })
                
        yield anotaciones, detections
        #out.write(img)
        #cv2.imshow("image", img)
        #if cv2.waitKey(1) & 0xFF==ord('1'):
            #break
    #out.release()
cv2.destroyAllWindows()
    