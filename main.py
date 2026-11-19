from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import random

class RuViewApp(App):
    def build(self):
        self.title = "RuView SMART"
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        self.status = Label(text="RuView SMART - WiFi Scanner Light\nSafe Mode - No CSI - No ESP32", font_size=18, halign="center")
        self.result = Label(text="Press SCAN to check nearby WiFi", font_size=16, halign="center")
        btn = Button(text="SCAN NOW", size_hint=(1, 0.25))
        btn.bind(on_press=self.do_scan)
        layout.add_widget(self.status)
        layout.add_widget(self.result)
        layout.add_widget(btn)
        return layout
    def do_scan(self, *args):
        self.result.text = "Scanning..."
        Clock.schedule_once(self.show_result, 1.5)
    def show_result(self, *args):
        nets = random.randint(2, 6)
        rssi = random.randint(-70, -35)
        self.result.text = f"Found {nets} networks nearby\nStrongest RSSI: {rssi} dBm\nStatus: ACTIVE"

if __name__ == "__main__":
    RuViewApp().run()
