"""
AndroStream - YouTube Live & Video Automation for Android
Mobile version using Kivy
"""

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from datetime import datetime, timedelta
import threading
import json
from pathlib import Path

# Import core modules
try:
    from auth import YouTubeAuth
    from youtube_service import YouTubeService
    # Try lite version first (for Android)
    try:
        from excel_parser_lite import ExcelParserLite as ExcelParser
    except ImportError:
        try:
            from excel_parser import ExcelParser
        except ImportError:
            ExcelParser = None
except ImportError as e:
    # Fallback untuk development
    print(f"Import warning: {e}")
    YouTubeAuth = None
    YouTubeService = None
    ExcelParser = None


class AuthScreen(Screen):
    """Screen for YouTube OAuth Authentication"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = None
        self.youtube_service = None
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='[b]🔐 YouTube Authentication[/b]',
            markup=True,
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='Not authenticated',
            size_hint_y=None,
            height=40,
            color=(1, 0.3, 0.3, 1)
        )
        layout.add_widget(self.status_label)
        
        # Account selector
        account_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        account_layout.add_widget(Label(text='Account:', size_hint_x=0.3))
        self.account_spinner = Spinner(
            text='No accounts',
            values=['No accounts'],
            size_hint_x=0.7
        )
        account_layout.add_widget(self.account_spinner)
        layout.add_widget(account_layout)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.btn_add = Button(text='Add Account', background_color=(0.2, 0.6, 1, 1))
        self.btn_add.bind(on_press=self.add_account)
        btn_layout.add_widget(self.btn_add)
        
        self.btn_switch = Button(text='Switch', background_color=(0.2, 0.8, 0.3, 1))
        self.btn_switch.bind(on_press=self.switch_account)
        btn_layout.add_widget(self.btn_switch)
        
        layout.add_widget(btn_layout)
        
        # Channel info
        self.channel_info = Label(
            text='No channel selected',
            size_hint_y=None,
            height=100
        )
        layout.add_widget(self.channel_info)
        
        # Logs
        log_scroll = ScrollView(size_hint=(1, 0.5))
        self.log_text = Label(
            text='',
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        self.log_text.bind(texture_size=lambda *x: setattr(self.log_text, 'height', self.log_text.texture_size[1]))
        log_scroll.add_widget(self.log_text)
        layout.add_widget(log_scroll)
        
        self.add_widget(layout)
        
        # Initialize auth
        if YouTubeAuth:
            self.auth = YouTubeAuth()
            Clock.schedule_once(lambda dt: self.load_saved_accounts(), 0.5)
    
    @mainthread
    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.text += f'\n[{timestamp}] {message}'
    
    def load_saved_accounts(self):
        """Load saved accounts"""
        if not self.auth:
            return
        
        try:
            accounts = self.auth.account_manager.get_all_accounts()
            if accounts:
                account_names = [acc['name'] for acc in accounts]
                self.account_spinner.values = account_names
                self.account_spinner.text = account_names[0]
                self.log('Loaded saved accounts')
        except Exception as e:
            self.log(f'Error loading accounts: {str(e)}')
    
    def add_account(self, instance):
        """Add new YouTube account"""
        # Show file chooser for client_secret.json
        content = BoxLayout(orientation='vertical')
        
        filechooser = FileChooserListView(
            filters=['*.json'],
            path=str(Path.home())
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        def select_file(instance):
            if filechooser.selection:
                popup.dismiss()
                self.authenticate_new_account(filechooser.selection[0])
        
        btn_select = Button(text='Select')
        btn_select.bind(on_press=select_file)
        btn_layout.add_widget(btn_select)
        
        btn_cancel = Button(text='Cancel')
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(btn_cancel)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Select client_secret.json',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def authenticate_new_account(self, secret_path):
        """Authenticate new account in background thread"""
        def auth_thread():
            try:
                self.log(f'Authenticating with: {secret_path}')
                success = self.auth.authenticate(secret_path, force_new=True)
                
                if success:
                    self.youtube_service = YouTubeService(self.auth.youtube, self.auth)
                    channels, error = self.auth.get_all_channels()
                    
                    if not error and channels:
                        self.log(f'✓ Authenticated! {len(channels)} channel(s)')
                        self.update_ui_after_auth()
                    else:
                        self.log(f'⚠ Auth OK but no channels: {error}')
                else:
                    self.log('✗ Authentication failed')
            except Exception as e:
                self.log(f'✗ Error: {str(e)}')
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    @mainthread
    def update_ui_after_auth(self):
        """Update UI after successful authentication"""
        self.status_label.text = '✓ Authenticated'
        self.status_label.color = (0.3, 1, 0.3, 1)
        self.load_saved_accounts()
        
        # Update channel info
        if self.auth and self.auth.all_channels:
            channel = self.auth.all_channels[0]
            self.channel_info.text = f"Channel: {channel['title']}\nID: {channel['id']}\nSubs: {channel['subscribers']}"
    
    def switch_account(self, instance):
        """Switch to selected account"""
        selected = self.account_spinner.text
        if selected == 'No accounts':
            return
        
        def switch_thread():
            try:
                self.log(f'Switching to: {selected}')
                accounts = self.auth.account_manager.get_all_accounts()
                
                for acc in accounts:
                    if acc['name'] == selected:
                        success = self.auth.switch_account(acc['id'])
                        if success:
                            self.youtube_service = YouTubeService(self.auth.youtube, self.auth)
                            self.log(f'✓ Switched to: {selected}')
                            self.update_ui_after_auth()
                        else:
                            self.log(f'✗ Failed to switch')
                        break
            except Exception as e:
                self.log(f'✗ Switch error: {str(e)}')
        
        threading.Thread(target=switch_thread, daemon=True).start()


class QuickCreateScreen(Screen):
    """Screen for quick broadcast creation"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Title
        title = Label(
            text='[b]⚡ Quick Create Broadcast[/b]',
            markup=True,
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        layout.add_widget(title)
        
        # Title input
        layout.add_widget(Label(text='Title:', size_hint_y=None, height=30))
        self.title_input = TextInput(
            text='Live Stream',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.title_input)
        
        # Description
        layout.add_widget(Label(text='Description:', size_hint_y=None, height=30))
        self.description_input = TextInput(
            text='Live streaming via YouTube API',
            multiline=True,
            size_hint_y=None,
            height=100
        )
        layout.add_widget(self.description_input)
        
        # Tags
        layout.add_widget(Label(text='Tags (comma-separated):', size_hint_y=None, height=30))
        self.tags_input = TextInput(
            text='live,stream',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.tags_input)
        
        # Category
        category_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        category_layout.add_widget(Label(text='Category:', size_hint_x=0.3))
        self.category_spinner = Spinner(
            text='20 (Gaming)',
            values=['20 (Gaming)', '22 (People & Blogs)', '24 (Entertainment)', '25 (News & Politics)', '28 (Science & Technology)'],
            size_hint_x=0.7
        )
        category_layout.add_widget(self.category_spinner)
        layout.add_widget(category_layout)
        
        # Privacy
        privacy_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        privacy_layout.add_widget(Label(text='Privacy:', size_hint_x=0.3))
        self.privacy_spinner = Spinner(
            text='public',
            values=['public', 'unlisted', 'private'],
            size_hint_x=0.7
        )
        privacy_layout.add_widget(self.privacy_spinner)
        layout.add_widget(privacy_layout)
        
        # Schedule time
        time_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        time_layout.add_widget(Label(text='Schedule:', size_hint_x=0.3))
        self.time_spinner = Spinner(
            text='+30 minutes',
            values=['Now', '+15 minutes', '+30 minutes', '+1 hour', '+2 hours', '+6 hours', '+1 day'],
            size_hint_x=0.7
        )
        self.time_spinner.bind(text=self.update_schedule_time)
        time_layout.add_widget(self.time_spinner)
        layout.add_widget(time_layout)
        
        # Schedule display
        self.schedule_label = Label(
            text='',
            size_hint_y=None,
            height=40,
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.schedule_label)
        
        # Options
        options_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        
        kids_layout = BoxLayout(size_hint_y=None, height=30)
        self.kids_check = CheckBox(size_hint_x=0.1)
        kids_layout.add_widget(self.kids_check)
        kids_layout.add_widget(Label(text='Made for Kids', size_hint_x=0.9))
        options_layout.add_widget(kids_layout)
        
        dvr_layout = BoxLayout(size_hint_y=None, height=30)
        self.dvr_check = CheckBox(active=True, size_hint_x=0.1)
        dvr_layout.add_widget(self.dvr_check)
        dvr_layout.add_widget(Label(text='Enable DVR', size_hint_x=0.9))
        options_layout.add_widget(dvr_layout)
        
        monetization_layout = BoxLayout(size_hint_y=None, height=30)
        self.monetization_check = CheckBox(active=True, size_hint_x=0.1)
        monetization_layout.add_widget(self.monetization_check)
        monetization_layout.add_widget(Label(text='Enable Monetization', size_hint_x=0.9))
        options_layout.add_widget(monetization_layout)
        
        layout.add_widget(options_layout)
        
        # Create button
        self.btn_create = Button(
            text='✨ Create Broadcast',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.8, 0.3, 1)
        )
        self.btn_create.bind(on_press=self.create_broadcast)
        layout.add_widget(self.btn_create)
        
        # Status
        self.status_label = Label(
            text='',
            size_hint_y=None,
            height=60
        )
        layout.add_widget(self.status_label)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        # Initialize schedule display
        Clock.schedule_once(lambda dt: self.update_schedule_time(None, self.time_spinner.text), 0.1)
    
    def update_schedule_time(self, spinner, text):
        """Update schedule time display"""
        offset_map = {
            'Now': timedelta(0),
            '+15 minutes': timedelta(minutes=15),
            '+30 minutes': timedelta(minutes=30),
            '+1 hour': timedelta(hours=1),
            '+2 hours': timedelta(hours=2),
            '+6 hours': timedelta(hours=6),
            '+1 day': timedelta(days=1)
        }
        
        offset = offset_map.get(text, timedelta(minutes=30))
        target_time = datetime.now() + offset
        
        self.schedule_label.text = f'Scheduled for: {target_time.strftime("%Y-%m-%d %H:%M")}'
    
    def create_broadcast(self, instance):
        """Create broadcast"""
        auth_screen = self.manager.get_screen('auth')
        
        if not auth_screen.youtube_service:
            self.show_popup('Error', 'Please authenticate first')
            return
        
        self.btn_create.disabled = True
        self.status_label.text = 'Creating broadcast...'
        self.status_label.color = (1, 1, 0, 1)
        
        def create_thread():
            try:
                # Calculate schedule time
                offset_map = {
                    'Now': timedelta(0),
                    '+15 minutes': timedelta(minutes=15),
                    '+30 minutes': timedelta(minutes=30),
                    '+1 hour': timedelta(hours=1),
                    '+2 hours': timedelta(hours=2),
                    '+6 hours': timedelta(hours=6),
                    '+1 day': timedelta(days=1)
                }
                
                offset = offset_map.get(self.time_spinner.text, timedelta(minutes=30))
                scheduled_time = (datetime.now() + offset).isoformat() + 'Z'
                
                # Get category ID
                category_id = self.category_spinner.text.split(' ')[0]
                
                # Prepare broadcast data
                broadcast_data = {
                    'title': self.title_input.text,
                    'description': self.description_input.text,
                    'tags': [tag.strip() for tag in self.tags_input.text.split(',')],
                    'categoryId': category_id,
                    'privacyStatus': self.privacy_spinner.text,
                    'scheduledStartTime': scheduled_time,
                    'madeForKids': self.kids_check.active,
                    'enableDvr': self.dvr_check.active,
                    'enableMonetization': self.monetization_check.active,
                    'enableEmbed': True,
                    'recordFromStart': True,
                    'latency': 'normal'
                }
                
                success, result = auth_screen.youtube_service.process_broadcast(
                    broadcast_data,
                    log_callback=lambda msg: auth_screen.log(msg)
                )
                
                if success:
                    self.show_result_on_main_thread(True, result)
                else:
                    self.show_result_on_main_thread(False, result)
                    
            except Exception as e:
                self.show_result_on_main_thread(False, str(e))
        
        threading.Thread(target=create_thread, daemon=True).start()
    
    @mainthread
    def show_result_on_main_thread(self, success, result):
        """Show result on main thread"""
        self.btn_create.disabled = False
        
        if success:
            self.status_label.text = f'✓ Created! ID: {result[:15]}...'
            self.status_label.color = (0.3, 1, 0.3, 1)
            self.show_popup('Success', f'Broadcast created!\n\nID: {result}')
        else:
            self.status_label.text = '✗ Failed'
            self.status_label.color = (1, 0.3, 0.3, 1)
            self.show_popup('Error', f'Failed to create broadcast:\n\n{result}')
    
    def show_popup(self, title, message):
        """Show popup message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class MainMenuScreen(Screen):
    """Main menu with navigation buttons"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # App title
        title = Label(
            text='[b]AndroStream[/b]\n[size=14sp]YouTube Live & Video Automation[/size]',
            markup=True,
            size_hint_y=None,
            height=100,
            font_size='24sp'
        )
        layout.add_widget(title)
        
        # Menu buttons
        buttons = [
            ('🔐 Authentication', 'auth', (0.2, 0.6, 1, 1)),
            ('⚡ Quick Create', 'quick_create', (0.2, 0.8, 0.3, 1)),
            ('📊 Batch Import', 'batch', (1, 0.6, 0, 1)),
            ('📹 Video Upload', 'video_upload', (0.8, 0.3, 0.8, 1)),
            ('📋 Upcoming', 'upcoming', (0.3, 0.7, 0.9, 1)),
        ]
        
        for text, screen_name, color in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=60,
                background_color=color,
                font_size='18sp'
            )
            btn.bind(on_press=lambda x, s=screen_name: self.goto_screen(s))
            layout.add_widget(btn)
        
        # Version info
        version_label = Label(
            text='v1.0.0 - Mobile Edition',
            size_hint_y=None,
            height=30,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(version_label)
        
        self.add_widget(layout)
    
    def goto_screen(self, screen_name):
        """Navigate to screen"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name


class AndroStreamApp(App):
    """Main application"""
    
    def build(self):
        """Build app"""
        # Screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(AuthScreen(name='auth'))
        sm.add_widget(QuickCreateScreen(name='quick_create'))
        
        # Placeholder screens
        for name, title in [('batch', 'Batch Import'), ('video_upload', 'Video Upload'), ('upcoming', 'Upcoming Broadcasts')]:
            screen = Screen(name=name)
            layout = BoxLayout(orientation='vertical', padding=20)
            layout.add_widget(Label(text=f'[b]{title}[/b]\n\n(Coming soon)', markup=True, font_size='20sp'))
            
            btn_back = Button(
                text='← Back to Menu',
                size_hint=(1, None),
                height=60,
                background_color=(0.5, 0.5, 0.5, 1)
            )
            btn_back.bind(on_press=lambda x: self.goto_menu())
            layout.add_widget(btn_back)
            
            screen.add_widget(layout)
            sm.add_widget(screen)
        
        # Bind Android back button
        Window.bind(on_keyboard=self.on_keyboard)
        
        return sm
    
    def goto_menu(self):
        """Go back to main menu"""
        self.root.transition = SlideTransition(direction='right')
        self.root.current = 'menu'
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle Android back button"""
        if key == 27:  # Escape / Back button
            if self.root.current != 'menu':
                self.goto_menu()
                return True
            else:
                return False
        return False


if __name__ == '__main__':
    AndroStreamApp().run()
