import pyautogui as ps
import time as t

print('Start in 5sec')
t.sleep(5)

for i in range(100):
    ps.write(" :/ ")
    t.sleep(.2)
    ps.press('Enter')
