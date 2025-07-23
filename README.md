# Intelligent Truck & Plate Recognition System

A real-time Flask web application for detecting trucks and recognizing license plates using YOLOv8 and OCR technologies. Designed to control access based on vehicle type and license plate verification against a local database. Supports mobile and PC webcams, and offers a responsive web UI for field use.

---

## Project Goal

To develop a smart security system capable of:

- Detecting trucks in real-time video  
- Extracting and recognizing license plates  
- Matching recognized plates with a registered whitelist  
- Triggering access (gate open) or denial (buzzer alert) decisions  
- Providing a responsive web interface for monitoring and registration  

---

## Live Demo Overview

- Detects trucks only (cars are rejected)  
- Reads the plate via OCR  
- Grants access if the plate is registered  
- Blocks access if the plate is unknown  
- Rejects cars with warning  
- Web interface displays video + messages  
- Extra page to register new plates  

---

## Tech Stack

| Component         | Technology               |
|------------------|--------------------------|
| Object Detection | YOLOv8 (Ultralytics)     |
| OCR Engine       | EasyOCR or PaddleOCR     |
| Backend          | Python + Flask           |
| Database         | SQLite                   |
| Frontend         | HTML5 + Bootstrap        |
| Video Input      | PC/Mobile Webcam (IP) via OpenCV |

---

## Mobile Camera Usage (Optional)

You can stream your phone's camera to the PC:

- **Android**: Install [DroidCam](https://www.dev47apps.com/)  
- **iOS**: Use [EpocCam](https://www.elgato.com/en/epoccam) or [NDI HX Camera](https://www.ndi.tv/tools/)

Update this line in `app.py`:

camera_source = "http://<your_phone_ip>:4747/video"

The system was tested using a mobile camera streamed through the IP Webcam app. : https://youtu.be/BMxCdjOMy6g

Tested using pre-recorded video footage. : https://youtu.be/USk4UG6hEFU


## Access Logic

| Vehicle Type | Plate Registered? | Action           |
|--------------|-------------------|------------------|
| Truck        | Yes               | Access Granted   |
| Truck        | No                | Access Denied    |
| Car          | Irrelevant        | Buzzer Alert     |

## Features

- **Real-time object detection**
- **OCR plate recognition**
- **SQLite plate validation**
- **Live video + access status UI**
- **Responsive design (mobile & desktop)**
-  **Admin panel to register new plates**

---

## Author

Developed by **Haticenur Yalman**  
This project was created as part of the Introduction to Computer Vision course.




