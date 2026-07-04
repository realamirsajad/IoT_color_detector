# IoT_color_detector
Color detection and classifying them using the Internet of Things (IoT)

### 📌 Project Overview
This project presents an automated, real-time industrial sorting asset developed as a Capstone Project 

The system leverages **Edge Computer Vision (OpenCV)** running on a **Raspberry Pi 4** to evaluate multi-class object color profiles across 12 distinct categories. Local inventory states are continuously updated and streamed asynchronously over a **Distributed IoT Network** directly to cloud dashboards (**ThingSpeak**), providing smart-factory transparency for remote operational monitoring.

---

## 🏗️ System Architecture & Workflow

```text
 📥 RAW ASSET INPUT (Conveyor Line)
         │
         ▼
 💡 HARDWARE SHIELDING ──► [Enclosed Chamber] + [8-LED Warm NeoPixel Array] (Light Noise Isolation)
         │
         ▼
 📸 EDGE INSPECTION   ──► [PiCamera] Capture ──► Force Close Routine (Capacitor Discharge Fix)
         │
         ▼
 🧠 VISION CORES      ──► [OpenCV] ROI Isolation ──► 3D HSV Average Vector Classification
         │
         ▼
 📊 DATA METRICS      ──► Local Inventory Tracking Array Incremented
         │
         ▼
 🌐 CLOUD STREAMING   ──► [Asynchronous REST Serialization] ──► ThingSpeak IoT Dashboards
