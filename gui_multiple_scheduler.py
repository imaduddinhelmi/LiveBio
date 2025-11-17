"""
Multiple Scheduler GUI Component
Menggantikan scheduler tunggal dengan multiple scheduler
"""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime
from color_utils import (
    get_adaptive_gray_color,
    get_adaptive_success_color,
    get_adaptive_error_color,
    get_adaptive_warning_color
)

class MultipleSchedulerPanel(ctk.CTkFrame):
    """Panel untuk mengelola multiple scheduled batches"""
    
    def __init__(self, parent, scheduler_v2, process_callback, log_callback, is_dark_mode):
        super().__init__(parent, fg_color=("#E3F2FD", "#1A237E"), corner_radius=10)
        
        self.scheduler = scheduler_v2
        self.process_callback = process_callback
        self.log_callback = log_callback
        self.is_dark_mode = is_dark_mode
        
        self.setup_ui()
        self.refresh_schedule_list()
    
    def setup_ui(self):
        """Setup UI components"""
        
        # Header
        ctk.CTkLabel(self, text="⏰ Multiple Daily\nScheduling", 
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(10,5))
        
        ctk.CTkLabel(self, text="Manage multiple daily batch schedules",
                    font=ctk.CTkFont(size=10), wraplength=340).pack(pady=(0,10))
        
        # Add New Schedule Section
        add_frame = ctk.CTkFrame(self, fg_color="transparent")
        add_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(add_frame, text="➕ Add New Schedule:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", pady=(5,2))
        
        input_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(input_frame, text="Time:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0,3))
        self.new_schedule_time = ctk.CTkEntry(input_frame, width=70, placeholder_text="09:00")
        self.new_schedule_time.pack(side="left", padx=2)
        self.new_schedule_time.insert(0, "09:00")
        
        ctk.CTkLabel(input_frame, text="Name:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(5,3))
        self.new_schedule_name = ctk.CTkEntry(input_frame, width=100, placeholder_text="Schedule 1")
        self.new_schedule_name.pack(side="left", padx=2)
        
        ctk.CTkButton(
            add_frame,
            text="➕ Add Schedule",
            command=self.add_new_schedule,
            height=28,
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(fill="x", pady=3)
        
        # Separator
        separator1 = ctk.CTkFrame(self, height=2, fg_color=get_adaptive_gray_color(self.is_dark_mode))
        separator1.pack(fill="x", padx=20, pady=10)
        
        # Schedule List
        ctk.CTkLabel(self, text="📋 Scheduled Batches:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=10, pady=(0,5))
        
        # Scrollable frame for schedules
        self.schedules_frame = ctk.CTkScrollableFrame(self, height=200)
        self.schedules_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Control Buttons
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_start_all = ctk.CTkButton(
            control_frame,
            text="▶ Start All Enabled",
            command=self.start_scheduler,
            height=35,
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.btn_start_all.pack(fill="x", pady=2)
        
        self.btn_stop_all = ctk.CTkButton(
            control_frame,
            text="⏹ Stop Scheduler",
            command=self.stop_scheduler,
            height=30,
            fg_color="#DC143C",
            hover_color="#B22222",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        self.btn_stop_all.pack(fill="x", pady=2)
        
        ctk.CTkButton(
            control_frame,
            text="🔄 Refresh List",
            command=self.refresh_schedule_list,
            height=30,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(fill="x", pady=2)
        
        # Status Display
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.lbl_scheduler_status = ctk.CTkLabel(
            status_frame,
            text="⚪ Scheduler: Stopped",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=get_adaptive_gray_color(self.is_dark_mode),
            wraplength=340
        )
        self.lbl_scheduler_status.pack(pady=2)
        
        self.lbl_schedule_count = ctk.CTkLabel(
            status_frame,
            text="0 schedule(s)",
            font=ctk.CTkFont(size=9),
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        )
        self.lbl_schedule_count.pack(pady=2)
        
        # Update status periodically
        self.after(5000, self.update_status_display)
    
    def add_new_schedule(self):
        """Add a new schedule"""
        time_str = self.new_schedule_time.get().strip()
        name = self.new_schedule_name.get().strip()
        
        if not time_str:
            messagebox.showerror("Error", "Please enter a time (HH:MM)")
            return
        
        if not name:
            name = f"Schedule {len(self.scheduler.get_all_schedules()) + 1}"
        
        # Get current Excel file path
        excel_path = getattr(self, 'excel_path', None)
        if not excel_path:
            messagebox.showerror("Error", "No Excel file loaded. Please load an Excel file first.")
            return
        
        schedule_id = self.scheduler.add_schedule(time_str, excel_path, name, enabled=True)
        
        if schedule_id:
            self.log_callback(f"[SCHEDULER] Added: {name} at {time_str}")
            self.refresh_schedule_list()
            
            # Clear inputs
            self.new_schedule_time.delete(0, "end")
            self.new_schedule_time.insert(0, "09:00")
            self.new_schedule_name.delete(0, "end")
            
            messagebox.showinfo("Success", f"Schedule added: {name} at {time_str}")
        else:
            messagebox.showerror("Error", "Failed to add schedule. Check time format (HH:MM)")
    
    def refresh_schedule_list(self):
        """Refresh the list of schedules"""
        # Clear current list
        for widget in self.schedules_frame.winfo_children():
            widget.destroy()
        
        schedules = self.scheduler.get_all_schedules()
        
        if not schedules:
            ctk.CTkLabel(
                self.schedules_frame,
                text="No schedules yet.\nAdd your first schedule above.",
                font=ctk.CTkFont(size=10),
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            ).pack(pady=20)
            
            self.lbl_schedule_count.configure(text="0 schedule(s)")
            return
        
        # Get next run times
        next_runs = self.scheduler.get_next_run_times()
        
        # Display each schedule
        for sched in schedules:
            self.create_schedule_item(sched, next_runs.get(sched['id']))
        
        # Update count
        enabled_count = len([s for s in schedules if s.get('enabled', False)])
        self.lbl_schedule_count.configure(
            text=f"{len(schedules)} schedule(s) • {enabled_count} enabled"
        )
    
    def create_schedule_item(self, schedule, next_run=None):
        """Create UI for a single schedule item"""
        frame = ctk.CTkFrame(self.schedules_frame, fg_color=("#F0F0F0", "#2C2C2C"))
        frame.pack(fill="x", pady=3, padx=2)
        
        # Top row: Name and time
        top_row = ctk.CTkFrame(frame, fg_color="transparent")
        top_row.pack(fill="x", padx=5, pady=3)
        
        # Status indicator
        status_emoji = "🟢" if schedule.get('enabled', False) else "⚫"
        
        ctk.CTkLabel(
            top_row,
            text=f"{status_emoji} {schedule['name']}",
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            top_row,
            text=f"⏰ {schedule['time']}",
            font=ctk.CTkFont(size=10),
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        ).pack(side="right")
        
        # Bottom row: Info and buttons
        bottom_row = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_row.pack(fill="x", padx=5, pady=3)
        
        # Info
        info_text = ""
        if next_run:
            info_text = f"Next: {next_run}"
        elif schedule.get('last_run'):
            last_run_dt = datetime.fromisoformat(schedule['last_run'])
            info_text = f"Last: {last_run_dt.strftime('%Y-%m-%d %H:%M')}"
        else:
            info_text = "Never run"
        
        ctk.CTkLabel(
            bottom_row,
            text=info_text,
            font=ctk.CTkFont(size=9),
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        ).pack(side="left")
        
        # Buttons
        btn_frame = ctk.CTkFrame(bottom_row, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Toggle enable/disable
        toggle_text = "Disable" if schedule.get('enabled', False) else "Enable"
        toggle_color = "#FFA500" if schedule.get('enabled', False) else "#2E7D32"
        
        ctk.CTkButton(
            btn_frame,
            text=toggle_text,
            command=lambda s=schedule: self.toggle_schedule(s['id']),
            width=60,
            height=24,
            fg_color=toggle_color,
            font=ctk.CTkFont(size=9)
        ).pack(side="left", padx=2)
        
        # Delete button
        ctk.CTkButton(
            btn_frame,
            text="🗑",
            command=lambda s=schedule: self.delete_schedule(s['id'], s['name']),
            width=35,
            height=24,
            fg_color="#DC143C",
            hover_color="#B22222",
            font=ctk.CTkFont(size=9)
        ).pack(side="left", padx=2)
    
    def toggle_schedule(self, schedule_id):
        """Toggle enable/disable for a schedule"""
        schedule = self.scheduler.get_schedule(schedule_id)
        if schedule:
            new_enabled = not schedule.get('enabled', False)
            self.scheduler.update_schedule(schedule_id, enabled=new_enabled)
            
            action = "enabled" if new_enabled else "disabled"
            self.log_callback(f"[SCHEDULER] {schedule['name']}: {action}")
            
            self.refresh_schedule_list()
            
            # Restart scheduler if running
            if self.scheduler.is_running:
                self.scheduler.restart_scheduler(self.process_callback)
    
    def delete_schedule(self, schedule_id, name):
        """Delete a schedule"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Delete schedule: {name}?",
            icon='warning'
        )
        
        if result:
            if self.scheduler.remove_schedule(schedule_id):
                self.log_callback(f"[SCHEDULER] Deleted: {name}")
                self.refresh_schedule_list()
                
                # Restart scheduler if running
                if self.scheduler.is_running:
                    self.scheduler.restart_scheduler(self.process_callback)
                
                messagebox.showinfo("Success", f"Schedule deleted: {name}")
    
    def start_scheduler(self):
        """Start the scheduler"""
        enabled = self.scheduler.get_enabled_schedules()
        
        if not enabled:
            messagebox.showerror("Error", "No enabled schedules. Please enable at least one schedule.")
            return
        
        if self.scheduler.start_scheduler(self.process_callback):
            self.update_status_display()
            messagebox.showinfo("Scheduler Started", 
                              f"Scheduler started with {len(enabled)} schedule(s).\n\n"
                              "Keep application running for automatic execution.")
        else:
            messagebox.showerror("Error", "Failed to start scheduler")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if self.scheduler.stop_scheduler():
            self.update_status_display()
            messagebox.showinfo("Scheduler Stopped", "All schedules have been stopped.")
    
    def update_status_display(self):
        """Update status display"""
        status = self.scheduler.get_status()
        
        if status['running']:
            self.lbl_scheduler_status.configure(
                text=f"🟢 Scheduler: Active ({status['enabled_schedules']} schedule(s))",
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            self.btn_start_all.configure(state="disabled")
            self.btn_stop_all.configure(state="normal")
        else:
            self.lbl_scheduler_status.configure(
                text="⚪ Scheduler: Stopped",
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            )
            self.btn_start_all.configure(state="normal")
            self.btn_stop_all.configure(state="disabled")
        
        # Schedule next update if running
        if status['running']:
            self.after(5000, self.update_status_display)
    
    def set_excel_path(self, path):
        """Set the Excel file path for new schedules"""
        self.excel_path = path
    
    def update_theme(self, is_dark_mode):
        """Update colors when theme changes"""
        self.is_dark_mode = is_dark_mode
        self.refresh_schedule_list()
        self.update_status_display()


# CARA MENGINTEGRASIKAN KE gui.py:
"""
1. Di setup_import_tab(), gantikan scheduler panel lama dengan:

    # Right panel: Multiple Scheduler
    from gui_multiple_scheduler import MultipleSchedulerPanel
    
    self.multiple_scheduler_panel = MultipleSchedulerPanel(
        right_panel,
        self.batch_scheduler_v2,
        self.scheduled_process_batch_v2,  # New callback
        self.log_message,
        self.is_dark_mode
    )
    self.multiple_scheduler_panel.pack(fill="both", expand=True, padx=5, pady=5)

2. Tambahkan method baru untuk process callback:

def scheduled_process_batch_v2(self, excel_path, schedule_name):
    '''Process batch dari multiple scheduler'''
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

3. Di select_excel_file(), tambahkan:
    
    if hasattr(self, 'multiple_scheduler_panel'):
        self.multiple_scheduler_panel.set_excel_path(file_path)
"""
