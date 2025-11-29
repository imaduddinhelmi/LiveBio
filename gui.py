import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from datetime import datetime, timedelta, timezone
from auth import YouTubeAuth
from excel_parser import ExcelParser
from youtube_service import YouTubeService
from gui_video_upload import VideoUploadTab
from batch_scheduler import BatchScheduler
import config
import json
from pathlib import Path
from color_utils import (
    get_adaptive_text_color,
    get_adaptive_gray_color,
    get_adaptive_success_color,
    get_adaptive_error_color,
    get_adaptive_warning_color
)

# Load saved theme or use default
SETTINGS_FILE = Path.home() / ".ytlive" / "settings.json"

def load_theme():
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                return settings.get('theme', 'dark')
    except:
        pass
    return 'dark'

def save_theme(theme):
    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        settings = {'theme': theme}
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
        settings['theme'] = theme
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except:
        pass

# Set initial theme
initial_theme = load_theme()
ctk.set_appearance_mode(initial_theme)
ctk.set_default_color_theme("green")  # Changed to green for softer look

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.geometry("1200x800")
        
        # Set minimum window size
        self.minsize(1000, 700)
        
        self.auth = YouTubeAuth()
        self.parser = ExcelParser()
        self.youtube_service = None
        self.batch_scheduler = BatchScheduler(log_callback=self.log_message)
        
        self.client_secret_path = None
        
        # Track current theme for adaptive colors
        self.is_dark_mode = ctk.get_appearance_mode() == "Dark"
        
        # Flag to prevent multiple auto-loads
        self.auto_load_done = False
        
        self.create_tabs()
        
        # Auto-load account after GUI is ready (with delay)
        self.after(1000, self.auto_load_active_account)
        
    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_auth = self.tabview.add("Auth")
        self.tab_quick = self.tabview.add("Quick Create")
        self.tab_import = self.tabview.add("Import & Run")
        self.tab_video_upload = self.tabview.add("Video Upload")
        self.tab_upcoming = self.tabview.add("Upcoming")
        self.tab_settings = self.tabview.add("Settings")
        self.tab_logs = self.tabview.add("Logs")
        
        self.setup_auth_tab()
        self.setup_quick_tab()
        self.setup_import_tab()
        self.video_upload_tab = VideoUploadTab(self, self.tab_video_upload)
        self.setup_upcoming_tab()
        self.setup_settings_tab()
        self.setup_logs_tab()
    
    def setup_auth_tab(self):
        frame = ctk.CTkFrame(self.tab_auth)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="🔐 YouTube OAuth Authentication", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # ========== SAVED ACCOUNTS SECTION ==========
        saved_accounts_frame = ctk.CTkFrame(frame, fg_color=("#D5F4E6", "#2E7D32"), corner_radius=10)
        saved_accounts_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(saved_accounts_frame, text="📚 Saved Accounts", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10,5))
        
        # Account selector
        accounts_control = ctk.CTkFrame(saved_accounts_frame, fg_color="transparent")
        accounts_control.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(accounts_control, text="Select Account:", 
                    font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        
        self.account_selector = ctk.CTkComboBox(
            accounts_control,
            values=["No saved accounts"],
            command=self.on_account_selected,
            width=300,
            state="readonly"
        )
        self.account_selector.pack(side="left", padx=5)
        
        self.btn_switch_account = ctk.CTkButton(
            accounts_control,
            text="✓ Use This Account",
            command=self.switch_to_selected_account,
            width=140,
            state="disabled",
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        self.btn_switch_account.pack(side="left", padx=5)
        
        self.btn_remove_account = ctk.CTkButton(
            accounts_control,
            text="🗑 Remove",
            command=self.remove_selected_account,
            width=100,
            state="disabled",
            fg_color="#DC143C",
            hover_color="#B22222"
        )
        self.btn_remove_account.pack(side="left", padx=5)
        
        # Account info display
        self.lbl_account_info = ctk.CTkLabel(
            saved_accounts_frame,
            text="No account selected",
            font=ctk.CTkFont(size=11),
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        )
        self.lbl_account_info.pack(padx=10, pady=(0,10))
        
        # Separator
        separator1 = ctk.CTkFrame(frame, height=2, fg_color=get_adaptive_gray_color(self.is_dark_mode))
        separator1.pack(fill="x", padx=10, pady=10)
        
        # ========== ADD NEW ACCOUNT SECTION ==========
        new_account_label = ctk.CTkLabel(frame, text="➕ Add New Account", 
                     font=ctk.CTkFont(size=16, weight="bold"))
        new_account_label.pack(pady=(10,5))
        
        ctk.CTkLabel(frame, text="Select client_secret.json file:").pack(pady=5)
        
        self.btn_select_secret = ctk.CTkButton(
            frame, text="Select client_secret.json", 
            command=self.select_client_secret
        )
        self.btn_select_secret.pack(pady=5)
        
        self.lbl_secret_path = ctk.CTkLabel(frame, text="No file selected", 
                                            text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_secret_path.pack(pady=5)
        
        btn_auth_frame = ctk.CTkFrame(frame)
        btn_auth_frame.pack(pady=20)
        
        self.btn_login = ctk.CTkButton(
            btn_auth_frame, text="🔑 Add New Account", 
            command=self.do_login, state="disabled",
            fg_color="#1976D2",
            hover_color="#1565C0"
        )
        self.btn_login.pack(side="left", padx=5)
        
        self.btn_logout = ctk.CTkButton(
            btn_auth_frame, text="Logout / Reset", 
            command=self.do_logout, state="disabled",
            fg_color="#DC143C", hover_color="#B22222"
        )
        self.btn_logout.pack(side="left", padx=5)
        
        self.lbl_auth_status = ctk.CTkLabel(frame, text="Not authenticated", 
                                            text_color=get_adaptive_error_color(self.is_dark_mode))
        self.lbl_auth_status.pack(pady=10)
        
        ctk.CTkLabel(frame, text="Select Channel:").pack(pady=5)
        
        self.channel_selector = ctk.CTkComboBox(
            frame, 
            values=["No channels available"],
            command=self.on_channel_selected,
            state="disabled"
        )
        self.channel_selector.pack(pady=5)
        
        self.text_channel_info = ctk.CTkTextbox(frame, height=150, state="disabled")
        self.text_channel_info.pack(fill="both", expand=True, pady=10)
        
        # Initialize account list
        self.refresh_account_list()
    
    def select_client_secret(self):
        file_path = filedialog.askopenfilename(
            title="Select client_secret.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.client_secret_path = file_path
            self.lbl_secret_path.configure(text=file_path)
            self.btn_login.configure(state="normal")
    
    def refresh_account_list(self):
        """Refresh the list of saved accounts"""
        try:
            accounts = self.auth.account_manager.get_all_accounts()
            
            if accounts:
                account_names = []
                for acc in accounts:
                    channels_count = len(acc.get('channels', []))
                    label = f"{acc['name']} ({channels_count} channel{'s' if channels_count != 1 else ''})"
                    account_names.append(label)
                
                self.account_selector.configure(values=account_names, state="readonly")
                self.account_selector.set(account_names[0])
                self.btn_switch_account.configure(state="normal")
                self.btn_remove_account.configure(state="normal")
                
                # Update info label
                active_account = self.auth.account_manager.get_active_account()
                if active_account:
                    info_text = f"✓ Active: {active_account['name']}"
                    if self.auth.is_authenticated():
                        info_text += " | Logged In"
                    self.lbl_account_info.configure(
                        text=info_text,
                        text_color=get_adaptive_success_color(self.is_dark_mode)
                    )
                else:
                    self.lbl_account_info.configure(
                        text=f"{len(accounts)} account(s) saved • Select one to use",
                        text_color=get_adaptive_gray_color(self.is_dark_mode)
                    )
            else:
                self.account_selector.configure(values=["No saved accounts"], state="disabled")
                self.account_selector.set("No saved accounts")
                self.btn_switch_account.configure(state="disabled")
                self.btn_remove_account.configure(state="disabled")
                self.lbl_account_info.configure(
                    text="No saved accounts • Add your first account below",
                    text_color=get_adaptive_gray_color(self.is_dark_mode)
                )
        except Exception as e:
            self.log_message(f"✗ Error refreshing account list: {str(e)}")
    
    def on_account_selected(self, choice):
        """Handle account selection from dropdown"""
        # Update info based on selected account
        accounts = self.auth.account_manager.get_all_accounts()
        if accounts:
            # Find selected account by matching name
            selected_name = choice.split(' (')[0]
            for acc in accounts:
                if acc['name'] == selected_name:
                    channels_count = len(acc.get('channels', []))
                    info_text = f"Selected: {acc['name']} • {channels_count} channel(s) • Last used: {acc.get('last_used', 'Never')[:10]}"
                    self.lbl_account_info.configure(
                        text=info_text,
                        text_color=get_adaptive_gray_color(self.is_dark_mode)
                    )
                    break
    
    def switch_to_selected_account(self):
        """Switch to the selected account"""
        try:
            selected_text = self.account_selector.get()
            if "No saved accounts" in selected_text:
                return
            
            # Find account by name
            selected_name = selected_text.split(' (')[0]
            accounts = self.auth.account_manager.get_all_accounts()
            
            target_account = None
            for acc in accounts:
                if acc['name'] == selected_name:
                    target_account = acc
                    break
            
            if not target_account:
                messagebox.showerror("Error", "Account not found")
                return
            
            def switch_thread():
                try:
                    self.log_message(f"Switching to: {target_account['name']}...")
                    
                    # Disable buttons during switch
                    self.after(0, lambda: self.btn_switch_account.configure(state="disabled", text="Switching..."))
                    
                    success = self.auth.switch_account(target_account['id'])
                    
                    if success:
                        # Initialize services
                        self.youtube_service = YouTubeService(self.auth.youtube, self.auth)
                        if hasattr(self, 'video_upload_tab') and self.video_upload_tab:
                            self.video_upload_tab.initialize_uploader(self.youtube_service)
                        
                        channels, error = self.auth.get_all_channels()
                        
                        if error:
                            self.log_message(f"⚠ {error}")
                            self.after(0, lambda: self.lbl_auth_status.configure(
                                text=f"⚠ {target_account['name']} (No Channels)",
                                text_color=get_adaptive_warning_color(self.is_dark_mode)
                            ))
                            self.after(0, lambda: messagebox.showwarning("Warning", 
                                f"Switched to {target_account['name']}, but no channels found:\n\n{error}"))
                        else:
                            self.log_message(f"✓ Switched to {target_account['name']} • {len(channels)} channel(s)")
                            
                            # Update UI in main thread
                            def update_ui():
                                try:
                                    self.lbl_auth_status.configure(
                                        text=f"✓ Logged in as: {target_account['name']}",
                                        text_color=get_adaptive_success_color(self.is_dark_mode)
                                    )
                                    
                                    # Update channel selector
                                    if channels:
                                        channel_names = [f"{ch['title']} ({ch['id']})" for ch in channels]
                                        self.channel_selector.configure(values=channel_names, state="normal")
                                        self.channel_selector.set(channel_names[0])
                                        self.update_channel_info_display(channels[0])
                                    
                                    self.btn_logout.configure(state="normal")
                                    self.refresh_account_list()
                                    
                                    messagebox.showinfo("Success", 
                                        f"✓ Switched to: {target_account['name']}\n\n{len(channels)} channel(s) available")
                                except Exception as e:
                                    self.log_message(f"✗ UI update error: {str(e)}")
                            
                            self.after(0, update_ui)
                    else:
                        self.log_message(f"✗ Failed to switch account")
                        self.after(0, lambda: messagebox.showerror("Error", 
                            f"Failed to switch to {target_account['name']}\n\n"
                            "The saved credentials may be invalid.\n"
                            "Try removing and re-adding the account."))
                    
                    # Re-enable button
                    self.after(0, lambda: self.btn_switch_account.configure(state="normal", text="✓ Use This Account"))
                    
                except Exception as e:
                    self.log_message(f"✗ Switch error: {str(e)}")
                    import traceback
                    self.log_message(traceback.format_exc())
                    self.after(0, lambda: messagebox.showerror("Error", f"Switch failed:\n\n{str(e)}"))
                    self.after(0, lambda: self.btn_switch_account.configure(state="normal", text="✓ Use This Account"))
            
            threading.Thread(target=switch_thread, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"✗ Switch account error: {str(e)}")
            messagebox.showerror("Error", f"Failed to switch account:\n\n{str(e)}")
    
    def remove_selected_account(self):
        """Remove the selected account"""
        selected_text = self.account_selector.get()
        if "No saved accounts" in selected_text:
            return
        
        selected_name = selected_text.split(' (')[0]
        
        result = messagebox.askyesno(
            "Confirm Remove Account",
            f"Are you sure you want to remove account:\n\n{selected_name}\n\n"
            "This will delete the saved credentials for this account."
        )
        
        if not result:
            return
        
        accounts = self.auth.account_manager.get_all_accounts()
        for acc in accounts:
            if acc['name'] == selected_name:
                success = self.auth.account_manager.remove_account(acc['id'])
                if success:
                    self.log_message(f"✓ Removed account: {selected_name}")
                    
                    # If this was the active account, clear auth
                    if self.auth.current_account_id == acc['id']:
                        self.auth.credentials = None
                        self.auth.youtube = None
                        self.auth.current_account_id = None
                        self.youtube_service = None
                        self.lbl_auth_status.configure(
                            text="Not authenticated",
                            text_color=get_adaptive_error_color(self.is_dark_mode)
                        )
                        self.btn_logout.configure(state="disabled")
                        self.channel_selector.configure(values=["No channels available"], state="disabled")
                    
                    self.refresh_account_list()
                    messagebox.showinfo("Success", f"Account removed: {selected_name}")
                else:
                    messagebox.showerror("Error", "Failed to remove account")
                break
    
    def auto_load_active_account(self):
        """Auto-load the active account on startup"""
        if self.auto_load_done:
            return
        
        self.auto_load_done = True
        
        try:
            active_account = self.auth.account_manager.get_active_account()
            if not active_account:
                self.log_message("ℹ No saved accounts found. Add an account to get started.")
                return
            
            def load_thread():
                try:
                    self.log_message(f"Auto-loading account: {active_account['name']}...")
                    
                    # Try to switch to the account
                    success = self.auth.switch_account(active_account['id'])
                    
                    if success:
                        # Initialize services
                        self.youtube_service = YouTubeService(self.auth.youtube, self.auth)
                        if hasattr(self, 'video_upload_tab') and self.video_upload_tab:
                            self.video_upload_tab.initialize_uploader(self.youtube_service)
                        
                        # Get channels
                        channels, error = self.auth.get_all_channels()
                        
                        if not error and channels:
                            self.log_message(f"✓ Loaded: {active_account['name']} • {len(channels)} channel(s)")
                            
                            # Update UI in main thread
                            self.after(0, lambda: self.update_auth_ui_after_load(active_account['name'], channels))
                        else:
                            self.log_message(f"⚠ Account loaded but no channels: {error or 'Unknown error'}")
                            self.after(0, lambda: self.lbl_auth_status.configure(
                                text=f"⚠ {active_account['name']} (No Channels)",
                                text_color=get_adaptive_warning_color(self.is_dark_mode)
                            ))
                    else:
                        self.log_message(f"✗ Could not load account: {active_account['name']}")
                        self.log_message("  Try selecting it manually or re-authenticating.")
                        
                except Exception as e:
                    self.log_message(f"✗ Auto-load error: {str(e)}")
                    import traceback
                    self.log_message(traceback.format_exc())
            
            threading.Thread(target=load_thread, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"✗ Auto-load initialization error: {str(e)}")
    
    def update_auth_ui_after_load(self, account_name, channels):
        """Update UI after successful account load"""
        try:
            self.lbl_auth_status.configure(
                text=f"✓ Logged in as: {account_name}",
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            
            channel_names = [f"{ch['title']} ({ch['id']})" for ch in channels]
            self.channel_selector.configure(values=channel_names, state="normal")
            self.channel_selector.set(channel_names[0])
            self.update_channel_info_display(channels[0])
            self.btn_logout.configure(state="normal")
            self.refresh_account_list()
        except Exception as e:
            self.log_message(f"✗ UI update error: {str(e)}")
    
    def do_login(self):
        if not self.client_secret_path:
            messagebox.showerror("Error", "Please select client_secret.json first")
            return
        
        # Ask for account name
        from tkinter import simpledialog
        account_name = simpledialog.askstring(
            "Account Name",
            "Enter a name for this account\n(e.g., 'My Channel', 'Work Account'):",
            parent=self
        )
        
        if not account_name:
            return
        
        def login_thread():
            try:
                self.log_message("Starting OAuth2 authentication for new account...")
                success = self.auth.authenticate(self.client_secret_path, account_name=account_name, force_new=True)
                
                if success:
                    self.youtube_service = YouTubeService(self.auth.youtube, self.auth)
                    self.video_upload_tab.initialize_uploader(self.youtube_service)
                    self.log_message("Fetching all channels (owned + managed)...")
                    channels, error = self.auth.get_all_channels()
                    
                    if error:
                        # Authentication succeeded but channel fetch failed
                        self.log_message(f"✗ {error}")
                        self.lbl_auth_status.configure(text="⚠ Authenticated (No Channels)", 
                                                      text_color=get_adaptive_warning_color(self.is_dark_mode))
                        messagebox.showerror("Channel Error", 
                            f"Authentication successful, but could not load channels:\n\n{error}\n\n"
                            "Possible solutions:\n"
                            "1. Make sure your Google account has a YouTube channel\n"
                            "2. Create a channel at youtube.com if you don't have one\n"
                            "3. Check that you granted all permissions during login\n"
                            "4. Try logging out and logging in again")
                        self.btn_logout.configure(state="normal")
                        return
                    
                    self.log_message(f"Found {len(channels)} channel(s) total")
                    
                    account_info = self.auth.get_current_account_info()
                    display_name = account_info['name'] if account_info else "Unknown"
                    
                    self.lbl_auth_status.configure(
                        text=f"✓ Logged in as: {display_name}",
                        text_color=get_adaptive_success_color(self.is_dark_mode)
                    )
                    
                    if channels:
                        channel_names = [f"{ch['title']} ({ch['id']})" for ch in channels]
                        self.channel_selector.configure(values=channel_names, state="normal")
                        self.channel_selector.set(channel_names[0])
                        
                        self.update_channel_info_display(channels[0])
                    
                    self.btn_logout.configure(state="normal")
                    self.refresh_account_list()
                    
                    self.log_message(f"✓ Account added: {display_name} - {len(channels)} channel(s)")
                    messagebox.showinfo("Success", 
                        f"Account added successfully!\n\n"
                        f"Name: {display_name}\n"
                        f"Channels: {len(channels)}\n\n"
                        f"You can now switch between accounts anytime!")
                else:
                    self.log_message("✗ Authentication failed")
                    messagebox.showerror("Error", "Authentication failed")
            except Exception as e:
                self.log_message(f"✗ Error: {str(e)}")
                messagebox.showerror("Error", f"Authentication error: {str(e)}")
        
        threading.Thread(target=login_thread, daemon=True).start()
    
    def do_logout(self):
        current_account = self.auth.get_current_account_info()
        account_name = current_account['name'] if current_account else "current account"
        
        result = messagebox.askyesno(
            "Confirm Logout", 
            f"Logout from: {account_name}?\n\n"
            "This will end the current session but keep the account saved.\n"
            "You can switch back to it anytime without re-authenticating."
        )
        
        if not result:
            return
        
        try:
            # Just clear current session, don't delete the account
            self.auth.credentials = None
            self.auth.youtube = None
            self.auth.selected_channel_id = None
            self.auth.all_channels = []
            self.youtube_service = None
            
            self.lbl_auth_status.configure(text="Not authenticated", 
                                          text_color=get_adaptive_error_color(self.is_dark_mode))
            self.channel_selector.configure(values=["No channels available"], state="disabled")
            self.channel_selector.set("No channels available")
            
            self.text_channel_info.configure(state="normal")
            self.text_channel_info.delete("1.0", "end")
            self.text_channel_info.configure(state="disabled")
            
            self.btn_logout.configure(state="disabled")
            self.refresh_account_list()
            
            self.log_message(f"✓ Logged out from {account_name}")
            messagebox.showinfo("Success", 
                f"Logged out from: {account_name}\n\n"
                "The account is still saved. Use 'Select Account' to switch back anytime!")
        except Exception as e:
            self.log_message(f"✗ Logout error: {str(e)}")
            messagebox.showerror("Error", f"Logout error: {str(e)}")
    
    def on_channel_selected(self, choice):
        selected_text = choice
        channel_id = selected_text.split('(')[-1].rstrip(')')
        
        self.auth.set_selected_channel(channel_id)
        
        for channel in self.auth.all_channels:
            if channel['id'] == channel_id:
                self.update_channel_info_display(channel)
                self.log_message(f"Channel selected: {channel['title']} ({channel_id})")
                break
    
    def update_channel_info_display(self, channel):
        info_text = f"Channel: {channel['title']}\n"
        info_text += f"Channel ID: {channel['id']}\n"
        info_text += f"Subscribers: {channel['subscribers']}\n"
        if channel.get('customUrl') and channel['customUrl'] != 'N/A':
            info_text += f"Custom URL: {channel['customUrl']}"
        
        self.text_channel_info.configure(state="normal")
        self.text_channel_info.delete("1.0", "end")
        self.text_channel_info.insert("1.0", info_text)
        self.text_channel_info.configure(state="disabled")
    
    def setup_quick_tab(self):
        frame = ctk.CTkFrame(self.tab_quick)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="⚡ Quick Create Broadcast (Real-Time)", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        form_frame = ctk.CTkFrame(frame)
        form_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(form_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.quick_title = ctk.CTkEntry(form_frame, width=400)
        self.quick_title.grid(row=0, column=1, padx=10, pady=5)
        self.quick_title.insert(0, "Live Stream")
        
        ctk.CTkLabel(form_frame, text="Description:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.quick_description = ctk.CTkTextbox(form_frame, width=400, height=80)
        self.quick_description.grid(row=1, column=1, padx=10, pady=5)
        self.quick_description.insert("1.0", "Live streaming via YouTube API")
        
        ctk.CTkLabel(form_frame, text="Tags (comma-separated):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.quick_tags = ctk.CTkEntry(form_frame, width=400)
        self.quick_tags.grid(row=2, column=1, padx=10, pady=5)
        self.quick_tags.insert(0, "live,stream")
        
        ctk.CTkLabel(form_frame, text="Category ID:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.quick_category = ctk.CTkEntry(form_frame, width=400)
        self.quick_category.grid(row=3, column=1, padx=10, pady=5)
        self.quick_category.insert(0, "20")
        
        ctk.CTkLabel(form_frame, text="Privacy Status:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.quick_privacy = ctk.CTkComboBox(form_frame, values=["public", "unlisted", "private"], width=400)
        self.quick_privacy.grid(row=4, column=1, padx=10, pady=5)
        self.quick_privacy.set("public")
        
        ctk.CTkLabel(form_frame, text="Time Offset:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.quick_offset = ctk.CTkComboBox(
            form_frame, 
            values=["Now", "+15 minutes", "+30 minutes", "+1 hour", "+2 hours", "+6 hours", "+12 hours", "+1 day", "+2 days", "+7 days"],
            width=400,
            command=self.update_quick_datetime
        )
        self.quick_offset.grid(row=5, column=1, padx=10, pady=5)
        self.quick_offset.set("+30 minutes")
        
        ctk.CTkLabel(form_frame, text="Set Specific Time (24h):").grid(row=5, column=2, sticky="w", padx=10, pady=5)
        self.quick_specific_time = ctk.CTkEntry(form_frame, width=80, placeholder_text="HH:MM")
        self.quick_specific_time.grid(row=5, column=3, padx=10, pady=5)
        self.quick_specific_time.insert(0, "")  # Empty = use current time
        
        ctk.CTkLabel(form_frame, text="Scheduled Date:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.quick_date = ctk.CTkEntry(form_frame, width=400)
        self.quick_date.grid(row=6, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Scheduled Time:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.quick_time = ctk.CTkEntry(form_frame, width=400)
        self.quick_time.grid(row=7, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Thumbnail:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        thumbnail_frame = ctk.CTkFrame(form_frame)
        thumbnail_frame.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkButton(thumbnail_frame, text="Select Image", command=self.select_quick_thumbnail, width=120).pack(side="left", padx=5)
        self.lbl_quick_thumbnail = ctk.CTkLabel(thumbnail_frame, text="No thumbnail selected", 
                                               text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_quick_thumbnail.pack(side="left", padx=5)
        
        self.quick_thumbnail_path = None
        
        options_frame = ctk.CTkFrame(form_frame)
        options_frame.grid(row=9, column=0, columnspan=2, pady=10)
        
        self.quick_made_for_kids = ctk.CTkCheckBox(options_frame, text="Made for Kids")
        self.quick_made_for_kids.pack(side="left", padx=10)
        
        self.quick_synthetic_media = ctk.CTkCheckBox(options_frame, text="Contains Synthetic Media (AI/Modified)")
        self.quick_synthetic_media.pack(side="left", padx=10)
        
        self.quick_enable_dvr = ctk.CTkCheckBox(options_frame, text="Enable DVR")
        self.quick_enable_dvr.pack(side="left", padx=10)
        self.quick_enable_dvr.select()
        
        self.quick_enable_monetization = ctk.CTkCheckBox(options_frame, text="Enable Monetization", fg_color="green")
        self.quick_enable_monetization.pack(side="left", padx=10)
        self.quick_enable_monetization.select()
        
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="🔄 Update Time to Now", command=self.update_quick_datetime).pack(side="left", padx=5)
        self.btn_quick_create = ctk.CTkButton(btn_frame, text="✨ Create Broadcast", command=self.quick_create_broadcast)
        self.btn_quick_create.pack(side="left", padx=5)
        
        self.lbl_quick_status = ctk.CTkLabel(frame, text="")
        self.lbl_quick_status.pack(pady=5)
        
        self.update_quick_datetime()
    
    def select_quick_thumbnail(self):
        file_path = filedialog.askopenfilename(
            title="Select Thumbnail Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.quick_thumbnail_path = file_path
            import os
            filename = os.path.basename(file_path)
            self.lbl_quick_thumbnail.configure(text=f"✓ {filename}", 
                                              text_color=get_adaptive_success_color(self.is_dark_mode))
        else:
            self.quick_thumbnail_path = None
            self.lbl_quick_thumbnail.configure(text="No thumbnail selected", 
                                              text_color=get_adaptive_gray_color(self.is_dark_mode))
    
    def update_quick_datetime(self, choice=None):
        offset_map = {
            "Now": timedelta(0),
            "+15 minutes": timedelta(minutes=15),
            "+30 minutes": timedelta(minutes=30),
            "+1 hour": timedelta(hours=1),
            "+2 hours": timedelta(hours=2),
            "+6 hours": timedelta(hours=6),
            "+12 hours": timedelta(hours=12),
            "+1 day": timedelta(days=1),
            "+2 days": timedelta(days=2),
            "+7 days": timedelta(days=7)
        }
        
        offset = offset_map.get(self.quick_offset.get(), timedelta(minutes=30))
        
        # Check if specific time is provided
        specific_time_str = self.quick_specific_time.get().strip()
        
        if specific_time_str:
            # Use specific time
            try:
                time_parts = specific_time_str.split(':')
                if len(time_parts) == 2:
                    specific_hour = int(time_parts[0])
                    specific_minute = int(time_parts[1])
                    
                    if 0 <= specific_hour <= 23 and 0 <= specific_minute <= 59:
                        # Calculate target date
                        target_date = datetime.now().date() + timedelta(days=offset.days)
                        target_time = datetime.combine(target_date, datetime.min.time())
                        target_time = target_time.replace(hour=specific_hour, minute=specific_minute)
                        
                        self.quick_date.delete(0, "end")
                        self.quick_date.insert(0, target_time.strftime("%Y-%m-%d"))
                        
                        self.quick_time.delete(0, "end")
                        self.quick_time.insert(0, target_time.strftime("%H:%M"))
                        
                        self.lbl_quick_status.configure(
                            text=f"✓ Using custom time: {target_time.strftime('%Y-%m-%d %H:%M')} (24h format)", 
                            text_color=get_adaptive_success_color(self.is_dark_mode)
                        )
                        return
                    else:
                        self.lbl_quick_status.configure(
                            text="⚠ Invalid time! Use 00:00 to 23:59 format", 
                            text_color=get_adaptive_error_color(self.is_dark_mode)
                        )
                        return
            except (ValueError, IndexError):
                self.lbl_quick_status.configure(
                    text="⚠ Invalid time format! Use HH:MM (e.g., 05:00)", 
                    text_color=get_adaptive_error_color(self.is_dark_mode)
                )
                return
        
        # Default behavior: use current time + offset
        target_time = datetime.now() + offset
        
        self.quick_date.delete(0, "end")
        self.quick_date.insert(0, target_time.strftime("%Y-%m-%d"))
        
        self.quick_time.delete(0, "end")
        self.quick_time.insert(0, target_time.strftime("%H:%M"))
        
        self.lbl_quick_status.configure(text=f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                       text_color=get_adaptive_gray_color(self.is_dark_mode))
    
    def quick_create_broadcast(self):
        if not self.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.youtube_service:
            messagebox.showerror("Error", "YouTube service not initialized")
            return
        
        title = self.quick_title.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        
        description = self.quick_description.get("1.0", "end").strip()
        tags = [tag.strip() for tag in self.quick_tags.get().split(',') if tag.strip()]
        category_id = self.quick_category.get().strip()
        privacy = self.quick_privacy.get()
        
        scheduled_date = self.quick_date.get().strip()
        scheduled_time = self.quick_time.get().strip()
        
        try:
            dt = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%Y-%m-%d %H:%M")
            # Convert local time to UTC
            utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
            dt_utc = dt - timedelta(seconds=utc_offset_seconds)
            scheduled_start_time = dt_utc.isoformat() + 'Z'
        except:
            messagebox.showerror("Error", "Invalid date/time format")
            return
        
        broadcast_data = {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "privacyStatus": privacy,
            "scheduledStartTime": scheduled_start_time,
            "thumbnailPath": self.quick_thumbnail_path,
            "madeForKids": self.quick_made_for_kids.get() == 1,
            "containsSyntheticMedia": self.quick_synthetic_media.get() == 1,
            "enableDvr": self.quick_enable_dvr.get() == 1,
            "enableEmbed": True,
            "recordFromStart": True,
            "latency": "normal",
            "enableMonetization": self.quick_enable_monetization.get() == 1
        }
        
        def create_thread():
            self.btn_quick_create.configure(state="disabled")
            self.lbl_quick_status.configure(text="Creating broadcast...", 
                                           text_color=get_adaptive_warning_color(self.is_dark_mode))
            
            success, result = self.youtube_service.process_broadcast(
                broadcast_data,
                log_callback=self.log_message
            )
            
            if success:
                self.lbl_quick_status.configure(text=f"✓ Broadcast created successfully! ID: {result}", 
                                               text_color=get_adaptive_success_color(self.is_dark_mode))
                messagebox.showinfo("Success", f"Broadcast created successfully!\n\nBroadcast ID: {result}")
            else:
                self.lbl_quick_status.configure(text=f"✗ Failed to create broadcast", 
                                               text_color=get_adaptive_error_color(self.is_dark_mode))
                messagebox.showerror("Error", f"Failed to create broadcast:\n{result}")
            
            self.btn_quick_create.configure(state="normal")
        
        threading.Thread(target=create_thread, daemon=True).start()
    
    def setup_import_tab(self):
        # Main container with 2 columns
        main_container = ctk.CTkFrame(self.tab_import)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel (main content)
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Right panel (scheduler)
        right_panel = ctk.CTkFrame(main_container, width=380)
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # ========== LEFT PANEL CONTENT ==========
        ctk.CTkLabel(left_panel, text="📊 Import Excel & Process Broadcasts", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(left_panel)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_select_excel = ctk.CTkButton(
            btn_frame, text="Select Excel File", 
            command=self.select_excel_file
        )
        self.btn_select_excel.pack(side="left", padx=5)
        
        self.btn_process = ctk.CTkButton(
            btn_frame, text="Process Batch", 
            command=self.process_batch, state="disabled"
        )
        self.btn_process.pack(side="left", padx=5)
        
        self.lbl_excel_status = ctk.CTkLabel(left_panel, text="No file loaded", 
                                            text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_excel_status.pack(pady=5)
        
        datetime_frame = ctk.CTkFrame(left_panel)
        datetime_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(datetime_frame, text="⏰ Schedule Time (Applied to ALL broadcasts):").pack(anchor="w", padx=10, pady=5)
        
        # Specific Time Input (24h format)
        time_input_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        time_input_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(time_input_frame, text="🕐 Set Broadcast Time (24h format):", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=5)
        
        self.batch_specific_time = ctk.CTkEntry(time_input_frame, width=100, placeholder_text="HH:MM")
        self.batch_specific_time.pack(side="left", padx=5)
        self.batch_specific_time.insert(0, "05:00")  # Default: 05:00
        self.batch_specific_time.bind("<KeyRelease>", lambda e: self.update_batch_datetime())
        
        ctk.CTkLabel(time_input_frame, text="(e.g., 05:00 for 5 AM, 17:30 for 5:30 PM)",
                    font=ctk.CTkFont(size=9), 
                    text_color=get_adaptive_gray_color(self.is_dark_mode)).pack(side="left", padx=5)
        
        # Multiple Base Time Selection
        multitime_label_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        multitime_label_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(multitime_label_frame, text="📋 Select Days:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=5)
        ctk.CTkLabel(multitime_label_frame, text="(Select multiple days to schedule broadcasts)",
                    font=ctk.CTkFont(size=9), 
                    text_color=get_adaptive_gray_color(self.is_dark_mode)).pack(side="left", padx=5)
        
        # Create scrollable frame for multiple time checkboxes
        multitime_scroll = ctk.CTkScrollableFrame(datetime_frame, height=120, fg_color=("#F0F0F0", "#2C2C2C"))
        multitime_scroll.pack(fill="x", padx=10, pady=5)
        
        # Time options with checkboxes
        self.base_time_options = {}
        time_choices = ["Now", "+1 day", "+2 days", "+3 days", "+4 days", 
                       "+5 days", "+6 days", "+7 days"]
        
        # Default: Select all 7 days (not "Now")
        default_selected = ["+1 day", "+2 days", "+3 days", "+4 days", 
                           "+5 days", "+6 days", "+7 days"]
        
        for i, time_choice in enumerate(time_choices):
            row_frame = ctk.CTkFrame(multitime_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            var = ctk.BooleanVar(value=(time_choice in default_selected))
            checkbox = ctk.CTkCheckBox(
                row_frame, 
                text=time_choice,
                variable=var,
                width=150,
                command=self.update_batch_datetime
            )
            checkbox.pack(side="left", padx=5)
            
            # Add preview time label
            time_label = ctk.CTkLabel(
                row_frame, 
                text="",
                font=ctk.CTkFont(size=9),
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            )
            time_label.pack(side="left", padx=10)
            
            self.base_time_options[time_choice] = {"var": var, "label": time_label}
        
        # Interval and quick action buttons
        time_controls = ctk.CTkFrame(datetime_frame)
        time_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(time_controls, text="Interval:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=5)
        self.batch_interval = ctk.CTkComboBox(
            time_controls,
            values=["0 min (all same)", "+5 min", "+10 min", "+15 min", "+30 min", "+1 hour", "+2 hours", "+1 day"],
            width=150,
            command=self.update_batch_datetime
        )
        self.batch_interval.pack(side="left", padx=5)
        self.batch_interval.set("0 min (all same)")
        
        ctk.CTkButton(
            time_controls, 
            text="ℹ️ What is Interval?", 
            command=self.show_interval_explanation,
            width=120,
            height=28,
            fg_color=("#3498db", "#2980b9"),
            font=ctk.CTkFont(size=10)
        ).pack(side="left", padx=5)
        
        # Quick selection buttons
        quick_select_frame = ctk.CTkFrame(datetime_frame)
        quick_select_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            quick_select_frame, 
            text="✓ Select All", 
            command=lambda: self.toggle_all_times(True),
            width=100,
            height=25,
            fg_color="#2E7D32"
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            quick_select_frame, 
            text="✗ Deselect All", 
            command=lambda: self.toggle_all_times(False),
            width=100,
            height=25,
            fg_color="#DC143C"
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            quick_select_frame, 
            text="🔄 Refresh Preview", 
            command=self.update_batch_datetime,
            width=120,
            height=25
        ).pack(side="left", padx=3)
        
        # 30 Days Shortcut Checkbox
        days_30_frame = ctk.CTkFrame(datetime_frame, fg_color=("#E8F5E9", "#1B5E20"), corner_radius=8)
        days_30_frame.pack(fill="x", padx=10, pady=10)
        
        self.schedule_30_days = ctk.CTkCheckBox(
            days_30_frame,
            text="📅 Schedule 30 Days (Overrides individual day selection)",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.on_30_days_toggle
        )
        self.schedule_30_days.pack(padx=10, pady=8)
        
        self.lbl_batch_time_info = ctk.CTkLabel(datetime_frame, text="", 
                                               text_color=get_adaptive_gray_color(self.is_dark_mode))
        self.lbl_batch_time_info.pack(anchor="w", padx=10, pady=2)
        
        batch_options_frame = ctk.CTkFrame(left_panel)
        batch_options_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(batch_options_frame, text="⚙️ Global Options (Override Excel):").pack(anchor="w", padx=10, pady=5)
        
        options_row = ctk.CTkFrame(batch_options_frame)
        options_row.pack(fill="x", padx=10, pady=5)
        
        self.batch_force_monetization = ctk.CTkCheckBox(
            options_row, 
            text="Enable Monetization for ALL broadcasts (ignores Excel column)",
            command=self.on_batch_monetization_toggle
        )
        self.batch_force_monetization.pack(side="left", padx=10)
        
        self.lbl_monetization_status = ctk.CTkLabel(
            options_row, 
            text="", 
            text_color=get_adaptive_gray_color(self.is_dark_mode)
        )
        self.lbl_monetization_status.pack(side="left", padx=10)
        
        ctk.CTkLabel(left_panel, text="Preview (first 10 rows):").pack(pady=5)
        
        self.text_preview = ctk.CTkTextbox(left_panel, height=300)
        self.text_preview.pack(fill="both", expand=True, pady=10)
        
        # ========== RIGHT PANEL: AUTOMATIC SCHEDULING ==========
        scheduler_frame = ctk.CTkFrame(right_panel, fg_color=("#E3F2FD", "#1A237E"), corner_radius=10)
        scheduler_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(scheduler_frame, text="⏰ Automatic Daily\nScheduling", 
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(10,5))
        
        ctk.CTkLabel(scheduler_frame, text="Run batch processing\nautomatically every day",
                    font=ctk.CTkFont(size=10), wraplength=340).pack(pady=(0,10))
        
        # Time configuration
        config_frame = ctk.CTkFrame(scheduler_frame, fg_color="transparent")
        config_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(config_frame, text="Daily Run Time:", 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", pady=(5,2))
        
        time_input_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        time_input_frame.pack(fill="x", pady=5)
        
        self.scheduler_time = ctk.CTkEntry(time_input_frame, width=100, placeholder_text="09:00")
        self.scheduler_time.pack(side="left", padx=(0,5))
        self.scheduler_time.insert(0, "09:00")
        
        ctk.CTkLabel(time_input_frame, text="(HH:MM)", 
                    font=ctk.CTkFont(size=9),
                    text_color=get_adaptive_gray_color(self.is_dark_mode)).pack(side="left")
        
        # Control buttons
        button_frame = ctk.CTkFrame(scheduler_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_enable_scheduler = ctk.CTkButton(
            button_frame,
            text="▶ Enable Scheduler",
            command=self.toggle_scheduler,
            height=35,
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        self.btn_enable_scheduler.pack(fill="x", pady=2)
        
        ctk.CTkButton(
            button_frame,
            text="🔄 Update Time",
            command=self.update_scheduler_time,
            height=32
        ).pack(fill="x", pady=2)
        
        ctk.CTkButton(
            button_frame,
            text="❌ Cancel Schedule",
            command=self.cancel_scheduler,
            height=32,
            fg_color="#DC143C",
            hover_color="#B22222"
        ).pack(fill="x", pady=2)
        
        # Status display
        status_frame = ctk.CTkFrame(scheduler_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=10)
        
        self.lbl_scheduler_status = ctk.CTkLabel(
            status_frame,
            text="⚪ Scheduler: Disabled",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=get_adaptive_gray_color(self.is_dark_mode),
            wraplength=340
        )
        self.lbl_scheduler_status.pack(pady=2)
        
        self.lbl_scheduler_next_run = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=9),
            text_color=get_adaptive_gray_color(self.is_dark_mode),
            wraplength=340
        )
        self.lbl_scheduler_next_run.pack(pady=2)
        
        # Separator
        separator = ctk.CTkFrame(scheduler_frame, height=2, fg_color=get_adaptive_gray_color(self.is_dark_mode))
        separator.pack(fill="x", padx=20, pady=10)
        
        # Important notes
        notes_frame = ctk.CTkFrame(scheduler_frame, fg_color="transparent")
        notes_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        
        ctk.CTkLabel(notes_frame, text="📌 Important:",
                    font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(0,5))
        
        note_text = "• Uses currently loaded Excel file\n• Authentication required\n• Keep application running\n• Computer must stay awake"
        ctk.CTkLabel(notes_frame, text=note_text,
                    font=ctk.CTkFont(size=9),
                    justify="left",
                    text_color=get_adaptive_gray_color(self.is_dark_mode)).pack(anchor="w", padx=5)
        
        self.update_batch_datetime()
        
        # Load scheduler status on startup
        self.after(500, self.update_scheduler_status)
    
    def on_batch_monetization_toggle(self):
        if self.batch_force_monetization.get():
            self.lbl_monetization_status.configure(
                text="⚠ Monetization will be enabled for ALL broadcasts", 
                text_color=get_adaptive_warning_color(self.is_dark_mode)
            )
            self.log_message("[INFO] Global monetization enabled - will override Excel settings")
        else:
            self.lbl_monetization_status.configure(text="", 
                                                   text_color=get_adaptive_gray_color(self.is_dark_mode))
            self.log_message("[INFO] Global monetization disabled - using Excel settings")
    
    def toggle_all_times(self, select=True):
        """Select or deselect all base time checkboxes"""
        for time_choice, widgets in self.base_time_options.items():
            widgets["var"].set(select)
        self.update_batch_datetime()
    
    def on_30_days_toggle(self):
        """Handle 30 days checkbox toggle"""
        is_30_days_mode = self.schedule_30_days.get()
        
        if is_30_days_mode:
            # Disable individual checkboxes when 30 days mode is active
            for time_choice, widgets in self.base_time_options.items():
                widgets["var"].set(False)
            self.log_message("[INFO] 30 Days mode enabled - will schedule broadcasts for 30 consecutive days")
        else:
            # Re-enable individual selection
            self.log_message("[INFO] 30 Days mode disabled - using individual day selection")
        
        self.update_batch_datetime()
    
    def show_interval_explanation(self):
        """Show explanation about interval feature"""
        explanation = """
🕒 APA ITU INTERVAL?

Interval adalah jarak waktu antara setiap broadcast yang dijadwalkan.

CONTOH PENGGUNAAN:

1️⃣ "0 min (all same)" = Semua Broadcast di Waktu yang Sama
   • Base Time: +1 day (besok jam 10:00)
   • Interval: 0 min
   • Hasil: Semua 10 broadcast dijadwalkan besok jam 10:00

2️⃣ "+15 min" = Jarak 15 Menit Antar Broadcast
   • Base Time: +1 day (besok jam 10:00)
   • Interval: +15 min
   • Hasil: 
     - Broadcast 1: Besok 10:00
     - Broadcast 2: Besok 10:15
     - Broadcast 3: Besok 10:30
     - Broadcast 4: Besok 10:45, dst...

3️⃣ "+1 hour" = Jarak 1 Jam Antar Broadcast
   • Base Time: +1 day (besok jam 10:00)
   • Interval: +1 hour
   • Hasil:
     - Broadcast 1: Besok 10:00
     - Broadcast 2: Besok 11:00
     - Broadcast 3: Besok 12:00, dst...

4️⃣ "+1 day" = Jarak 1 Hari Antar Broadcast
   • Base Time: +1 day (besok jam 10:00)
   • Interval: +1 day
   • Hasil:
     - Broadcast 1: Besok 10:00
     - Broadcast 2: Lusa 10:00
     - Broadcast 3: 3 hari lagi 10:00, dst...

📋 MULTIPLE BASE TIMES (DEFAULT):
Secara default, 7 hari sudah tercentang!
Sistem akan membuat batch terpisah untuk setiap hari.

Contoh: 7 hari tercentang, interval "0 min", 1 row Excel
• Batch 1: Besok jam 10:00
• Batch 2: Lusa jam 10:00
• Batch 3-7: 3-7 hari lagi, masing-masing jam 10:00
→ Total: 7 broadcasts, satu per hari!
        """
        messagebox.showinfo("Penjelasan Interval", explanation)
    
    def update_batch_datetime(self, choice=None):
        """Update preview for all selected base times"""
        offset_map = {
            "Now": timedelta(0),
            "+1 day": timedelta(days=1),
            "+2 days": timedelta(days=2),
            "+3 days": timedelta(days=3),
            "+4 days": timedelta(days=4),
            "+5 days": timedelta(days=5),
            "+6 days": timedelta(days=6),
            "+7 days": timedelta(days=7)
        }
        
        # Get specific time from input (24h format HH:MM)
        specific_time_str = self.batch_specific_time.get().strip()
        use_specific_time = False
        specific_hour = 0
        specific_minute = 0
        
        if specific_time_str:
            try:
                # Parse HH:MM format
                time_parts = specific_time_str.split(':')
                if len(time_parts) == 2:
                    specific_hour = int(time_parts[0])
                    specific_minute = int(time_parts[1])
                    
                    # Validate time
                    if 0 <= specific_hour <= 23 and 0 <= specific_minute <= 59:
                        use_specific_time = True
                    else:
                        self.lbl_batch_time_info.configure(
                            text="⚠️ Invalid time! Use 00:00 to 23:59 format",
                            text_color=get_adaptive_error_color(self.is_dark_mode)
                        )
                        return
            except (ValueError, IndexError):
                self.lbl_batch_time_info.configure(
                    text="⚠️ Invalid time format! Use HH:MM (e.g., 05:00)",
                    text_color=get_adaptive_error_color(self.is_dark_mode)
                )
                return
        
        # Check if 30 days mode is enabled
        is_30_days_mode = self.schedule_30_days.get()
        
        # Update preview for each time option
        selected_times = []
        
        if is_30_days_mode:
            # Generate 30 consecutive days
            for day_num in range(1, 31):
                if use_specific_time:
                    base_date = datetime.now().date() + timedelta(days=day_num)
                    target_time = datetime.combine(base_date, datetime.min.time())
                    target_time = target_time.replace(hour=specific_hour, minute=specific_minute)
                else:
                    target_time = datetime.now() + timedelta(days=day_num)
                
                selected_times.append((f"+{day_num} day{'s' if day_num > 1 else ''}", target_time))
            
            # Update individual checkbox previews (for display only)
            for time_choice, widgets in self.base_time_options.items():
                offset = offset_map.get(time_choice, timedelta(minutes=30))
                
                if use_specific_time:
                    base_date = datetime.now().date() + offset.days * timedelta(days=1)
                    target_time = datetime.combine(base_date, datetime.min.time())
                    target_time = target_time.replace(hour=specific_hour, minute=specific_minute)
                else:
                    target_time = datetime.now() + offset
                
                preview_text = f"→ {target_time.strftime('%Y-%m-%d %H:%M')}"
                widgets["label"].configure(text=preview_text)
        else:
            # Normal mode: use individual checkbox selection
            for time_choice, widgets in self.base_time_options.items():
                offset = offset_map.get(time_choice, timedelta(minutes=30))
                
                if use_specific_time:
                    # Use specific time set by user
                    base_date = datetime.now().date() + offset.days * timedelta(days=1)
                    target_time = datetime.combine(base_date, datetime.min.time())
                    target_time = target_time.replace(hour=specific_hour, minute=specific_minute)
                else:
                    # Use current time + offset (original behavior)
                    target_time = datetime.now() + offset
                
                # Update preview label
                preview_text = f"→ {target_time.strftime('%Y-%m-%d %H:%M')}"
                widgets["label"].configure(text=preview_text)
                
                # Track selected times
                if widgets["var"].get():
                    selected_times.append((time_choice, target_time))
        
        # Update info label
        interval_str = self.batch_interval.get()
        
        if is_30_days_mode:
            # Special info for 30 days mode
            first_time = selected_times[0][1]
            last_time = selected_times[-1][1]
            if use_specific_time:
                info_text = f"📅 30 DAYS MODE: Scheduling from {first_time.strftime('%Y-%m-%d')} to {last_time.strftime('%Y-%m-%d')} at {specific_time_str}\n"
            else:
                info_text = f"📅 30 DAYS MODE: Scheduling 30 consecutive days starting {first_time.strftime('%Y-%m-%d %H:%M')}\n"
            info_text += f"    Interval: {interval_str} between each broadcast"
        elif not selected_times:
            info_text = "⚠️ Please select at least one day or enable 30 Days mode!"
        elif len(selected_times) == 1:
            time_choice, target_time = selected_times[0]
            if "all same" in interval_str:
                if use_specific_time:
                    info_text = f"All broadcasts will be scheduled at: {target_time.strftime('%Y-%m-%d %H:%M')} (Custom Time)"
                else:
                    info_text = f"All broadcasts will be scheduled at: {target_time.strftime('%Y-%m-%d %H:%M')}"
            else:
                info_text = f"Start time: {target_time.strftime('%Y-%m-%d %H:%M')}, with {interval_str} interval"
        else:
            if use_specific_time:
                info_text = f"📋 {len(selected_times)} days selected at {specific_time_str} (Custom Time), each with {interval_str} interval\n"
            else:
                info_text = f"📋 {len(selected_times)} different start times selected, each with {interval_str} interval\n"
            info_text += "    Times: " + ", ".join([t.strftime('%Y-%m-%d %H:%M') for _, t in selected_times[:3]])
            if len(selected_times) > 3:
                info_text += f" ... (+{len(selected_times) - 3} more)"
        
        self.lbl_batch_time_info.configure(
            text=info_text,
            text_color=get_adaptive_text_color(self.is_dark_mode)
        )
    
    def select_excel_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            success, message = self.parser.load_excel(file_path)
            
            if success:
                self.lbl_excel_status.configure(text=f"✓ {message}", 
                                               text_color=get_adaptive_success_color(self.is_dark_mode))
                self.btn_process.configure(state="normal" if self.auth.is_authenticated() else "disabled")
                
                preview_df = self.parser.get_preview(10)
                
                cols_to_show = ['title', 'description', 'tags', 'categoryId', 'privacyStatus', 
                               'madeForKids', 'containsSyntheticMedia', 'enableDvr', 
                               'enableMonetization', 'latency']
                
                available_cols = [col for col in cols_to_show if col in preview_df.columns]
                preview_limited = preview_df[available_cols]
                
                preview_text = "=" * 100 + "\n"
                preview_text += "PREVIEW - First 10 Rows\n"
                preview_text += "=" * 100 + "\n\n"
                
                for idx, row in preview_limited.iterrows():
                    preview_text += f"Row {idx + 1}:\n"
                    preview_text += "-" * 80 + "\n"
                    for col in available_cols:
                        value = row[col]
                        if col == 'title':
                            preview_text += f"  {col:25s}: {value}\n"
                        elif col == 'description':
                            desc_short = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
                            preview_text += f"  {col:25s}: {desc_short}\n"
                        elif col == 'tags':
                            preview_text += f"  {col:25s}: {value}\n"
                        else:
                            preview_text += f"  {col:25s}: {value}\n"
                    preview_text += "\n"
                
                self.text_preview.delete("1.0", "end")
                self.text_preview.insert("1.0", preview_text)
                
                self.log_message(f"Excel loaded: {message}")
            else:
                self.lbl_excel_status.configure(text=f"✗ {message}", 
                                               text_color=get_adaptive_error_color(self.is_dark_mode))
                messagebox.showerror("Error", message)
                self.log_message(f"Excel load error: {message}")
    
    def process_batch(self):
        if not self.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.youtube_service:
            messagebox.showerror("Error", "YouTube service not initialized")
            return
        
        rows = self.parser.get_all_rows()
        if not rows:
            messagebox.showerror("Error", "No data to process")
            return
        
        # Get selected base times
        offset_map = {
            "Now": timedelta(0),
            "+1 day": timedelta(days=1),
            "+2 days": timedelta(days=2),
            "+3 days": timedelta(days=3),
            "+4 days": timedelta(days=4),
            "+5 days": timedelta(days=5),
            "+6 days": timedelta(days=6),
            "+7 days": timedelta(days=7)
        }
        
        # Get specific time from input (24h format HH:MM)
        specific_time_str = self.batch_specific_time.get().strip()
        use_specific_time = False
        specific_hour = 0
        specific_minute = 0
        
        if specific_time_str:
            try:
                # Parse HH:MM format
                time_parts = specific_time_str.split(':')
                if len(time_parts) == 2:
                    specific_hour = int(time_parts[0])
                    specific_minute = int(time_parts[1])
                    
                    # Validate time
                    if 0 <= specific_hour <= 23 and 0 <= specific_minute <= 59:
                        use_specific_time = True
                    else:
                        messagebox.showerror("Error", "Invalid time! Use 00:00 to 23:59 format")
                        return
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Invalid time format! Use HH:MM (e.g., 05:00)")
                return
        
        # Check if 30 days mode is enabled
        is_30_days_mode = self.schedule_30_days.get()
        
        selected_base_times = []
        
        if is_30_days_mode:
            # Generate 30 consecutive days
            for day_num in range(1, 31):
                if use_specific_time:
                    base_date = datetime.now().date() + timedelta(days=day_num)
                    base_dt = datetime.combine(base_date, datetime.min.time())
                    base_dt = base_dt.replace(hour=specific_hour, minute=specific_minute)
                else:
                    base_dt = datetime.now() + timedelta(days=day_num)
                
                selected_base_times.append((f"+{day_num} day{'s' if day_num > 1 else ''}", base_dt))
        else:
            # Normal mode: use individual checkbox selection
            for time_choice, widgets in self.base_time_options.items():
                if widgets["var"].get():
                    offset = offset_map.get(time_choice, timedelta(days=1))
                    
                    if use_specific_time:
                        # Use specific time set by user
                        base_date = datetime.now().date() + offset.days * timedelta(days=1)
                        base_dt = datetime.combine(base_date, datetime.min.time())
                        base_dt = base_dt.replace(hour=specific_hour, minute=specific_minute)
                    else:
                        # Use current time + offset (original behavior)
                        base_dt = datetime.now() + offset
                    
                    selected_base_times.append((time_choice, base_dt))
        
        if not selected_base_times:
            messagebox.showerror("Error", "Please select at least one day or enable 30 Days mode!")
            return
        
        interval_map = {
            "0 min (all same)": timedelta(0),
            "+5 min": timedelta(minutes=5),
            "+10 min": timedelta(minutes=10),
            "+15 min": timedelta(minutes=15),
            "+30 min": timedelta(minutes=30),
            "+1 hour": timedelta(hours=1),
            "+2 hours": timedelta(hours=2),
            "+1 day": timedelta(days=1)
        }
        
        interval = interval_map.get(self.batch_interval.get(), timedelta(0))
        force_monetization = self.batch_force_monetization.get()
        
        def process_thread():
            self.btn_process.configure(state="disabled")
            
            if force_monetization:
                self.log_message(f"\n{'='*50}\n[MONETIZATION] Global monetization is ENABLED - All broadcasts will have monetization turned ON\n{'='*50}\n")
            
            self.log_message(f"\n{'='*60}")
            if is_30_days_mode:
                self.log_message(f"STARTING 30 DAYS BATCH PROCESS")
                self.log_message(f"{'='*60}")
                self.log_message(f"Mode: 📅 30 CONSECUTIVE DAYS")
            else:
                self.log_message(f"STARTING MULTI-TIME BATCH PROCESS")
                self.log_message(f"{'='*60}")
            self.log_message(f"Total broadcasts per batch: {len(rows)}")
            self.log_message(f"Number of days/batches: {len(selected_base_times)}")
            self.log_message(f"Interval between broadcasts: {self.batch_interval.get()}")
            if use_specific_time:
                self.log_message(f"Custom time: {specific_time_str} (24h format)")
            self.log_message(f"{'='*60}\n")
            
            total_success = 0
            total_errors = 0
            
            # Process for each selected base time
            for batch_idx, (time_choice, base_dt) in enumerate(selected_base_times, 1):
                self.log_message(f"\n{'='*60}")
                self.log_message(f"📋 BATCH {batch_idx}/{len(selected_base_times)}: {time_choice}")
                self.log_message(f"Start time: {base_dt.strftime('%Y-%m-%d %H:%M')}")
                self.log_message(f"{'='*60}\n")
                
                success_count = 0
                error_count = 0
                
                for idx, row_data in enumerate(rows):
                    # Create a copy to avoid modifying original
                    row_copy = row_data.copy()
                    
                    if "error" in row_copy:
                        self.log_message(f"[X] Skipped: {row_copy['error']}")
                        error_count += 1
                        continue
                    
                    # Calculate broadcast time for this base time
                    if not row_copy.get("scheduledStartTime"):
                        broadcast_time = base_dt + (interval * idx)
                        # Convert local time to UTC
                        utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                        broadcast_time_utc = broadcast_time - timedelta(seconds=utc_offset_seconds)
                        row_copy["scheduledStartTime"] = broadcast_time_utc.isoformat() + 'Z'
                        self.log_message(f"[{idx+1}] Scheduled for: {broadcast_time.strftime('%Y-%m-%d %H:%M')} (Local) - {row_copy.get('title', 'No title')[:50]}")
                    
                    # Apply global monetization override
                    if force_monetization:
                        row_copy["enableMonetization"] = True
                    
                    success, result = self.youtube_service.process_broadcast(
                        row_copy, 
                        log_callback=self.log_message
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        self.log_message(f"[X] Error detail: {result}\n")
                
                self.log_message(f"\n{'='*60}")
                self.log_message(f"Batch {batch_idx} ({time_choice}) Complete!")
                self.log_message(f"[OK] Success: {success_count} | [X] Errors: {error_count}")
                self.log_message(f"{'='*60}\n")
                
                total_success += success_count
                total_errors += error_count
            
            # Final summary
            self.log_message(f"\n{'='*60}")
            self.log_message(f"🎉 ALL BATCHES COMPLETE!")
            self.log_message(f"{'='*60}")
            self.log_message(f"Total batches processed: {len(selected_base_times)}")
            self.log_message(f"Total broadcasts created: {total_success}")
            self.log_message(f"Total errors: {total_errors}")
            self.log_message(f"{'='*60}\n")
            
            self.btn_process.configure(state="normal")
            
            summary = f"Multi-Time Batch Processing Complete!\n\n"
            summary += f"Batches: {len(selected_base_times)}\n"
            summary += f"Total Success: {total_success}\n"
            summary += f"Total Errors: {total_errors}"
            
            messagebox.showinfo("Complete", summary)
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def toggle_scheduler(self):
        """Toggle the automatic scheduler on/off"""
        if not self.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        if not self.parser.get_all_rows():
            messagebox.showerror("Error", "Please load an Excel file first")
            return
        
        if self.batch_scheduler.is_running:
            # Stop scheduler
            if self.batch_scheduler.stop_scheduler():
                self.batch_scheduler.enabled = False
                self.batch_scheduler.save_schedule()
                self.update_scheduler_status()
                messagebox.showinfo("Scheduler Stopped", "Automatic scheduling has been disabled")
        else:
            # Start scheduler
            time_str = self.scheduler_time.get().strip()
            
            # Get current Excel file path
            excel_path = getattr(self.parser, 'file_path', None)
            if not excel_path:
                messagebox.showerror("Error", "Excel file path not found. Please reload the file.")
                return
            
            # Configure and save schedule
            if self.batch_scheduler.set_schedule(time_str, excel_path, enabled=True):
                # Start the scheduler with the batch processing callback
                if self.batch_scheduler.start_scheduler(self.scheduled_process_batch):
                    self.update_scheduler_status()
                    next_run = self.batch_scheduler.get_next_run_time()
                    messagebox.showinfo("Scheduler Started", 
                        f"Automatic scheduling enabled!\n\n"
                        f"Daily run time: {time_str}\n"
                        f"Next run: {next_run if next_run else 'Calculating...'}\n\n"
                        f"Keep this application running for the scheduler to work.")
                else:
                    messagebox.showerror("Error", "Failed to start scheduler")
            else:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM (e.g., 09:00)")
    
    def update_scheduler_time(self):
        """Update the scheduled time without enabling/disabling"""
        time_str = self.scheduler_time.get().strip()
        
        # Get current Excel file path
        excel_path = getattr(self.parser, 'file_path', None)
        if not excel_path:
            messagebox.showwarning("Warning", "No Excel file loaded. Time will be saved but scheduler won't start until you load a file.")
            excel_path = self.batch_scheduler.excel_file_path or ""
        
        current_enabled = self.batch_scheduler.enabled
        
        if self.batch_scheduler.set_schedule(time_str, excel_path, current_enabled):
            # If scheduler was running, restart it with new time
            if self.batch_scheduler.is_running:
                self.batch_scheduler.stop_scheduler()
                self.batch_scheduler.start_scheduler(self.scheduled_process_batch)
            
            self.update_scheduler_status()
            messagebox.showinfo("Time Updated", f"Scheduled time updated to: {time_str}")
        else:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM (e.g., 09:00)")
    
    def cancel_scheduler(self):
        """Cancel/disable the automatic scheduler"""
        if not self.batch_scheduler.enabled and not self.batch_scheduler.is_running:
            messagebox.showinfo("No Schedule", "No active schedule to cancel.")
            return
        
        result = messagebox.askyesno(
            "Cancel Schedule",
            "This will disable the automatic daily scheduling.\n\n"
            "You can enable it again anytime by clicking 'Enable Scheduler'.\n\n"
            "Cancel the schedule?",
            icon='warning'
        )
        
        if result:
            # Stop scheduler if running
            if self.batch_scheduler.is_running:
                self.batch_scheduler.stop_scheduler()
            
            # Disable schedule
            excel_path = self.batch_scheduler.excel_file_path or ""
            time_str = self.batch_scheduler.scheduled_time
            self.batch_scheduler.set_schedule(time_str, excel_path, enabled=False)
            
            self.update_scheduler_status()
            self.log_message("[SCHEDULER] Schedule cancelled and disabled")
            messagebox.showinfo("Schedule Cancelled", "Automatic daily scheduling has been disabled.")
    
    def update_scheduler_status(self):
        """Update the scheduler status display"""
        status = self.batch_scheduler.get_status()
        
        # Load saved time into input field
        if status['scheduled_time']:
            self.scheduler_time.delete(0, "end")
            self.scheduler_time.insert(0, status['scheduled_time'])
        
        if status['running']:
            self.lbl_scheduler_status.configure(
                text="🟢 Scheduler: Active",
                text_color=get_adaptive_success_color(self.is_dark_mode)
            )
            self.btn_enable_scheduler.configure(
                text="⏸ Disable Scheduler",
                fg_color="#DC143C",
                hover_color="#B22222"
            )
            
            next_run = status['next_run']
            if next_run:
                self.lbl_scheduler_next_run.configure(
                    text=f"Next scheduled run: {next_run}",
                    text_color=get_adaptive_success_color(self.is_dark_mode)
                )
            else:
                self.lbl_scheduler_next_run.configure(text="")
        elif status['enabled']:
            self.lbl_scheduler_status.configure(
                text="🟡 Scheduler: Configured (Not Running)",
                text_color=get_adaptive_warning_color(self.is_dark_mode)
            )
            self.btn_enable_scheduler.configure(
                text="▶ Enable Scheduler",
                fg_color="#2E7D32",
                hover_color="#1B5E20"
            )
            self.lbl_scheduler_next_run.configure(
                text="Click 'Enable Scheduler' to start automatic processing",
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            )
        else:
            self.lbl_scheduler_status.configure(
                text="⚪ Scheduler: Disabled",
                text_color=get_adaptive_gray_color(self.is_dark_mode)
            )
            self.btn_enable_scheduler.configure(
                text="▶ Enable Scheduler",
                fg_color="#2E7D32",
                hover_color="#1B5E20"
            )
            self.lbl_scheduler_next_run.configure(text="")
        
        # Schedule next status update in 60 seconds if running
        if status['running']:
            self.after(60000, self.update_scheduler_status)
    
    def scheduled_process_batch(self):
        """Wrapper for process_batch to be called by scheduler"""
        # Reload Excel file to get latest data
        excel_path = self.batch_scheduler.excel_file_path
        if excel_path:
            success, message = self.parser.load_excel(excel_path)
            if not success:
                self.log_message(f"✗ Failed to reload Excel file: {message}")
                return
            self.log_message(f"✓ Excel file reloaded: {message}")
        
        # Call the regular process_batch in the main thread
        self.after(0, self._process_batch_internal)
    
    def _process_batch_internal(self):
        """Internal method for batch processing (for scheduler)"""
        rows = self.parser.get_all_rows()
        if not rows:
            self.log_message("✗ No data to process")
            return
        
        # Get selected base times
        offset_map = {
            "Now": timedelta(0),
            "+1 day": timedelta(days=1),
            "+2 days": timedelta(days=2),
            "+3 days": timedelta(days=3),
            "+4 days": timedelta(days=4),
            "+5 days": timedelta(days=5),
            "+6 days": timedelta(days=6),
            "+7 days": timedelta(days=7)
        }
        
        selected_base_times = []
        for time_choice, widgets in self.base_time_options.items():
            if widgets["var"].get():
                offset = offset_map.get(time_choice, timedelta(days=1))
                base_dt = datetime.now() + offset
                selected_base_times.append((time_choice, base_dt))
        
        # If no time selected, use default (7 days)
        if not selected_base_times:
            self.log_message(f"⚠ No base time selected, using default: 7 days")
            for day in range(1, 8):
                base_dt = datetime.now() + timedelta(days=day)
                selected_base_times.append((f"+{day} day(s) (default)", base_dt))
        
        interval_map = {
            "0 min (all same)": timedelta(0),
            "+5 min": timedelta(minutes=5),
            "+10 min": timedelta(minutes=10),
            "+15 min": timedelta(minutes=15),
            "+30 min": timedelta(minutes=30),
            "+1 hour": timedelta(hours=1),
            "+2 hours": timedelta(hours=2),
            "+1 day": timedelta(days=1)
        }
        
        interval = interval_map.get(self.batch_interval.get(), timedelta(0))
        force_monetization = self.batch_force_monetization.get()
        
        if force_monetization:
            self.log_message(f"\n{'='*50}\n[MONETIZATION] Global monetization is ENABLED\n{'='*50}\n")
        
        self.log_message(f"\n{'='*60}")
        self.log_message(f"SCHEDULED MULTI-TIME BATCH PROCESS")
        self.log_message(f"{'='*60}")
        self.log_message(f"Total broadcasts: {len(rows)}")
        self.log_message(f"Number of base times: {len(selected_base_times)}")
        self.log_message(f"Interval: {self.batch_interval.get()}")
        self.log_message(f"{'='*60}\n")
        
        total_success = 0
        total_errors = 0
        
        # Process for each selected base time
        for batch_idx, (time_choice, base_dt) in enumerate(selected_base_times, 1):
            self.log_message(f"\n{'='*60}")
            self.log_message(f"📋 BATCH {batch_idx}/{len(selected_base_times)}: {time_choice}")
            self.log_message(f"Start time: {base_dt.strftime('%Y-%m-%d %H:%M')}")
            self.log_message(f"{'='*60}\n")
            
            success_count = 0
            error_count = 0
            
            for idx, row_data in enumerate(rows):
                # Create a copy to avoid modifying original
                row_copy = row_data.copy()
                
                if "error" in row_copy:
                    self.log_message(f"[X] Skipped: {row_copy['error']}")
                    error_count += 1
                    continue
                
                if not row_copy.get("scheduledStartTime"):
                    broadcast_time = base_dt + (interval * idx)
                    # Convert local time to UTC
                    utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
                    broadcast_time_utc = broadcast_time - timedelta(seconds=utc_offset_seconds)
                    row_copy["scheduledStartTime"] = broadcast_time_utc.isoformat() + 'Z'
                    self.log_message(f"[{idx+1}] Scheduled for: {broadcast_time.strftime('%Y-%m-%d %H:%M')} (Local) - {row_copy.get('title', 'No title')[:50]}")
                
                if force_monetization:
                    row_copy["enableMonetization"] = True
                
                success, result = self.youtube_service.process_broadcast(
                    row_copy, 
                    log_callback=self.log_message
                )
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    self.log_message(f"[X] Error detail: {result}\n")
            
            self.log_message(f"\n{'='*60}")
            self.log_message(f"Batch {batch_idx} ({time_choice}) Complete!")
            self.log_message(f"[OK] Success: {success_count} | [X] Errors: {error_count}")
            self.log_message(f"{'='*60}\n")
            
            total_success += success_count
            total_errors += error_count
        
        # Final summary
        self.log_message(f"\n{'='*60}")
        self.log_message(f"🎉 ALL SCHEDULED BATCHES COMPLETE!")
        self.log_message(f"{'='*60}")
        self.log_message(f"Total batches processed: {len(selected_base_times)}")
        self.log_message(f"Total broadcasts created: {total_success}")
        self.log_message(f"Total errors: {total_errors}")
        self.log_message(f"{'='*60}\n")
    
    def setup_upcoming_tab(self):
        frame = ctk.CTkFrame(self.tab_upcoming)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="📅 Upcoming Broadcasts", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        self.btn_refresh_upcoming = ctk.CTkButton(
            frame, text="Refresh", 
            command=self.refresh_upcoming
        )
        self.btn_refresh_upcoming.pack(pady=10)
        
        self.text_upcoming = ctk.CTkTextbox(frame, height=500)
        self.text_upcoming.pack(fill="both", expand=True, pady=10)
    
    def refresh_upcoming(self):
        if not self.auth.is_authenticated():
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        def refresh_thread():
            self.log_message("Fetching upcoming broadcasts...")
            success, result = self.youtube_service.get_upcoming_broadcasts()
            
            if success:
                self.text_upcoming.delete("1.0", "end")
                
                if not result:
                    self.text_upcoming.insert("1.0", "No upcoming broadcasts found.")
                else:
                    text = f"Found {len(result)} upcoming broadcasts:\n\n"
                    for idx, item in enumerate(result, 1):
                        snippet = item['snippet']
                        status = item['status']
                        text += f"{idx}. {snippet['title']}\n"
                        text += f"   Scheduled: {snippet.get('scheduledStartTime', 'N/A')}\n"
                        text += f"   Privacy: {status['privacyStatus']}\n"
                        text += f"   ID: {item['id']}\n\n"
                    
                    self.text_upcoming.insert("1.0", text)
                
                self.log_message(f"✓ Found {len(result)} upcoming broadcasts")
            else:
                self.text_upcoming.delete("1.0", "end")
                self.text_upcoming.insert("1.0", f"Error: {result}")
                self.log_message(f"✗ Error fetching broadcasts: {result}")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def setup_settings_tab(self):
        frame = ctk.CTkFrame(self.tab_settings)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="⚙️ Application Settings", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Theme Settings
        theme_frame = ctk.CTkFrame(frame)
        theme_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(theme_frame, text="🎨 Appearance Theme:", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)
        
        theme_desc = ctk.CTkLabel(theme_frame, 
                                  text="Choose between light and dark mode for the application interface",
                                  font=ctk.CTkFont(size=12),
                                  text_color="gray")
        theme_desc.pack(anchor="w", padx=10, pady=(0,10))
        
        theme_buttons = ctk.CTkFrame(theme_frame)
        theme_buttons.pack(fill="x", padx=10, pady=10)
        
        current_theme = ctk.get_appearance_mode()
        
        self.btn_theme_light = ctk.CTkButton(
            theme_buttons,
            text="☀️ Light Mode",
            command=lambda: self.change_theme("light"),
            width=150,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="white" if current_theme == "Light" else "gray",
            text_color="black" if current_theme == "Light" else "white",
            hover_color="#E0E0E0"
        )
        self.btn_theme_light.pack(side="left", padx=5)
        
        self.btn_theme_dark = ctk.CTkButton(
            theme_buttons,
            text="🌙 Dark Mode",
            command=lambda: self.change_theme("dark"),
            width=150,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1F6AA5" if current_theme == "Dark" else "gray",
            hover_color="#144870"
        )
        self.btn_theme_dark.pack(side="left", padx=5)
        
        self.lbl_theme_status = ctk.CTkLabel(
            theme_buttons,
            text=f"Current: {current_theme} Mode",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_theme_status.pack(side="left", padx=20)
        
        # App Info
        info_frame = ctk.CTkFrame(frame)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(info_frame, text="ℹ️ Application Info:", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)
        
        info_text = f"""
        App Name: {config.APP_NAME}
        Version: {config.APP_VERSION}
        
        Features:
        • Live Broadcast Creation & Management
        • Batch Upload from Excel
        • Video Upload with Scheduling
        • Automatic Monetization Settings
        • Multi-Channel Support
        
        Settings Location: {Path.home() / '.ytlive'}
        """
        
        ctk.CTkLabel(info_frame, text=info_text, 
                    justify="left",
                    font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=10)
    
    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
        save_theme(theme)
        
        # Update is_dark_mode flag
        self.is_dark_mode = ctk.get_appearance_mode() == "Dark"
        
        # Update button colors
        current = ctk.get_appearance_mode()
        
        if current == "Light":
            self.btn_theme_light.configure(fg_color="white", text_color="black")
            self.btn_theme_dark.configure(fg_color="gray")
        else:
            self.btn_theme_light.configure(fg_color="gray")
            self.btn_theme_dark.configure(fg_color="#1F6AA5")
        
        self.lbl_theme_status.configure(text=f"Current: {current} Mode")
        
        # Update all adaptive colors
        self.update_adaptive_colors()
        
        self.log_message(f"[SETTINGS] Theme changed to {theme} mode")
        messagebox.showinfo("Theme Changed", 
                          f"Theme changed to {theme} mode!\n\nAll colors have been updated for better readability.")
    
    def setup_logs_tab(self):
        frame = ctk.CTkFrame(self.tab_logs)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="📝 Activity Logs", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", pady=5)
        
        ctk.CTkButton(btn_frame, text="Clear Logs", command=self.clear_logs).pack(side="left", padx=5)
        
        self.text_logs = ctk.CTkTextbox(frame, height=500)
        self.text_logs.pack(fill="both", expand=True, pady=10)
    
    def log_message(self, message):
        self.text_logs.insert("end", f"{message}\n")
        self.text_logs.see("end")
    
    def clear_logs(self):
        self.text_logs.delete("1.0", "end")
    
    def update_adaptive_colors(self):
        """Update all adaptive colors based on current theme"""
        # Auth tab
        if hasattr(self, 'lbl_secret_path'):
            current_text = self.lbl_secret_path.cget("text")
            if "No file" in current_text:
                self.lbl_secret_path.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
        
        # Update status labels
        if hasattr(self, 'lbl_auth_status'):
            current_text = self.lbl_auth_status.cget("text")
            if "Not authenticated" in current_text:
                self.lbl_auth_status.configure(text_color=get_adaptive_error_color(self.is_dark_mode))
            elif "Authenticated" in current_text:
                if "No Channels" in current_text:
                    self.lbl_auth_status.configure(text_color=get_adaptive_warning_color(self.is_dark_mode))
                else:
                    self.lbl_auth_status.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
        
        # Quick tab
        if hasattr(self, 'lbl_quick_thumbnail'):
            current_text = self.lbl_quick_thumbnail.cget("text")
            if "No thumbnail" in current_text:
                self.lbl_quick_thumbnail.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
            elif "✓" in current_text:
                self.lbl_quick_thumbnail.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
        
        # Import tab
        if hasattr(self, 'lbl_excel_status'):
            current_text = self.lbl_excel_status.cget("text")
            if "No file" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
            elif "✓" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_success_color(self.is_dark_mode))
            elif "✗" in current_text:
                self.lbl_excel_status.configure(text_color=get_adaptive_error_color(self.is_dark_mode))
        
        if hasattr(self, 'lbl_batch_time_info'):
            self.lbl_batch_time_info.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
        
        if hasattr(self, 'lbl_monetization_status'):
            current_text = self.lbl_monetization_status.cget("text")
            if "⚠" in current_text:
                self.lbl_monetization_status.configure(text_color=get_adaptive_warning_color(self.is_dark_mode))
            else:
                self.lbl_monetization_status.configure(text_color=get_adaptive_gray_color(self.is_dark_mode))
        
        # Update video upload tab colors
        if hasattr(self, 'video_upload_tab'):
            self.video_upload_tab.update_adaptive_colors(self.is_dark_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
