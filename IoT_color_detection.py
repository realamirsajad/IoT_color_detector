"""
Industrial Automation: IoT-Driven Color Recognition, Sorting, & Counting System
BSc Capstone Project - K. N. Toosi University of Technology
Author: Amir Sajjad Ebrahimi & Farshid Hosseinzadeh

Description:
This script integrates custom ambient lighting via an 8-LED NeoPixel ring with 
an OpenCV HSV-based color profiling engine. It classifies objects into 12 distinct 
color categories, counters them, manages hardware camera initialization/closure 
to prevent capacitor degradation, and logs real-time telemetry to ThingSpeak.
"""

import time
import os
import cv2
import numpy as np
import board 
import neopixel 
import picamera 
import thingspeak 

# ==========================================
# === 1. SYSTEM CONFIGURATION & CALIBRATION ===
# ==========================================
INTERVAL = 12 
DESKTOP_PATH = '/home/pi/Desktop' 
NUM_LEDS = 8 

# Initialize NeoPixel Ring on GPIO 18
np_ring = neopixel.NeoPixel(board.D18, NUM_LEDS) 
np_ring.brightness = 1.0

# ThingSpeak Cloud Configuration 
# Note: Replace these with your active keys if deploying on live hardware
THINGSPEAK_API_KEY_1 = 'QKWX4J0V7EB2XNTS' 
CHANNEL_ID_1 = '2322926' 
THINGSPEAK_API_KEY_2 = 'Q0AIFC2F7GCLGPCB' 
CHANNEL_ID_2 = '2358608' 

# Calibrated HSV boundaries for 12 core industrial colors
COLOR_RANGES = { 
    "Red": ((0, 100, 90), (5, 255, 255)), 
    "Red": ((174, 100, 90), (180, 255, 255)), # Wrap-around red spectrum
    "Orange": ((5, 100, 90), (17, 255, 255)), 
    "Yellow": ((17, 100, 90), (34, 255, 255)), 
    "Green": ((34, 100, 90), (75, 255, 255)), 
    "Cyan": ((75, 100, 90), (100, 255, 255)), 
    "Blue": ((100, 100, 60), (140, 255, 255)), 
    "Purple": ((140, 100, 50), (167, 255, 255)), 
    "Pink": ((167, 100, 90), (174, 255, 255)), 
    "Brown": ((3, 100, 20), (30, 255, 200)), 
    "Gray": ((0, 0, 90), (180, 60, 200)), 
    "White": ((0, 0, 90), (70, 70, 255)), 
    "Black": ((0, 0, 0), (180, 255, 100)) 
} 

# Initialize multi-class inventory tracker counters
color_counts = {color: 0 for color in COLOR_RANGES}
color_counts["Red"] = 0 # Consolidated Red key

# ==========================================
# === 2. HARDWARE & CLOUD TELEMETRY      ===
# ==========================================
def apply_ambient_lighting(): 
    """Displays a calibrated warm static white light while turning off noise-prone nodes.""" 
    for i in range(NUM_LEDS): 
        if i in [1, 3, 5, 7]: 
            np_ring[i] = (0, 0, 0)  # Turn off alternating LEDs to prevent glare
        else: 
            np_ring[i] = (255, 200, 40)  # Custom calibrated warm lighting vector
    np_ring.show() 

def send_to_thingspeak_ch1(counts): 
    """Dispatches aggregated inventory telemetry for Channel 1 colors."""
    try:
        channel = thingspeak.Channel(id=CHANNEL_ID_1, api_key=THINGSPEAK_API_KEY_1) 
        # Consolidation of Red sub-keys for reporting consistency
        total_red = counts["Red_1"] + counts["Red_2"] + counts["Red"]
        response = channel.update({
            'field1': counts["Blue"], 'field2': total_red, 
            'field3': counts["Green"], 'field4': counts["Purple"], 
            'field5': counts["Pink"], 'field6': counts["White"]
        }) 
        print(f'[IoT CLOUD] ThingSpeak Channel 1 update response: {response}') 
    except Exception as e:
        print(f'[IoT CLOUD ERROR] Channel 1 dispatch failed: {e}')

def send_to_thingspeak_ch2(counts): 
    """Dispatches aggregated inventory telemetry for Channel 2 colors."""
    try:
        channel = thingspeak.Channel(id=CHANNEL_ID_2, api_key=THINGSPEAK_API_KEY_2) 
        response = channel.update({
            'field1': counts["Cyan"], 'field2': counts["Brown"], 
            'field3': counts["Yellow"], 'field4': counts["Orange"], 
            'field5': counts["Gray"], 'field6': counts["Black"]
        }) 
        print(f'[IoT CLOUD] ThingSpeak Channel 2 update response: {response}') 
    except Exception as e:
        print(f'[IoT CLOUD ERROR] Channel 2 dispatch failed: {e}')

# ==========================================
# === 3. COMPUTER VISION PROCESSOR       ===
# ==========================================
def get_color(image_path): 
    """Extracts spatial mean vectors across HSV dimensions to classify objects."""
    img = cv2.imread(image_path) 
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 

    mean_h = np.mean(hsv_img[:, :, 0]) 
    mean_s = np.mean(hsv_img[:, :, 1]) 
    mean_v = np.mean(hsv_img[:, :, 2]) 
 
    print(f"[VISION ENGINE] Spatial HSV Averages -> H: {mean_h:.2f}, S: {mean_s:.2f}, V: {mean_v:.2f}") 
 
    for color, (lower, upper) in COLOR_RANGES.items(): 
        if (lower[0] <= mean_h <= upper[0] and 
            lower[1] <= mean_s <= upper[1] and 
            lower[2] <= mean_v <= upper[2]): 
            return color 
 
    return "Unknown" 

# ==========================================
# === 4. DETERMINISTIC EXECUTION BRANCHES ===
# ==========================================
try: 
    # Initialize hardware lighting array
    apply_ambient_lighting()

    print("=== Industrial Color Sorting & Tracking Pipeline ===") 
    print("1. Capture and Process Multiple Pictures (Production Mode)") 
    print("2. Capture and Detect Color for a Single Picture (Test Mode)") 
    mode = input("Enter execution mode (1/2): ") 
 
    if mode == '1': 
        num_pictures = int(input("Enter number of sorting cycles to run: ")) 
 
        for i in range(num_pictures): 
            # --- CRITICAL HARDWARE FIX: SYSTEMATIC CAMERA RESET ---
            # Re-instantiating the camera object per loop explicitly discharges internal 
            # charge-coupled capacitors, eliminating light bias drift over long uptimes.
            camera = picamera.PiCamera() 
            camera.resolution = (2592, 1944) 
 
            filename = f'{DESKTOP_PATH}/picture_{i}.jpg' 
            camera.capture(filename) 
            print(f"[HARDWARE] Captured raw asset: {filename}") 
 
            # Region of Interest (ROI) isolation cropping
            x, y, w, h = 500, 500, 850, 850 
            image = cv2.imread(filename) 
            cropped_image = image[y:y+h, x:x+w] 
 
            image_filename = f'cropped_image_{i}.jpg' 
            cropped_path = os.path.join(DESKTOP_PATH, image_filename) 
            cv2.imwrite(cropped_path, cropped_image) 
 
            # Evaluate Color Vector
            detected_color = get_color(cropped_path) 
            
            # Map sub-keys to main tracking categories
            display_color = "Red" if "Red" in detected_color else detected_color
            color_counts[detected_color] += 1 
            print(f"[CLASSIFIER] Target designated as: {display_color}") 
 
            # Explicit hardware release to discharge camera electronics safely
            camera.close() 
            time.sleep(INTERVAL) 
 
        # Sync local data inventory arrays to IoT Server
        print("[DATA METRICS] Conveyor batch completed. Syncing cloud analytics...")
        send_to_thingspeak_ch1(color_counts) 
        send_to_thingspeak_ch2(color_counts) 
 
    elif mode == '2': 
        camera = picamera.PiCamera() 
        camera.resolution = (2592, 1944) 
 
        filename = f'{DESKTOP_PATH}/single_picture.jpg' 
        camera.capture(filename) 
        print(f"[HARDWARE] Single evaluation frame captured: {filename}") 
 
        x, y, w, h = 500, 500, 850, 850 
        image = cv2.imread(filename) 
        cropped_image = image[y:y+h, x:x+w] 
 
        cropped_path = os.path.join(DESKTOP_PATH, 'cropped_single.jpg') 
        cv2.imwrite(cropped_path, cropped_image) 
 
        detected_color = get_color(cropped_path) 
        display_color = "Red" if "Red" in detected_color else detected_color
        print(f"[CLASSIFIER] Test run evaluation color: {display_color}") 
         
        camera.close() 
        
        # Open verification UI frame
        cv2.imshow("Enclosed Chamber Crop Verification", cropped_image) 
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 
     
    else: 
        print("[SYSTEM ERROR] Invalid configuration branch selected.") 
         
except KeyboardInterrupt: 
    print("\n[SYSTEM WARNING] Operations interrupted via operator console input.") 
finally:
    # Safe resource tracking shutdown
    if 'camera' in locals(): 
        camera.close()
    print("[SYSTEM] Infrastructure decoupled safely.")