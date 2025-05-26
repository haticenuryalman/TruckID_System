# Gerekli kütüphaneler import ediliyor
from flask import Flask, render_template, Response, request  # Web sunucusu ve sayfa işlemleri
import cv2  # OpenCV ile video ve görüntü işleme
from ultralytics import YOLO  # YOLOv8 modelini kullanmak için
import easyocr  # Plaka okuma işlemi için OCR
import sqlite3  # Veritabanı işlemleri (plaka kayıtları)
import os  # Dosya ve klasör işlemleri
import time  # Bekleme/delay için
import numpy as np  # Sayısal işlemler (gerektiğinde)
import re  # Plaka metnini temizlemek için (regex)

# Flask uygulaması başlatılıyor
app = Flask(__name__)

# YOLOv8 modeli yükleniyor (truck, car, plate sınıflarını tanıyacak şekilde eğitilmiş özel model)
model = YOLO("truck_best.pt")

# OCR motoru başlatılıyor (EasyOCR, İngilizce karakter tanıyacak şekilde)
reader = easyocr.Reader(['en'])

# SQLite veritabanı dosya adı
DB_FILE = "plakalar.db"

# Başlangıçta gösterilecek mesaj ve son tespit edilen plaka
son_plaka_mesaji = "Waiting for detection..."
last_detected_plate = ""

# Veritabanı dosyası yoksa oluşturulur (ilk çalıştırmada)
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE plakalar (id INTEGER PRIMARY KEY, plaka TEXT UNIQUE)")
    conn.commit()
    conn.close()

# Kullanılacak kamera kaynağı:
# - "0": PC kamerası
# - "test_video.mp4": Test videosu
# - "http://192.168.x.x:4747/video": Mobil cihaz kamerası (DroidCam)
camera_source = "test_video.mp4"
camera = cv2.VideoCapture(camera_source)

# Veritabanındaki kayıtlı plakaları liste olarak döndürür
def get_kayitli_plakalar():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT plaka FROM plakalar")
    plakalar = [row[0] for row in c.fetchall()]
    conn.close()
    return plakalar

# Kamera görüntüsünü kare kare işleyip canlı video akışını üretir
def generate_frames():
    global son_plaka_mesaji, last_detected_plate

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Gerekirse döndür: frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # YOLO ile obje (truck, car, plate) tespiti
        results = model(frame)
        annotated_frame = results[0].plot()  # Tespitleri görselleştir

        truck_confident = False
        truck_box = None
        car_detected = False

        # Truck veya car tespiti kontrolü
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            cls_name = results[0].names[cls_id]
            confidence = float(box.conf[0])

            if cls_name == "truck" and confidence >= 0.55:
                truck_confident = True
                truck_box = box
                break  # İlk güçlü tespitte dur
            elif cls_name == "car":
                car_detected = True

        # Eğer tespit edilen araç truck ise, plaka tespit ve OCR yapılır
        if truck_confident:
            plate_found = False
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                cls_name = results[0].names[cls_id]

                if cls_name == "plate":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    crop = frame[y1:y2, x1:x2]

                    # OCR için ön işlem: gri tonlama + blur + threshold + büyütme
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray, (3, 3), 0)
                    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    resized = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

                    # EasyOCR ile plaka metni okunur
                    ocr_result = reader.readtext(resized)
                    if ocr_result:
                        raw_text = ocr_result[0][1]
                        # Plakadan harf ve rakam dışındaki karakterler temizlenir
                        plaka = re.sub(r"[^A-Z0-9]", "", raw_text).upper()

                        if 5 <= len(plaka) <= 10:
                            last_detected_plate = plaka

                            # Plaka veritabanında kayıtlı mı kontrol edilir
                            if plaka in get_kayitli_plakalar():
                                son_mesaj = f"Access Granted: {plaka}"
                                renk = (0, 255, 0)
                                cv2.imwrite("onayli_plaka_kameradan.jpg", frame)  # Görüntü kaydı
                                son_plaka_mesaji = son_mesaj
                                # Görüntü üzerine yazı yazılır
                                cv2.putText(annotated_frame, plaka, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
                                cv2.putText(annotated_frame, son_mesaj, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, renk, 2)
                                time.sleep(2)
                            else:
                                son_mesaj = f"Access Denied: {plaka}"
                                renk = (0, 0, 255)
                                son_plaka_mesaji = son_mesaj
                                cv2.putText(annotated_frame, plaka, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
                                cv2.putText(annotated_frame, son_mesaj, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, renk, 2)
                            plate_found = True
                            break

            # Truck var ama plaka tespit edilemedi
            if not plate_found:
                son_plaka_mesaji = "Truck detected but no plate found."
                cv2.putText(annotated_frame, son_plaka_mesaji, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

        elif car_detected:
            # Eğer araç araba ise buzzer mesajı göster
            son_plaka_mesaji = "Buzzer Alert: Car Detected!"
            cv2.putText(annotated_frame, son_plaka_mesaji, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            son_plaka_mesaji = "No relevant vehicle detected."

        # Görüntüyü HTTP üzerinden MJPEG olarak gönder
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Ana sayfa: Canlı görüntü ve mesaj
@app.route('/')
def index():
    return render_template("index.html", mesaj=son_plaka_mesaji)

# Canlı video yayını endpoint'i (video.html'de <img src="/video"> ile çağrılır)
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Yeni plaka ekleme sayfası (GET/POST form destekli)
@app.route('/ekle', methods=["GET", "POST"])
def ekle():
    mesaj = ""
    if request.method == "POST":
        plaka = request.form.get("plaka").replace(" ", "").upper()
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO plakalar (plaka) VALUES (?)", (plaka,))
            conn.commit()
            mesaj = "Plate added successfully."
        except sqlite3.IntegrityError:
            mesaj = "This plate is already registered."
        finally:
            conn.close()
    return render_template("ekle.html", mesaj=mesaj)

# Sayfa dışında son mesajı JSON olarak verir (JavaScript ile dinamik mesaj güncellemede kullanılır)
@app.route('/mesaj')
def mesaj():
    return {"mesaj": son_plaka_mesaji}

# Flask sunucusunu başlatır
# 0.0.0.0 = ağ üzerinden diğer cihazlardan da erişilebilir
# port=5050 = sunucuya http://localhost:5050 veya http://ip:5050 ile ulaşılır
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)

