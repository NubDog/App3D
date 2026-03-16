import keyboard
import time
import os
from PIL import ImageGrab

SAVE_DIR = r"F:\Project\ROK Tool\img\Babarian Level"

def save_screenshot():
    name = input("Nhập tên file ảnh (không cần .png): ").strip()
    if not name:
        print("❌ Tên file trống, bỏ qua.")
        return
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    print("Bây giờ hãy nhấn Win + Shift + S để chụp ảnh màn hình...")
    # Chờ cho đến khi clipboard có ảnh
    img = None
    while img is None:
        time.sleep(0.5)
        img = ImageGrab.grabclipboard()
    
    file_path = os.path.join(SAVE_DIR, f"{name}.png")
    img.save(file_path)
    print(f"✅ Ảnh đã được lưu tại: {file_path}\n")

if __name__ == "__main__":
    print("=== Screenshot Saver by SharkEatRice ===")
    while True:
        save_screenshot()