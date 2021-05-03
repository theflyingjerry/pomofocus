#!
#pomofocus.py

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import datetime, time, sys, platform
from datetime import date
from ttkthemes import ThemedTk
try:
   import os
except:
    import winsound
    
timerCounterNum=0
worktime=0
timerRunning=False
breakSetting=False
dataRecorded=False
name=''

#Timer Function Portion

def timerCounter(label):
    def count():
        global timerRunning
        if timerRunning:
            global timerCounterNum, worktime, breakSetting
            if timerCounterNum==0:
                display='Time is up!'
                if platform.system() == 'Windows':
                    winsound.Beep(5000,1000)
                elif platform.system()=='Darwin':
                    os.system('say Ding. Ding. Time is up')
                elif platform.system()=='Linux':
                    os.system('beep -f 5000')
                timerRunning=False
                StartStopButton['text']='START'
                resetButton.state(['!disabled'])
                shortBreakButton.state(['!disabled'])
                longBreakButton.state(['!disabled'])
                recordButton.state(['!disabled'])
                styleTimerLabel.configure("timer.TLabel",foreground='black')
                taskNum=taskNumEntry.get()
                if breakSetting==False:
                    timerTimeSr=pomoTimeEntry.get()
                    hours,minutes,seconds=timerTimeSr.split(':')
                    minutes=int(minutes)+(60*int(hours))
                    seconds=int(seconds)+(minutes*60)
                    worktime+=seconds
                if taskNum.isnumeric()==True and int(taskNum)!=0 and breakSetting==False:
                    taskNum=str(int(taskNum)-1)
                    taskNumEntry.delete(0,tk.END)
                    taskNumEntry.insert(0,taskNum)
                if taskNum=='0' and breakSetting==False:
                    time.sleep(2)
                    if platform.system()=='Darwin':
                        os.system('say Congratulations all tasks complete')
                breakSetting=False
            else:
                tt=datetime.datetime.fromtimestamp(timerCounterNum)
                string=tt.strftime('%M:%S')
                display=string
                timerCounterNum-=1
            label.config(text=display)
            if timerCounterNum<=300:
                styleTimerLabel.configure("timer.TLabel",foreground='red')
            label.after(1000,count)
    count()

#Start Stop Button Control Portion

def StartStop():
    if StartStopButton['text']=='START':
        global timerRunning, timerCounterNum
        timerRunning=True
        if timerCounterNum==0:
            timerTimeSr=pomoTimeEntry.get()
            hours,minutes,seconds=timerTimeSr.split(':')
            minutes=int(minutes)+(60*int(hours))
            seconds=int(seconds)+(minutes*60)
            timerCounterNum+=seconds
            styleTimerLabel.configure("timer.TLabel",foreground='black')
        timerCounter(timerLabel)
        StartStopButton['text']='STOP'
        longBreakButton.state(['disabled'])
        shortBreakButton.state(['disabled'])
        resetButton.state(['disabled'])
        recordButton.state(['disabled'])
    elif StartStopButton['text']=='STOP':
        timerRunning=False
        StartStopButton['text']='START'
        resetButton.state(['!disabled'])
        recordButton.state(['!disabled'])

def Reset():
    global timerCounterNum
    timerCounterNum=0
    styleTimerLabel.configure("timer.TLabel",foreground='black')
    timerLabel.config(text='00:00')
    timerCounter(timerLabel)
    longBreakButton.state(['!disabled'])
    shortBreakButton.state(['!disabled'])

#Long Break Button Control Portion

def longBreakTimer():
    global timerRunning, timerCounterNum, breakSetting
    timerRunning=True
    breakSetting=True
    styleTimerLabel.configure("timer.TLabel",foreground='black')
    if timerCounterNum==0:
        longBreakTime=float(longTimeEntry.get())
        longBreakTimeSec=60*longBreakTime
        timerCounterNum+=longBreakTimeSec
        timerCounter(timerLabel)
        StartStopButton['text']='STOP'
        longBreakButton.state(['disabled'])
        shortBreakButton.state(['disabled'])
        resetButton.state(['disabled'])

#Short Break Button Control Portion

def shortBreakTimer():
    global timerRunning, timerCounterNum, breakSetting
    timerRunning=True
    breakSetting=True
    styleTimerLabel.configure("timer.TLabel",foreground='black')
    if timerCounterNum==0:
        shortBreakTime=float(shortTimeEntry.get())
        shortBreakTimeSec=60*shortBreakTime
        timerCounterNum+=shortBreakTimeSec
        timerCounter(timerLabel)
        StartStopButton['text']='STOP'
        longBreakButton.state(['disabled'])
        shortBreakButton.state(['disabled'])
        resetButton.state(['disabled'])

#Record Button Control Portion

def Record():
    global name, nameEntry, nameWindow, worktime, timerCounterNum, dataRecorded
    p=Path(Path.home()/'Documents')
    if Path(p/'pomofocus_recordings.txt').exists()==False:
        nameWindow=tk.Tk()
        nameWindow.resizable(False,False)
        nameWindow.title('')
        nameLabel=tk.Label(master=nameWindow,text='Please input name below:')
        nameLabel.pack(anchor='center',fill='both')
        nameEntry=tk.Entry(master=nameWindow)
        nameEntry.pack(anchor='center',fill='both')
        enterButton=tk.Button(master=nameWindow,text='ENTER',command=Enter)
        enterButton.pack(side=tk.RIGHT)
    else:
        pomoRecord=open(p/'pomofocus_recordings.txt','a')
        today=date.today()
        date1=today.strftime('%m/%d/%y')
        taskName=taskNameEntry.get()
        if timerCounterNum!=0 and breakSetting==False:
            timerTimeSr=pomoTimeEntry.get()
            hours,minutes,seconds=timerTimeSr.split(':')
            minutes=int(minutes)+(60*int(hours))
            seconds=int(seconds)+(minutes*60)
            elapsedtime=seconds-timerCounterNum
            worktime+=elapsedtime
        workTimeMin=int(worktime/60)
        pomoRecord.write(f'{date1} {taskName} {workTimeMin} mins\n')
        pomoRecord.close()
        dataRecorded=True

#Enter Button Control Portion

def Enter():
    global name, nameEntry, nameWindow, worktime, timerCounterNum, dataRecorded
    name=nameEntry.get()
    p=Path(Path.home()/'Documents')
    pomoRecord=open(p/'pomofocus_recordings.txt','a')
    pomoRecord.write(name+'\n')
    today=date.today()
    date1=today.strftime('%m/%d/%y')
    taskName=taskNameEntry.get()
    if timerCounterNum!=0 and breakSetting==False:
        timerTimeSr=pomoTimeEntry.get()
        hours,minutes,seconds=timerTimeSr.split(':')
        minutes=int(minutes)+(60*int(hours))
        seconds=int(seconds)+(minutes*60)
        elapsedtime=seconds-timerCounterNum
        worktime+=elapsedtime
    workTimeMin=int(worktime/60)
    pomoRecord.write(f'{date1} {taskName} {workTimeMin} mins\n')
    dataRecorded=True
    pomoRecord.close()
    nameWindow.destroy()

#Quit Button Control Portion

def Quit():
    global dataRecorded, popUpWindow
    if dataRecorded==False:
        popUpWindow=tk.Tk()
        popUpWindow.title('')
        popUpWindow.resizable(False,False)
        warningLabel1=tk.Label(master=popUpWindow,text='WARNING: DATA WILL BE LOST BY QUITTING')
        warningLabel2=tk.Label(master=popUpWindow,text="Would you like to record this session's data?")
        warningLabel1.pack(anchor='center',fill='both')
        warningLabel2.pack(anchor='center',fill='both')
        popUpWindowFrame=tk.Frame(master=popUpWindow)
        popUpWindowFrame.pack(anchor='center')
        yesButton=tk.Button(master=popUpWindowFrame,text='YES',command=Yes)
        noButton=tk.Button(master=popUpWindowFrame,text='NO',command=No)
        yesButton.pack(side=tk.LEFT)
        noButton.pack(side=tk.RIGHT)
    else:
        window.destroy()
        sys.exit('Goodbye')

#Yes Pop Up Button From Quit Control Portion

def Yes():
    global popUpWindow
    popUpWindow.destroy()

#Yes Pop Up Button From Quit Control Portion

def No():
    global popUpWindow
    popUpWindow.destroy()
    window.destroy()
    sys.exit('Goodbye')

#Window and Tab Layout Portion
    
now=datetime.datetime.now()
if int(now.hour)>=21 or int(now.hour)<5:
    themeCurrent='equilux'
else:
    themeCurrent='yaru'
window=ThemedTk(theme=themeCurrent)
window.title('Pomofocus')
window.resizable(True,True)
tab_parent=ttk.Notebook(window)


mainTab=ttk.Frame(tab_parent)
timerTab=ttk.Frame(tab_parent)
helpTab=ttk.Frame(tab_parent)
tab_parent.add(mainTab,text='HOME')
tab_parent.add(timerTab,text='TIMER')
tab_parent.add(helpTab,text='HELP')
tab_parent.pack(expand=1,fill=tk.BOTH)

#Main Tab Layout Portion

mainTab.rowconfigure([0,1,2],weight=1)
mainTab.columnconfigure(0,weight=1)

frameTop=ttk.Frame(master=mainTab)
frameTop.columnconfigure([0,1],weight=1)
frameTop.rowconfigure(0,weight=1)
frameTop.grid(row=0,column=0,sticky='nsew')

frameTopLeft=ttk.Frame(master=frameTop)
frameTopLeft.rowconfigure(0,weight=1)
frameTopLeft.columnconfigure(0,weight=1)
frameTopLeft.grid(row=0,column=0,sticky='nsew')

StartStopButton=ttk.Button(text='START',master=frameTopLeft,command=StartStop)
StartStopButton.grid(row=0,column=0,sticky='nsew')

frameTopRight=ttk.Frame(master=frameTop)
frameTopRight.rowconfigure([0,1],weight=1)
frameTopRight.columnconfigure(0,weight=1)
frameTopRight.grid(row=0,column=1,sticky='nsew')

longBreakButton=ttk.Button(master=frameTopRight,text='Long Break',command=longBreakTimer)
longBreakButton.grid(row=1,column=0,sticky='nsew')
shortBreakButton=ttk.Button(master=frameTopRight,text='Short Break', command=shortBreakTimer)
shortBreakButton.grid(row=0,column=0,sticky='nsew')

frameMiddle=ttk.Frame(master=mainTab)
frameMiddle.rowconfigure([0,1,2,3],weight=1)
frameMiddle.columnconfigure([0,1],weight=1)
frameMiddle.grid(row=1,column=0,sticky='nsew')

taskNameLabel=ttk.Label(master=frameMiddle,text='Task name:')
taskNumLabel=ttk.Label(master=frameMiddle,text='Num. of rounds:')
longTimeLabel=ttk.Label(master=frameMiddle,text='Long Break dur. (min):')
shortTimeLabel=ttk.Label(master=frameMiddle,text='Short break dur. (min):')
taskNameEntry=ttk.Entry(master=frameMiddle)
taskNumEntry=ttk.Entry(master=frameMiddle)
longTimeEntry=ttk.Entry(master=frameMiddle)
longTimeEntry.insert(0,'15')
shortTimeEntry=ttk.Entry(master=frameMiddle)
shortTimeEntry.insert(0,'5')
taskNameLabel.grid(row=0,column=0,sticky='nse')
taskNameEntry.grid(row=0,column=1,sticky='nsew')
taskNumLabel.grid(row=1,column=0,sticky='nse')
taskNumEntry.grid(row=1,column=1,sticky='nsew')
longTimeLabel.grid(row=4,column=0,sticky='nse')
longTimeEntry.grid(row=4,column=1,sticky='nsew')
shortTimeLabel.grid(row=3,column=0,sticky='nse')
shortTimeEntry.grid(row=3,column=1,sticky='nsew')

frameBottom=ttk.Frame(master=mainTab)
frameBottom.rowconfigure(0,weight=1)
frameBottom.columnconfigure([0,1,2],weight=1)
frameBottom.grid(row=2,column=0,sticky='nsew')

quitButton=ttk.Button(master=frameBottom,text='QUIT',command=Quit)
recordButton=ttk.Button(master=frameBottom,text='RECORD',command=Record)
resetButton=ttk.Button(master=frameBottom,text='RESET', command=Reset)
quitButton.grid(row=0,column=2,sticky='nsew')
recordButton.grid(row=0,column=1,sticky='nsew')
resetButton.grid(row=0,column=0,sticky='nsew')

#Timer Tab Layout Portion

spaceLabel1=ttk.Label(master=timerTab,text='''


''')
spaceLabel1.pack(anchor='center',fill='both')

styleTimerLabel=ttk.Style()
styleTimerLabel.configure("timer.TLabel",font='calibri 40 bold',foreground='black',anchor=tk.CENTER)

timerLabel=ttk.Label(master=timerTab,text='00:00',style="timer.TLabel")
timerLabel.pack(fill='both')
spaceLabel2=ttk.Label(master=timerTab,text='''



''')
spaceLabel2.pack(anchor='center',fill='both')

#Help Tab Layout Portion

helpStyle=ttk.Style()
helpStyle.configure("help.TLabel",font='calibri 12 bold',anchor=tk.CENTER)
styleSmallLabel=ttk.Style()
styleSmallLabel.configure("small.TLabel",font='calibri 10',anchor=tk.CENTER)
styleSmallestLabel=ttk.Style()
styleSmallestLabel.configure("smallest.TLabel",font='calibri 8',anchor=tk.CENTER)

helpLabel=ttk.Label(master=helpTab,text='Welcome to PomoFocus!',style="help.TLabel")
helpLabel.pack(fill='both')
helpDesLabel=ttk.Label(master=helpTab,text='''This application is designed to help focus and productivity.
The start button starts a 24 minute timer which is based on
an Italian tradition. Pressing the button again will stop the
timer. The timer can be seen in the timer tab. The short and
long break buttons start a timer designated to the interval
imputed. Pressing reset will return the timer to original state
but pressed prior to timer expiring the elasped time will not
be included in recording. The record button will take the name
of the task and time or rounds completed and date and record
it to a text file to stay organized. The Study time interval
can be changed below.
''',style="small.TLabel")
helpDesLabel.pack(anchor='center',fill='both')
pomoTimeEntry=ttk.Entry(master=helpTab)
pomoTimeEntry.insert(0,'00:24:00')
pomoTimeEntry.pack(anchor='center',fill='both')
pomoTimeEntryLabel=ttk.Label(master=helpTab,text="Enter Timer Time. Eg -> 01:30:30, 01 -> Hour, 30 -> Minutes, 30 -> Seconds",style="smallest.TLabel")
pomoTimeEntryLabel.pack(anchor='center',fill='both')

window.mainloop()
