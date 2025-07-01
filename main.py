# -*- coding: utf-8 -*-
# Kivy framework import karein
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform

# Python ke built-in modules import karein
import threading
import os
import sys
import json
import time

# yt-dlp aur requests library import karein
try:
    import yt_dlp
    import requests
except ImportError:
    # Agar libraries install na hon to error message den
    print("yt-dlp or requests not installed. Please run 'pip install yt-dlp requests certifi'")
    sys.exit(1)

# Pyjnius import karein Android-specific functionalities ke liye
# Yeh sirf Android par chalega
if platform == 'android':
    try:
        from jnius import autoclass, cast
        # Android classes ko import karein
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        String = autoclass('java.lang.String')
        Context = autoclass('android.content.Context')
        File = autoclass('java.io.File')
        Environment = autoclass('android.os.Environment')
        PackageManager = autoclass('android.content.pm.PackageManager')
        Toast = autoclass('android.widget.Toast')

        # Permissions check karein
        # STORAGE_PERMISSION_REQUEST_CODE = 1
        # def request_permissions():
        #     from android.permissions import request_permissions, Permission
        #     request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    except Exception as e:
        print(f"Pyjnius or Android classes import failed: {e}")
        # Agar pyjnius na mile to Android-specific features disable kar den
        platform = 'other' # Platform ko 'other' set kar den taake error na aaye

# Kivy UI layout ko define karein (KV language)
KV = """
#:import C kivy.utils.get_color_from_hex
<DownloadItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(100)
    padding: dp(10)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: C('#F3F4F6') if self.index % 2 == 0 else C('#E5E7EB') # Background color for rows
        Rectangle:
            pos: self.pos
            size: self.size
    
    AsyncImage:
        id: thumbnail_image
        source: root.thumbnail # Video thumbnail
        size_hint: None, None
        size: dp(80), dp(80)
        allow_stretch: True
        keep_ratio: True
        canvas.before:
            Color:
                rgba: 0.8, 0.8, 0.8, 1
            Rectangle:
                pos: self.pos
                size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(5)
        spacing: dp(5)
        Label:
            id: title_label
            text: root.video_title # Video ka title
            font_size: '16sp'
            color: C('#374151')
            halign: 'left'
            valign: 'top'
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
        Label:
            id: progress_label
            text: root.progress_text # Download progress (e.g., 50% - 1.2MB/s)
            font_size: '14sp'
            color: C('#6B7280')
            halign: 'left'
            valign: 'top'
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1]
        ProgressBar:
            id: progress_bar
            value: root.progress_value # Progress bar value (0-100)
            size_hint_y: None
            height: dp(10)
            max: 100
            color: C('#22C55E') # Green color for progress

    BoxLayout:
        orientation: 'vertical'
        size_hint_x: None
        width: dp(60)
        spacing: dp(5)
        Button:
            id: action_button
            text: root.action_text # Pause/Resume/Cancel
            font_size: '12sp'
            background_normal: ''
            background_color: C('#3B82F6') if root.action_text == 'Pause' else C('#F97316') if root.action_text == 'Resume' else C('#EF4444')
            color: C('#FFFFFF')
            on_release: app.root.download_manager.toggle_download_status(root.download_id)
            size_hint_y: None
            height: dp(35)
        Button:
            text: 'Delete'
            font_size: '12sp'
            background_normal: ''
            background_color: C('#DC2626')
            color: C('#FFFFFF')
            on_release: app.root.download_manager.delete_download(root.download_id)
            size_hint_y: None
            height: dp(35)

<FastTubeAppLayout>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    
    # Top Section: Search Bar
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        TextInput:
            id: url_input
            hint_text: 'Video URL paste karein ya search karein...'
            multiline: False
            size_hint_x: 0.8
            font_size: '18sp'
            padding: [dp(10), dp(10), dp(10), dp(10)]
            background_normal: ''
            background_active: ''
            background_color: C('#F3F4F6')
            foreground_color: C('#374151')
            cursor_color: C('#10B981')
            halign: 'left'
            on_text_validate: app.root.search_or_process_url(self.text)
        Button:
            text: 'Search'
            size_hint_x: 0.2
            font_size: '18sp'
            background_normal: ''
            background_color: C('#10B981') # Green color
            color: C('#FFFFFF')
            on_release: app.root.search_or_process_url(url_input.text)
    
    # Main Content Area: Download List
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 1
        Label:
            text: 'Ongoing Downloads'
            font_size: '20sp'
            color: C('#374151')
            size_hint_y: None
            height: dp(40)
            halign: 'left'
            valign: 'middle'
            text_size: self.width, None
            padding_x: dp(10)

        RecycleView:
            id: rv_downloads
            viewclass: 'DownloadItem'
            data: app.root.download_manager.download_data
            size_hint_y: 1
            bar_width: dp(10)
            scroll_type: ['bars', 'content']
            do_scroll_x: False
            do_scroll_y: True
            RecycleBoxLayout:
                default_size: None, dp(100)
                default_size_hint: 1, None
                orientation: 'vertical'
                spacing: dp(5)
                padding: dp(5)
                size_hint_y: None
                height: self.minimum_height
                key_viewclass: 'viewclass'

    # Bottom Navigation
    BoxLayout:
        size_hint_y: None
        height: dp(60)
        canvas.before:
            Color:
                rgba: C('#FFFFFF')
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: 'Download'
            font_size: '14sp'
            background_normal: ''
            background_color: C('#10B981')
            color: C('#FFFFFF')
            # on_release: app.root.show_download_screen()
        Button:
            text: 'Play'
            font_size: '14sp'
            background_normal: ''
            background_color: C('#6B7280')
            color: C('#FFFFFF')
            # on_release: app.root.show_play_screen()
        Button:
            text: 'Settings'
            font_size: '14sp'
            background_normal: ''
            background_color: C('#6B7280')
            color: C('#FFFFFF')
            # on_release: app.root.show_settings_screen()
"""

# DownloadItem class for RecycleView
class DownloadItem(RecycleDataViewBehavior, BoxLayout):
    video_title = StringProperty('')
    progress_text = StringProperty('')
    progress_value = NumericProperty(0)
    thumbnail = StringProperty('')
    download_id = StringProperty('')
    action_text = StringProperty('Pause') # Default action text

    def refresh_view_attrs(self, rv, index, data):
        self.download_id = data['download_id']
        self.video_title = data['video_title']
        self.progress_text = data['progress_text']
        self.progress_value = data['progress_value']
        self.thumbnail = data['thumbnail']
        self.action_text = data['action_text']
        return super().refresh_view_attrs(rv, index, data)

# DownloadManager class to handle download logic and state
class DownloadManager:
    def __init__(self):
        self.downloads = {} # Dictionary to store download info: {id: {data, thread, status}}
        self.download_data = [] # List for RecycleView data
        self.next_download_id = 0
        self.download_folder = self.get_download_folder()

        # Download folder banayen agar mojood nahi hai
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"Download folder created: {self.download_folder}")

    def get_download_folder(self):
        # Android par public download folder istemal karein
        if platform == 'android':
            # Android/data/com.fasttube.app/files/Download
            # Ya direct public Downloads folder
            # external_storage_path = os.path.abspath(os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), 'Download'))
            # return external_storage_path
            return str(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS).getAbsolutePath())
        else:
            # Desktop par current directory mein 'downloads' folder
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

    def add_download(self, url, format_id='best', title='Unknown Title', thumbnail=''):
        download_id = str(self.next_download_id)
        self.next_download_id += 1

        download_info = {
            'download_id': download_id,
            'url': url,
            'format_id': format_id,
            'video_title': title,
            'thumbnail': thumbnail,
            'progress_text': 'Waiting...',
            'progress_value': 0,
            'status': 'pending', # pending, downloading, paused, completed, failed
            'action_text': 'Pause',
            'thread': None,
            'start_time': 0,
            'total_bytes': 0,
            'downloaded_bytes': 0
        }
        self.downloads[download_id] = download_info
        self.download_data.append({
            'viewclass': 'DownloadItem',
            **download_info
        })
        self.update_recycleview()
        self.start_download(download_id)
        return download_id

    def update_recycleview(self):
        # RecycleView ko update karne ke liye data list ko naya banayen
        # Kivy mein RecycleView ko refresh karne ka yeh tareeqa hai
        self.download_data = self.download_data[:]
        App.get_running_app().root.ids.rv_downloads.data = self.download_data

    def start_download(self, download_id):
        download = self.downloads[download_id]
        if download['status'] == 'pending' or download['status'] == 'paused':
            download['status'] = 'downloading'
            download['action_text'] = 'Pause'
            download['start_time'] = time.time() # Download start time

            # Download thread start karein
            download['thread'] = threading.Thread(target=self._download_task, args=(download_id,))
            download['thread'].daemon = True # App band hone par thread bhi band ho jaye
            download['thread'].start()
            self.update_recycleview()

    def toggle_download_status(self, download_id):
        download = self.downloads.get(download_id)
        if not download:
            return

        if download['status'] == 'downloading':
            download['status'] = 'paused'
            download['action_text'] = 'Resume'
            # Yahan thread ko pause karne ki logic aayegi (yt-dlp mein direct pause nahi hota, toh restart karna padega)
            # Filhal sirf status update karein
            Clock.schedule_once(lambda dt: self.update_recycleview(), 0) # UI update karein
        elif download['status'] == 'paused':
            download['status'] = 'pending' # Restarting as pending
            download['action_text'] = 'Pause'
            Clock.schedule_once(lambda dt: self.update_recycleview(), 0) # UI update karein
            self.start_download(download_id) # Download dobara start karein

    def delete_download(self, download_id):
        if download_id in self.downloads:
            # Agar download chal rahi ho to usay rok den
            if self.downloads[download_id]['status'] == 'downloading':
                self.downloads[download_id]['status'] = 'cancelled' # Thread ko cancel hone ka signal den
                # Yahan thread ko force stop karne ki logic aayegi agar zaroori ho

            # File ko delete karein
            file_path = os.path.join(self.download_folder, f"{self.downloads[download_id]['video_title']}.mp4") # Ya jo bhi format ho
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"File deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

            # Download data se remove karein
            self.downloads.pop(download_id)
            self.download_data = [item for item in self.download_data if item['download_id'] != download_id]
            self.update_recycleview()
            self.show_toast(f"Download deleted: {download_id}") # User ko message den

    def _download_task(self, download_id):
        download = self.downloads[download_id]
        url = download['url']
        format_id = download['format_id']
        output_template = os.path.join(self.download_folder, '%(title)s.%(ext)s')

        # yt-dlp hook function for progress updates
        def progress_hook(d):
            if download['status'] == 'cancelled':
                raise yt_dlp.utils.DownloadError("Download cancelled by user.")

            if d['status'] == 'downloading':
                download['downloaded_bytes'] = d.get('downloaded_bytes', 0)
                download['total_bytes'] = d.get('total_bytes', d.get('total_bytes_estimate', 0))
                
                p = d.get('fragment_index', 0) / d['fragment_count'] * 100 if 'fragment_index' in d and 'fragment_count' in d else d.get('percent', 0)
                speed = d.get('speed', 0)
                
                download['progress_value'] = p
                
                # Speed ko human-readable format mein convert karein
                speed_str = f"{speed / 1024:.2f} KiB/s" if speed < 1024*1024 else f"{speed / (1024*1024):.2f} MiB/s"
                
                # Total size ko human-readable format mein convert karein
                total_size_str = f"{download['total_bytes'] / (1024*1024):.2f} MiB" if download['total_bytes'] > 0 else "N/A"

                download['progress_text'] = f"{p:.1f}% - {speed_str} ({total_size_str})"
                
                # UI update ko main thread par schedule karein
                Clock.schedule_once(lambda dt: self.update_recycleview(), 0)
            elif d['status'] == 'finished':
                download['status'] = 'completed'
                download['progress_text'] = 'Completed!'
                download['progress_value'] = 100
                download['action_text'] = 'Done'
                Clock.schedule_once(lambda dt: self.update_recycleview(), 0)
                Clock.schedule_once(lambda dt: self.show_toast(f"Download completed: {download['video_title']}"), 0)
            elif d['status'] == 'error':
                download['status'] = 'failed'
                download['progress_text'] = f"Failed: {d.get('error', 'Unknown error')}"
                download['action_text'] = 'Retry'
                Clock.schedule_once(lambda dt: self.update_recycleview(), 0)
                Clock.schedule_once(lambda dt: self.show_toast(f"Download failed: {download['video_title']}"), 0)

        ydl_opts = {
            'format': format_id,
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'noplaylist': True, # Sirf single video download karein
            'retries': 5, # Download retries
            'fragment_retries': 5,
            'ignoreerrors': True, # Errors ko ignore karein taake process continue ho
            'postprocessors': [{ # MP3 conversion ke liye
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if 'audio' in format_id else [], # Agar audio format select kiya gaya ho
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Video info fetch karein
                info = ydl.extract_info(url, download=False)
                download['video_title'] = info.get('title', 'Unknown Title')
                download['thumbnail'] = info.get('thumbnail', '')
                
                # Agar download resume ho rahi ho
                if download['downloaded_bytes'] > 0 and 'total_bytes' in download and download['total_bytes'] > 0:
                    ydl_opts['continuedl'] = True # Resume download
                    ydl_opts['noprogress'] = True # Progress hook handle karega

                # Download start karein
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            if "Download cancelled by user" in str(e):
                print(f"Download {download_id} cancelled.")
            else:
                print(f"Download error for {url}: {e}")
                download['status'] = 'failed'
                download['progress_text'] = f"Failed: {e}"
                Clock.schedule_once(lambda dt: self.update_recycleview(), 0)
                Clock.schedule_once(lambda dt: self.show_toast(f"Download failed: {download['video_title']}"), 0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            download['status'] = 'failed'
            download['progress_text'] = f"Failed: {e}"
            Clock.schedule_once(lambda dt: self.update_recycleview(), 0)
            Clock.schedule_once(lambda dt: self.show_toast(f"Download failed: {download['video_title']}"), 0)

    def show_toast(self, message):
        if platform == 'android':
            Toast.makeText(PythonActivity.mActivity, String(message), Toast.LENGTH_SHORT).show()
        else:
            print(f"TOAST: {message}") # Desktop par console output

# Main Kivy App Layout
class FastTubeAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_manager = DownloadManager()
        
        # Share Intent handling (Android only)
        if platform == 'android':
            self.handle_share_intent()
            # Permissions request
            # request_permissions()

    def handle_share_intent(self):
        # Intent data ko process karein
        intent = PythonActivity.get = PythonActivity.getIntent()
        action = intent.getAction()
        type = intent.getType()

        if action == Intent.ACTION_SEND and type == 'text/plain':
            shared_text = intent.getStringExtra(Intent.EXTRA_TEXT)
            if shared_text:
                print(f"Shared text received: {shared_text}")
                self.ids.url_input.text = shared_text # Input field mein link paste karein
                self.show_quality_selection(shared_text) # Quality selection show karein

    def search_or_process_url(self, query):
        if query.startswith('http'):
            self.show_quality_selection(query)
        else:
            self.perform_search(query)

    def perform_search(self, query):
        # Search logic yahan aayegi
        # Filhal demo ke liye
        self.show_toast(f"Searching for: {query}")
        print(f"Searching for: {query}")
        # Placeholder: yt-dlp se search results la sakte hain
        # ya kisi search API ka istemal kar sakte hain

    def show_quality_selection(self, url):
        # Video details fetch karein aur quality options show karein
        self.show_toast(f"Fetching details for: {url}")
        print(f"Fetching details for: {url}")
        
        # Ek naya thread start karein taake UI block na ho
        threading.Thread(target=self._fetch_and_show_formats, args=(url,)).start()

    def _fetch_and_show_formats(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'force_generic_extractor': False, # YT-DLP ko site detect karne den
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                video_title = info.get('title', 'Unknown Title')
                thumbnail = info.get('thumbnail', '')

                # Formats ko filter aur organize karein
                available_formats = []
                for f in formats:
                    if f.get('ext') in ['mp4', 'webm', 'm4a'] and f.get('acodec') != 'none': # Video with audio
                        if f.get('vcodec') != 'none': # Video format
                            quality = f.get('resolution', 'N/A')
                            if quality == 'N/A' and f.get('height'):
                                quality = f"{f['height']}p"
                            available_formats.append({
                                'format_id': f['format_id'],
                                'description': f"{quality} ({f.get('ext')})",
                                'size': f.get('filesize', f.get('filesize_approx', 0))
                            })
                        elif f.get('acodec') != 'none' and f.get('vcodec') == 'none': # Audio only
                            available_formats.append({
                                'format_id': f['format_id'],
                                'description': f"Audio only ({f.get('acodec')}) - {f.get('abr', 'N/A')}k",
                                'size': f.get('filesize', f.get('filesize_approx', 0))
                            })
                
                # Sort by quality/size
                available_formats.sort(key=lambda x: x['size'] if x['size'] else 0, reverse=True)

                # UI ko main thread par update karein
                Clock.schedule_once(lambda dt: self._display_format_options(url, video_title, thumbnail, available_formats), 0)

        except yt_dlp.utils.DownloadError as e:
            error_msg = f"Error fetching details: {e}"
            print(error_msg)
            Clock.schedule_once(lambda dt: self.show_toast(error_msg), 0)
        except Exception as e:
            error_msg = f"An unexpected error occurred while fetching formats: {e}"
            print(error_msg)
            Clock.schedule_once(lambda dt: self.show_toast(error_msg), 0)

    def _display_format_options(self, url, video_title, thumbnail, formats):
        # Yahan ek pop-up ya modal banayenge jo quality options show karega
        # Filhal, demo ke liye pehla option download kar denge
        if formats:
            selected_format = formats[0] # Pehla (highest quality) select karein demo ke liye
            self.download_manager.add_download(
                url,
                selected_format['format_id'],
                video_title,
                thumbnail
            )
            self.show_toast(f"Download started: {video_title}")
        else:
            self.show_toast("No downloadable formats found.")

    def show_toast(self, message):
        self.download_manager.show_toast(message) # DownloadManager ke toast function ko call karein

# Main App class
class FastTubeApp(App):
    def build(self):
        # Kivy UI layout ko load karein
        self.root = Builder.load_string(KV)
        return self.root

    def on_start(self):
        # App start hone par permissions request karein (Android only)
        # if platform == 'android':
        #     request_permissions()
        pass # Filhal permissions ko Buildozer handle karega

    def on_pause(self):
        # App pause hone par downloads ko pause karne ki logic yahan aayegi
        return True # True return karna zaroori hai

    def on_resume(self):
        # App resume hone par downloads ko resume karne ki logic yahan aayegi
        pass

if __name__ == '__main__':
    FastTubeApp().run()
