
from robot_cmd_ros import *

import enum

class Gender(enum.Enum):
    male  = ("he","his" , "him")
    female = ("she", "her", "her")

class Guest:
    def __init__(self,name,gender,drink):
        self.name = name
        self.gender = gender
        self.drink = drink
        




def speakToGuest():
    
    say("hello , what's your name?")
    answ = name = ""
    findname = findrink = True
    gender = None
    list=["hello","hi","my", "name", "is"]
    oldansw = ""
    while findname: 
        
        answ = asr()
        a = adjustString(answ,list)
        name = " ".join(a)
        if oldansw == name and name != "":
            findname = False
        elif name != "" :
            say("so your name is " + name + " right?")
        
            answ = asr()
            answ = adjustString(answ)
                
            if "yes" in answ :
                findname = False
            elif "no" in answ:
                oldansw = ""
        if findname:
            oldansw = name
            say("sorry can you repeat your name")

    
    say("do you want me to refer you as male or female?")
    while gender == None :
        answ = asr()
        answ = adjustString(answ)
        if isFemale(answ) :
            gender = Gender.female
        elif isMale(answ) :
            gender = Gender.male
        else:
            say("please choose male or female, the first one if you want me to use the pronoun he, or the second one if you want me to use the pronoun she")
    

    
    say("ok and what's your favourite drink " + name + "?")
    list = ["my", "favourite", "drink", "is", "i", "like"]
    oldansw=""
    while findrink:
        answ = asr() 
        answ = adjustString(answ,list)
        
        drink = " ".join(answ)
        if drink == oldansw and drink != "":
            findrink = False
        elif drink != "":
            if  "don't" in answ or  "not" in answ or "haven't" in answ or "no" in answ:
                drink = " doesn't have a favourite drink"
                say("so you don't have a favourite drink, isn't it?")
            else:
                say("so your favourite drink is " + drink + "isn't it?")
            answ = asr()
            answ = adjustString(answ)
            if "yes" in answ :
                findrink = False
            elif "no" in answ:
                oldansw = ""
        if findrink:
            oldansw = drink
            say("then what's your favourite drink?")
    say("ok thank you")
    return Guest(name,gender,drink)

def isFemale(list):
    return "female" in list or "she" in list or "woman" in list or "girl" in list or "second" in list
def isMale(list):
    return "male" in list or "he" in list or "man" in list or "boy" in list or "first" in list

def adjustString(string,list=[]):
    newstring = string.lower()
    newstring = newstring.strip()
    newstring = newstring.split()

    list.append("google")
    list.append("sky")
    
    for x in range(len(newstring)-1,-1,-1):
        if newstring[x] in list:
            newstring.pop(x)


    return newstring

def introduceGuest(guest):
    gender=guest.genere.value
    say("hi john," + gender[0] + "  is " + guest.name)
    if guest.drink == " doesn't have a favourite drink":
        say(gender[0] + guest.drink)
    else:
        say(gender[1] + " favourite drink is " + guest.drink)
    


