"""
AndroStream - Minimal Test Version
Just to verify build works before adding full features
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainScreen(Screen):
    """Simple main screen for testing"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='[b]AndroStream[/b]\n[size=14sp]Minimal Test Version[/size]',
            markup=True,
            size_hint_y=None,
            height=100,
            font_size='24sp'
        )
        layout.add_widget(title)
        
        # Info
        info = Label(
            text='This is a minimal test build.\n\nIf you see this, the build worked!\n\nFull version coming soon...',
            size_hint_y=0.5
        )
        layout.add_widget(info)
        
        # Test button
        btn = Button(
            text='Test Button',
            size_hint_y=None,
            height=60,
            background_color=(0.2, 0.8, 0.3, 1)
        )
        btn.bind(on_press=self.on_test_button)
        layout.add_widget(btn)
        
        # Status
        self.status = Label(
            text='Ready',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status)
        
        self.add_widget(layout)
    
    def on_test_button(self, instance):
        """Test button handler"""
        self.status.text = 'Button clicked! Build is working!'


class AndroStreamMinimalApp(App):
    """Minimal test app"""
    
    def build(self):
        """Build app"""
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm


if __name__ == '__main__':
    AndroStreamMinimalApp().run()
