from django.shortcuts import render
import socket
import cv2
from .models import FacialExpressionModel
import numpy as np


# Create your views here.
class Chatting:
    def __init__(self):
        # self.textmessages=[]
        # self.mymessages=[]
        self.reactionmessages=[]
        self.name={'192.168.0.11':"Aditya"}
        # self.lenother=0
        # self.lenself=0
        self.messagelist=[]

    def home(self, request):
        return render(request, 'connection.html')

    def add(self, request):
        self.facec = cv2.CascadeClassifier('static/jsfile/haarcascade_frontalface_default.xml')
        self.model = FacialExpressionModel()
        self.cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        host=request.POST["host"]
        self.servername = host
        if host in self.name:
            self.servername=self.name[host]
        self.s = socket.socket()
        port=8080
        self.s.connect((host, port))
        incoming_message1 = self.s.recv(1024)
        incoming_message1 = incoming_message1.decode()
        # self.textmessages.append(incoming_message1)
        # self.lenother+=1

        incoming_message2 = self.s.recv(1024)
        incoming_message2 = incoming_message2.decode()
        self.reactionmessages.append(incoming_message2)

        self.messagelist=[[incoming_message1, ""]]
        if incoming_message2=="angry":
            list=['Dont lose patience, everything shall be fine', 'I understand your disagreement, but have patience', 'Anger is not good for health']

        elif incoming_message2=="disgust":
            list=['I am sorry if I offended you', 'I did not mean that', 'I am sorry']

        elif incoming_message2=="afraid":
            list=['Have faith in God', 'Do you want me next to you', 'Are you okay? You can share with me.']
        elif incoming_message2=="happy":
            list=['May I also know the joke', 'Very happy for you']
        elif incoming_message2=="neutral":
            list=['Good Morning', 'Good night', 'Hi', 'Hello']
        elif incoming_message2=="sad":
            list=['Cheer up dear, everything shall be fine', 'Your mood really effects me', 'Cannot see you like that', 'Tell what I can do for you']
        else:
            list=['Its too good but yes true', 'You read it correct :)']

        # return render(request, 'home.html', {'msg_from_server':self.textmessages, 'reaction_of_server':self.reactionmessages, 'servername':self.servername, 'mymessage':self.mymessages})
        # return render(request, 'home.html',{'msg_from_server': incoming_message1})
        return render(request, 'home.html',
                      {'reaction_of_server': self.reactionmessages,
                       'servername': self.servername,
                       'messagelist': self.messagelist, 'list':list})

    def sendmsg(self, request):
        message = request.POST["msg_from_client"]
        message_decoded=message
        # self.mymessages.append(message)
        # self.lenself+=1
        message = message.encode()

        self.s.send(message)

        ret, frame = self.cam.read()

        gray_fr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pred="Happy"
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
        # self.textmessages.append(incoming_message1)
        # self.lenother+=1
        incoming_message2 = self.s.recv(1024)
        incoming_message2 = incoming_message2.decode()
        self.reactionmessages.append(incoming_message2)
        if incoming_message2=="angry":
            list=['Dont lose patience, everything shall be fine', 'I understand your disagreement, but have patience', 'Anger is not good for health']

        elif incoming_message2=="disgust":
            list=['I am sorry if I offended you', 'I did not mean that', 'I am sorry']

        elif incoming_message2=="afraid":
            list=['Have faith in God', 'Do you want me next to you', 'Are you okay? You can share with me.']
        elif incoming_message2=="happy":
            list=['May I also know the joke', 'Very happy for you']
        elif incoming_message2=="neutral":
            list=['Good Morning', 'Good night', 'Hi', 'Hello']
        elif incoming_message2=="sad":
            list=['Cheer up dear, everything shall be fine', 'Your mood really effects me', 'Cannot see you like that', 'Tell what I can do for you']
        else:
            list=['Its too good but yes true', 'You read it correct :)']
        # for i in range(self.lenother):
        #     if i<self.lenself:
        #         self.messagelist.append([self.textmessages[i], self.mymessages[i]])
        #     else:
        #         self.messagelist.append([self.textmessages[i], ""])
        self.messagelist[-1][1]=message_decoded
        self.messagelist.append([incoming_message1, ""])

        return render(request, 'home.html', {'reaction_of_server':self.reactionmessages,
                                             'servername':self.servername, 'messagelist': self.messagelist, 'list':list})
        # return render(request, 'home.html', {'msg_from_server': incoming_message1})