# Gerçek Zamanlı Tır Tanıma ve Plaka Doğrulama Sistemi

Bu proje, Flask tabanlı bir web uygulaması olarak gerçek zamanlı tır ve plaka tanıma işlemi yapmaktadır. Kamera görüntüsü üzerinden aracın tır veya otomobil olduğu tespit edilir, plakası okunur ve SQLite veritabanında daha önceden kayıtlı olan plakalarla karşılaştırılır. Plaka kayıtlıysa "Access Granted" (Geçiş Onaylandı), kayıtlı değilse "Access Denied" (Geçiş Reddedildi) uyarısı verilir. Araç tır değilse buzzer uyarısı simüle edilir.

# ✨ Temel Amaç:

Kamera görüntüsünden gelen bilgileri işleyerek:

Tır/kamyon algılamak

Plaka tanıyıp doğrulamak

İlgili duruma göre karar vermek

# 🔹 Adım Adım Proje Gelişimi

# 1. YOLOv8 Modeliyle Nesne Tespiti

Roboflow kullanılarak 3 sınıflı (truck, car, plate) bir dataset oluşturuldu. YOLOv8 kullanılarak bu veri seti üzerinde ağırılıklar eğitildi:

# from ultralytics import YOLO
# model = YOLO('yolov8n.pt')
# model.train(
   #  data='data.yaml',
   #  epochs=50,
   #  imgsz=640,
   #  batch=16,
   #  project='plate_project',
   #  name='truck_best',
   #  exist_ok=True
# )

