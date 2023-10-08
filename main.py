from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import time
import webbrowser  

Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        """
        starts camera and changes the button text
        """
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """stops the camera and changes the button text
        """
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None
    
    def capture(self):
        """creates a filename with the current time and 
        captures and saves a photo under the filename
        """
        current_timee = time.strftime('%Y%m%d-%H%H%S')
        self.filepath = "files/{current_timee}.png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_sceen.ids.img.source = self.filepath

class ImageScreen(Screen):
    link_message = 'Create a link first'
    def create_link(self):
        """Access the photo filepath, uploads it to the wen
        and inserts the link in the label widget
        """
        file_path = App.get_running_app().root.ids\
            .camera_screen.filepath
        filesharer = FileSharer(filepath=file_path)
        self.url = filesharer.share()
        self.ids.link.text = self.url
    
    def copy_link(self):
        """Copy link to the clipboard available for pasting
        """
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message
    
    def open_link(self):
        """Open link in the default webbrowser
        """
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    

MainApp().run()