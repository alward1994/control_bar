from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import pandas as pd
import time
import serial
import csv
import numpy as np
from matplotlib import pyplot as plt

app = QtWidgets.QApplication([])
ui = uic.loadUi("design1.ui")
ui.setWindowTitle("SerialGUI")

serialData = QSerialPort()
serialData.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)

listX = []
for x in range(100):
    listX.append(0)
listY = []
for x in range(100):
    listY.append(0)


def test():
    f = open('dataSerial2.csv', 'w')
    f.truncate()
    f.close()
    print("hi")


def onOpen():
    serialData.setPortName(ui.comL.currentText())
    serialData.open(QIODevice.ReadWrite)


def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serialData.write(txs.encode())


def serSend(val):
    if val == 2:
        val = 1
    serialSend([1, val])


def openFile():
    txsTime = ""
    txsTime += ui.lineinput.displayText()
    print(txsTime)

    with open(txsTime, newline='') as f:
        reader = csv.reader(f)
        dat = list(reader)
        list_to_arr(dat)
        lenData = len(dat)
        return dat, lenData


def list_to_arr(dat):
    for n, i in enumerate(dat):
        for k, j in enumerate(i):
            dat[n][k] = float(j)


def save_csv():
    with open('dataSerial2.csv', 'r') as dataSave:
        dataSaveCsv = csv.reader(dataSave, delimiter=',')
        dataOpen = pd.DataFrame(dataSaveCsv)
        dataOpen.to_csv('new_dataSerial2.csv', index=False, header=False)


def onClose():
    serSend(0)
    serialData.close()
    print("off")


def control(current, bar, t1, t2, bar_control):
    if current >= t1:
        if current <= t2:
            if bar <= bar_control:
                serSend(1)
            else:
                serSend(0)
        else:
            serSend(0)
    else:
        serSend(0)
# def openRead():
#     rx = serialData.readLine()
#     rxs = str(rx, 'utf-8').strip()
#     data = rxs.split(',')
#     print(data)


def onRead():
    if not serialData.canReadLine(): return
    rx = serialData.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    dataSave = open('dataSerial2.csv', "a")
    dataSave.write(rxs + "\n")
    dataSave.close()

    if data[0] == '0':
        ui.parN.display(float(data[2]))
        ui.prbar.setValue(int(float(data[2])))
        print(float(data[2]))

        dat, lenDat = openFile()
        i = -1
        while i < lenDat:
            control(float(data[1]), float(data[2]), dat[i][0], dat[lenDat-1][0], dat[i][1])
            i += 1

        global listX
        global listY
        ui.grf.clear()
        listX = listX[0:]
        listX.append(float(data[1]))
        listY = listY[0:]
        listY.append(float(data[2]))
        ui.grf.plot(listX, listY)
        ui.grf.setTitle("График зависимости давления от времени при сверхпластической формовке", color="w", size="10pt")
        ui.grf.setLabel('bottom', "<span style=\"color:red;font-size:10px\">Время, (с) </span>")
        ui.grf.setLabel('left', "<span style=\"color:red;font-size:10px\">давления, (бар)</span>")

        plt.plot(listX, listY, label="График зависимости давления от времени при сверхпластической формовке")
        plt.xlabel('Время, (с)')
        plt.ylabel('давления, (бар)')
        plt.savefig("imgData.png")


serialData.readyRead.connect(onRead)
ui.openbtn.clicked.connect(onOpen)
ui.closebtn.clicked.connect(onClose)

ui.comL.currentIndexChanged.connect(test)
ui.checkB.stateChanged.connect(serSend)
ui.btnsv.clicked.connect(save_csv)
ui.inputF.clicked.connect(openFile)


ui.show()
app.exec()
