import cv2
import requests
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from kivy.uix.gridlayout import GridLayout

class CameraApp(App):
    capture = None
    process_current_frame = False
    baseURL = "https://www.maillot-can.me/face_recognition"
    cascadeURL = "assets/haarcascade_frontalface_default.xml"
    recognized_faces = []

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.my_camera = Image()
        layout.add_widget(self.my_camera)

        button_layout = GridLayout(cols=2, size_hint_y=None, height=50)
        self.start_button = Button(text="Start")
        self.start_button.bind(on_press=self.start_camera)
        button_layout.add_widget(self.start_button)

        self.stop_button = Button(text="Stop", disabled=True)
        self.stop_button.bind(on_press=self.stop_camera)
        button_layout.add_widget(self.stop_button)

        layout.add_widget(button_layout)

        Clock.schedule_interval(self.update, 1.0 / 5.0)
        return layout

    def start_camera(self, instance):
        self.capture = cv2.VideoCapture(0)
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.process_current_frame = True

    def stop_camera(self, instance):
        if self.capture:
            self.capture.release()
            self.start_button.disabled = False
            self.stop_button.disabled = True
            self.process_current_frame = False
            self.recognized_faces = []

    def update(self, dt):
        if self.capture and self.process_current_frame:
            ret, frame = self.capture.read()
            if ret:
                # Inverse horizontalement pour corriger la vue inversée
                frame = cv2.flip(frame, 1)

                # Detect faces in the frame using the Haar Cascade classifier
                face_cascade = cv2.CascadeClassifier(self.cascadeURL)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

                # Send the detected faces to the backend for recognition
                self.recognized_faces = []

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # Extract the detected face
                    detected_face = frame[y:y+h, x:x+w]

                    # Send the detected face to the backend for recognition
                    _, img_encoded = cv2.imencode('.jpg', detected_face)
                    response = requests.post(self.baseURL, files={'image': img_encoded.tostring()})

                    if response.status_code == 200:
                        face_data = response.json()
                        recognized_names = face_data.get("face_names")
                        self.recognized_faces.append((x, y, w, h, recognized_names))

                for (x, y, w, h, names) in self.recognized_faces:
                    for name in names:
                        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                buf1 = cv2.flip(frame, 0).tobytes()
                texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture1.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
                self.my_camera.texture = texture1

if __name__ == '__main__':
    CameraApp().run()
