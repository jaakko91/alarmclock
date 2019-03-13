import threading
import datetime
import time
from tkinter import *
from tkinter import messagebox


global exitFlag
exitFlag = False
global alarmActive
alarmActive = False

#Class for the thread for updating the clock in the UI.
class clockUpdateThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
      
    def run(self):
        global currentTimeH, currentTimeMin, currentTimeSec, exitFlag
        exitFlag = False
        #While exit is not requested, get the current time and update the currentTime label.
        while(not exitFlag):
            now = datetime.datetime.now()
            currentTimeH = format(now.hour, '02')
            currentTimeMin = format(now.minute, '02')
            currentTimeSec = format(now.second, '02')
            currentTime.set(currentTimeH + ":" + currentTimeMin + ":" + currentTimeSec)
            time.sleep(1)
            
#Class for the thread for alarm functionality.
#It is done in a separate thread since the main thread is used by Tkinter GUI.
#The thread receives desired hour and minute for the alarm as parameters.
class alarmThread (threading.Thread):
    def __init__(self, threadID, alarm_h, alarm_min):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.alarm_h = alarm_h
        self.alarm_min = alarm_min
      
    def run(self):
        #alarmActive global variable is used to cancel the alarm from the other thread.
        global alarmActive
        alarmActive = True
        #While alarmActive is true, check the time every 5 seconds and if it matches with alarm time,
        #send out a notification and set alarmActive to false which exits the loop.
        #alarmActive can also be set to false from the main program in which case the alarm is silently canceled.
        while(alarmActive):
            now = datetime.datetime.now()
            #print("current time: " + format(now.hour, '02') + ":" + format(now.minute, '02') + ":" + format(now.second, '02') )
            if now.hour == self.alarm_h and now.minute == self.alarm_min:
                alarmActive = False
                messagebox.showinfo("Alarm!", "Alarm! Time is now " + format(now.hour, '02') + ":" + format(now.minute, '02') + ".")
            time.sleep(5)

#TKinter code. Create the window, GUI elements etc.
root = Tk()
root.title("Alarm clock")
root.geometry("250x150+1000+400")
root.resizable(width=False, height=False)

currentTime = StringVar()
currentTimeLabel = Label(root, textvariable=currentTime, font=("Helvetica", 20))
currentTimeLabel.pack()

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

alarmHourInput = StringVar()
hourEntry = Entry(root, textvariable=alarmHourInput, justify='center')
hourEntry.pack()
alarmHourInput.set("Enter hour")

alarmMinInput = StringVar()
minEntry = Entry(root, textvariable=alarmMinInput, justify='center')
minEntry.pack()
alarmMinInput.set("Enter min")

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=5)

frame = Frame(root)
frame.pack()

#Start thread which is updating the clock on the GUI.
clockThread = clockUpdateThread(1)
clockThread.start()

#Action for "Set alarm" button.
#Get the values from the textboxes and start new alarm thread with these values, unless the alarm is already set.
def set_alarm():
    if not alarmActive:
        #Check that entered value is digit and that it is an acceptable time input.
        if (alarmHourInput.get().isdigit() and alarmMinInput.get().isdigit() and
        int(alarmHourInput.get()) >= 0 and int(alarmHourInput.get()) <= 23 and
        int(alarmMinInput.get()) >= 0 and int(alarmMinInput.get()) <= 59):
            alarmH = int(alarmHourInput.get())
            alarmMin = int(alarmMinInput.get())
            alarmThread1 = alarmThread(1, alarmH, alarmMin)
            alarmThread1.start()
            messagebox.showinfo("Alarm set", "Alarm set on " + format(alarmH, '02') + ":" + format(alarmMin, '02') + ".")
        else:
            messagebox.showinfo("Information", "Time entry is not correct!")
    else:
        messagebox.showinfo("Information", "Alarm is already set!")

#Action for "Cancel alarm" button.
#Set alarmActive to false, if it is true, which cancels the alarm in the other thread.
def cancel_alarm():
    global alarmActive
    if alarmActive:
        alarmActive = False
        messagebox.showinfo("Alarm canceled", "Alarm canceled.")
    else:
        messagebox.showinfo("Information", "No alarm is active!")

#TKinter code. Creates the buttons.                      
quitprogram = Button(frame, text="Quit", command=frame.quit)
quitprogram.pack(side=RIGHT)

setalarm = Button(frame, text="Set alarm", command=set_alarm)
setalarm.pack(side=LEFT)
                                    
cancelalarm = Button(frame, text="Cancel alarm", command=cancel_alarm)
cancelalarm.pack(side=LEFT)

#Enter TKinter main loop.
root.mainloop()

#Destroy the program when exiting main loop.
exitFlag = True
alarmActive = False
root.destroy()
