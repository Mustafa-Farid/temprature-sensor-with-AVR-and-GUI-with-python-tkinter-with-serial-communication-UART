# UART Tx/Rx demo
import tkinter as tk
from tkinter import ttk
import threading
import serial
import time
# A simple Information Window
class InformWindow:
    def __init__(self,informStr):
        self.window = tk.Tk()
        self.window.title("Information")
        self.window.geometry("220x60")
        label = tk.Label(self.window, text=informStr)
        buttonOK = tk.Button(self.window,text="OK",command=self.processButtonOK)
        label.pack(side = tk.TOP)
        buttonOK.pack(side = tk.BOTTOM)
        self.window.mainloop()

    def processButtonOK(self):
        self.window.destroy()
class mainGUI:
    def __init__(self):
        window = tk.Tk()
        window.title("GUI UART Tx/Rx Demo")
        self.uartState = False # is uart open or not

        # a frame contains COM's information, and start/stop button
        frame_COMinf = tk.Frame(window)
        frame_COMinf.grid(row = 1, column = 1)

        labelCOM = tk.Label(frame_COMinf,text="COMx: ")
        self.COM = tk.StringVar(value = "COM4")
        ertryCOM = tk.Entry(frame_COMinf, textvariable = self.COM)
        labelCOM.grid(row = 1, column = 1, padx = 5, pady = 3)
        ertryCOM.grid(row = 1, column = 2, padx = 5, pady = 3)

        labelBaudrate = tk.Label(frame_COMinf,text="Baudrate: ")
        self.Baudrate = tk.IntVar(value = 9600)
        ertryBaudrate = tk.Entry(frame_COMinf, textvariable = self.Baudrate)
        labelBaudrate.grid(row = 1, column = 3, padx = 5, pady = 3)
        ertryBaudrate.grid(row = 1, column = 4, padx = 5, pady = 3)

        labelParity = tk.Label(frame_COMinf,text="Parity: ")
        self.Parity = tk.StringVar(value ="NONE")
        comboParity = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Parity)
        comboParity["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        comboParity["state"] = "readonly"
        labelParity.grid(row = 2, column = 1, padx = 5, pady = 3)
        comboParity.grid(row = 2, column = 2, padx = 5, pady = 3)

        labelStopbits = tk.Label(frame_COMinf,text="Stopbits: ")
        self.Stopbits = tk.StringVar(value ="1")
        comboStopbits = ttk.Combobox(frame_COMinf, width = 17, textvariable=self.Stopbits)
        comboStopbits["values"] = ("1","1.5","2")
        comboStopbits["state"] = "readonly"
        labelStopbits.grid(row = 2, column = 3, padx = 5, pady = 3)
        comboStopbits.grid(row = 2, column = 4, padx = 5, pady = 3)
        
        self.buttonSS = tk.Button(frame_COMinf, text = "Start", command = self.processButtonSS)
        self.buttonSS.grid(row = 3, column = 4, padx = 5, pady = 3, sticky = tk.E)

        self.buttonOn = tk.Button(frame_COMinf, text = "ON",command = self.processButtonOn)
        self.buttonOn.grid(row = 3, column = 3, padx = 5, pady = 3, sticky = tk.E)

        self.buttonOff = tk.Button(frame_COMinf, text = "OFF",command = self.processButtonOff)
        self.buttonOff.grid(row = 3, column = 2, padx = 5, pady = 3, sticky = tk.E)
        # serial object
        self.ser = serial.Serial()
        # serial read threading
        self.ReadUARTThread = threading.Thread(target=self.ReadUART)
        self.ReadUARTThread.start()

        frameRecv1 = tk.Frame(window)
        frameRecv1.grid(row = 2, column = 1)
        labelOutText1 = tk.Label(frameRecv1,text="Temprature:")
        labelOutText1.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameRecvSon1 = tk.Frame(frameRecv1)
        frameRecvSon1.grid(row = 2, column =1)
        scrollbarRecv1 = tk.Scrollbar(frameRecvSon1)
        scrollbarRecv1.pack(side = tk.RIGHT, fill = tk.Y)
        self.OutputText1 = tk.Text(frameRecvSon1, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarRecv1.set)
        self.OutputText1.pack()

        frameRecv2 = tk.Frame(window)
        frameRecv2.grid(row = 3, column = 1)
        labelOutText2 = tk.Label(frameRecv2,text="Character:")
        labelOutText2.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameRecvSon2 = tk.Frame(frameRecv2)
        frameRecvSon2.grid(row = 2, column =1)
        scrollbarRecv2 = tk.Scrollbar(frameRecvSon2)
        scrollbarRecv2.pack(side = tk.RIGHT, fill = tk.Y)
        self.OutputText2 = tk.Text(frameRecvSon2, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarRecv2.set)
        self.OutputText2.pack()

        frameTrans = tk.Frame(window)
        frameTrans.grid(row = 4, column = 1)
        labelInText = tk.Label(frameTrans,text="To Transmit Data:")
        labelInText.grid(row = 1, column = 1, padx = 3, pady = 2, sticky = tk.W)
        frameTransSon = tk.Frame(frameTrans)
        frameTransSon.grid(row = 2, column =1)
        scrollbarTrans = tk.Scrollbar(frameTransSon)
        scrollbarTrans.pack(side = tk.RIGHT, fill = tk.Y)
        self.InputText = tk.Text(frameTransSon, wrap = tk.WORD, width = 60, height = 5, yscrollcommand = scrollbarTrans.set)
        self.InputText.pack()
        self.buttonSend = tk.Button(frameTrans, text = "Send", command = self.processButtonSend)
        self.buttonSend.grid(row = 3, column = 1, padx = 5, pady = 3, sticky = tk.E)
        self.buttonClose = tk.Button(frameTrans, text = "CLOSE", command = window.destroy)
        self.buttonClose.grid(row = 3, column = 0, padx = 5, pady = 3, sticky = tk.E)
        window.mainloop()


    def processButtonSS(self):
        # print(self.Parity.get())
        if (self.uartState):
            self.ser.close()
            self.buttonSS["text"] = "Start"
            self.uartState = False
        else:
            # restart serial port
            self.ser.port = self.COM.get()
            self.ser.baudrate = self.Baudrate.get()
            
            strParity = self.Parity.get()
            if (strParity=="NONE"):
                self.ser.parity = serial.PARITY_NONE
            elif(strParity=="ODD"):
                self.ser.parity = serial.PARITY_ODD
            elif(strParity=="EVEN"):
                self.ser.parity = serial.PARITY_EVEN
            elif(strParity=="MARK"):
                self.ser.parity = serial.PARITY_MARK
            elif(strParity=="SPACE"):
                self.ser.parity = serial.PARITY_SPACE
                
            strStopbits = self.Stopbits.get()
            if (strStopbits == "1"):
                self.ser.stopbits = serial.STOPBITS_ONE
            elif (strStopbits == "1.5"):
                self.ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            elif (strStopbits == "2"):
                self.ser.stopbits = serial.STOPBITS_TWO
            
            try:
                self.ser.open()
            except:
                infromStr = "Can't open "+self.ser.port
                InformWindow(infromStr)
            
            if (self.ser.isOpen()): # open success
                self.buttonSS["text"] = "Stop"
                self.uartState = True

    def processButtonSend(self):
        if (self.uartState):
            strToSend = self.InputText.get(1.0,tk.END)
            bytesToSend = strToSend[0:-1].encode(encoding='ascii')
            self.ser.write(bytesToSend)
            print(bytesToSend)
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)
    def processButtonOn(self):
        if (self.uartState):
            self.ser.write('o'.encode())
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)
    def processButtonOff(self):
        if (self.uartState):
            self.ser.write('f'.encode())
        else:
            infromStr = "Not In Connect!"
            InformWindow(infromStr)

    def ReadUART(self):
        # print("Threading...")
        while True:
            if (self.uartState):
                try:
                    ch = self.ser.read().decode(encoding='ascii')
                    print(ch,end='')
                    #self.OutputText1.insert(tk.END,ch)
                    if ch == 'A' or ch == 'Z':
                         self.OutputText2.insert(tk.END,ch)
                    else:
                         self.OutputText1.insert(tk.END,ch)
                         time.sleep(.01)
                         
                    
                except:
                    infromStr = "Something wrong in receiving."
                    InformWindow(infromStr)
                    self.ser.close() # close the serial when catch exception
                    self.buttonSS["text"] = "Start"
                    self.uartState = False
                    

mainGUI()