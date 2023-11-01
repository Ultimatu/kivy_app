from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window

class SelfieApp(App):
    def build(self):
        self.camera = Camera(resolution=(640, 480), play=True)
        self.camera.keep_ratio = False
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.camera)

        self.label = Label(text="Prenez un selfie!")
        self.button = Button(text="Prendre une photo")
        self.button.bind(on_press=self.take_picture)
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        
        return layout

    def take_picture(self, instance):
        self.label.text = "Traitement de la photo..."
        self.camera.export_to_png("selfie.png")
        self.label.text = "Selfie sauvegardé sous selfie.png"

if __name__ == '__main__':
    SelfieApp().run()
