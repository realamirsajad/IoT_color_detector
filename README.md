# 🌐 IoT-Driven Color Recognition, Sorting, & Counting System

### 📌 Project Overview
The system addresses critical challenges in modern industrial automation, product lines, and smart factory sorting by integrating an edge-computed computer vision engine with remote cloud infrastructure. It builds a fully automated, real-time color profiling and asset-counting device driven by **Raspberry Pi, OpenCV, and IoT connectivity**.

---

## 🛠️ System Architecture & Features

### 👁️ 1. HSV-Based Computer Vision Engine
Instead of relying on fragile, standard RGB sensors that suffer under shifting conditions, the system leverages an advanced image processing pipeline implemented in Python and OpenCV on a Raspberry Pi:
* **Pixel-Level Feature Extraction:** For every captured frame, the script dynamically evaluates the Hue (H), Saturation (S), and Value (V) profiles across individual pixels.
* **3D Characteristic Vectors:** The system calculates a spatial mathematical average of these parameters to construct a distinct, 3-dimensional characteristic vector representing the dominant color of the object.
* **Multi-Class Classification:** The algorithm reliably classifies targeted objects into **12 distinct color categories** (including primary, secondary, and neutral industrial tones) with exceptional accuracy.

### 💡 2. Controlled Ambient Calibration (Eliminating Light Noise)
To completely neutralize external light noise and guarantee absolute data consistency across operations, the system relies on an integrated ambient calibration setup:
* **Enclosed Sensing Chamber:** The hardware is housed within a sealed junction chamber to completely isolate the inspected object from external, unpredictable environmental light variables.
* **Addressable NeoPixel Ring:** An 8-LED addressable NeoPixel ring is integrated inside the chamber, delivering a software-controlled, statically uniform light field that mimics ideal natural ambient light during exposure.

### ⚙️ 3. Embedded Hardware Optimization & Dual-Mode Execution
To bridge prototyping with field usability, the control logic features an interactive execution gateway split into two distinct operational profiles:

* **Mode 1: Continuous Batch Processing (Production Mode)**
  Engineered for automated conveyor lines. It sequentially triggers lighting configurations, performs live asset capture, executes the vision pipeline, updates localized inventory arrays, and flushes data packets directly to the cloud server upon batch completion.
* **Mode 2: Targeted Asset Inspection (Single-Frame Test Mode)**
  Designed for diagnostic and sensor-calibration routines. It prompts the hardware to capture an isolated evaluation frame, executes localized Region-of-Interest (ROI) processing, and deploys a desktop verification UI (`cv2.imshow`) so operators can verify structural alignment and color categorization accuracy on the fly.

> ⚠️ **Hardware Edge-Case Fix:** While deploying sequential image captures on the Raspberry Pi camera module, back-to-back captures quickly saturated the camera’s internal charge-coupled capacitors, causing progressive image degradation and color distortion. To solve this, at the end of every sampling cycle, the script systematically invokes a `.close()` routine to force-discharge the camera capacitors before immediately re-initializing the module for the next asset inspection loop.

### 🌐 4. Cloud IoT Monitoring & Analytics
After classifying and incrementing the item count, data packets are instantly serialized and transmitted via REST APIs to a remote **ThingSpeak IoT cloud server**:
* Provides production managers with remote access to real-time throughput metrics.
* Generates live sorting distribution charts and device health statistics accessible from any location worldwide.

---

## 📈 Key Technical Competencies Demonstrated

* **Software Engineering:** Python, OpenCV (Image Processing), Adafruit NeoPixel Library, Linux Environment, API Integrations, Git Version Control.
* **Hardware Interfacing:** Raspberry Pi 4 Architecture, Addressable LED Arrays, CSI Camera Interfaces, Custom Sensing/Isolation Chambers.
* **Control Theory & Systems:** Sensor Calibration, Metric Noise-Filtering, Distributed System Architecture, Edge-to-Cloud Topology.

---

## 📂 File Structure
```text
├── IoT_color_detection.py      # Main Python pipeline (Vision, NeoPixel control, & Cloud Streaming)
└── README.md                   # Project documentation 
