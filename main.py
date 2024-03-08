import machine
import random
import utime
from machine import Pin
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR = 0x3f
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 16


i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()

testbutton1 = Pin(2, Pin.IN, Pin.PULL_DOWN)
testbutton2 = Pin(3, Pin.IN, Pin.PULL_DOWN)
testbutton3 = Pin(4, Pin.IN, Pin.PULL_DOWN)

cur = ''
ttype = ''
num1 = 0;
answer = 0;
testing = False

def addnum(num):
    global cur
    if len(cur) < 16:
        cur += str(num)
        print(cur)
        lcd.clear()
        lcd.putstr(cur)
        lcd.show_cursor()
        
def settype(newtype):
    global ttype
    global cur
    global num1
    ttype = str(newtype)
    num1 = float(cur)
    cur = ''
    lcd.clear()
def calc(t):
    global ttype
    global cur
    global num1
    global answer
    if ttype == 'add':
        answer = num1 + float(cur)
    if ttype == 'sub':
        answer = num1 - float(cur)
    if ttype == 'mult':
        answer = num1 * float(cur)
    if ttype == 'div':
        answer = num1 / float(cur)
    newansw = str(answer)
    if len(newansw) > 16:
        print(newansw + ':' + str(len(newansw)))
        toremove = len(newansw) - 16
        newansw = newansw[0:-toremove]
        print(newansw + ':' + str(len(newansw)))
        answer = newansw
    num1 = 0
    cur = ''
    if t == 0:
        print(answer)
        lcd.clear()
        lcd.putstr(str(answer))
    else:
        return(answer)
        lcd.clear()
        lcd.putstr(str(answer))
    lcd.show_cursor()


def testvars():
    print(cur)
    print(ttype)
    print(num1)
    lcd.clear()
    lcd.putstr(cur + ':' + ttype + ':' + str(num1))
def test(t):
    
    if t == 0:
        addnum(1)
        settype('add')
        addnum(4)
        answer = calc(1)
        if answer == 5:
            print('Success')
        else:
            print('Failure')
    if t == 1:
        addnum(4)
        settype('sub')
        addnum(1)
        answer = calc(1)
        if answer == 3:
            print('Success')
        else:
            print('Failure')
    if t == 2:
        addnum(2)
        settype('mult')
        addnum(4)
        answer = calc(1)
        if answer == 8:
            print('Success')
        else:
            print('Failure')
    if t == 3:
        addnum(8)
        settype('div')
        addnum(2)
        answer = calc(1)
        if answer == 4:
            print('Success')
        else:
            print('Failure')
    if t == 4:
        addnum(1)
        addnum('.')
        addnum(5)
        settype('add')
        addnum(1)
        answer = calc(1)
        if answer == 2.5:
            print('Success')
        else:
            print('Failure')
    if t == 5:
        addnum(1)
        addnum('.')
        addnum(5)
        settype('sub')
        addnum(1)
        answer = calc(1)
        if answer == 0.5:
            print('Success')
        else:
            print('Failure')
    if t == 6:
        addnum(1)
        addnum('.')
        addnum(5)
        settype('mult')
        addnum(1)
        answer = calc(1)
        if answer == 1.5:
            print('Success')
        else:
            print('Failure')
    if t == 7:
        addnum(1)
        addnum('.')
        addnum(5)
        settype('div')
        addnum(1)
        answer = calc(1)
        if answer == 1.5:
            print('Success')
        else:
            print('Failure')
       
def fulltest():
    testing = True
    for i in range(3):
        test(0)
        utime.sleep_ms(100)
    for i in range(3):
        test(1)
        utime.sleep_ms(100)
    for i in range(3):
        test(2)
        utime.sleep_ms(100)
    for i in range(3):
        test(3)
        utime.sleep_ms(100)
    for i in range(3):
        test(4)
        utime.sleep_ms(100)
    for i in range(3):
        test(5)
        utime.sleep_ms(100)
    for i in range(3):
        test(6)
        utime.sleep_ms(100)
    for i in range(3):
        test(7)
        utime.sleep_ms(100)
    testing = False
    utime.sleep_ms(100)
    testcut()
def testcut():
    testing = True
    lcd.clear()
    newansw = str(63141371376341786314137137634)
    lcd.putstr(newansw + ':' + str(len(newansw)))
    print(newansw + ':' + str(len(newansw)))
    toremove = len(newansw) - 16
    newansw = newansw[0:-toremove]
    utime.sleep_ms(1000)
    lcd.clear()
    lcd.putstr(newansw + ':' + str(len(newansw)))
    print(newansw + ':' + str(len(newansw)))
    testing = False
while True:
    if testbutton1.value():
        if testing == False:
            fulltest()
    if testbutton2.value():
        if testing == False:
            testcut()
    if testbutton3.value():
        lcd.clear()
