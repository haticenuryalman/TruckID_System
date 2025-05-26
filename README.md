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

# 2. EasyOCR ile Plaka Tanıma

YOLO ile plaka tespit edildikten sonra bu plaka bölgesi işlenip EasyOCR ile okunur:

<img width="349" alt="Ekran Resmi 2025-05-27 00 11 25" src="https://github.com/user-attachments/assets/46b38447-d897-40a0-8b6d-2e9b963d7145" />

OCR sonucunda elde edilen yazı regex ile filtrelenip sadece A-Z/0-9 karakterleri kalacak şekilde temizlenir.

# 3. Flask Arayüz Geliştirme

Flask kullanılarak basit bir web uygulaması geliştirildi. 2 ana sayfa vardır:

/ : Canlı kamera yayını + anlık mesajlar

/ekle : Yeni plaka ekleme formu

HTML sayfaları Bootstrap ile mobil uyumlu hale getirildi.

<img width="542" alt="Ekran Resmi 2025-05-27 00 12 42" src="https://github.com/user-attachments/assets/cd216a7b-ccdd-40f3-b1ee-561750bbc628" />

# 4. SQLite ile Plaka Saklama

Uygulama ilk başladığında bir plakalar.db dosyası oluşturur. Kullanıcı yeni plaka ekledikçe veritabanına yazılır.

<img width="666" alt="Ekran Resmi 2025-05-27 00 14 22" src="https://github.com/user-attachments/assets/3a5ed59a-6e40-4022-8ca8-ed6b1fbe36b7" />

# 5. Mobil Cihaz Kamerası ile Test

Uygulama mobil kameradan test edilebilecek şekilde geliştirildi. Telefon kameranın IP adresi "camera_source" değişkenine atanır:

<img width="666" alt="Ekran Resmi 2025-05-27 00 15 05" src="https://github.com/user-attachments/assets/4da23f83-33b7-4af8-b4ab-56c60767c036" />
DroidCam veya EpocCam ile mobil cihazlar desteklenebilir.

# 6. Webcam, Video ve Mobil Seçenekleri

   <img width="666" alt="Ekran Resmi 2025-05-27 00 16 04" src="https://github.com/user-attachments/assets/efc1aa38-d480-43a1-90fb-3ab65e3ad2a2" />
   
# 7. Yatay Video Sorunu Çözümü

Bazı telefon kameraları dikey video verir. Çerçeveyi yatay döndürmek için bu satır aktif edilir:

<img width="666" alt="Ekran Resmi 2025-05-27 00 17 12" src="https://github.com/user-attachments/assets/b70db8cd-9f48-4f89-bc5a-a9abe41ff350" />


# 🌐 Projede Ne Yaptık?

YOLOv8 ile tır, araba ve plaka tespiti yaptık

EasyOCR ile plakaları okuduk

Veritabanı kontrolü ile plaka eşleştirme yaptık

Flask arayüzü ile mobil uyumlu, responsive bir arayüz yaptık

Mobil kamerayla canlı test yeteneği ekledik

Yönlendirme mesajlarıyla kullanıcıyı bilgilendiren sistem tasarladık

Tüm kodlar, HTML sayfaları ve model dosyası ile birlikte proje çalışır hâle getirilmiştir.

