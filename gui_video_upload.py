import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from datetime import datetime, timedelta
from video_uploader import VideoUploader
from video_excel_parser import VideoExcelParser
from color_utils import (
    get_adaptive_gray_color,
    get_adaptive_success_color,
    get_adaptive_error_color,
    get_adaptive_warning_color
)

class VideoUploadTab:
    def __init__(self, parent_app, tab_frame):
        self.app = parent_app
        self.tab = tab_frame
        self.video_uploader = None
        self.video_parser = VideoExcelParser()
        self.selected_video_path = None
        self.selected_thumbnail_path = None
        self.is_dark_mode = ctk.get_appearance_mode() == "Dark"
        self.setup_tab()
    
    def initialize_uploader(self, youtube_service):
        """Initialize video uploader with YouTube service"""
        self.video_uploader = VideoUploader(youtube_service)
    
    def setup_tab(self):
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(self.tab)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_single = self.notebook.add("Single Upload")
        self.tab_batch = self.notebook.add("Batch Upload")
        
        self.setup_single_upload_tab()
        self.setup_batch_upload_tab()
    
    def setup_single_upload_tab(self):
        frame = ctk.CTkFrame(self.tab_single)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="🎬 Video Upload Manager", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Main container with two columns
        main_container = ctk.CTkFrame(frame)
        main_container.pack(fill="both", expand=True, pady=10)
        
        # Left side - Upload form
        left_frame = ctk.CTkFrame(main_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.setup_upload_form(left_frame)
        
        # Right side - Scheduled uploads list
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.setup_scheduled_list(right_frame)
    
    def setup_upload_form(self, parent):
        # Header
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header_frame, text="📤 Upload Video", 
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", padx=10)
        
        # Video file selection (Fixed at top)
        video_frame = ctk.CTkFrame(parent, fg_color=("#AED6F1", "#5DADE2"), corner_radius=10)
        video_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(video_frame, text="1️⃣ SELECT VIDEO FILE:", 
                    font=ctk.CTkFont(weight="bold", size=13)).pack(anchor="w", padx=10, pady=(10,5))
        
        btn_frame = ctk.CTkFrame(video_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0,10))
        
        ctk.CTkButton(btn_frame, text="📁 Select Video File", 
                     command=self.select_video, 
                     width=150,
                     height=35,
                     font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        self.lbl_video = ctk.CTkLabel(btn_frame, text="No video selected", 
                                     text_color=get_adaptive_warning_color(self.is_dark_mode),
                                     font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_video.pack(side="left", padx=10)
        
        # Separator
        separator = ctk.CTkFrame(parent, height=2, fg_color="gray")
        separator.pack(fill="x", padx=10, pady=10)
        
        # Scrollable metadata form
        scroll_label = ctk.CTkLabel(parent, text="2️⃣ FILL VIDEO METADATA (optional - scroll to see all):",
                                   font=ctk.CTkFont(weight="bold", size=13))
        scroll_label.pack(anchor="w", padx=10, pady=(5,5))
        
        form_frame = ctk.CTkScrollableFrame(parent, height=250, fg_color=("#2B2B2B", "#1F1F1F"))
        form_frame.pack(fill="both", expand=True, padx=10, pady=(0,5))
        
        # White text color for metadata labels
        label_color = "white"
        
        ctk.CTkLabel(form_frame, text="Title:", text_color=label_color).pack(anchor="w", pady=2)
        self.video_title = ctk.CTkEntry(form_frame)
        self.video_title.pack(fill="x", pady=2)
        self.video_title.insert(0, "My Video Title")
        
        ctk.CTkLabel(form_frame, text="Description:", text_color=label_color).pack(anchor="w", pady=2)
        self.video_description = ctk.CTkTextbox(form_frame, height=80)
        self.video_description.pack(fill="x", pady=2)
        self.video_description.insert("1.0", "Video description")
        
        ctk.CTkLabel(form_frame, text="Tags (comma-separated):", text_color=label_color).pack(anchor="w", pady=2)
        self.video_tags = ctk.CTkEntry(form_frame)
        self.video_tags.pack(fill="x", pady=2)
        self.video_tags.insert(0, "video,youtube")
        
        ctk.CTkLabel(form_frame, text="Category ID:", text_color=label_color).pack(anchor="w", pady=2)
        self.video_category = ctk.CTkEntry(form_frame)
        self.video_category.pack(fill="x", pady=2)
        self.video_category.insert(0, "22")
        
        ctk.CTkLabel(form_frame, text="Privacy:", text_color=label_color).pack(anchor="w", pady=2)
        self.video_privacy = ctk.CTkComboBox(form_frame, 
                                            values=["public", "unlisted", "private"])
        self.video_privacy.pack(fill="x", pady=2)
        self.video_privacy.set("public")
        
        # Thumbnail
        ctk.CTkLabel(form_frame, text="Thumbnail (optional):", text_color=label_color).pack(anchor="w", pady=2)
        thumb_frame = ctk.CTkFrame(form_frame)
        thumb_frame.pack(fill="x", pady=2)
        
        ctk.CTkButton(thumb_frame, text="Select", 
                     command=self.select_thumbnail, width=80).pack(side="left", padx=5)
        self.lbl_thumbnail = ctk.CTkLabel(thumb_frame, text="No thumbnail", 
                                          text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_thumbnail.pack(side="left", padx=5)
        
        # Options (without checkboxes, using labels and switches)
        options_frame = ctk.CTkFrame(form_frame, fg_color=("#1a1a1a", "#1a1a1a"))
        options_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(options_frame, text="Content Settings:", 
                    text_color=label_color, 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=(5,2))
        
        # Made for Kids
        kids_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        kids_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(kids_frame, text="Made for Kids:", text_color=label_color).pack(side="left", padx=(0,10))
        self.video_made_for_kids = ctk.CTkSwitch(kids_frame, text="")
        self.video_made_for_kids.pack(side="left")
        
        # Synthetic Media (Always ON)
        synthetic_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        synthetic_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(synthetic_frame, text="Synthetic Media (AI):", text_color=label_color).pack(side="left", padx=(0,10))
        self.video_synthetic_media = ctk.CTkSwitch(synthetic_frame, text="")
        self.video_synthetic_media.pack(side="left")
        self.video_synthetic_media.select()  # Always ON
        
        # Monetization
        monetization_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        monetization_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(monetization_frame, text="Enable Monetization:", text_color=label_color).pack(side="left", padx=(0,10))
        self.video_enable_monetization = ctk.CTkSwitch(monetization_frame, text="", 
                                                       button_color="green", button_hover_color="#2D8F47")
        self.video_enable_monetization.pack(side="left")
        self.video_enable_monetization.select()
    
    def setup_scheduled_list(self, parent):
        ctk.CTkLabel(parent, text="📋 Upload Control Panel", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # ========== CHOOSE UPLOAD METHOD ==========
        upload_method_frame = ctk.CTkFrame(parent, fg_color=("#D5F4E6", "#58D68D"), corner_radius=10)
        upload_method_frame.pack(fill="x", padx=10, pady=(0,10))
        
        ctk.CTkLabel(upload_method_frame, text="🚀 CHOOSE UPLOAD METHOD:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        # All buttons in one row
        btn_row = ctk.CTkFrame(upload_method_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=5)
        
        # Upload Now Button (Soft Blue)
        self.btn_upload_now = ctk.CTkButton(
            btn_row, 
            text="⚡ Upload Now",
            command=self.upload_now, 
            fg_color="#5DADE2",
            hover_color="#85C1E9",
            height=32,
            width=120,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=6
        )
        self.btn_upload_now.pack(side="left", padx=3)
        
        # Schedule Button (Soft Green)
        self.btn_schedule = ctk.CTkButton(
            btn_row, 
            text="📅 Schedule",
            command=self.schedule_upload,
            fg_color="#2ECC71",
            hover_color="#58D68D",
            height=32,
            width=110,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=6
        )
        self.btn_schedule.pack(side="left", padx=3)
        
        # Refresh Button
        ctk.CTkButton(btn_row, text="🔄 Refresh",
                     command=self.refresh_scheduled_list, 
                     width=90,
                     height=32,
                     font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
        
        # Clear Completed Button
        ctk.CTkButton(btn_row, text="🗑 Clear",
                     command=self.clear_completed, 
                     width=80,
                     height=32,
                     font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
        
        # Cancel Button
        ctk.CTkButton(btn_row, text="❌ Cancel",
                     command=self.cancel_selected_upload, 
                     width=90,
                     height=32,
                     fg_color="#DC143C",
                     hover_color="#B22222",
                     font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
        
        # Status
        self.lbl_upload_status = ctk.CTkLabel(upload_method_frame, text="", 
                                             font=ctk.CTkFont(size=11, weight="bold"))
        self.lbl_upload_status.pack(padx=10, pady=(5,8))
        
        # ========== UPLOAD TIME SETTINGS ==========
        time_settings_frame = ctk.CTkFrame(parent, fg_color=("#AED6F1", "#5DADE2"), corner_radius=10)
        time_settings_frame.pack(fill="x", padx=10, pady=(0,10))
        
        ctk.CTkLabel(time_settings_frame, text="⏰ Upload Time Settings:", 
                     font=ctk.CTkFont(weight="bold", size=12)).pack(anchor="w", padx=10, pady=(10,5))
        
        # All time controls in one row
        time_frame = ctk.CTkFrame(time_settings_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(time_frame, text="Quick:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(0,3))
        self.time_preset = ctk.CTkComboBox(
            time_frame,
            values=["Now +5 min", "Now +10 min", "Now +30 min", "Now +1 hour", 
                   "Now +2 hours", "Now +6 hours", "Today 20:00", "Tomorrow 08:00", "Custom"],
            width=110,
            command=self.apply_time_preset,
            font=ctk.CTkFont(size=10)
        )
        self.time_preset.pack(side="left", padx=2)
        self.time_preset.set("Now +10 min")
        
        ctk.CTkLabel(time_frame, text="Date:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(5,3))
        self.upload_date = ctk.CTkEntry(time_frame, width=85, placeholder_text="YYYY-MM-DD",
                                       font=ctk.CTkFont(size=10))
        self.upload_date.pack(side="left", padx=2)
        
        ctk.CTkLabel(time_frame, text="Time:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(3,3))
        self.upload_time = ctk.CTkEntry(time_frame, width=60, placeholder_text="HH:MM",
                                       font=ctk.CTkFont(size=10))
        self.upload_time.pack(side="left", padx=2)
        
        # Scheduled time display
        self.lbl_scheduled_time = ctk.CTkLabel(time_settings_frame, text="", 
                                              font=ctk.CTkFont(size=10, weight="bold"),
                                              text_color=get_adaptive_warning_color(self.is_dark_mode),
                                              wraplength=280)
        self.lbl_scheduled_time.pack(padx=10, pady=(3,5))
        
        # Scheduler status in same row as time (on the right)
        status_frame = ctk.CTkFrame(time_settings_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=(0,8))
        
        ctk.CTkLabel(status_frame, text="📊 Status:", 
                    font=ctk.CTkFont(weight="bold", size=15)).pack(side="left", padx=(0,5))
        
        self.lbl_scheduler_status = ctk.CTkLabel(
            status_frame, 
            text="⚫ Idle - No scheduled uploads",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        )
        self.lbl_scheduler_status.pack(side="left", padx=0)
        
        # Separator
        separator = ctk.CTkFrame(parent, height=2, fg_color=("#E8DAEF", "#BB8FCE"))
        separator.pack(fill="x", padx=10, pady=8)
        
        # Scheduled list label
        ctk.CTkLabel(parent, text="📋 Scheduled List:", 
                     font=ctk.CTkFont(weight="bold", size=12)).pack(anchor="w", padx=10, pady=(0,5))
        
        # Scheduled list (larger)
        self.text_scheduled = ctk.CTkTextbox(parent, height=700)
        self.text_scheduled.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize time preset
        self.apply_time_preset("Now +10 min")
        
        # Auto-refresh every 10 seconds
        self.refresh_scheduled_list()
        self.auto_refresh_scheduled()
    
    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_video_path = file_path
            import os
            filename = os.path.basename(file_path)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            self.lbl_video.configure(text=f"✓ {filename} ({size_mb:.1f} MB)", 
                                    text_color=get_adaptive_success_color(self.is_dark_mode))
        else:
            self.selected_video_path = None
            self.lbl_video.configure(text="No video selected", 
                                    text_color=get_adaptive_gray_color(self.is_dark_mode))
    
    def select_thumbnail(self):
        file_path = filedialog.askopenfilename(
            title="Select Thumbnail",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_thumbnail_path = file_path
            import os
            filename = os.path.basename(file_path)
            self.lbl_thumbnail.configure(text=f"✓ {filename}", 
                                        text_color=get_adaptive_success_color(self.is_dark_mode))
        else:
            self.selected_thumbnail_path = None
            self.lbl_thumbnail.configure(text="No thumbnail", 
                                        text_color=get_adaptive_gray_color(self.is_dark_mode))
    
    def apply_time_preset(self, choice):
        """Apply time preset to date/time fields"""
        now = datetime.now()
        
        preset_map = {
            "Now +5 min": now + timedelta(minutes=5),
            "Now +10 min": now + timedelta(minutes=10),
            "Now +30 min": now + timedelta(minutes=30),
            "Now +1 hour": now + timedelta(hours=1),
            "Now +2 hours": now + timedelta(hours=2),
            "Now +6 hours": now + timedelta(hours=6),
            "Today 20:00": now.replace(hour=20, minute=0, second=0),
            "Tomorrow 08:00": (now + timedelta(days=1)).replace(hour=8, minute=0, second=0),
        }
        
        if choice == "Custom":
            # Don't change current values for custom
            scheduled_time = self.get_scheduled_datetime()
            if scheduled_time:
                self.update_scheduled_time_display(scheduled_time)
            return
        
        target_time = preset_map.get(choice, now + timedelta(minutes=10))
        
        self.upload_date.delete(0, "end")
        self.upload_date.insert(0, target_time.strftime("%Y-%m-%d"))
        
        self.upload_time.delete(0, "end")
        self.upload_time.insert(0, target_time.strftime("%H:%M"))
        
        self.update_scheduled_time_display(target_time)
    
    def update_scheduled_time_display(self, scheduled_dt):
        """Update the scheduled time display label"""
        now = datetime.now()
        time_diff = scheduled_dt - now
        
        if time_diff.total_seconds() < 0:
            display_text = f"⚠️ Scheduled: {scheduled_dt.strftime('%Y-%m-%d %H:%M')} (IN THE PAST!)"
            color = get_adaptive_error_color(self.is_dark_mode)
        elif time_diff.total_seconds() < 60:
            display_text = f"📤 Will upload: {scheduled_dt.strftime('%Y-%m-%d %H:%M')} (NOW!)"
            color = get_adaptive_warning_color(self.is_dark_mode)
        else:
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            
            if hours > 0:
                time_str = f"{hours}h {minutes}m"
            else:
                time_str = f"{minutes}m"
            
            display_text = f"📤 Will upload: {scheduled_dt.strftime('%Y-%m-%d %H:%M')} (in {time_str})"
            color = get_adaptive_success_color(self.is_dark_mode)
        
        self.lbl_scheduled_time.configure(text=display_text, text_color=color)
    
    def get_scheduled_datetime(self):
        """Get scheduled datetime from form fields"""
        try:
            date_str = self.upload_date.get().strip()
            time_str = self.upload_time.get().strip()
            if date_str and time_str:
                return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except:
            pass
        return None
    
    def set_time_now(self):
        now = datetime.now() + timedelta(minutes=5)
        self.upload_date.delete(0, "end")
        self.upload_date.insert(0, now.strftime("%Y-%m-%d"))
        self.upload_time.delete(0, "end")
        self.upload_time.insert(0, now.strftime("%H:%M"))
        self.update_scheduled_time_display(now)
    
    def get_video_data(self):
        """Collect video data from form"""
        if not self.selected_video_path:
            raise ValueError("No video file selected")
        
        title = self.video_title.get().strip()
        if not title:
            raise ValueError("Title is required")
        
        description = self.video_description.get("1.0", "end").strip()
        tags = [tag.strip() for tag in self.video_tags.get().split(',') if tag.strip()]
        
        return {
            "videoPath": self.selected_video_path,
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": self.video_category.get().strip(),
            "privacyStatus": self.video_privacy.get(),
            "thumbnailPath": self.selected_thumbnail_path,
            "madeForKids": self.video_made_for_kids.get() == 1,
            "containsSyntheticMedia": self.video_synthetic_media.get() == 1,
            "enableMonetization": self.video_enable_monetization.get() == 1
        }
    
    def schedule_upload(self):
        if not self.app.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.video_uploader:
            messagebox.showerror("Error", "Video uploader not initialized")
            return
        
        try:
            video_data = self.get_video_data()
            
            date_str = self.upload_date.get().strip()
            time_str = self.upload_time.get().strip()
            scheduled_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            if scheduled_dt <= datetime.now():
                result = messagebox.askyesno("Warning", 
                    "Scheduled time is in the past or very soon.\nUpload immediately instead?")
                if result:
                    self.upload_now()
                    return
                else:
                    return
            
            index = self.video_uploader.schedule_upload(video_data, scheduled_dt.isoformat())
            
            self.lbl_upload_status.configure(
                text=f"✓ Video scheduled for {scheduled_dt.strftime('%Y-%m-%d %H:%M')}", 
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            
            self.app.log_message(f"[SCHEDULE] Video scheduled: {video_data['title']} at {scheduled_dt}")
            self.refresh_scheduled_list()
            
            # Auto-start scheduler if not running
            if not self.video_uploader.is_running:
                self.start_scheduler()
            
            messagebox.showinfo("Success", 
                f"Video scheduled successfully!\n\nUpload time: {scheduled_dt.strftime('%Y-%m-%d %H:%M')}\n\n"
                "Scheduler has been started automatically.")
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule: {str(e)}")
    
    def upload_now(self):
        if not self.app.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.video_uploader:
            messagebox.showerror("Error", "Video uploader not initialized")
            return
        
        try:
            video_data = self.get_video_data()
            
            def upload_thread():
                self.btn_upload_now.configure(state="disabled")
                self.btn_schedule.configure(state="disabled")
                self.lbl_upload_status.configure(text="⏳ Uploading...", 
                                                text_color=get_adaptive_warning_color(self.is_dark_mode))
                
                success, result = self.video_uploader.upload_video_immediate(
                    video_data,
                    log_callback=self.app.log_message
                )
                
                if success:
                    self.lbl_upload_status.configure(
                        text=f"✓ Upload complete! Video ID: {result}", 
                        text_color=get_adaptive_success_color(self.is_dark_mode)
                    )
                    messagebox.showinfo("Success", f"Video uploaded successfully!\n\nVideo ID: {result}")
                else:
                    self.lbl_upload_status.configure(
                        text=f"✗ Upload failed", 
                        text_color=get_adaptive_error_color(self.is_dark_mode)
                    )
                    messagebox.showerror("Error", f"Upload failed:\n{result}")
                
                self.btn_upload_now.configure(state="normal")
                self.btn_schedule.configure(state="normal")
            
            threading.Thread(target=upload_thread, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start upload: {str(e)}")
    
    def start_scheduler(self):
        if not self.video_uploader:
            self.app.log_message("[SCHEDULER] Error: Video uploader not initialized")
            return
        
        success, message = self.video_uploader.start_scheduler(
            log_callback=self.app.log_message
        )
        
        if success:
            self.lbl_scheduler_status.configure(
                text="🟢 Active - Monitoring scheduled uploads", 
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            self.app.log_message("[SCHEDULER] Started successfully - checking every 30 seconds")
        else:
            self.app.log_message(f"[SCHEDULER] {message}")
    
    def stop_scheduler(self):
        if not self.video_uploader:
            return
        
        success, message = self.video_uploader.stop_scheduler()
        
        if success:
            self.lbl_scheduler_status.configure(
                text="⚫ Stopped", 
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            )
            self.app.log_message("[SCHEDULER] Stopped")
    
    def update_scheduler_status(self):
        """Update scheduler status display"""
        if self.video_uploader and self.video_uploader.is_running:
            scheduled = self.video_uploader.get_scheduled_uploads()
            pending = [s for s in scheduled if s["status"] == "pending"]
            if pending:
                self.lbl_scheduler_status.configure(
                    text=f"🟢 Active - {len(pending)} video(s) pending",
                    text_color=get_adaptive_success_color(self.is_dark_mode)
                )
            else:
                self.lbl_scheduler_status.configure(
                    text="🟢 Active - No pending uploads",
                    text_color=get_adaptive_success_color(self.is_dark_mode)
                )
        else:
            scheduled = self.video_uploader.get_scheduled_uploads() if self.video_uploader else []
            pending = [s for s in scheduled if s["status"] == "pending"]
            if pending:
                self.lbl_scheduler_status.configure(
                    text=f"⚠️ Idle - {len(pending)} video(s) waiting (scheduler not started)",
                    text_color=get_adaptive_warning_color(self.is_dark_mode)
                )
            else:
                self.lbl_scheduler_status.configure(
                    text="⚫ Idle - No scheduled uploads",
                    text_color=get_adaptive_gray_color(self.is_dark_mode)
                )
    
    def refresh_scheduled_list(self):
        if not self.video_uploader:
            return
        
        # Update scheduler status
        self.update_scheduler_status()
        
        scheduled = self.video_uploader.get_scheduled_uploads()
        
        self.text_scheduled.configure(state="normal")
        self.text_scheduled.delete("1.0", "end")
        
        if not scheduled:
            self.text_scheduled.insert("1.0", "No scheduled uploads.\n\nSchedule a video to see it here.")
        else:
            text = f"Total: {len(scheduled)} scheduled upload(s)\n"
            text += "=" * 80 + "\n\n"
            
            for idx, item in enumerate(scheduled):
                video_data = item["video_data"]
                scheduled_time = datetime.fromisoformat(item["scheduled_time"])
                status = item["status"]
                
                status_emoji = {
                    "pending": "⏳",
                    "processing": "🔄",
                    "completed": "✓",
                    "failed": "✗"
                }
                
                text += f"{idx + 1}. {status_emoji.get(status, '•')} {video_data['title']}\n"
                text += f"   Status: {status.upper()}\n"
                text += f"   Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                if status == "completed":
                    text += f"   Video ID: {item.get('video_id', 'N/A')}\n"
                    text += f"   Completed: {item.get('completed_at', 'N/A')}\n"
                elif status == "failed":
                    text += f"   Error: {item.get('error', 'Unknown')}\n"
                
                text += "\n"
            
            self.text_scheduled.insert("1.0", text)
        
        self.text_scheduled.configure(state="disabled")
    
    def clear_completed(self):
        if not self.video_uploader:
            return
        
        self.video_uploader.clear_completed_uploads()
        self.refresh_scheduled_list()
        self.app.log_message("[SCHEDULER] Cleared completed/failed uploads")
    
    def cancel_selected_upload(self):
        """Cancel selected scheduled uploads"""
        if not self.video_uploader:
            messagebox.showwarning("Warning", "Video uploader not initialized")
            return
        
        scheduled = self.video_uploader.get_scheduled_uploads()
        pending = [s for s in scheduled if s["status"] == "pending"]
        
        if not pending:
            messagebox.showinfo("No Pending Uploads", "There are no pending uploads to cancel.")
            return
        
        # Create selection window
        select_window = ctk.CTkToplevel(self.app)
        select_window.title("Cancel Scheduled Upload")
        select_window.geometry("600x500")
        select_window.grab_set()
        
        ctk.CTkLabel(select_window, text="Select Upload(s) to Cancel", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(select_window, text=f"{len(pending)} pending upload(s)", 
                    font=ctk.CTkFont(size=12)).pack(pady=5)
        
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
                messagebox.showwarning("No Selection", "Please select at least one upload to cancel")
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
            messagebox.showinfo("Success", f"Successfully cancelled {cancelled_count} upload(s)")
        
        ctk.CTkButton(btn_frame, text="✓ Select All", 
                     command=select_all, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✗ Deselect All", 
                     command=deselect_all, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Close", 
                     command=select_window.destroy, width=100).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Cancel Selected", 
                     command=cancel_selected, width=140,
                     fg_color="#DC143C", hover_color="#B22222").pack(side="right", padx=5)
    
    def auto_refresh_scheduled(self):
        """Auto-refresh scheduled list every 10 seconds"""
        self.refresh_scheduled_list()
        self.tab.after(10000, self.auto_refresh_scheduled)
    
    def setup_batch_upload_tab(self):
        """Setup batch upload from Excel tab"""
        frame = ctk.CTkFrame(self.tab_batch)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="📊 Batch Video Upload from Excel", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # File selection
        file_frame = ctk.CTkFrame(frame)
        file_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(file_frame, text="Select Excel File", 
                     command=self.select_excel_file, width=150).pack(side="left", padx=5)
        
        self.lbl_excel_status = ctk.CTkLabel(file_frame, text="No file selected", 
                                            text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_excel_status.pack(side="left", padx=10)
        
        # Scheduling options
        schedule_frame = ctk.CTkFrame(frame)
        schedule_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(schedule_frame, text="⏰ Batch Scheduling:", 
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        options_frame = ctk.CTkFrame(schedule_frame)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(options_frame, text="Start Time:").pack(side="left", padx=5)
        self.batch_start_date = ctk.CTkEntry(options_frame, width=100)
        self.batch_start_date.pack(side="left", padx=5)
        
        self.batch_start_time = ctk.CTkEntry(options_frame, width=80)
        self.batch_start_time.pack(side="left", padx=5)
        
        ctk.CTkButton(options_frame, text="🔄 Now", 
                     command=self.set_batch_time_now, width=60).pack(side="left", padx=5)
        
        ctk.CTkLabel(options_frame, text="Interval:").pack(side="left", padx=10)
        self.batch_interval = ctk.CTkComboBox(options_frame, 
                                              values=["0 min", "5 min", "10 min", "15 min", "30 min", "1 hour"],
                                              width=100)
        self.batch_interval.pack(side="left", padx=5)
        self.batch_interval.set("10 min")
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_schedule_batch = ctk.CTkButton(btn_frame, text="📅 Schedule All Videos",
                                                command=self.schedule_batch_videos)
        self.btn_schedule_batch.pack(side="left", padx=5)
        
        self.lbl_batch_status = ctk.CTkLabel(frame, text="")
        self.lbl_batch_status.pack(pady=5)
        
        # Preview
        ctk.CTkLabel(frame, text="Preview (first 5 videos):").pack(pady=5)
        self.text_batch_preview = ctk.CTkTextbox(frame, height=300)
        self.text_batch_preview.pack(fill="both", expand=True, pady=10)
        
        self.set_batch_time_now()
    
    def select_excel_file(self):
        """Select Excel file for batch upload"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            success, message = self.video_parser.load_excel(file_path)
            
            if success:
                self.lbl_excel_status.configure(text=f"✓ {message}", 
                                                text_color=get_adaptive_success_color(self.is_dark_mode))
                self.app.log_message(f"[BATCH] Excel loaded: {message}")
                self.preview_batch_videos()
            else:
                self.lbl_excel_status.configure(text=f"✗ {message}", 
                                                text_color=get_adaptive_error_color(self.is_dark_mode))
                messagebox.showerror("Error", message)
                self.app.log_message(f"[BATCH] Error: {message}")
    
    def set_batch_time_now(self):
        """Set batch start time to now + 5 minutes"""
        now = datetime.now() + timedelta(minutes=5)
        self.batch_start_date.delete(0, "end")
        self.batch_start_date.insert(0, now.strftime("%Y-%m-%d"))
        self.batch_start_time.delete(0, "end")
        self.batch_start_time.insert(0, now.strftime("%H:%M"))
    
    def preview_batch_videos(self):
        """Preview videos from Excel"""
        preview_df = self.video_parser.get_preview(5)
        
        if preview_df is None:
            return
        
        text = "=" * 100 + "\n"
        text += "PREVIEW - First 5 Videos\n"
        text += "=" * 100 + "\n\n"
        
        videos = self.video_parser.get_all_videos()[:5]
        
        for idx, video in enumerate(videos, 1):
            if "error" in video:
                text += f"❌ Row {idx}: ERROR - {video['error']}\n\n"
                continue
            
            text += f"✓ Video {idx}:\n"
            text += "-" * 80 + "\n"
            text += f"  Path: {video['videoPath']}\n"
            text += f"  Title: {video['title']}\n"
            text += f"  Tags: {', '.join(video['tags'])}\n"
            text += f"  Category: {video['categoryId']}\n"
            text += f"  Privacy: {video['privacyStatus']}\n"
            text += f"  Monetization: {video['enableMonetization']}\n"
            if video.get('scheduledTime'):
                text += f"  Scheduled: {video['scheduledTime']}\n"
            text += "\n"
        
        self.text_batch_preview.delete("1.0", "end")
        self.text_batch_preview.insert("1.0", text)
    
    def schedule_batch_videos(self):
        """Schedule all videos from Excel"""
        if not self.app.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.video_uploader:
            messagebox.showerror("Error", "Video uploader not initialized")
            return
        
        videos = self.video_parser.get_all_videos()
        if not videos:
            messagebox.showerror("Error", "No videos to schedule")
            return
        
        try:
            # Parse start time and interval
            date_str = self.batch_start_date.get().strip()
            time_str = self.batch_start_time.get().strip()
            start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            interval_map = {
                "0 min": timedelta(0),
                "5 min": timedelta(minutes=5),
                "10 min": timedelta(minutes=10),
                "15 min": timedelta(minutes=15),
                "30 min": timedelta(minutes=30),
                "1 hour": timedelta(hours=1)
            }
            interval = interval_map.get(self.batch_interval.get(), timedelta(minutes=10))
            
            scheduled_count = 0
            error_count = 0
            
            for idx, video in enumerate(videos):
                if "error" in video:
                    self.app.log_message(f"[BATCH] Skipped row {idx+1}: {video['error']}")
                    error_count += 1
                    continue
                
                # Use scheduled time from Excel if provided, otherwise calculate
                if video.get('scheduledTime'):
                    scheduled_time = video['scheduledTime']
                else:
                    video_dt = start_dt + (interval * idx)
                    scheduled_time = video_dt.isoformat()
                
                self.video_uploader.schedule_upload(video, scheduled_time)
                scheduled_count += 1
                
                self.app.log_message(f"[BATCH] Scheduled: {video['title']} at {scheduled_time}")
            
            self.lbl_batch_status.configure(
                text=f"✓ Scheduled {scheduled_count} videos ({error_count} errors)", 
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            
            self.refresh_scheduled_list()
            
            messagebox.showinfo("Success", 
                f"Batch scheduling complete!\n\n"
                f"Scheduled: {scheduled_count}\n"
                f"Errors: {error_count}\n\n"
                f"Start the scheduler to begin uploading.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule batch: {str(e)}")
    
    def update_adaptive_colors(self, is_dark_mode):
        """Update all adaptive colors based on theme"""
        self.is_dark_mode = is_dark_mode
        
        # Update video selection label
        if hasattr(self, 'lbl_video'):
            current_text = self.lbl_video.cget("text")
            if "No video" in current_text:
                self.lbl_video.configure(text_color=get_adaptive_warning_color(self.is_dark_mode))
            elif "✓" in current_text:
                self.lbl_video.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
        
        # Update thumbnail label
        if hasattr(self, 'lbl_thumbnail'):
            current_text = self.lbl_thumbnail.cget("text")
            if "No thumbnail" in current_text:
                self.lbl_thumbnail.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
            elif "✓" in current_text:
                self.lbl_thumbnail.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
        
        # Update upload status
        if hasattr(self, 'lbl_upload_status'):
            current_text = self.lbl_upload_status.cget("text")
            if "✓" in current_text:
                self.lbl_upload_status.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
            elif "✗" in current_text:
                self.lbl_upload_status.configure(text_color=get_adaptive_error_color(self.is_dark_mode))
            elif "⏳" in current_text:
                self.lbl_upload_status.configure(text_color=get_adaptive_warning_color(self.is_dark_mode))
        
        # Update scheduler status
        if hasattr(self, 'lbl_scheduler_status'):
            self.update_scheduler_status()
        
        # Update scheduled time display
        if hasattr(self, 'lbl_scheduled_time'):
            scheduled_dt = self.get_scheduled_datetime()
            if scheduled_dt:
                self.update_scheduled_time_display(scheduled_dt)
        
        # Update batch excel status
        if hasattr(self, 'lbl_excel_status'):
            current_text = self.lbl_excel_status.cget("text")
            if "No file" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
            elif "✓" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
            elif "✗" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_error_color(self.is_dark_mode))
        
        # Update batch status
        if hasattr(self, 'lbl_batch_status'):
            current_text = self.lbl_batch_status.cget("text")
            if "✓" in current_text:
                self.lbl_batch_status.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
