'''
kivyFaceRecognition Example (Based on Kivys "Camera Example")
====================================================

This example demonstrates a simple use of the camera with face detection.
It shows a window with buttons "Play", "Face detection" and "Capture".
Note that not finding a camera, perhaps because gstreamer is not installed,
will throw an exception during the kv language processing.
'''

import time
import os
from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from facecamera import FaceCamera


Builder.load_string('''

<CameraClick>:
    face_camera: camera
    orientation: 'vertical'

    FaceCamera:
        id: camera
        size_hint_y: None
        pos: self.x, dp(48)
        height: root.height - dp(48)
        allow_stretch: True
        keep_ratio: False
        resolution: (1280, 720)
        play: True

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '48dp'

        ToggleButton:
            text: 'Pause'
            state: 'down'
            on_press:
                camera.play = not camera.play
                self.text = 'Pause' if self.text == 'Play' else 'Play'

        ToggleButton:
            text: 'Face detection'
            state: 'down'
            on_press:
                camera.enable_face_detection = not camera.enable_face_detection

        Button:
            text: 'Capture'
            on_press: root.capture()
''')


class CameraClick(FloatLayout):

    face_camera = ObjectProperty()
    '''
    Reference to camera instance.
    '''

    def on_face_camera(self, ins, camera):
        # Crée une liste des noms de fichiers dans le dossier "know_faces"
        image_folder = "./assets/know_faces"
        image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

        # Enregistre chaque personne avec son image correspondante
        for image_file in image_files:
           name = image_file.split("_")[0]  # Coupe le nom au niveau du caractère "_"
           image_path = os.path.join(image_folder, image_file)
        camera.register_person("Tonde", "./assets/know_faces/Test.png")
        


    def capture(self):
        """
        Capture an image and save it by using the current timestamp as name.
        """
        # show camera shutter flash
        Animation.cancel_all(self.face_camera)
        anim = Animation(opacity=0.0, duration=0.125)
        anim += Animation(opacity=1.0, duration=0.125)
        anim.start(self.face_camera)

        # capture picture from texture
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.face_camera.capture_image("IMG_{}.png".format(timestr))


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
