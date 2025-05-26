from ultralytics import YOLO
import cv2
import easyocr
import serial
import time

# YOLO modeli ve OCR motoru
model = YOLO("truck_best.pt")
reader = easyocr.Reader(['en'])

# Arduino seri port bağlantısı (senin porta göre düzenle!)
arduino = serial.Serial('/dev/tty.usbmodem14101', 9600)
time.sleep(2)

# Kayıtlı plakalar listesi
kayitli_plakalar = ["34ABC123", "06XYZ456", "35EFG789"]

# Kamerayı başlat
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
                plaka = ocr_result[0][1].replace(" ", "").upper()
                print("Tespit edilen plaka:", plaka)
                if plaka in kayitli_plakalar:
                    arduino.write(b"A")  # kapı aç
                    cv2.putText(annotated_frame, f"GIRIS: {plaka}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    arduino.write(b"B")  # buzzer çal
                    cv2.putText(annotated_frame, f"RED: {plaka}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Kontrollü Giriş", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()





