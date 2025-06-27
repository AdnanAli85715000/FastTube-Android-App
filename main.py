# -*- coding: utf-8 -*-
# Kivy framework ke zaroori modules import karein
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.utils import platform

# Video downloading ke liye zaroori modules
import threading
import subprocess
import os
import re # Regular expressions for URL validation
import json # yt-dlp info ko parse karne ke liye
import time # Time module for unique filenames and tracking

# Android Intent handling ke liye pyjnius (sirf Android par)
if platform == 'android':
    from jnius import autoclass, cast

# Window size ko mobile-friendly set karein
Window.size = (360, 640)

# Download directory setup (Android par public Download directory)
if platform == 'android':
    Environment = autoclass('android.os.Environment')
    DOWNLOAD_DIR = os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), 'Download', 'FastTubeDownloads')
else:
    DOWNLOAD_DIR = os.path.join(os.getcwd(), 'FastTubeDownloads')

# Download directory agar mojood nahi hai to banayen
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class QualityPopup(Popup):
    """
    Ek pop-up jo YouTube video ke available qualities aur formats ko show karta hai,
    aur user ko apni pasand ki quality select karne deta hai.
    """
    def __init__(self, url, callback, **kwargs):
        super().__init__(title='Quality Choose Karein', size_hint=(0.95, 0.8), **kwargs)
        self.url = url
        self.callback = callback
        self.selected_format = None # User ki select ki hui quality/format
        self.format_buttons = [] # Buttons ko track karne ke liye
        self.status_label = Label(text='Formats load ho rahen hain...', size_hint_y=None, height=40)

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.status_label)
        
        # Scrollable area for quality buttons
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        # Download button
        self.download_btn = Button(
            text='Download Selected',
            size_hint=(1, 0.15),
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1) # Blue color
        )
        self.download_btn.bind(on_press=self.on_download)
        self.download_btn.disabled = True # Jab tak quality select na ho, disabled rakhen
        self.layout.add_widget(self.download_btn)

        self.content = self.layout
        
        # Formats ko background thread mein load karein
        threading.Thread(target=self.load_formats).start()

    def load_formats(self):
        """
        YouTube video ke available formats ko yt-dlp se fetch karta hai
        aur UI par buttons ke taur par add karta hai.
        """
        try:
            # yt-dlp options to get info without downloading
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'forcejson': True,
                'simulate': True,
                'format': 'bestvideo+bestaudio/best' # Default best quality for info
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                formats = info.get('formats', [])
                title = info.get('title', 'Video')

            # Audio aur Video formats ko alag karein
            # MP3 formats (vcodec is none, acodec is not none, ext is mp3 or m4a)
            audios = sorted([f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('abr')],
                            key=lambda x: x.get('abr', 0), reverse=True)
            # Video formats (vcodec is not none, acodec is not none, ext is mp4)
            videos = sorted([f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4' and f.get('height')],
                            key=lambda x: x.get('height', 0), reverse=True)

            # UI update main thread mein hona chahiye
            Clock.schedule_once(lambda dt: self.add_format_buttons(videos, audios, title))

        except yt_dlp.utils.DownloadError as e:
            Clock.schedule_once(lambda dt: self.update_status_and_dismiss(f"[color=ff0000]Error: Video formats load nahi ho sake. {e}[/color]"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status_and_dismiss(f"[color=ff0000]Error loading formats: {e}[/color]"))

    def add_format_buttons(self, videos, audios, title):
        """Fetched formats ke liye UI buttons add karta hai."""
        self.title = f'"{title[:30]}..." ke liye Quality Choose Karein'
        self.status_label.text = 'Formats Load Ho Gaye.'
        
        if not videos and not audios:
            self.grid.add_widget(Label(text="Koi downloadable format nahi mila.", size_hint_y=None, height=50))
            self.download_btn.disabled = True
            return

        # Video Qualities
        self.grid.add_widget(Label(text='[b]Video (MP4)[/b]', markup=True, size_hint_y=None, height=40, font_size='18sp'))
        for f in videos:
            quality = f.get('height', 'unknown')
            filesize_mb = round(f.get('filesize', 0) / (1024 * 1024), 2) if f.get('filesize') else 'N/A'
            label = f"MP4 - {quality}p - {filesize_mb}MB"
            btn = Button(text=label, size_hint_y=None, height=50)
            btn.bind(on_press=lambda inst, fmt=f: self.set_selection(fmt, inst))
            self.grid.add_widget(btn)
            self.format_buttons.append(btn)

        # Audio Qualities
        self.grid.add_widget(Label(text='[b]Audio (MP3)[/b]', markup=True, size_hint_y=None, height=40, font_size='18sp'))
        for f in audios:
            abr = f.get('abr', 'unknown')
            filesize_mb = round(f.get('filesize', 0) / (1024 * 1024), 2) if f.get('filesize') else 'N/A'
            label = f"MP3 - {abr}kbps - {filesize_mb}MB"
            btn = Button(text=label, size_hint_y=None, height=50)
            btn.bind(on_press=lambda inst, fmt=f: self.set_selection(fmt, inst))
            self.grid.add_widget(btn)
            self.format_buttons.append(btn)
        
        self.download_btn.disabled = False # Formats load hone ke baad enable karein

    def set_selection(self, fmt, button_instance):
        """User ki selection ko set karta hai aur button ko highlight karta hai."""
        self.selected_format = fmt
        # Sab buttons ko reset karein
        for btn in self.format_buttons:
            btn.background_color = (1, 1, 1, 1) # Default white
            btn.color = (0, 0, 0, 1) # Default black text
        # Select kiye hue button ko highlight karein
        button_instance.background_color = (0.2, 0.6, 0.8, 1) # Highlight color
        button_instance.color = (1, 1, 1, 1) # White text

    def on_download(self, instance):
        """Selected quality ke sath download shuru karta hai."""
        if self.selected_format:
            self.dismiss() # Pop-up ko band karein
            self.callback(self.selected_format) # Callback function ko call karein
        else:
            # Status message parent screen par update karein
            App.get_running_app().root.ids.main_screen.update_status("[color=ff0000]Error: Quality select karein.[/color]")

    def update_status_and_dismiss(self, message):
        """Status update kare aur pop-up ko dismiss kare."""
        self.dismiss()
        # Status message parent screen par update karein
        App.get_running_app().root.ids.main_screen.update_status(message)

class DownloadItem(BoxLayout):
    """
    Download list mein har individual download item ko represent karta hai.
    """
    filename_display = StringProperty('')
    progress_text = StringProperty('0%')
    download_speed = StringProperty('0 KB/s')

    def __init__(self, url, title, selected_format, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=60, **kwargs)
        self.url = url
        self.title = title
        self.selected_format = selected_format
        self.process = None # Subprocess ko track karne ke liye
        self.download_thread = None # Download thread ko track karne ke liye
        self.last_downloaded_bytes = 0
        self.last_timestamp = time.time()

        self.filename_display = f"{self.title[:25]}..." if len(self.title) > 25 else self.title
        
        self.add_widget(Label(text=self.filename_display, size_hint_x=0.4, font_size='14sp'))
        self.progress_label = Label(text=self.progress_text, size_hint_x=0.2, font_size='14sp')
        self.add_widget(self.progress_label)
        self.speed_label = Label(text=self.download_speed, size_hint_x=0.2, font_size='14sp')
        self.add_widget(self.speed_label)
        
        # Pause/Resume/Cancel buttons ko ignore kiya gaya hai jaisa ke request kiya gaya
        # self.pause_btn = Button(text='Pause', size_hint_x=0.1)
        # self.cancel_btn = Button(text='Cancel', size_hint_x=0.1)
        # self.add_widget(self.pause_btn)
        # self.add_widget(self.cancel_btn)

        self.start_download()

    def start_download(self):
        """Download process ko background thread mein shuru karta hai."""
        self.download_thread = threading.Thread(target=self.execute_download)
        self.download_thread.daemon = True # App band hone par thread bhi band ho jaye
        self.download_thread.start()

    def execute_download(self):
        """yt-dlp ka istemal kar ke select ki hui quality download karta hai."""
        try:
            # Output filename template
            output_template = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

            ydl_opts = {
                'format': self.selected_format['format_id'],
                'outtmpl': output_template,
                'progress_hooks': [self.download_progress_hook],
                'quiet': True,
                'noplaylist': True, # Sirf single video download karein
            }

            # Agar audio only hai to --extract-audio aur --audio-format lagayen
            if self.selected_format.get('vcodec') == 'none' and self.selected_format.get('acodec') != 'none':
                ydl_opts['extract_audio'] = True
                ydl_opts['audioformat'] = self.selected_format.get('ext', 'mp3') # MP3 ya jo bhi audio format hai
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': ydl_opts['audioformat'],
                    'preferredquality': self.selected_format.get('abr', '192') # Use selected bitrate
                }]

            # Agar video aur audio alag alag hain to merge karein
            # yt-dlp aam taur par best video aur best audio ko khud merge karta hai agar format 'best' ho.
            # Agar specific video format select kiya hai aur us mein audio nahi hai, to best audio merge karein
            if self.selected_format.get('vcodec') != 'none' and self.selected_format.get('acodec') == 'none':
                ydl_opts['format'] = f"{self.selected_format['format_id']}+bestaudio[ext=m4a]"
                ydl_opts['merge_output_format'] = 'mp4'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            Clock.schedule_once(lambda dt: self.update_item_status(
                f"[color=008000]Done[/color]"))
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', '100%'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))

        except yt_dlp.utils.DownloadError as e:
            Clock.schedule_once(lambda dt: self.update_item_status(
                f"[color=ff0000]Error: {e}[/color]"))
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', 'Error'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))
        except FileNotFoundError:
            Clock.schedule_once(lambda dt: self.update_item_status(
                "[color=ff0000]Error: yt-dlp ya ffmpeg install nahi hain.[/color]"))
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', 'Error'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_item_status(
                f"[color=ff0000]Unexpected Error: {e}[/color]"))
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', 'Error'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))

    def download_progress_hook(self, d):
        """yt-dlp se download progress receive karta hai aur UI update karta hai."""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').strip()
            speed_str = d.get('_speed_str', 'N/A').strip()
            
            # Calculate actual speed if _speed_str is not reliable or missing
            if 'downloaded_bytes' in d and 'elapsed' in d:
                current_bytes = d['downloaded_bytes']
                current_time = time.time()
                
                if current_time - self.last_timestamp > 0: # Avoid division by zero
                    bytes_diff = current_bytes - self.last_downloaded_bytes
                    time_diff = current_time - self.last_timestamp
                    
                    if time_diff > 0:
                        calculated_speed_bps = bytes_diff / time_diff
                        if calculated_speed_bps >= 1024 * 1024:
                            speed_str = f"{calculated_speed_bps / (1024 * 1024):.2f} MB/s"
                        elif calculated_speed_bps >= 1024:
                            speed_str = f"{calculated_speed_bps / 1024:.2f} KB/s"
                        else:
                            speed_str = f"{calculated_speed_bps:.0f} B/s"
                    
                self.last_downloaded_bytes = current_bytes
                self.last_timestamp = current_time

            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', percent))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', speed_str))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', '100%'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))
            Clock.schedule_once(lambda dt: self.update_item_status("[color=008000]Done[/color]"))
        elif d['status'] == 'error':
            Clock.schedule_once(lambda dt: self.update_item_status("[color=ff0000]Error[/color]"))
            Clock.schedule_once(lambda dt: setattr(self, 'progress_text', 'Error'))
            Clock.schedule_once(lambda dt: setattr(self, 'download_speed', ''))

    def update_item_status(self, message):
        """Download item ke status label ko update karta hai."""
        self.progress_label.text = message # Progress label ko status ke liye istemal karein

class MainScreen(Screen):
    """
    App ki main screen jahan user URL paste karta hai aur quality select karta hai.
    """
    url_input_text = StringProperty('')
    status_message = StringProperty('YouTube link paste karein ya share karein.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_screen' # ID for easy access from other classes
        
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=10)

        # App title
        layout.add_widget(Label(text='[b]FastTube Downloader[/b]', markup=True,
                                font_size='24sp', size_hint_y=0.15))

        # URL input field
        self.url_input = TextInput(
            hint_text='YouTube URL yahan paste karein',
            size_hint_y=0.2,
            multiline=False,
            font_size='18sp',
            padding=[10, 10, 10, 10]
        )
        self.url_input.bind(text=self.setter('url_input_text'))
        layout.add_widget(self.url_input)

        # Choose Quality & Download button
        self.choose_quality_btn = Button(
            text='[b]Quality Choose Karein & Download[/b]',
            markup=True,
            size_hint_y=0.15,
            font_size='20sp',
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1) # Blue color
        )
        self.choose_quality_btn.bind(on_press=self.open_quality_popup)
        layout.add_widget(self.choose_quality_btn)

        # Status Label
        self.status_label = Label(
            text=self.status_message,
            size_hint_y=0.1,
            font_size='16sp',
            markup=True,
            halign='center',
            valign='middle'
        )
        self.bind(status_message=self.status_label.setter('text'))
        layout.add_widget(self.status_label)
        
        # Progress Bar (Label ke taur par, as Kivy's ProgressBar is complex for simple display)
        # MainScreen par global progress nahi, har download item ka apna progress hoga
        # Isko yahan se hata diya gaya hai.

        self.add_widget(layout)

        # Android Intent handling ko schedule karein
        Clock.schedule_once(self.handle_android_intent, 0)
    
    def update_status(self, message):
        """Status message ko UI par update karta hai."""
        self.status_message = message

    def is_valid_youtube_url(self, url):
        """YouTube URL ko validate karta hai."""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return re.match(youtube_regex, url) is not None

    def open_quality_popup(self, instance):
        """Quality selection pop-up ko open karta hai."""
        url = self.url_input_text.strip()
        if not url:
            self.update_status("[color=ff0000]Error: URL darj karein.[/color]")
            return
        if not self.is_valid_youtube_url(url):
            self.update_status("[color=ff0000]Error: Invalid YouTube URL.[/color]")
            return

        self.update_status("[color=0000ff]Formats load ho rahen hain...[/color]")
        popup = QualityPopup(url, self.download_selected_format)
        popup.open()

    def download_selected_format(self, selected_format):
        """
        User ki select ki hui quality/format ke mutabiq download shuru karta hai.
        """
        url = self.url_input_text.strip()
        # Download item ko DownloadsScreen mein add karein
        App.get_running_app().root.ids.screen_manager.get_screen('downloads_screen').add_download(url, selected_format)
        self.update_status(f"[color=0000ff]Download shuru: {selected_format.get('format_note', 'Selected Format')}[/color]")
        # Downloads screen par switch karein
        App.get_running_app().root.ids.screen_manager.current = 'downloads_screen'

    def handle_android_intent(self, dt):
        """Android Share Intent se URL capture karta hai."""
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            
            intent = PythonActivity.mActivity.getIntent()
            action = intent.getAction()
            
            if action == Intent.ACTION_SEND:
                shared_text = intent.getStringExtra(Intent.EXTRA_TEXT)
                if shared_text and self.is_valid_youtube_url(shared_text):
                    self.url_input.text = shared_text
                    self.update_status("[color=000080]YouTube link share intent se mila.[/color]")
                    # Link milte hi quality popup open karein
                    Clock.schedule_once(lambda dt: self.open_quality_popup(None), 0.5) # Thodi der baad open karein
                else:
                    self.update_status("[color=ff8c00]Share intent mila, lekin valid YouTube link nahi.[/color]")
            
            # Intent ko clear karein taake app dobara launch hone par purana intent na uthaye
            # Yeh step ahem hai taake har launch par naya intent hi process ho
            intent.setAction(Intent.ACTION_MAIN)
            intent.removeCategory(Intent.CATEGORY_LAUNCHER)
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED)
            PythonActivity.mActivity.setIntent(intent)

class DownloadsScreen(Screen):
    """
    App ki downloads manager screen jahan ongoing aur completed downloads show hote hain.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'downloads_screen' # ID for easy access
        
        main_layout = BoxLayout(orientation='vertical')
        
        main_layout.add_widget(Label(text='[b]Downloads[/b]', markup=True,
                                     font_size='24sp', size_hint_y=0.1))

        self.downloads_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.downloads_grid.bind(minimum_height=self.downloads_grid.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.downloads_grid)
        main_layout.add_widget(scroll_view)
        
        self.add_widget(main_layout)

    def add_download(self, url, selected_format):
        """Nayi download item ko list mein add karta hai."""
        # yt-dlp se video title fetch karein
        title = "Downloading..."
        try:
            ydl_opts = {'quiet': True, 'skip_download': True, 'forcejson': True, 'simulate': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Video')
        except Exception as e:
            print(f"Error fetching title: {e}")
            title = "Unknown Video"

        item = DownloadItem(url, title, selected_format)
        self.downloads_grid.add_widget(item)

class FastTubeApp(App):
    """
    FastTube Kivy Application ki main class.
    """
    def build(self):
        self.title = 'FastTube' # App ka naam

        sm = ScreenManager(id='screen_manager') # ScreenManager ko ID dein
        sm.add_widget(MainScreen(name='main_screen')) # MainScreen ko ID dein
        sm.add_widget(DownloadsScreen(name='downloads_screen')) # DownloadsScreen ko ID dein

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(sm)

        # Bottom Navigation Bar
        nav_bar = BoxLayout(size_hint_y=0.1, height=50) # Fixed height for nav bar
        
        btn_home = Button(
            text='[b]🏠 Home[/b]',
            markup=True,
            font_size='16sp',
            background_normal='',
            background_color=(0.1, 0.1, 0.1, 1) # Dark background
        )
        btn_downloads = Button(
            text='[b]⬇ Downloads[/b]',
            markup=True,
            font_size='16sp',
            background_normal='',
            background_color=(0.1, 0.1, 0.1, 1) # Dark background
        )
        
        btn_home.bind(on_press=lambda x: setattr(sm, 'current', 'main_screen'))
        btn_downloads.bind(on_press=lambda x: setattr(sm, 'current', 'downloads_screen'))
        
        nav_bar.add_widget(btn_home)
        nav_bar.add_widget(btn_downloads)

        root_layout.add_widget(nav_bar)
        
        return root_layout

if __name__ == '__main__':
    FastTubeApp().run()
