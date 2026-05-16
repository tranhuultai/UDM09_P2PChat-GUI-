# UDM_09 · P2P Chat GUI

> Ứng dụng chat ngang hàng (Peer-to-Peer) không cần server trung tâm.
> Project được phát triển cho môn Lập trình Mạng bằng Python.

**Lớp:** 012012301310
**Nhóm:** Net2_Group_04
**Python:** 3.10+

---

## Tổng quan

P2P Chat GUI là project xây dựng ứng dụng chat Peer-to-Peer có giao diện GUI chạy trên Windows.

Ứng dụng cho phép các peer kết nối trực tiếp với nhau thông qua TCP Socket mà không cần server trung tâm.

Project tập trung vào:

* TCP Socket Programming
* Peer-to-Peer Communication
* Multi-threading
* GUI Desktop Application
* Message Encryption

---

## Chức năng dự kiến

* Kết nối trực tiếp giữa các peer
* Chat realtime
* Broadcast message
* Mã hóa tin nhắn bằng Fernet
* Multi-thread networking
* Theo dõi trạng thái kết nối
* Validate IP và port đầu vào
* Logging lịch sử chat
* Stress test và performance test

---

## ⚙️ Kiến trúc dự kiến

### Giao thức truyền dữ liệu

```text id="jlwm72"
┌─────────────┬──────────────────────────────┐
│  4 bytes    │  N bytes                     │
│  (length)   │  (encrypted payload)         │
└─────────────┴──────────────────────────────┘
```

---

### Mô hình threading

```text id="jlwm73"
main thread (GUI)
    │
    ├── server-listener thread
    ├── connect thread
    └── receive thread × N
```

---

## Cấu trúc project

```text id="jlwm74"
Code/P2PChat/
└── src/
    ├── main.py
    ├── protocol.py
    ├── gui/
    └── node/
```

---

## Khởi tạo project

```bash id="jlwm75"
git clone https://github.com/tranhuultai/UDM09_P2PChat-GUI-.git
```

---

## Kế hoạch Sprint

### Sprint 1 (Tuần 1–2)

* Setup GitHub repository
* Thiết kế cấu trúc project
* Thiết kế GUI cơ bản
* Nghiên cứu mô hình P2P
* Thiết kế giao thức truyền dữ liệu
* Chuẩn bị môi trường phát triển

---

### Sprint 2 (Tuần 3–4)

Dự kiến:

* TCP connection
* Realtime messaging
* Multi-thread networking
* Broadcast messaging

---

### Sprint 3 (Tuần 5–6)

Dự kiến:

* Fernet encryption
* Logging lịch sử chat
* Quản lý peer
* GUI improvements

---

### Sprint 4 (Tuần 7–8)

Dự kiến:

* Stress test
* Performance test
* Documentation
* Demo video
* Final bug fixing

---

## Requirements

* Python 3.10+
* cryptography
* customtkinter

---

## Thành viên nhóm

| MSSV         | Họ tên               |
| ------------ | -------------------- |
| 089205009200 | Trần Hữu Tài         |
| 052206013184 | Nguyễn Văn Tài       |
| 080306012851 | Trần Thị Thanh Thơ   |
| 052206003938 | Nguyễn Phan Hoài Bin |
| 082206002652 | Lê Quốc Thịnh        |
| 064206008244 | Nguyễn Xuân Thủy     |

---

## Ghi chú

Project hiện đang trong giai đoạn khởi tạo và thiết kế hệ thống.
Các chức năng sẽ được triển khai theo từng sprint.
