import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import cv2
import winsound
from matplotlib import pyplot as plt
import pyfirmata as f
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


run=True
def Led_ON():
    arduino = f.Arduino("COM3")
    while True:
        arduino.digital[3].write(1)
def Led_OFF():
    arduino = f.Arduino("COM3")
    while True:
        arduino.digital[3].write(0)

def take_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('webcamphoto.jpg', frame)
    cap.release()

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'primo' in command:
                command = command.replace('primo', '')
                print(command)
    except:
        pass
    return command


def run_assitant():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        if person== '':
            talk('Please tell me what you wanna know')
        else:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'take picture' in command:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        print(ret)
        print(frame)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        take_photo()
        plt.show()
        cap.release()
        talk('its Done       your pic in the project file')
    elif 'open security cam' in command:
        cam = cv2.VideoCapture(0)
        while cam.isOpened():
            ret, frame1 = cam.read()
            ret, frame2 = cam.read()
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
            for c in contours:
                if cv2.contourArea(c) < 5000:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if 'picture' in command:
                    take_photo()
                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
            if cv2.waitKey(10) == ord('q'):
                break
            cv2.imshow('Security Cam', frame1)
    elif 'switch on' in command:
        Led_ON()
    elif 'switch off' in command:
        Led_OFF()
    elif 'goodbye' in command:
        talk('have a nice day sir')
    else:
        talk('Please say the command again.')


while run==True:
    run_assitant()