from django.shortcuts import render
import socket
import cv2
from .models import FacialExpressionModel
import numpy as np


# Create your views here.
class Chatting:
    def home(self, request):
        return render(request, 'connection.html')

    def add(self, request):
        self.facec = cv2.CascadeClassifier('static/jsfile/haarcascade_frontalface_default.xml')
        self.model = FacialExpressionModel()
        self.cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        host=request.POST["host"]
        self.s = socket.socket()
        port=8080
        self.s.connect((host, port))
        incoming_message1 = self.s.recv(1024)
        incoming_message1 = incoming_message1.decode()

        incoming_message2 = self.s.recv(1024)
        incoming_message2 = incoming_message2.decode()

        return render(request, 'home.html', {'msg_from_server':incoming_message1, 'reaction_of_server':incoming_message2})
        # return render(request, 'home.html',{'msg_from_server': incoming_message1})

    def sendmsg(self, request):
        message = request.POST["msg_from_client"]
        message = message.encode()

        self.s.send(message)

        ret, frame = self.cam.read()

        gray_fr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pred="Default"
        faces = self.facec.detectMultiScale(gray_fr, 1.3, 5)
        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]
            roi = cv2.resize(fc, (48, 48))
            pred = self.model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        msg=pred

        msg = msg.encode()
        self.s.send(msg)

        incoming_message1 = self.s.recv(1024)
        incoming_message1 = incoming_message1.decode()
        incoming_message2 = self.s.recv(1024)
        incoming_message2 = incoming_message2.decode()

        return render(request, 'home.html', {'msg_from_server':incoming_message1, 'reaction_of_server':incoming_message2})
        # return render(request, 'home.html', {'msg_from_server': incoming_message1})