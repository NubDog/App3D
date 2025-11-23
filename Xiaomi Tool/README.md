# Xiaomi Bot - Automation Tool

## Cài đặt

1. Cài đặt Python 3.7 trở lên
2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Cách sử dụng

1. Chạy chương trình:

```bash
python Main.py
```

2. Chọn chế độ:
   - **Chế độ 1**: Chạy liên tục TURBO (nhanh nhất ⚡)
   - **Chế độ 2**: Chạy theo số lần TURBO
   - **Chế độ 3**: Chạy liên tục NORMAL (an toàn hơn)
   - **Chế độ 4**: Chạy theo số lần NORMAL
   - **Chế độ 5**: Thoát chương trình

## ⚡ TURBO Mode vs NORMAL Mode

| Tính năng | TURBO Mode | NORMAL Mode |
|-----------|------------|-------------|
| Click delay | 10-30ms | 50-300ms |
| Typing interval | 10ms/ký tự | 50ms/ký tự |
| Backspace delay | 5ms | 50ms |
| Wait after action | 50-300ms | 200-1200ms |
| Tốc độ | **5-10x nhanh hơn** | Ổn định |
| Khuyến nghị | Máy tốt, giao diện ổn định | Máy yếu hoặc test |

## Quy trình hoạt động

### Lần chạy đầu tiên:
1. Bot tìm hình ảnh "864" trên màn hình (lưu vị trí)
2. Click vào vị trí cách hình ảnh 400px sang bên phải (lưu vị trí)
3. Xóa 6 số cũ (nhấn backspace 6 lần)
4. Nhập 6 số ngẫu nhiên mới → Tạo số 9 chữ số (864 + 6 số)
5. Click vào nút "Tiếp theo" (lưu vị trí)
6. Kiểm tra có hình "Params invalid" không:
   - **Nếu có**: Đánh dấu fail, click OK (lưu vị trí), lưu log
   - **Nếu không**: Bot dừng lại
7. Sau khi click OK, quay lại bước 1

### Từ lần 2 trở đi (Tối ưu tốc độ):
1. **Dùng vị trí đã lưu** từ `location.txt` → Không cần quét tìm hình nữa
2. Click vào ô nhập (dùng vị trí đã lưu)
3. Xóa **9 số cũ** (backspace 9 lần)
4. Nhập **9 số ngẫu nhiên mới** hoàn toàn
5. Click "Tiếp theo" (dùng vị trí đã lưu)
6. Kiểm tra "Params invalid"
7. Click OK (dùng vị trí đã lưu), lưu log
8. Lặp lại

## Log Format

Mỗi dòng trong `log.txt` có định dạng:
```
[9 chữ số] [thời gian] [trạng thái]
```

Ví dụ:
```
864123456 2025-01-04 12:30:45 fail
864789012 2025-01-04 12:31:50 fail
```

## Location.txt - Tự động nhớ vị trí

File `location.txt` lưu trữ tọa độ các nút đã tìm được ở lần đầu tiên:

```json
{
  "pos_864": [x, y],
  "click_input": [x, y],
  "pos_next": [x, y],
  "pos_ok": [x, y]
}
```

**Lợi ích:**
- **Tăng tốc độ**: Từ lần 2, bot không cần quét tìm hình nữa → Nhanh hơn 5-10 lần
- **Giảm tải CPU**: Không cần chạy thuật toán nhận diện hình ảnh liên tục
- **Ổn định hơn**: Vị trí cố định, không bị sai lệch

**Lưu ý**: Nếu giao diện thay đổi vị trí, xóa file `location.txt` để bot tìm lại.

## 🚀 Các tối ưu hóa tốc độ

1. **Cache vị trí nút** - Không cần quét hình từ lần 2
2. **Cache số đã dùng** - Chỉ đọc file log 1 lần
3. **Giảm delay tối đa** - Click 10ms, typing 10ms/ký tự
4. **Loại bỏ print không cần thiết** - Chỉ hiển thị thông tin quan trọng
5. **In-line progress** - Dùng `\r` thay vì nhiều dòng
6. **Thống kê thời gian** - Hiển thị tốc độ trung bình

**Ước tính thời gian mỗi vòng:**
- Lần 1 (tìm hình): ~3-5 giây
- Lần 2+ TURBO: ~1-2 giây ⚡
- Lần 2+ NORMAL: ~3-4 giây

## Lưu ý khác

- Bot sẽ tự động kiểm tra và không nhập số trùng với log.txt
- Độ tin cậy nhận diện hình ảnh mặc định là 0.8
- Xóa `location.txt` nếu vị trí các nút trên giao diện thay đổi
- TURBO mode khuyến nghị cho máy có cấu hình tốt
- Nếu gặp lỗi với TURBO, chuyển sang NORMAL mode
