"""
Enhanced GUI Module - Patch untuk gui.py
Tambahkan import dan modifikasi ini ke gui.py yang ada
"""

# TAMBAHKAN IMPORT INI DI BAGIAN ATAS gui.py (setelah import yang sudah ada):
"""
from system_tray_handler import SystemTrayHandler
from batch_scheduler_v2 import BatchSchedulerV2
from error_handler import ErrorHandler, ResourceMonitor
import atexit
"""

# MODIFIKASI CLASS App.__init__() - Tambahkan setelah self.batch_scheduler:
"""
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
"""

# TAMBAHKAN METHODS BARU INI KE CLASS App:
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
    # Check if there are active operations
    has_active_scheduler = (self.batch_scheduler.is_running or 
                           self.batch_scheduler_v2.is_running or
                           (self.video_upload_tab.video_uploader and 
                            self.video_upload_tab.video_uploader.is_running))
    
    if has_active_scheduler:
        result = messagebox.askyesnocancel(
            "Active Operations",
            "Schedulers are running!\n\n"
            "• Yes: Minimize to system tray (keep running in background)\n"
            "• No: Close and stop all schedulers\n"
            "• Cancel: Do nothing",
            icon='warning'
        )
        
        if result is True:  # Yes - minimize to tray
            self.hide_to_tray()
        elif result is False:  # No - quit
            self.quit_application()
        # None/Cancel - do nothing
    else:
        result = messagebox.askyesno(
            "Close Application",
            "Close application?",
            icon='question'
        )
        if result:
            self.quit_application()

def quit_application(self):
    """Properly quit application with cleanup"""
    try:
        self.log_message("[SHUTDOWN] Closing application...")
        
        # Stop all schedulers
        if self.batch_scheduler.is_running:
            self.batch_scheduler.stop_scheduler()
        
        if self.batch_scheduler_v2.is_running:
            self.batch_scheduler_v2.stop_scheduler()
        
        if self.video_upload_tab.video_uploader:
            self.video_upload_tab.video_uploader.stop_scheduler()
        
        # Stop system tray
        if self.tray_handler.is_running:
            self.tray_handler.stop_tray()
        
        # Force resource cleanup
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
        
        if active_threads > 20:  # Warning threshold
            self.log_message(f"[RESOURCE WARNING] {active_threads} active threads detected")
        
        # Cleanup dead threads
        self.resource_monitor.cleanup_dead_threads()
        
    except Exception as e:
        self.log_message(f"[RESOURCE CHECK ERROR] {e}")
    finally:
        # Schedule next check
        self.after(300000, self.periodic_resource_check)

# TAMBAHKAN KE setup_settings_tab() - Sebelum "App Info" frame:
def add_background_settings(self, frame):
    """Add background mode settings to settings tab"""
    # Background Mode Settings
    bg_frame = ctk.CTkFrame(frame)
    bg_frame.pack(fill="x", padx=20, pady=20)
    
    ctk.CTkLabel(bg_frame, text="🌐 Background Mode:", 
                 font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)
    
    bg_desc = ctk.CTkLabel(bg_frame, 
                          text="Run application in background via system tray when minimizing window",
                          font=ctk.CTkFont(size=12),
                          text_color="gray")
    bg_desc.pack(anchor="w", padx=10, pady=(0,10))
    
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
    
    # Resource Monitor Info
    ctk.CTkButton(
        bg_buttons,
        text="📊 Show Resource Status",
        command=self.show_resource_status,
        width=180,
        height=40,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(side="left", padx=5)

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
