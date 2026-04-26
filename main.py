# main.py
# Kramer VP-437N Controller - Android Kivy App

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy import Config

# Фикс интерфейса
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', False)

from jnius import autoclass, JavaException
from android.permissions import request_permissions, Permission

from commands import COMMANDS
from decoder import decode_response
import threading
import time

Window.clearcolor = (0.1, 0.1, 0.15, 1)


class KramerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.bt_socket = None
        self.connected = False
        self.selected_device = None
        self.connecting = False
        self.socket_lock = threading.Lock()

        # Header
        self.add_widget(Label(text="🎛 Kramer VP-437N", size_hint_y=None, height=40,
                             bold=True, color=(1, 1, 1, 1), halign='center'))

        # Status + Connect
        status_frame = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.lbl_status = Label(text="❌ Not Connected", size_hint_x=0.6, halign='left')
        self.btn_connect = Button(text="🔗 Connect Device", size_hint_x=0.4,
                                 background_color=(0.2, 0.6, 1, 1))
        self.btn_connect.bind(on_press=self.show_device_list)
        status_frame.add_widget(self.lbl_status)
        status_frame.add_widget(self.btn_connect)
        self.add_widget(status_frame)

        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        content.bind(minimum_height=content.setter('height'))

        # Inputs
        self._add_section(content, "📺 INPUT SOURCE", 30)
        inputs_layout = BoxLayout(size_hint_y=None, height=140, spacing=4)
        inputs = [
            ('CV', 'Input: CV'), ('YC', 'Input: YC'), ('COMP1', 'Input: COMP1'),
            ('COMP2', 'Input: COMP2'), ('VGA', 'Input: VGA'),
            ('HDMI1', 'Input: HDMI1'), ('HDMI2', 'Input: HDMI2')
        ]
        for label, cmd in inputs:
            btn = Button(text=label)
            btn.bind(on_release=lambda x, c=cmd: self.send_cmd(c))
            inputs_layout.add_widget(btn)
        content.add_widget(inputs_layout)

        # Resolution
        self._add_section(content, "🖥 OUTPUT RESOLUTION", 30)
        res_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        res_list = [k for k in COMMANDS.keys() if k.startswith('Resolution:')]
        self.spin_res = Spinner(text='Select...', values=res_list)
        btn_set = Button(text="SET", background_color=(0.2, 0.8, 0.2, 1))
        btn_set.bind(on_release=lambda x: self.send_cmd(self.spin_res.text))
        res_layout.add_widget(self.spin_res)
        res_layout.add_widget(btn_set)
        content.add_widget(res_layout)

        # Power & Functions
        self._add_section(content, "⚡ POWER & FUNCTIONS", 30)
        func_layout = BoxLayout(size_hint_y=None, height=100, spacing=4)
        funcs = [
            ('ON', 'Power: ON'), ('OFF', 'Power: OFF'), ('REBOOT', 'Power: REBOOT'),
            ('INFO', 'Remote: INFO'), ('MENU', 'Remote: MENU'), ('EXIT', 'Remote: EXIT'),
            ('MUTE', 'Remote: MUTE'), ('FREEZE', 'Remote: FREEZE')
        ]
        for label, cmd in funcs:
            btn = Button(text=label)
            btn.bind(on_release=lambda x, c=cmd: self.send_cmd(c))
            func_layout.add_widget(btn)
        content.add_widget(func_layout)

        # Log
        self._add_section(content, "📋 LOG", 25)
        self.lbl_log = Label(text="Ready. Press 'Connect Device'", size_hint_y=None, height=60,
                            text_size=(Window.width - 20, None), halign='left',
                            valign='middle', color=(0.8, 1, 0.8, 1))
        content.add_widget(self.lbl_log)

        scroll.add_widget(content)
        self.add_widget(scroll)

        # Request permissions on start
        Clock.schedule_once(lambda dt: self._request_permissions(), 0.5)

    def _add_section(self, parent, text, height):
        parent.add_widget(Label(text=text, size_hint_y=None, height=height,
                               bold=True, color=(1, 0.8, 0.2, 1)))

    def _request_permissions(self):
        request_permissions([
            Permission.BLUETOOTH_SCAN,
            Permission.BLUETOOTH_CONNECT,
            Permission.ACCESS_FINE_LOCATION
        ])

    def show_device_list(self, instance):
        if self.connecting:
            self.log("⏳ Already connecting, please wait...")
            return

        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()

            if not adapter:
                self.log("❌ Device doesn't support Bluetooth")
                return

            if not adapter.isEnabled():
                self.log("⚠ Bluetooth is OFF. Please enable it in Android settings")
                try:
                    Intent = autoclass('android.content.Intent')
                    Settings = autoclass('android.provider.Settings')
                    intent = Intent(Settings.ACTION_BLUETOOTH_SETTINGS)
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    PythonActivity.mActivity.startActivity(intent)
                except:
                    pass
                return

            bonded = adapter.getBondedDevices()
            devices = []
            if bonded:
                iterator = bonded.iterator()
                while iterator.hasNext():
                    d = iterator.next()
                    name = d.getName() or "Unknown"
                    address = d.getAddress()
                    devices.append((name, address))
                    self.log(f"Found: {name} ({address})")

            if not devices:
                self.log("❌ No paired devices. Pair HC-06 in Bluetooth settings first.")
                return

            popup_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
            popup_layout.bind(minimum_height=popup_layout.setter('height'))

            for name, address in devices:
                btn = Button(
                    text=f"{name}\n{address}",
                    size_hint_y=None,
                    height=70,
                    text_size=(300, None),
                    halign='center',
                    valign='middle',
                    background_color=(0.15, 0.25, 0.4, 1)
                )
                btn.bind(size=btn.setter('text_size'))
                btn.bind(on_release=lambda x, n=name, a=address: self._select_device(n, a))
                popup_layout.add_widget(btn)

            cancel_btn = Button(text="Cancel", size_hint_y=None, height=50,
                               background_color=(0.5, 0.2, 0.2, 1))
            popup_layout.add_widget(cancel_btn)

            self.popup = Popup(title="🔗 Select Bluetooth Device", content=popup_layout,
                              size_hint=(0.9, 0.7))
            cancel_btn.bind(on_release=self.popup.dismiss)
            self.popup.open()

        except JavaException as e:
            self.log(f"❌ Bluetooth error: {str(e)[:60]}")
        except Exception as e:
            self.log(f"❌ Error: {str(e)[:60]}")

    def _select_device(self, name, address):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
        self.selected_device = {'name': name, 'address': address}
        self.log(f"📱 Selected: {name}\nConnecting to {address}...")
        threading.Thread(target=self._connect_thread, args=(address,), daemon=True).start()

    def _connect_thread(self, mac):
        if self.connecting:
            Clock.schedule_once(lambda dt: self.log("⏳ Already connecting..."), 0)
            return

        self.connecting = True
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()

            if not adapter:
                raise Exception("No Bluetooth adapter")

            device = adapter.getRemoteDevice(mac)
            
            # Специальный метод для HC-06 (RFCOMM channel 1)
            sock = None
            try:
                Method = autoclass('java.lang.reflect.Method')
                m = device.getClass().getMethod("createRfcommSocket", [int])
                sock = m.invoke(device, 1)
                sock.connect()
                self.log("Connected via RFCOMM channel 1")
            except Exception as e1:
                self.log(f"Channel 1 failed: {str(e1)[:30]}, trying standard SPP")
                try:
                    UUID = autoclass('java.util.UUID')
                    spp_uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                    sock = device.createRfcommSocketToServiceRecord(spp_uuid)
                    sock.connect()
                    self.log("Connected via Standard SPP")
                except Exception as e2:
                    raise Exception(f"Both methods failed: {str(e2)[:30]}")

            adapter.cancelDiscovery()

            with self.socket_lock:
                self.bt_socket = sock
                self.connected = True

            Clock.schedule_once(lambda dt: self._on_connect_success(), 0)

        except JavaException as e:
            error_msg = str(e)
            if "Permission denied" in error_msg:
                error_msg = "Permission denied"
            elif "Service discovery failed" in error_msg:
                error_msg = "Pair HC-06 in Bluetooth settings first"
            Clock.schedule_once(lambda dt: self._on_connect_failed(error_msg[:40]), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_connect_failed(str(e)[:40]), 0)
        finally:
            self.connecting = False

    def _on_connect_success(self):
        self.lbl_status.text = f"✅ {self.selected_device['name']}"
        self.lbl_status.color = (0, 1, 0, 1)
        self.btn_connect.text = "✖ Disconnect"
        try:
            self.btn_connect.unbind(on_press=self.show_device_list)
        except:
            pass
        self.btn_connect.bind(on_press=self._disconnect)
        self.log("🔗 Connected successfully!")

    def _on_connect_failed(self, error_msg):
        self.log(f"❌ Connection failed: {error_msg}")
        with self.socket_lock:
            self.bt_socket = None
            self.connected = False

    def _disconnect(self, instance=None):
        def do_disconnect():
            with self.socket_lock:
                if self.bt_socket:
                    try:
                        self.bt_socket.close()
                    except:
                        pass
                    self.bt_socket = None
            self.connected = False
            Clock.schedule_once(lambda dt: self._on_disconnect(), 0)

        threading.Thread(target=do_disconnect, daemon=True).start()

    def _on_disconnect(self):
        self.lbl_status.text = "❌ Not Connected"
        self.lbl_status.color = (1, 0, 0, 1)
        self.btn_connect.text = "🔗 Connect Device"
        try:
            self.btn_connect.unbind(on_press=self._disconnect)
        except:
            pass
        self.btn_connect.bind(on_press=self.show_device_list)
        self.log("🔌 Disconnected")

    def send_cmd(self, cmd_name):
        if not cmd_name or cmd_name == 'Select...':
            return

        if cmd_name not in COMMANDS:
            self.log(f"⚠ Unknown command: {cmd_name}")
            return

        if not self.connected:
            self.log("⚠ Not connected to device!")
            return

        with self.socket_lock:
            if not self.bt_socket:
                self.log("⚠ Socket is closed!")
                self._on_disconnect()
                return
            cmd_bytes = COMMANDS[cmd_name]

        hex_str = ' '.join(f'{b:02X}' for b in cmd_bytes)
        self.log(f">> {cmd_name} [{hex_str}]")

        try:
            with self.socket_lock:
                if self.bt_socket:
                    out_stream = self.bt_socket.getOutputStream()
                    out_stream.write(cmd_bytes)
                    out_stream.flush()

            Clock.schedule_once(lambda dt: self._read_response(cmd_name), 0.2)
        except Exception as e:
            self.log(f"❌ Send error: {str(e)[:40]}")
            self._disconnect()

    def _read_response(self, cmd_name):
        with self.socket_lock:
            if not self.bt_socket or not self.connected:
                return

            try:
                in_stream = self.bt_socket.getInputStream()
                if in_stream.available() > 0:
                    time.sleep(0.05)
                    response = bytearray()
                    while in_stream.available() > 0 and len(response) < 1024:
                        b = in_stream.read()
                        if b == -1:
                            break
                        response.append(b)
                        if b == 0x0D:
                            break

                    if response:
                        try:
                            decoded_str = response.decode('ascii', errors='replace').strip()
                            human_readable = decode_response(decoded_str)
                            self.log(f"<< {human_readable}")
                        except:
                            self.log(f"<< HEX: {' '.join(f'{b:02X}' for b in response)}")
            except Exception as e:
                pass

    def log(self, text):
        Clock.schedule_once(lambda dt: setattr(self.lbl_log, 'text', text), 0)


class KramerApp(App):
    def build(self):
        return KramerLayout()

    def on_stop(self):
        try:
            if hasattr(self.root, '_disconnect'):
                self.root._disconnect()
        except:
            pass


if __name__ == '__main__':
    KramerApp().run()