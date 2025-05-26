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

<img width="349" alt="Ekran Resmi 2025-05-27 00 10 21" src="https://github.com/user-attachments/assets/a4212c9b-936f-4303-859e-1c3c193e4286" />



