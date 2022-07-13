
#
import sys,os,cv2

sys.path.append(os.getcwd() + "\marrtino_apps\program")

#from robot_cmd_ros import *

#testare!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def detectGuest():
    while True:
        img = getImage()
        faces = fixedFaceDetection(img)
        if len(faces) > 1 :
            #dialogo per far si che si mostri un guest alla volta
            say("sorry i can detect one guest at time, now i see " + len(faces) + " faces, please show me one face at time, thank you" )
        else :
            return None



def findCascadeModel():
    trylist = ['//usr//share//opencv//', '//opt//ros//kinetic//share//OpenCV-3.3.1-dev//','' ]
    for t in trylist:
        f = t + 'haarcascade_frontalface_default.xml'
        if os.path.isfile(f):
            return cv2.CascadeClassifier(f)
    return None

faceCascade = None

def fixedFaceDetection(img,size):
    global faceCascade
    if faceCascade is None:
        faceCascade = findCascadeModel()
        if faceCascade is None:
            print("ERROR Cannot find Haar cascade model")
            return -1
    if img is None:
        print("ERROR No image")
        return -1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize= size
    )
    return faces


def findChairs(directions):
    # correggere in base a directions
    deg=4/directions
    n=0
    while n <4:
        right(deg)
        #trova sedia
        n+=deg


