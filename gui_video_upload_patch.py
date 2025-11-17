"""
Patch untuk gui_video_upload.py
Menambahkan tombol Cancel untuk scheduled uploads
"""

# TAMBAHKAN METHOD INI KE CLASS VideoUploadTab (setelah refresh_scheduled_list):

def cancel_selected_upload(self):
    """Cancel a selected scheduled upload - with selection dialog"""
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
    select_window.grab_set()  # Make modal
    
    ctk.CTkLabel(select_window, text="Select Upload(s) to Cancel", 
                font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    
    ctk.CTkLabel(select_window, text=f"{len(pending)} pending upload(s)", 
                font=ctk.CTkFont(size=12)).pack(pady=5)
    
    # Scrollable frame for checkboxes
    scroll_frame = ctk.CTkScrollableFrame(select_window, height=300)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create checkboxes for each pending upload
    checkbox_vars = []
    
    for idx, item in enumerate(pending):
        video_data = item["video_data"]
        scheduled_time = datetime.fromisoformat(item["scheduled_time"])
        
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(fill="x", pady=5, padx=5)
        
        var = ctk.BooleanVar(value=False)
        checkbox_vars.append((var, idx))
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text="",
            variable=var,
            width=30
        )
        checkbox.pack(side="left", padx=5)
        
        info_text = f"{idx+1}. {video_data['title']}\n"
        info_text += f"   Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        label = ctk.CTkLabel(frame, text=info_text, justify="left",
                           font=ctk.CTkFont(size=11))
        label.pack(side="left", padx=5, fill="x", expand=True)
    
    # Button frame
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
        
        # Confirm cancellation
        result = messagebox.askyesno(
            "Confirm Cancellation",
            f"Cancel {len(selected_indices)} selected upload(s)?",
            parent=select_window
        )
        
        if not result:
            return
        
        # Cancel selected uploads
        cancelled_count = 0
        for idx in sorted(selected_indices, reverse=True):  # Reverse to maintain indices
            if self.video_uploader.cancel_upload(idx):
                cancelled_count += 1
        
        self.app.log_message(f"[CANCEL] Cancelled {cancelled_count} upload(s)")
        self.refresh_scheduled_list()
        
        select_window.destroy()
        
        messagebox.showinfo("Success", 
                          f"Successfully cancelled {cancelled_count} upload(s)")
    
    ctk.CTkButton(btn_frame, text="✓ Select All", 
                 command=select_all, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="✗ Deselect All", 
                 command=deselect_all, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Cancel", 
                 command=select_window.destroy, width=100).pack(side="right", padx=5)
    ctk.CTkButton(btn_frame, text="🗑 Cancel Selected", 
                 command=cancel_selected, width=140,
                 fg_color="#DC143C", hover_color="#B22222").pack(side="right", padx=5)


# MODIFIKASI setup_scheduled_list() - Tambahkan tombol Cancel di btn_row (setelah tombol Clear):
"""
        # Cancel Selected Button (RED)
        ctk.CTkButton(btn_row, text="❌ Cancel",
                     command=self.cancel_selected_upload, 
                     width=90,
                     height=32,
                     fg_color="#DC143C",
                     hover_color="#B22222",
                     font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=3)
"""

# TAMBAHKAN METHOD KE video_uploader.py (di class VideoUploader):
"""
    def cancel_upload(self, index: int) -> bool:
        '''Cancel a scheduled upload by index'''
        try:
            if 0 <= index < len(self.scheduled_uploads):
                cancelled_item = self.scheduled_uploads[index]
                
                # Only cancel if status is pending
                if cancelled_item['status'] == 'pending':
                    cancelled_item['status'] = 'cancelled'
                    cancelled_item['cancelled_at'] = datetime.now().isoformat()
                    self.save_scheduled_uploads()
                    return True
            return False
        except Exception as e:
            print(f"Error cancelling upload: {e}")
            return False
    
    def clear_completed_uploads(self):
        '''Clear completed, failed, and cancelled uploads'''
        try:
            self.scheduled_uploads = [
                s for s in self.scheduled_uploads 
                if s['status'] not in ['completed', 'failed', 'cancelled']
            ]
            self.save_scheduled_uploads()
        except Exception as e:
            print(f"Error clearing uploads: {e}")
"""
