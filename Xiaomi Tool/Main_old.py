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
    def __init__(self):
        self.log_file = r"f:\Project\Xiaomi Tool\log.txt"
        self.location_file = r"f:\Project\Xiaomi Tool\location.txt"
        self.img_864 = r"f:\Project\Xiaomi Tool\img\864.png"
        self.img_failed = r"f:\Project\Xiaomi Tool\img\Faild.png"
        self.img_ok = r"f:\Project\Xiaomi Tool\img\Ok.png"
        self.img_next = r"f:\Project\Xiaomi Tool\img\Tiep-theo.png"
        self.confidence = 0.8
        self.cycle_count = 0  # Đếm số lần chạy
        self.locations = self.load_locations()
        
    def load_locations(self):
        """Đọc vị trí đã lưu từ location.txt"""
        if os.path.exists(self.location_file):
            try:
                with open(self.location_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_locations(self):
        """Lưu vị trí vào location.txt"""
        with open(self.location_file, 'w', encoding='utf-8') as f:
            json.dump(self.locations, f, indent=2, ensure_ascii=False)
        print(f"💾 Đã lưu vị trí vào {self.location_file}")
    
    def click(self, x, y):
        """Click chuột tại vị trí (x, y)"""
        win32api.SetCursorPos((x, y))
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.3)
    
    def find_image(self, template_path, confidence=None, use_cache=True, cache_key=None):
        """Tìm hình ảnh trên màn hình hoặc dùng vị trí đã lưu"""
        # Nếu có cache và đã lưu vị trí, dùng luôn
        if use_cache and cache_key and cache_key in self.locations:
            pos = self.locations[cache_key]
            print(f"📍 Dùng vị trí đã lưu: {cache_key} = {pos}")
            return tuple(pos)
        
        # Tìm bằng hình ảnh
        if confidence is None:
            confidence = self.confidence
            
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                # Chuyển đổi np.int64 sang int để JSON có thể serialize
                pos = (int(center.x), int(center.y))
                
                # Lưu vị trí vào cache
                if cache_key:
                    self.locations[cache_key] = list(pos)
                    print(f"💾 Lưu vị trí mới: {cache_key} = {pos}")
                
                return pos
        except Exception as e:
            print(f"Không tìm thấy hình: {template_path}")
        return None
    
    def get_used_numbers(self):
        """Đọc các số đã dùng từ log.txt"""
        used_numbers = set()
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Lấy 9 số đầu tiên của mỗi dòng
                    parts = line.strip().split()
                    if parts and len(parts[0]) == 9 and parts[0].isdigit():
                        used_numbers.add(parts[0])
        return used_numbers
    
    def generate_random_digits(self, digit_count=6):
        """Tạo số ngẫu nhiên không trùng với log"""
        used_numbers = self.get_used_numbers()
        
        # Tạo min và max dựa trên số chữ số
        min_val = 10 ** (digit_count - 1)
        max_val = 10 ** digit_count - 1
        
        # Thử tối đa 1000 lần để tìm số không trùng
        for _ in range(1000):
            random_digits = str(random.randint(min_val, max_val))
            
            # Kiểm tra không trùng
            if random_digits not in used_numbers:
                return random_digits
        
        # Nếu không tìm được sau 1000 lần, vẫn trả về số ngẫu nhiên
        print("Cảnh báo: Không tìm được số không trùng sau 1000 lần thử")
        return str(random.randint(min_val, max_val))
    
    def press_backspace(self, times):
        """Nhấn backspace n lần"""
        for _ in range(times):
            pyautogui.press('backspace')
            time.sleep(0.1)
    
    def type_number(self, number):
        """Nhập số vào"""
        pyautogui.typewrite(str(number), interval=0.1)
        time.sleep(0.3)
    
    def save_log(self, full_number, status="fail"):
        """Lưu log vào file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{full_number} {timestamp} {status}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(f"Đã lưu log: {log_entry.strip()}")
    
    def run_one_cycle(self):
        """Chạy 1 vòng lặp"""
        self.cycle_count += 1
        is_first_run = (self.cycle_count == 1)
        
        print("\n" + "="*50)
        print(f"Bắt đầu vòng lặp #{self.cycle_count}" + (" (LẦN ĐẦU - TÌM VÀ LƯU VỊ TRÍ)" if is_first_run else " (DÙNG VỊ TRÍ ĐÃ LƯU)"))
        
        # Bước 1: Tìm hình 864.png hoặc dùng vị trí đã lưu
        print("1. Tìm hình 864.png...")
        pos_864 = self.find_image(self.img_864, use_cache=not is_first_run, cache_key="pos_864")
        if not pos_864:
            print("❌ Không tìm thấy hình 864.png!")
            return False
        
        print(f"✓ Vị trí 864: {pos_864}")
        
        # Bước 2: Click vào vị trí cách 400px sang phải
        # Lần đầu: tính từ pos_864, lần sau: dùng click_input đã lưu
        if is_first_run:
            click_x = pos_864[0] + 400
            click_y = pos_864[1]
            self.locations["click_input"] = [click_x, click_y]
        else:
            click_x, click_y = self.locations["click_input"]
        
        print(f"2. Click vào ô nhập: ({click_x}, {click_y})")
        self.click(click_x, click_y)
        time.sleep(0.5)
        
        # Bước 3 & 4: Xóa và nhập số
        if is_first_run:
            # Lần đầu: xóa 6 số, nhập 6 số mới
            print("3. Xóa 6 số cũ (backspace 6 lần)...")
            self.press_backspace(6)
            
            random_digits = self.generate_random_digits(6)
            full_number = "864" + random_digits
            print(f"4. Nhập 6 số ngẫu nhiên: {random_digits} (Số đầy đủ: {full_number})")
            self.type_number(random_digits)
        else:
            # Lần 2 trở đi: xóa 9 số, nhập 9 số mới
            print("3. Xóa 9 số cũ (backspace 9 lần)...")
            self.press_backspace(9)
            
            full_number = self.generate_random_digits(9)
            print(f"4. Nhập 9 số ngẫu nhiên: {full_number}")
            self.type_number(full_number)
        
        time.sleep(0.5)
        
        # Bước 5: Click vào Tiep-theo.png
        print("5. Tìm và click vào Tiep-theo.png...")
        pos_next = self.find_image(self.img_next, use_cache=not is_first_run, cache_key="pos_next")
        if not pos_next:
            print("❌ Không tìm thấy Tiep-theo.png!")
            return False
        
        print(f"✓ Click Tiep-theo tại: {pos_next}")
        self.click(pos_next[0], pos_next[1])
        time.sleep(1.5)  # Đợi load
        
        # Lưu vị trí sau lần đầu
        if is_first_run:
            self.save_locations()
        
        # Bước 6: Kiểm tra có Faild.png không
        print("6. Kiểm tra Faild.png...")
        pos_failed = self.find_image(self.img_failed, use_cache=False)  # Không cache Faild vì không phải lúc nào cũng có
        
        if not pos_failed:
            print("❌ KHÔNG tìm thấy Faild.png - BOT DỪNG LẠI!")
            return "STOP"
        
        print(f"✓ Tìm thấy Faild tại: {pos_failed}")
        
        # Bước 7: Click vào Ok.png
        print("7. Tìm và click vào Ok.png...")
        pos_ok = self.find_image(self.img_ok, use_cache=not is_first_run, cache_key="pos_ok")
        if not pos_ok:
            print("❌ Không tìm thấy Ok.png!")
            return False
        
        print(f"✓ Click Ok tại: {pos_ok}")
        self.click(pos_ok[0], pos_ok[1])
        time.sleep(1)
        
        # Lưu vị trí Ok sau lần đầu (nếu chưa lưu)
        if is_first_run:
            self.save_locations()
        
        # Bước 8: Lưu log
        print(f"8. Lưu log...")
        self.save_log(full_number, "fail")
        
        print("✓ Hoàn thành 1 vòng lặp!")
        return True
    
    def run_continuous(self):
        """Chạy liên tục"""
        print("\n🔄 CHẠY LIÊN TỤC (Nhấn Ctrl+C để dừng)")
        self.cycle_count = 0  # Reset counter
        
        try:
            while True:
                result = self.run_one_cycle()
                
                if result == "STOP":
                    print("\n⛔ Bot dừng lại vì không tìm thấy Faild.png")
                    break
                elif not result:
                    print("\n⚠ Có lỗi xảy ra, thử lại sau 3 giây...")
                    time.sleep(3)
                else:
                    time.sleep(2)  # Nghỉ 2 giây giữa các vòng
                    
        except KeyboardInterrupt:
            print("\n\n⛔ Người dùng dừng bot!")
        
        print(f"\n📊 Tổng số vòng đã chạy: {self.cycle_count}")
    
    def run_limited(self, times):
        """Chạy theo số lần"""
        print(f"\n🔢 CHẠY {times} LẦN")
        self.cycle_count = 0  # Reset counter
        success_count = 0
        
        for i in range(times):
            result = self.run_one_cycle()
            
            if result == "STOP":
                print("\n⛔ Bot dừng lại vì không tìm thấy Faild.png")
                break
            elif not result:
                print("\n⚠ Có lỗi xảy ra, bỏ qua vòng này...")
            else:
                success_count += 1
                
            if i < times - 1:  # Không nghỉ ở vòng cuối
                time.sleep(2)
        
        print(f"\n📊 Hoàn thành {success_count}/{times} vòng thành công!")

def show_menu():
    """Hiển thị menu"""
    print("\n" + "="*50)
    print("🤖 XIAOMI BOT - AUTOMATION TOOL")
    print("="*50)
    print("1. Chạy liên tục (Continuous)")
    print("2. Chạy theo số lần (Limited)")
    print("3. Thoát (Exit)")
    print("="*50)

def main():
    bot = XiaomiBot()
    
    while True:
        show_menu()
        choice = input("Chọn chức năng (1-3): ").strip()
        
        if choice == "1":
            bot.run_continuous()
            
        elif choice == "2":
            try:
                times = int(input("Nhập số lần chạy: ").strip())
                if times > 0:
                    bot.run_limited(times)
                else:
                    print("❌ Số lần phải lớn hơn 0!")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ!")
                
        elif choice == "3":
            print("\n👋 Tạm biệt!")
            break
            
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
