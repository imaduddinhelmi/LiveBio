"""
System Tray Handler for AutoLiveBio
Allows application to run in background with system tray icon
"""

import pystray
from PIL import Image, ImageDraw
import threading
from typing import Callable, Optional

class SystemTrayHandler:
    def __init__(self, app_title="AutoLiveBio"):
        self.app_title = app_title
        self.icon = None
        self.show_window_callback = None
        self.quit_callback = None
        self.is_running = False
        
    def create_icon_image(self):
        """Create a simple icon image"""
        # Create 64x64 image with a simple design
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (46, 125, 50))  # Green background
        
        dc = ImageDraw.Draw(image)
        # Draw a white "Y" for YouTube
        dc.text((20, 15), "YT", fill=(255, 255, 255))
        
        return image
    
    def set_callbacks(self, show_window: Callable, quit_app: Callable):
        """Set callbacks for menu actions"""
        self.show_window_callback = show_window
        self.quit_callback = quit_app
    
    def on_show(self):
        """Show main window"""
        if self.show_window_callback:
            self.show_window_callback()
    
    def on_quit(self):
        """Quit application"""
        if self.icon:
            self.icon.stop()
        if self.quit_callback:
            self.quit_callback()
    
    def create_menu(self):
        """Create system tray menu"""
        return pystray.Menu(
            pystray.MenuItem("Show Window", self.on_show, default=True),
            pystray.MenuItem("Quit", self.on_quit)
        )
    
    def start_tray(self):
        """Start system tray icon"""
        if self.is_running:
            return
        
        try:
            image = self.create_icon_image()
            self.icon = pystray.Icon(
                self.app_title,
                image,
                self.app_title,
                menu=self.create_menu()
            )
            
            self.is_running = True
            
            # Run in separate thread
            def run_icon():
                try:
                    self.icon.run()
                except Exception as e:
                    print(f"Tray icon error: {e}")
                finally:
                    self.is_running = False
            
            tray_thread = threading.Thread(target=run_icon, daemon=True)
            tray_thread.start()
            
            return True
        except Exception as e:
            print(f"Failed to start system tray: {e}")
            return False
    
    def stop_tray(self):
        """Stop system tray icon"""
        if self.icon and self.is_running:
            try:
                self.icon.stop()
                self.is_running = False
            except Exception as e:
                print(f"Error stopping tray: {e}")
    
    def update_tooltip(self, text: str):
        """Update tray icon tooltip"""
        if self.icon and self.is_running:
            try:
                self.icon.title = text
            except Exception as e:
                print(f"Error updating tooltip: {e}")
