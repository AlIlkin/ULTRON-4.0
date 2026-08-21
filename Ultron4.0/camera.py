import cv2
import os
from datetime import datetime

def take_photo(output_dir="captures"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("\n[Ultron] Accessing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[Ultron Error] Could not open webcam.")
        return False
        
    try:
        ret, frame = cap.read()
        if not ret:
            print("[Ultron Error] Failed to grab frame.")
            return False
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"capture_{timestamp}.jpg")
        
        cv2.imwrite(filename, frame)
        print(f"\n[Ultron] Photo captured successfully and saved as '{filename}'!")
        return filename
        
    except Exception as e:
        print(f"[Ultron Error] Camera capture failed: {e}")
        return False
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
