from machine import Timer


button1_press_count = 0
button1_trigger = 0
button2_press_count = 0
button2_trigger = 0

def check_button(t):
    global button1_press_count
    global button1_trigger
    global button2_press_count
    global button2_trigger
    if button1.value() == 0:
        if button1_press_count <=100:
            button1_press_count += 1
        else:
            button1_press_count = 0
            button1_trigger = 1
            print('button1 tiggered', button1_trigger)
    else:
        button1_press_count = 0
    if button2.value() == 0:
        if button2_press_count <=100:
            button2_press_count += 1
        else:
            button2_press_count = 0
            button2_trigger = 1

timer0 = Timer(0)
timer0.init(period=5, mode=Timer.PERIODIC, callback=check_button)