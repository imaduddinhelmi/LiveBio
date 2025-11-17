# ⚡ Quick Start Implementation Guide

## 🎯 Implementasi Cepat (30 Menit)

Ikuti langkah-langkah ini untuk implementasi tercepat.

---

## 📦 Step 1: Install Dependencies (2 menit)

```bash
pip install pystray>=0.19.4 pynput>=1.7.6
```

---

## 🔧 Step 2: Implementasi Code Changes

### A. gui.py - Tambahkan Import (Baris ~15)

```python
from system_tray_handler import SystemTrayHandler
from batch_scheduler_v2 import BatchSchedulerV2
from error_handler import ErrorHandler, ResourceMonitor
from gui_multiple_scheduler import MultipleSchedulerPanel
import atexit
```

### B. gui.py - Update __init__() (Baris ~50, setelah self.batch_scheduler)

```python
# Enhanced components
self.batch_scheduler_v2 = BatchSchedulerV2(log_callback=self.log_message)
self.error_handler = ErrorHandler()
self.resource_monitor = ResourceMonitor(log_callback=self.log_message)

# System tray
self.tray_handler = SystemTrayHandler(f"{config.APP_NAME} v{config.APP_VERSION}")
self.tray_handler.set_callbacks(
    show_window=self.show_from_tray,
    quit_app=self.quit_application
)
self.tray_enabled = False

# Cleanup
atexit.register(self.cleanup_on_exit)
self.protocol("WM_DELETE_WINDOW", self.on_closing)
self.after(300000, self.periodic_resource_check)
```

### C. gui.py - Tambahkan Methods (Sebelum if __name__ == "__main__":)

Copy-paste methods berikut:

```python
def show_from_tray(self):
    """Show window from system tray"""
    self.deiconify()
    self.lift()
    self.focus_force()

def hide_to_tray(self):
    """Minimize to system tray"""
    if not self.tray_enabled:
        if self.tray_handler.start_tray():
            self.tray_enabled = True
            self.withdraw()
            self.log_message("[TRAY] Application minimized to system tray")
        else:
            messagebox.showerror("Error", "Failed to create system tray icon")
    else:
        self.withdraw()

def on_closing(self):
    """Handle window close event"""
    has_active_scheduler = (self.batch_scheduler.is_running or 
                           self.batch_scheduler_v2.is_running or
                           (self.video_upload_tab.video_uploader and 
                            self.video_upload_tab.video_uploader.is_running))
    
    if has_active_scheduler:
        result = messagebox.askyesnocancel(
            "Active Operations",
            "Schedulers are running!\n\n"
            "• Yes: Minimize to system tray (keep running)\n"
            "• No: Close and stop all schedulers\n"
            "• Cancel: Do nothing",
            icon='warning'
        )
        
        if result is True:
            self.hide_to_tray()
        elif result is False:
            self.quit_application()
    else:
        result = messagebox.askyesno("Close Application", "Close application?")
        if result:
            self.quit_application()

def quit_application(self):
    """Properly quit application with cleanup"""
    try:
        self.log_message("[SHUTDOWN] Closing application...")
        
        if self.batch_scheduler.is_running:
            self.batch_scheduler.stop_scheduler()
        if self.batch_scheduler_v2.is_running:
            self.batch_scheduler_v2.stop_scheduler()
        if self.video_upload_tab.video_uploader:
            self.video_upload_tab.video_uploader.stop_scheduler()
        if self.tray_handler.is_running:
            self.tray_handler.stop_tray()
        
        self.resource_monitor.force_cleanup()
        self.log_message("[SHUTDOWN] Cleanup complete")
    except Exception as e:
        self.log_message(f"[SHUTDOWN ERROR] {e}")
    finally:
        self.destroy()
        self.quit()

def cleanup_on_exit(self):
    """Cleanup function called on exit"""
    try:
        if hasattr(self, 'resource_monitor'):
            self.resource_monitor.force_cleanup()
    except:
        pass

def periodic_resource_check(self):
    """Periodically check and cleanup resources"""
    try:
        status = self.resource_monitor.get_status()
        active_threads = status['active_threads']
        
        if active_threads > 20:
            self.log_message(f"[RESOURCE WARNING] {active_threads} active threads")
        
        self.resource_monitor.cleanup_dead_threads()
    except Exception as e:
        self.log_message(f"[RESOURCE CHECK ERROR] {e}")
    finally:
        self.after(300000, self.periodic_resource_check)

def scheduled_process_batch_v2(self, excel_path, schedule_name):
    """Process batch from multiple scheduler"""
    self.log_message(f"[SCHEDULER] Running: {schedule_name}")
    
    success, message = self.parser.load_excel(excel_path)
    if not success:
        self.log_message(f"✗ Failed to load Excel: {message}")
        return
    
    if hasattr(self, 'multiple_scheduler_panel'):
        self.multiple_scheduler_panel.set_excel_path(excel_path)
    
    self._process_batch_internal()

def show_resource_status(self):
    """Show resource monitoring status"""
    try:
        status = self.resource_monitor.get_status()
        
        message = f"Active Threads: {status['active_threads']}\n"
        message += f"Cleanup Callbacks: {status['cleanup_callbacks']}\n\n"
        message += "Thread Details:\n"
        
        for thread_info in status['threads']:
            message += f"  • {thread_info['name']}: "
            message += f"{'Alive' if thread_info['alive'] else 'Dead'} "
            message += f"({thread_info['age_seconds']:.1f}s)\n"
        
        messagebox.showinfo("Resource Status", message)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get resource status:\n{e}")
```

### D. gui.py - Update setup_import_tab() 

Cari bagian "Right panel (scheduler)" di setup_import_tab() (sekitar baris 1100-1200), GANTI dengan:

```python
# Right panel (scheduler)
right_panel = ctk.CTkFrame(main_container, width=380)
right_panel.pack(side="right", fill="y", padx=(5, 0))
right_panel.pack_propagate(False)

# Multiple Scheduler Panel
self.multiple_scheduler_panel = MultipleSchedulerPanel(
    right_panel,
    self.batch_scheduler_v2,
    self.scheduled_process_batch_v2,
    self.log_message,
    self.is_dark_mode
)
self.multiple_scheduler_panel.pack(fill="both", expand=True, padx=5, pady=5)
```

### E. gui.py - Update select_excel_file()

Tambahkan di AKHIR method select_excel_file() (setelah self.log_message...):

```python
# Update multiple scheduler panel
if hasattr(self, 'multiple_scheduler_panel'):
    self.multiple_scheduler_panel.set_excel_path(file_path)
```

### F. gui.py - Update setup_settings_tab()

Tambahkan SEBELUM "# App Info" section:

```python
# Background Mode Settings
bg_frame = ctk.CTkFrame(frame)
bg_frame.pack(fill="x", padx=20, pady=20)

ctk.CTkLabel(bg_frame, text="🌐 Background Mode:", 
             font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)

ctk.CTkLabel(bg_frame, 
            text="Run application in background via system tray",
            font=ctk.CTkFont(size=12),
            text_color="gray").pack(anchor="w", padx=10, pady=(0,10))

bg_buttons = ctk.CTkFrame(bg_frame)
bg_buttons.pack(fill="x", padx=10, pady=10)

ctk.CTkButton(
    bg_buttons,
    text="🔽 Minimize to Tray Now",
    command=self.hide_to_tray,
    width=180,
    height=40,
    font=ctk.CTkFont(size=13, weight="bold")
).pack(side="left", padx=5)

self.lbl_tray_status = ctk.CTkLabel(
    bg_buttons,
    text=f"Tray: {'Active' if self.tray_enabled else 'Not Started'}",
    font=ctk.CTkFont(size=12, weight="bold")
)
self.lbl_tray_status.pack(side="left", padx=20)

ctk.CTkButton(
    bg_buttons,
    text="📊 Show Resource Status",
    command=self.show_resource_status,
    width=180,
    height=40,
    font=ctk.CTkFont(size=13, weight="bold")
).pack(side="left", padx=5)
```

---

### G. gui_video_upload.py - Tambahkan Import (Baris ~5)

Pastikan datetime sudah di-import:

```python
from datetime import datetime, timedelta
```

### H. gui_video_upload.py - Tambahkan Method

Tambahkan method ini di class VideoUploadTab (setelah clear_completed):

```python
def cancel_selected_upload(self):
    """Cancel selected scheduled uploads"""
    if not self.video_uploader:
        messagebox.showwarning("Warning", "Video uploader not initialized")
        return
    
    scheduled = self.video_uploader.get_scheduled_uploads()
    pending = [s for s in scheduled if s["status"] == "pending"]
    
    if not pending:
        messagebox.showinfo("No Pending Uploads", "No pending uploads to cancel.")
        return
    
    # Create selection window
    select_window = ctk.CTkToplevel(self.app)
    select_window.title("Cancel Scheduled Upload")
    select_window.geometry("600x500")
    select_window.grab_set()
    
    ctk.CTkLabel(select_window, text="Select Upload(s) to Cancel", 
                font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    
    # Scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(select_window, height=300)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    checkbox_vars = []
    
    for idx, item in enumerate(pending):
        video_data = item["video_data"]
        scheduled_time = datetime.fromisoformat(item["scheduled_time"])
        
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(fill="x", pady=5, padx=5)
        
        var = ctk.BooleanVar(value=False)
        checkbox_vars.append((var, idx))
        
        checkbox = ctk.CTkCheckBox(frame, text="", variable=var, width=30)
        checkbox.pack(side="left", padx=5)
        
        info_text = f"{idx+1}. {video_data['title']}\n"
        info_text += f"   Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        label = ctk.CTkLabel(frame, text=info_text, justify="left",
                           font=ctk.CTkFont(size=11))
        label.pack(side="left", padx=5, fill="x", expand=True)
    
    # Buttons
    btn_frame = ctk.CTkFrame(select_window)
    btn_frame.pack(fill="x", padx=10, pady=10)
    
    def select_all():
        for var, _ in checkbox_vars:
            var.set(True)
    
    def deselect_all():
        for var, _ in checkbox_vars:
            var.set(False)
    
    def cancel_selected():
        selected_indices = [idx for var, idx in checkbox_vars if var.get()]
        
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one upload")
            return
        
        result = messagebox.askyesno(
            "Confirm Cancellation",
            f"Cancel {len(selected_indices)} selected upload(s)?",
            parent=select_window
        )
        
        if not result:
            return
        
        cancelled_count = 0
        for idx in sorted(selected_indices, reverse=True):
            if self.video_uploader.cancel_upload(idx):
                cancelled_count += 1
        
        self.app.log_message(f"[CANCEL] Cancelled {cancelled_count} upload(s)")
        self.refresh_scheduled_list()
        select_window.destroy()
        messagebox.showinfo("Success", f"Cancelled {cancelled_count} upload(s)")
    
    ctk.CTkButton(btn_frame, text="✓ Select All", 
                 command=select_all, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="✗ Deselect All", 
                 command=deselect_all, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Cancel", 
                 command=select_window.destroy, width=100).pack(side="right", padx=5)
    ctk.CTkButton(btn_frame, text="🗑 Cancel Selected", 
                 command=cancel_selected, width=140,
                 fg_color="#DC143C", hover_color="#B22222").pack(side="right", padx=5)
```

### I. gui_video_upload.py - Update setup_scheduled_list()

Cari bagian btn_row (yang ada tombol Refresh, Clear), tambahkan SETELAH tombol Clear:

```python
# Cancel Button
ctk.CTkButton(btn_row, text="❌ Cancel",
             command=self.cancel_selected_upload, 
             width=90,
             height=32,
             fg_color="#DC143C",
             hover_color="#B22222",
             font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
```

---

### J. video_uploader.py - Tambahkan Methods

Tambahkan methods berikut di class VideoUploader (setelah clear_completed_uploads):

```python
def cancel_upload(self, index: int) -> bool:
    """Cancel a scheduled upload"""
    try:
        if 0 <= index < len(self.scheduled_uploads):
            upload_item = self.scheduled_uploads[index]
            
            if upload_item['status'] == 'pending':
                upload_item['status'] = 'cancelled'
                upload_item['cancelled_at'] = datetime.now().isoformat()
                self.save_scheduled_uploads()
                return True
        return False
    except Exception as e:
        print(f"Error cancelling upload: {e}")
        return False

def get_upload_statistics(self) -> dict:
    """Get upload statistics"""
    stats = {
        'total': len(self.scheduled_uploads),
        'pending': 0,
        'processing': 0,
        'completed': 0,
        'failed': 0,
        'cancelled': 0
    }
    
    for upload in self.scheduled_uploads:
        status = upload.get('status', 'unknown')
        if status in stats:
            stats[status] += 1
    
    return stats
```

### K. video_uploader.py - Update clear_completed_uploads()

GANTI method clear_completed_uploads() dengan:

```python
def clear_completed_uploads(self):
    """Remove completed, failed, and cancelled uploads"""
    try:
        self.scheduled_uploads = [
            item for item in self.scheduled_uploads 
            if item['status'] not in ['completed', 'failed', 'cancelled']
        ]
        self.save_scheduled_uploads()
        return True
    except Exception as e:
        print(f"Error clearing uploads: {e}")
        return False
```

---

## ✅ Step 3: Test (5 menit)

### Quick Test Checklist

1. **Run Application**
   ```bash
   python main.py
   ```

2. **Test Background Mode**
   - Go to Settings → Click "Minimize to Tray Now"
   - Check system tray for icon
   - Click icon → Show Window

3. **Test Multiple Scheduler**
   - Import & Run tab → Load Excel
   - Right panel → Add 2-3 schedules
   - Click "Start All Enabled"
   - Check status

4. **Test Cancel Upload**
   - Video Upload tab → Schedule 2-3 videos
   - Click "❌ Cancel" button
   - Select and cancel

5. **Check Logs**
   - Logs tab should show all activities
   - No error messages

---

## 🎉 Done!

Jika semua test berhasil, aplikasi sudah siap digunakan dengan fitur baru:
- ✅ Background mode
- ✅ Multiple scheduling
- ✅ Cancel uploads
- ✅ Better stability

---

## 🆘 Quick Troubleshooting

**Error: Module not found**
```bash
pip install --upgrade -r requirements.txt
```

**System tray tidak muncul**
- Check Windows taskbar settings → Show hidden icons
- Restart aplikasi

**Scheduler tidak jalan**
- Pastikan schedule enabled (hijau)
- Load Excel file dulu
- Check logs untuk error

---

## 📞 Need Help?

Jika ada masalah:
1. Check logs
2. Backup dan restore jika perlu
3. Restart aplikasi

Selamat! 🚀
