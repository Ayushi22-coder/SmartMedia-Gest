import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import pyautogui
import time
import keyboard  # Added for YouTube Shorts control

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Volume Control Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol, max_vol = vol_range[0], vol_range[1]

# Webcam Setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Control Modes
MODE_VOLUME = 0
MODE_BRIGHTNESS = 1
MODE_MEDIA = 2
current_mode = MODE_VOLUME
last_mode_change = 0
mode_cooldown = 1  # seconds

# Media Control States
media_playing = True
last_gesture_time = 0
gesture_cooldown = 0.5  # seconds

def set_brightness(percent):
    try:
        sbc.set_brightness(percent)
    except Exception as e:
        print("Brightness control error:", e)

def media_control(command):
    global media_playing, last_gesture_time
    current_time = time.time()
    if current_time - last_gesture_time < gesture_cooldown:
        return
    
    try:
        if command == "play_pause":
            pyautogui.press('playpause')
            media_playing = not media_playing
        elif command == "next":
            # For YouTube Shorts (Chrome/Firefox)
            keyboard.press_and_release('shift+n')  # Next Short
        elif command == "previous":
            # For YouTube Shorts (Chrome/Firefox)
            keyboard.press_and_release('shift+p')  # Previous Short
        last_gesture_time = current_time
    except Exception as e:
        print("Media control error:", e)

while True:
    success, img = cap.read()
    if not success:
        continue
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            lm_list = []
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            
            if len(lm_list) >= 21:
                # Mode Switching (Thumb + Pinky)
                thumb_tip = lm_list[4]
                pinky_tip = lm_list[20]
                distance = math.hypot(pinky_tip[1]-thumb_tip[1], pinky_tip[2]-thumb_tip[2])
                
                current_time = time.time()
                if distance > 100 and (current_time - last_mode_change) > mode_cooldown:
                    current_mode = (current_mode + 1) % 3
                    last_mode_change = current_time
                
                # Volume Control
                if current_mode == MODE_VOLUME:
                    index_tip = lm_list[8]
                    length = math.hypot(index_tip[1]-thumb_tip[1], index_tip[2]-thumb_tip[2])
                    vol = np.interp(length, [30, 200], [min_vol, max_vol])
                    volume.SetMasterVolumeLevel(vol, None)
                    
                    cv2.putText(img, "VOLUME MODE", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0, 255, 0), 2)
                    cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, (index_tip[1], index_tip[2]), 15, (0, 255, 0), cv2.FILLED)
                
                # Brightness Control
                elif current_mode == MODE_BRIGHTNESS:
                    index_tip = lm_list[8]
                    length = math.hypot(index_tip[1]-thumb_tip[1], index_tip[2]-thumb_tip[2])
                    brightness = np.interp(length, [30, 200], [0, 100])
                    set_brightness(int(brightness))
                    
                    cv2.putText(img, "BRIGHTNESS MODE", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (255, 255, 0), 2)
                    cv2.circle(img, (thumb_tip[1], thumb_tip[2]), 15, (255, 255, 0), cv2.FILLED)
                    cv2.circle(img, (index_tip[1], index_tip[2]), 15, (255, 255, 0), cv2.FILLED)
                
                # Media Control
                elif current_mode == MODE_MEDIA:
                    index_tip = lm_list[8]
                    middle_tip = lm_list[12]
                    ring_tip = lm_list[16]
                    
                    # Play/Pause
                    dist_index = math.hypot(index_tip[1]-thumb_tip[1], index_tip[2]-thumb_tip[2])
                    if dist_index < 30:
                        media_control("play_pause")
                        cv2.putText(img, "PLAY/PAUSE", (thumb_tip[1]-50, thumb_tip[2]-30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    # Next Short
                    dist_middle = math.hypot(middle_tip[1]-thumb_tip[1], middle_tip[2]-thumb_tip[2])
                    if dist_middle < 30:
                        media_control("next")
                        cv2.putText(img, "NEXT SHORT", (middle_tip[1]-70, middle_tip[2]-30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    # Previous Short
                    dist_ring = math.hypot(ring_tip[1]-thumb_tip[1], ring_tip[2]-thumb_tip[2])
                    if dist_ring < 30:
                        media_control("previous")
                        cv2.putText(img, "PREV SHORT", (ring_tip[1]-70, ring_tip[2]-30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    
                    cv2.putText(img, "MEDIA MODE", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                1, (0, 165, 255), 2)
                    cv2.putText(img, f"Status: {'PLAYING' if media_playing else 'PAUSED'}", 
                                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
    
    cv2.putText(img, f"MODE: {['VOLUME', 'BRIGHTNESS', 'MEDIA'][current_mode]} (Switch: Thumb+Pinky)", 
                (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()