import cv2
import numpy as np
import pyautogui
import win32api
import win32con
import time
import random
from datetime import datetime
import os
import json

class XiaomiBot:
    def __init__(self, turbo_mode=True):
        self.log_file = r"f:\Project\Xiaomi Tool\log.txt"
        self.location_file = r"f:\Project\Xiaomi Tool\location.txt"
        self.img_864 = r"f:\Project\Xiaomi Tool\img\864.png"
        self.img_failed = r"f:\Project\Xiaomi Tool\img\Faild.png"
        self.img_ok = r"f:\Project\Xiaomi Tool\img\Ok.png"
        self.img_next = r"f:\Project\Xiaomi Tool\img\Tiep-theo.png"
        self.confidence = 0.8
        self.cycle_count = 0
        self.turbo_mode = turbo_mode
        self.locations = self.load_locations()
        self.used_numbers_cache = None
        
    def load_locations(self):
        if os.path.exists(self.location_file):
            try:
                with open(self.location_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_locations(self):
        with open(self.location_file, 'w', encoding='utf-8') as f:
            json.dump(self.locations, f, indent=2, ensure_ascii=False)
    
    def click(self, x, y):
        win32api.SetCursorPos((x, y))
        if self.turbo_mode:
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            time.sleep(0.03)
        else:
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            time.sleep(0.03)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            time.sleep(0.1)
    
    def find_image(self, template_path, use_cache=True, cache_key=None):
        # Dùng cache nếu có
        if use_cache and cache_key and cache_key in self.locations:
            return tuple(self.locations[cache_key])
        
        # Tìm bằng hình ảnh
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=self.confidence)
            if location:
                center = pyautogui.center(location)
                pos = (int(center.x), int(center.y))
                
                if cache_key:
                    self.locations[cache_key] = list(pos)
                
                return pos
        except:
            pass
        return None
    
    def get_used_numbers(self):
        if self.used_numbers_cache is not None:
            return self.used_numbers_cache
        
        used_numbers = set()
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts and len(parts[0]) == 9 and parts[0].isdigit():
                        used_numbers.add(parts[0])
        
        self.used_numbers_cache = used_numbers
        return used_numbers
    
    def generate_random_digits(self, digit_count=6):
        used_numbers = self.get_used_numbers()
        min_val = 10 ** (digit_count - 1)
        max_val = 10 ** digit_count - 1
        
        for _ in range(1000):
            random_digits = str(random.randint(min_val, max_val))
            if random_digits not in used_numbers:
                used_numbers.add(random_digits)
                return random_digits
        
        return str(random.randint(min_val, max_val))
    
    def press_backspace(self, times):
        delay = 0.005 if self.turbo_mode else 0.05
        for _ in range(times):
            pyautogui.press('backspace')
            time.sleep(delay)
    
    def type_number(self, number):
        interval = 0.01 if self.turbo_mode else 0.05
        pyautogui.typewrite(str(number), interval=interval)
        time.sleep(0.02 if self.turbo_mode else 0.1)
    
    def save_log(self, full_number, status="fail"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{full_number} {timestamp} {status}\n"
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def run_one_cycle(self):
        self.cycle_count += 1
        is_first_run = (self.cycle_count == 1)
        start_time = time.time()
        
        # Tìm 864
        pos_864 = self.find_image(self.img_864, use_cache=not is_first_run, cache_key="pos_864")
        if not pos_864:
            print("\n❌ Không tìm thấy 864!")
            return False
        
        # Click vào ô nhập
        if is_first_run:
            click_x = pos_864[0] + 400
            click_y = pos_864[1]
            self.locations["click_input"] = [click_x, click_y]
        else:
            click_x, click_y = self.locations["click_input"]
        
        self.click(click_x, click_y)
        time.sleep(0.05 if self.turbo_mode else 0.2)
        
        # Xóa và nhập số
        if is_first_run:
            self.press_backspace(6)
            random_digits = self.generate_random_digits(6)
            full_number = "864" + random_digits
            print(f"Lần 1: {full_number}")
            self.type_number(random_digits)
        else:
            self.press_backspace(9)
            full_number = self.generate_random_digits(9)
            self.type_number(full_number)
        
        time.sleep(0.05 if self.turbo_mode else 0.2)
        
        # Click Tiep-theo
        pos_next = self.find_image(self.img_next, use_cache=not is_first_run, cache_key="pos_next")
        if not pos_next:
            print("\n❌ Không tìm thấy Tiep-theo!")
            return False
        
        self.click(pos_next[0], pos_next[1])
        time.sleep(0.6 if self.turbo_mode else 1.2)
        
        # Lưu vị trí lần đầu
        if is_first_run:
            self.save_locations()
            print("✓ Đã lưu vị trí các nút")
        
        # Kiểm tra Faild
        pos_failed = self.find_image(self.img_failed, use_cache=False)
        if not pos_failed:
            print("\n❌ Không có Faild - DỪNG!")
            return "STOP"
        
        # Click Ok
        pos_ok = self.find_image(self.img_ok, use_cache=not is_first_run, cache_key="pos_ok")
        if not pos_ok:
            print("\n❌ Không tìm thấy Ok!")
            return False
        
        self.click(pos_ok[0], pos_ok[1])
        time.sleep(0.2 if self.turbo_mode else 0.5)
        
        if is_first_run:
            self.save_locations()
        
        # Lưu log
        self.save_log(full_number, "fail")
        
        elapsed = time.time() - start_time
        print(f"\r🚀 #{self.cycle_count} | {full_number} | {elapsed:.2f}s", end="", flush=True)
        
        return True
    
    def run_continuous(self):
        print(f"\n🔄 CHẠY LIÊN TỤC {'[TURBO]' if self.turbo_mode else '[NORMAL]'} (Ctrl+C để dừng)")
        self.cycle_count = 0
        start_time = time.time()
        
        try:
            while True:
                result = self.run_one_cycle()
                
                if result == "STOP":
                    print("\n⛔ Dừng: Không có Faild")
                    break
                elif not result:
                    print("\n⚠ Lỗi, thử lại sau 1s...")
                    time.sleep(1)
                else:
                    time.sleep(0.3 if self.turbo_mode else 1)
                    
        except KeyboardInterrupt:
            print("\n\n⛔ Dừng bởi người dùng")
        
        elapsed = time.time() - start_time
        avg_time = elapsed / self.cycle_count if self.cycle_count > 0 else 0
        print(f"\n📊 Tổng: {self.cycle_count} vòng | {elapsed:.1f}s | TB: {avg_time:.2f}s/vòng")
    
    def run_limited(self, times):
        print(f"\n🔢 CHẠY {times} LẦN {'[TURBO]' if self.turbo_mode else '[NORMAL]'}")
        self.cycle_count = 0
        success_count = 0
        start_time = time.time()
        
        for i in range(times):
            result = self.run_one_cycle()
            
            if result == "STOP":
                print("\n⛔ Dừng: Không có Faild")
                break
            elif not result:
                print("\n⚠ Lỗi, bỏ qua...")
            else:
                success_count += 1
                
            if i < times - 1:
                time.sleep(0.3 if self.turbo_mode else 1)
        
        elapsed = time.time() - start_time
        avg_time = elapsed / success_count if success_count > 0 else 0
        print(f"\n📊 Hoàn thành: {success_count}/{times} | {elapsed:.1f}s | TB: {avg_time:.2f}s/vòng")

def show_menu():
    print("\n" + "="*50)
    print("🤖 XIAOMI BOT - TURBO MODE")
    print("="*50)
    print("1. Chạy liên tục TURBO (Nhanh nhất)")
    print("2. Chạy theo số lần TURBO")
    print("3. Chạy liên tục NORMAL (An toàn)")
    print("4. Chạy theo số lần NORMAL")
    print("5. Thoát")
    print("="*50)

def main():
    while True:
        show_menu()
        choice = input("Chọn (1-5): ").strip()
        
        if choice == "1":
            bot = XiaomiBot(turbo_mode=True)
            bot.run_continuous()
            
        elif choice == "2":
            try:
                times = int(input("Nhập số lần: ").strip())
                if times > 0:
                    bot = XiaomiBot(turbo_mode=True)
                    bot.run_limited(times)
                else:
                    print("❌ Số lần phải > 0!")
            except ValueError:
                print("❌ Nhập số hợp lệ!")
                
        elif choice == "3":
            bot = XiaomiBot(turbo_mode=False)
            bot.run_continuous()
            
        elif choice == "4":
            try:
                times = int(input("Nhập số lần: ").strip())
                if times > 0:
                    bot = XiaomiBot(turbo_mode=False)
                    bot.run_limited(times)
                else:
                    print("❌ Số lần phải > 0!")
            except ValueError:
                print("❌ Nhập số hợp lệ!")
                
        elif choice == "5":
            print("\n👋 Tạm biệt!")
            break
            
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
