
from robot_cmd_ros import *

import enum

class Gender(enum.Enum):
    male  = ("he","his" , "him")
    female = ("she", "her", "her")

def speakToGuest():
    
    say("hello , what's your name?")
    answ = name = ""
    findname = findrink = True
    gender = None
    while findname: 
        answ = asr()
        answ = adjustString(answ)
        answ = answ.strip("hello")
        answ = answ.strip("hi")
        answ = answ.strip("my name is")
        answ = answ.strip()
        if len(answ.split()) == 1:
            name = answ
            say("so your name is " + name + " right?")
            answ = asr()
            answ = adjustString(answ)
            if answ.find("yes") != -1 :
                findname = False
        if findname:
            say("sorry can you repeat your name")

    
    say("do you want me to refer you as male or female?")
    while gender == None :
        answ = asr()
        answ = adjustString(answ)
        if "female" in answ.split() :
            gender = Gender.female
        elif "male" in answ.split() :
            gender = Gender.male
        else:
            say("please choose male or female, the first one if you want me to use the pronoun he, or the second one if you want me to use the pronoun she")
    
    
    say("ok and what's your favourite drink " + name + "?")
    while findrink:
        answ = asr() 
        answ = adjustString(answ)
        answ = answ.strip("my favourite drink is")
        answ = answ.strip("i like")
        answ = answ.strip()
        drink = answ
        if answ == "i don't know" or answ == "i don't  have a favourite drink" or answ == "i haven't got a favourite drink":
            drink = " doesn't have a favourite drink"
            say("so you don't have a favourite drink, isn't it?")
        else:
            say("so your favourite drink is " + drink + "isn't it?")
        answ = asr()
        answ = adjustString(answ)
        if answ.find("yes") != -1 :
            findrink = False
        if findrink:
            say("then what's your favourite drink?")
    
    return (name,gender,drink)

def adjustString(string):
    newstring = string.lower()
    newstring = newstring.strip()
    newstring = newstring.strip("google")
    newstring = newstring.strip("sky")
    return newstring

def introduceGuest(name,gender,drink):
    say("hi john," + gender[0] + "  is " + name)
    if drink == " doesn't have a favourite drink":
        say(gender[0] + drink)
    else:
        say(gender[1] + " favourite drink is " + drink)
    


