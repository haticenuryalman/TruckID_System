from ultralytics import YOLO
import cv2

# Modeli yükle
model = YOLO("truck_best.pt")

# Kamera aç
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO ile tahmin yap
    results = model(frame)

    # Sonuçları çiz
    annotated_frame = results[0].plot()
    cv2.imshow("Truck + Plate Detection", annotated_frame)

    # 'q' ile çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
