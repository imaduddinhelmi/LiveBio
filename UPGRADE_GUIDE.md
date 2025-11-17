# 🚀 Panduan Upgrade Aplikasi AutoLiveBio

## 📋 Ringkasan Perubahan

Upgrade ini menambahkan fitur-fitur penting untuk stabilitas dan fungsionalitas aplikasi:

### ✨ Fitur Baru

1. **Stabilitas Jangka Panjang**
   - Error handling yang lebih baik
   - Resource monitoring untuk mencegah memory leaks
   - Auto-recovery dari error
   - Thread management yang lebih robust

2. **Background Mode (System Tray)**
   - Aplikasi bisa berjalan di background
   - System tray icon
   - Minimize to tray functionality
   - Keep schedulers running tanpa window terlihat

3. **Multiple Daily Scheduling**
   - Buat beberapa jadwal harian sekaligus
   - Enable/disable individual schedules
   - Manage schedules dengan UI yang mudah
   - Setiap schedule bisa punya nama dan waktu berbeda

4. **Cancel Scheduled Uploads**
   - Tombol cancel untuk video uploads yang sudah dijadwalkan
   - Bisa cancel multiple uploads sekaligus
   - Select/deselect dengan checkbox

---

## 📦 Langkah 1: Install Dependencies Baru

```bash
pip install pystray>=0.19.4 pynput>=1.7.6
```

Atau update dari requirements.txt yang sudah dimodifikasi:

```bash
pip install -r requirements.txt
```

---

## 🔧 Langkah 2: Implementasi Perubahan

### A. File Baru yang Perlu Ditambahkan

File-file baru berikut sudah dibuat dan siap digunakan:

1. `system_tray_handler.py` ✅
2. `batch_scheduler_v2.py` ✅
3. `error_handler.py` ✅
4. `gui_multiple_scheduler.py` ✅
5. Patch files untuk reference

---

### B. Update gui.py

#### 1. Tambahkan Import di bagian atas

```python
# Tambahkan setelah import yang sudah ada
from system_tray_handler import SystemTrayHandler
from batch_scheduler_v2 import BatchSchedulerV2
from error_handler import ErrorHandler, ResourceMonitor
import atexit
```

#### 2. Update `__init__()` method (sekitar baris 50)

Tambahkan setelah `self.batch_scheduler = ...`:

```python
# Initialize enhanced components
self.batch_scheduler_v2 = BatchSchedulerV2(log_callback=self.log_message)
self.error_handler = ErrorHandler()
self.resource_monitor = ResourceMonitor(log_callback=self.log_message)

# Initialize system tray
self.tray_handler = SystemTrayHandler(f"{config.APP_NAME} v{config.APP_VERSION}")
self.tray_handler.set_callbacks(
    show_window=self.show_from_tray,
    quit_app=self.quit_application
)
self.tray_enabled = False

# Register cleanup
atexit.register(self.cleanup_on_exit)

# Override window close protocol
self.protocol("WM_DELETE_WINDOW", self.on_closing)

# Periodic resource monitoring
self.after(300000, self.periodic_resource_check)  # Every 5 minutes
```

#### 3. Tambahkan Methods Baru

Copy semua methods dari `gui_enhanced.py` ke dalam class App:
- `show_from_tray()`
- `hide_to_tray()`
- `on_closing()`
- `quit_application()`
- `cleanup_on_exit()`
- `periodic_resource_check()`

#### 4. Update `setup_import_tab()` untuk Multiple Scheduler

Ganti bagian scheduler panel (sekitar baris 1100-1200) dengan:

```python
# Right panel: Multiple Scheduler
from gui_multiple_scheduler import MultipleSchedulerPanel

self.multiple_scheduler_panel = MultipleSchedulerPanel(
    right_panel,
    self.batch_scheduler_v2,
    self.scheduled_process_batch_v2,
    self.log_message,
    self.is_dark_mode
)
self.multiple_scheduler_panel.pack(fill="both", expand=True, padx=5, pady=5)
```

#### 5. Tambahkan Method untuk Multiple Scheduler Callback

```python
def scheduled_process_batch_v2(self, excel_path, schedule_name):
    """Process batch from multiple scheduler"""
    self.log_message(f"[SCHEDULER] Running: {schedule_name}")
    
    # Load Excel file
    success, message = self.parser.load_excel(excel_path)
    if not success:
        self.log_message(f"✗ Failed to load Excel: {message}")
        return
    
    # Set Excel path for panel
    if hasattr(self, 'multiple_scheduler_panel'):
        self.multiple_scheduler_panel.set_excel_path(excel_path)
    
    # Run batch process
    self._process_batch_internal()
```

#### 6. Update `select_excel_file()`

Tambahkan di akhir method setelah sukses load Excel:

```python
# Update multiple scheduler panel
if hasattr(self, 'multiple_scheduler_panel'):
    self.multiple_scheduler_panel.set_excel_path(file_path)
```

#### 7. Update `setup_settings_tab()`

Tambahkan sebelum "App Info" section:

```python
# Background Mode Settings
self.add_background_settings(frame)
```

Dan tambahkan methods:
- `add_background_settings()`
- `show_resource_status()`

(Lihat `gui_enhanced.py` untuk implementasi lengkap)

---

### C. Update gui_video_upload.py

#### 1. Tambahkan Import

```python
from datetime import datetime  # Jika belum ada
```

#### 2. Tambahkan Method `cancel_selected_upload()`

Copy method lengkap dari `gui_video_upload_patch.py`.

#### 3. Update `setup_scheduled_list()`

Tambahkan tombol Cancel di btn_row (setelah tombol "Clear"):

```python
# Cancel Selected Button
ctk.CTkButton(btn_row, text="❌ Cancel",
             command=self.cancel_selected_upload, 
             width=90,
             height=32,
             fg_color="#DC143C",
             hover_color="#B22222",
             font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
```

---

### D. Update video_uploader.py

Tambahkan methods baru dari `video_uploader_patch.py`:

1. `cancel_upload(index)`
2. `cancel_multiple_uploads(indices)`
3. `get_upload_statistics()`
4. Update `clear_completed_uploads()`
5. Update `_scheduler_loop()` dengan versi yang lebih robust

---

## 🧪 Langkah 3: Testing

### Test 1: Background Mode

1. Jalankan aplikasi
2. Buka Settings tab
3. Klik "Minimize to Tray Now"
4. Verifikasi aplikasi hilang dari taskbar tapi icon muncul di system tray
5. Klik icon tray → "Show Window" untuk restore
6. Close window dengan scheduler aktif → pilih "Yes" untuk minimize to tray

### Test 2: Multiple Scheduling

1. Load Excel file di Import & Run tab
2. Di panel kanan, tambahkan beberapa schedule:
   - Schedule 1: 09:00
   - Schedule 2: 14:00
   - Schedule 3: 20:00
3. Enable/disable individual schedules
4. Klik "Start All Enabled"
5. Verifikasi status menunjukkan scheduler active
6. Hapus salah satu schedule
7. Verifikasi schedule terhapus dan scheduler restart otomatis

### Test 3: Cancel Video Upload

1. Buka Video Upload tab
2. Schedule beberapa video uploads
3. Klik tombol "❌ Cancel"
4. Pilih upload yang ingin dicancel dengan checkbox
5. Klik "Cancel Selected"
6. Verifikasi uploads ter-cancel dan status berubah

### Test 4: Long Running Stability

1. Jalankan aplikasi dengan multiple schedulers aktif
2. Minimize to tray
3. Biarkan running minimal 2-4 jam
4. Check logs untuk memastikan tidak ada error
5. Restore window dan verify semua masih berfungsi

### Test 5: Resource Monitoring

1. Buka Settings tab
2. Klik "Show Resource Status"
3. Verifikasi jumlah active threads masuk akal (< 20)
4. Tutup aplikasi
5. Buka lagi dan verify cleanup berhasil

---

## ⚠️ Troubleshooting

### Masalah 1: Import Error

**Error**: `ModuleNotFoundError: No module named 'pystray'`

**Solusi**:
```bash
pip install pystray pynput
```

### Masalah 2: System Tray Tidak Muncul

**Penyebab**: Beberapa OS memerlukan konfigurasi khusus untuk system tray

**Solusi**:
- Windows: Pastikan "Show hidden icons" enabled di taskbar settings
- Cek logs untuk error message
- Restart aplikasi

### Masalah 3: Scheduler Tidak Jalan

**Penyebab**: Schedule belum di-enable atau Excel file tidak valid

**Solusi**:
- Pastikan schedule di-enable (hijau)
- Load Excel file yang valid terlebih dahulu
- Check logs untuk error message

### Masalah 4: Memory Leak

**Gejala**: Aplikasi menggunakan RAM semakin banyak seiring waktu

**Solusi**:
- Check "Resource Status" di Settings
- Jika active threads > 20, restart aplikasi
- Report di logs jika masalah persisten

---

## 📊 Struktur File Baru

```
AutoLiveBio/
├── system_tray_handler.py      (NEW - System tray management)
├── batch_scheduler_v2.py        (NEW - Multiple scheduling)
├── error_handler.py             (NEW - Error handling & monitoring)
├── gui_multiple_scheduler.py    (NEW - Multiple scheduler UI)
├── gui_enhanced.py              (REFERENCE - Patches for gui.py)
├── gui_video_upload_patch.py    (REFERENCE - Patches for video upload)
├── video_uploader_patch.py      (REFERENCE - Patches for uploader)
├── UPGRADE_GUIDE.md             (THIS FILE)
├── gui.py                       (MODIFIED)
├── gui_video_upload.py          (MODIFIED)
├── video_uploader.py            (MODIFIED)
└── requirements.txt             (MODIFIED)
```

---

## ✅ Checklist Implementasi

Gunakan checklist ini untuk memastikan semua sudah diimplementasi:

- [ ] Install dependencies baru (pystray, pynput)
- [ ] File baru sudah ada (system_tray_handler.py, dll)
- [ ] Update gui.py:
  - [ ] Import statements
  - [ ] __init__() modifications
  - [ ] New methods (show_from_tray, hide_to_tray, etc)
  - [ ] setup_import_tab() with multiple scheduler
  - [ ] setup_settings_tab() with background settings
- [ ] Update gui_video_upload.py:
  - [ ] cancel_selected_upload() method
  - [ ] Cancel button in UI
- [ ] Update video_uploader.py:
  - [ ] cancel_upload() method
  - [ ] Improved _scheduler_loop()
- [ ] Testing:
  - [ ] Background mode works
  - [ ] Multiple scheduling works
  - [ ] Cancel upload works
  - [ ] Long running stability test
  - [ ] Resource monitoring works

---

## 🎯 Best Practices

### 1. Backup

Selalu backup file original sebelum modifikasi:

```bash
copy gui.py gui.py.backup
copy gui_video_upload.py gui_video_upload.py.backup
copy video_uploader.py video_uploader.py.backup
```

### 2. Gradual Implementation

Implement fitur satu per satu:
1. Error handling & resource monitoring dulu
2. Kemudian system tray
3. Lalu multiple scheduling
4. Terakhir cancel uploads

### 3. Testing Between Changes

Test setiap kali selesai implement satu fitur sebelum lanjut ke fitur berikutnya.

### 4. Log Monitoring

Selalu monitor tab Logs untuk detect error early:
- Error messages akan muncul dengan prefix `[ERROR]`
- Resource warnings dengan prefix `[RESOURCE WARNING]`
- Scheduler activity dengan prefix `[SCHEDULER]`

---

## 🆘 Butuh Bantuan?

Jika mengalami masalah:

1. Check logs di tab "Logs"
2. Check resource status di Settings → "Show Resource Status"
3. Restart aplikasi
4. Jika masih bermasalah, restore dari backup

---

## 📝 Catatan Penting

### Perubahan Breaking

Tidak ada breaking changes - aplikasi tetap backward compatible.
Scheduler lama (`batch_scheduler.py`) tetap ada dan bisa digunakan bersamaan dengan scheduler baru.

### Performa

- Resource monitoring berjalan setiap 5 menit (low overhead)
- Multiple scheduler menggunakan single thread (efficient)
- System tray minimal impact on performance

### Keamanan

- Tidak ada perubahan pada authentication atau credentials
- Tidak ada network changes
- Semua data tetap tersimpan lokal

---

## 🎉 Selesai!

Setelah mengikuti panduan ini, aplikasi Anda akan memiliki:

✅ Stabilitas lebih baik untuk running jangka panjang  
✅ Background mode dengan system tray  
✅ Multiple daily scheduling  
✅ Cancel scheduled uploads  
✅ Better error handling & recovery  
✅ Resource monitoring  

Selamat menggunakan aplikasi yang sudah diupgrade! 🚀
