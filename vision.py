
from robot_cmd_ros import *

#testare!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def detectGuest():
    while True:
        img = getImage()
        faces = faceDetection(img)
        if len(faces) == 1:
            #salvare info per riconoscere la faccia se si vuole riconoscere il guest
            pass
        elif len(faces) > 1 :
            #dialogo per far si che si mostri un guest alla volta
            say("sorry i can detect one guest at time, now i see " + len(faces) + " faces, please show me one face at time, thank you" )
        else :
            return None




def findChairs(directions):
    # correggere in base a directions
    deg=4/directions
    n=0
    while n <4:
        right(deg)
        #trova sedia
        n+=deg