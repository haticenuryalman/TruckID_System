from ultralytics import YOLO
import cv2
import easyocr

model = YOLO("truck_best.pt")
reader = easyocr.Reader(['en'])  # Türkçe plakalar da 'en' ile okunur

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated_frame = results[0].plot()

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = results[0].names[cls_id]
        if cls_name == "plate":
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_crop = frame[y1:y2, x1:x2]
            ocr_result = reader.readtext(plate_crop)
            if ocr_result:
                text = ocr_result[0][1]
                cv2.putText(annotated_frame, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("Truck + Plate + OCR", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

