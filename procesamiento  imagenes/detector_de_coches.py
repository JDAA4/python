import torch
import cv2
import yolov5


device = torch.device('cpu')


model = yolov5.load('yolov5s.pt', device=device)


model.conf = 0.25  
model.iou = 0.45  
model.agnostic = False  
model.multi_label = False  
model.max_det = 1000  


video_path = 'race_car.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error al abrir el archivo de video.")
    exit()


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)


fourcc = cv2.VideoWriter_fourcc(*'mp4v') 


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    results = model(frame)


    predictions = results.pred[0]
    boxes = predictions[:, :4]  
    scores = predictions[:, 4]
    categories = predictions[:, 5]


    auto_indices = categories == 2
    auto_boxes = boxes[auto_indices]
    auto_scores = scores[auto_indices]


    for box in auto_boxes:
        x1, y1, x2, y2 = map(int, box)
      

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, "Auto", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


    cv2.imshow('Autos Detectados', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
