# RuView SMART FINAL v1.0.0 - Professional
# Features: Smart Learning, Zone ID, Normal vs Abnormal, Night Guard, Elderly Care, Fall, SOS, Log
# Privacy: Local only, No data sent to other phone, Visible notification, Requires user press START
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import math, random, time, datetime, os, json

try:
    from plyer import notification
    HAS_NOTIF = True
except:
    HAS_NOTIF = False

LOG_PATH = "events.json"

def get_rssi():
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        Context = autoclass('android.content.Context')
        wifi = activity.getSystemService(Context.WIFI_SERVICE)
        info = wifi.getConnectionInfo()
        rssi = info.getRssi()
        if rssi != 0:
            return int(rssi), True
    except:
        pass
    return None, False

def send_notif(title, msg):
    if HAS_NOTIF:
        try:
            notification.notify(title=title, message=msg, app_name='RuView SMART')
        except:
            pass
    print("NOTIF: " + title + " - " + msg)

def save_event(event_type, zone, rssi, var):
    try:
        data = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                data = json.load(f)
        data.append({
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": event_type,
            "zone": zone,
            "rssi": rssi,
            "variance": var
        })
        if len(data) > 100:
            data = data[-100:]
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        self.history = []
        self.log = []
        self.running = False
        self.mode = 'Normal'
        self.i = 0
        self.last_motion = time.time()
        self.last_notify = 0
        self.last_no_motion_alert = 0
        self.prev_rssi = -55
        self.learning = False
        self.learn_data = []
        self.baseline_rssi = -55
        self.baseline_var = 2
        self.normal_limit = 8
        self.abnormal_limit = 12
        self.title = Label(text='RuView SMART v1.0.0 - Safety', font_size=24, bold=True)
        self.info = Label(text='PROFESSIONAL BUILD\nRunning with your permission\nLocal only - No data to other phone\nPress START', font_size=15)
        self.rssi_label = Label(text='RSSI: -- dBm', font_size=30, bold=True)
        self.status_label = Label(text='Stopped', font_size=22)
        self.zone_label = Label(text='Zone: --', font_size=20)
        self.smart_label = Label(text='Smart: Not learned yet', font_size=17)
        self.log_label = Label(text='Log: No events yet', font_size=13)
        self.btn = Button(text='START Monitoring', size_hint=(1, 0.22), background_color=(0, 0.8, 0.4, 1))
        self.btn.bind(on_press=self.toggle)
        self.btn_normal = Button(text='Mode: Normal', size_hint=(1, 0.16))
        self.btn_normal.bind(on_press=lambda x: self.set_mode('Normal'))
        self.btn_night = Button(text='Mode: Night Guard 00:00-05:00', size_hint=(1, 0.16), background_color=(0.2, 0.2, 0.8, 1))
        self.btn_night.bind(on_press=lambda x: self.set_mode('Night Guard'))
        self.btn_elder = Button(text='Mode: Elderly Care 30 min', size_hint=(1, 0.16), background_color=(0.8, 0.6, 0.1, 1))
        self.btn_elder.bind(on_press=lambda x: self.set_mode('Elderly Care'))
        self.btn_sos = Button(text='SOS - Need Help !!!', size_hint=(1, 0.28), background_color=(0.9, 0.1, 0.1, 1))
        self.btn_sos.bind(on_press=self.do_sos)
        self.add_widget(self.title)
        self.add_widget(self.info)
        self.add_widget(self.rssi_label)
        self.add_widget(self.status_label)
        self.add_widget(self.zone_label)
        self.add_widget(self.smart_label)
        self.add_widget(self.btn_normal)
        self.add_widget(self.btn_night)
        self.add_widget(self.btn_elder)
        self.add_widget(self.btn_sos)
        self.add_widget(self.btn)
        self.add_widget(self.log_label)

    def set_mode(self, m):
        self.mode = m
        self.add_log('Mode changed to ' + m)

    def add_log(self, msg):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.log.append(f'{now} - {msg}')
        if len(self.log) > 5:
            self.log = self.log[-5:]
        self.log_label.text = 'Log:\n' + '\n'.join(self.log)

    def do_sos(self, *args):
        send_notif('SOS! Need Help', 'Someone pressed SOS button in home!')
        save_event('SOS', self.zone_label.text, self.prev_rssi, 0)
        self.add_log('SOS pressed')
        self.status_label.text = 'SOS !!!'

    def get_zone(self, rssi):
        if rssi > -45:
            return 'Near Router'
        elif rssi >= -65:
            return 'In Living Room'
        else:
            return 'Far From Router'

    def toggle(self, *args):
        if not self.running:
            self.running = True
            self.learning = True
            self.learn_data = []
            self.i = 0
            self.btn.text = 'STOP Monitoring'
            self.btn.background_color = (0.9, 0.2, 0.2, 1)
            self.last_motion = time.time()
            self.smart_label.text = 'Smart: Learning home... Stay still 30 sec'
            Clock.schedule_interval(self.update, 1.0)
            send_notif('RuView SMART ON', 'Learning home 30 sec - Stay still')
        else:
            self.running = False
            self.learning = False
            self.btn.text = 'START Monitoring'
            self.btn.background_color = (0, 0.8, 0.4, 1)
            Clock.unschedule(self.update)
            self.status_label.text = 'Stopped'

    def update(self, dt):
        self.i += 1
        rssi, is_real = get_rssi()
        if not is_real:
            base = -55
            move = 9 * math.sin(self.i / 6.0) if 20 < (self.i % 60) < 30 else 0
            rssi = int(base + random.uniform(-2, 2) + move)
            label = 'SIM - Enable Location for REAL'
        else:
            label = 'REAL'
        if self.learning:
            self.learn_data.append(rssi)
            self.rssi_label.text = f'RSSI: {rssi} dBm - Learning {len(self.learn_data)}/30'
            self.status_label.text = 'Learning... Stay still'
            if len(self.learn_data) >= 30:
                self.baseline_rssi = sum(self.learn_data) / len(self.learn_data)
                self.baseline_var = max(self.learn_data) - min(self.learn_data)
                self.normal_limit = self.baseline_var + 4
                self.abnormal_limit = self.baseline_var + 12
                self.learning = False
                self.smart_label.text = f'Smart: Learned! Home {int(self.baseline_rssi)} dBm - Normal up to {int(self.normal_limit)} - Abnormal over {int(self.abnormal_limit)}'
                send_notif('Learned your home!', f'Normal up to {int(self.normal_limit)} - Abnormal over {int(self.abnormal_limit)}')
                self.add_log(f'Learned - baseline {int(self.baseline_rssi)}')
            return
        drop = self.prev_rssi - rssi
        if drop > 20:
            send_notif('Possible Fall!', f'RSSI dropped from {self.prev_rssi} to {rssi}')
            save_event('FALL', self.get_zone(rssi), rssi, drop)
            self.add_log(f'Fall {self.prev_rssi} -> {rssi}')
        self.prev_rssi = rssi
        zone = self.get_zone(rssi)
        self.zone_label.text = 'Zone: ' + zone
        self.history.append(rssi)
        if len(self.history) > 8:
            self.history = self.history[-8:]
        if len(self.history) >= 5:
            var = max(self.history) - min(self.history)
            hour = datetime.datetime.now().hour
            is_night = hour >= 0 and hour < 5
            if var < 4:
                status = 'Stable - No Movement'
                cls = 'stable'
            elif var < self.normal_limit:
                status = 'Normal Movement'
                cls = 'normal'
                self.last_motion = time.time()
                self.add_log(f'Normal {zone} {rssi}')
                save_event('NORMAL', zone, rssi, var)
            elif var < self.abnormal_limit:
                status = 'Strong Movement'
                cls = 'strong'
                self.last_motion = time.time()
                self.add_log(f'Strong {zone} {rssi}')
                save_event('STRONG', zone, rssi, var)
            else:
                status = '>>> Abnormal Movement! <<<'
                cls = 'abnormal'
                self.last_motion = time.time()
                self.add_log(f'Abnormal {zone} {rssi}')
                save_event('ABNORMAL', zone, rssi, var)
            if is_night and cls in ['strong', 'abnormal'] and self.mode == 'Night Guard':
                status = '>>> Abnormal Movement at Night! <<<'
                cls = 'abnormal_night'
        else:
            status = 'Collecting...'
            cls = '...'
            var = 0
        self.rssi_label.text = f'RSSI: {rssi} dBm - {label}'
        self.status_label.text = status
        now = time.time()
        if cls == 'abnormal' and (now - self.last_notify > 10):
            send_notif('Abnormal Movement!', f'{zone} - RSSI {rssi} dBm - Var over {int(self.abnormal_limit)}')
            self.last_notify = now
        if cls == 'abnormal_night' and (now - self.last_notify > 10):
            send_notif('Strange Movement at Night!', f'{zone} - RSSI {rssi}')
            self.last_notify = now
        if self.mode == 'Elderly Care':
            no_motion_min = (now - self.last_motion) / 60
            if no_motion_min > 30 and (now - self.last_no_motion_alert > 600):
                send_notif('Check on them!', 'No movement for 30 min - Check elderly')
                self.add_log('No movement 30 min!')
                save_event('NO_MOTION_30MIN', zone, rssi, 0)
                self.last_no_motion_alert = now
        if rssi < -75:
            self.status_label.text = status + ' | Phone Far!'

class RuViewApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    RuViewApp().run()
