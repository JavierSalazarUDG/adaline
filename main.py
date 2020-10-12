import sys
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Adaline import *
from AdalineGD import *
import numpy as np
import time
import win32api
import matplotlib
matplotlib.use('TkAgg')


if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import math 
import random as rnd

root = Tk.Tk()
root.wm_title("Adaline")

f = Figure(figsize=(9, 6), dpi=100)

a = f.add_subplot(211)
a.set_xlim([-1, 1])
a.set_ylim([-1, 1])
a.grid(True)

err = f.add_subplot(212)
err.set_title('Error acumulado')
err.set_ylabel('Error', Fontsize=12)
err.set_xlabel('Épocas', Fontsize=12)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

lines = []
colors = ['r', 'g']


# def newLine(w):
#     m = -w[0]/w[2]
#     b = -w[1]/w[3]
#     return [m, b]



def clear(i):
    global lines

    if i < len(lines):
        l = lines.pop(i)
        l.remove()
        del l


def plot(weights):
    global lines
    print(weights)
    # [m, b] = newLine(weights)
    x = np.linspace(-1,1,100)
    y = (weights[0]- weights[1]*x)/weights[2]
    clear(0)
    lines = a.plot(x,y,'k')
    # lines = a.plot(
    #     [ -1, 0, 1], 
    #     [ (m*-1)+b, (m*0)+b, (m*1)+b], 
    #     'k'
    # )
    
    canvas.draw()


if __name__ == '__main__':
    xi = []
    d = []

    adalineTrained = False
    lr = 0.1
    epochs = 500
    weights = []
    precision = 0.01
    w_ajustado = []
    n_muestras = len(d)

    def clicked(event):
        global n_muestras,adalineTrained
        if adalineTrained == False:
            if event.xdata and event.ydata and not adalineTrained and event.inaxes == a:

                desiredClass = -1

                if event.button == 3:
                    desiredClass = 1
                xi.append([-1,event.xdata, event.ydata])
                d.append(desiredClass)
                color = ''
                if desiredClass == 1:
                    color = 'g'
                else:
                    color = 'r'
                a.scatter(event.xdata, event.ydata, c=color)
                n_muestras = len(d)
        else:
            eval(event.xdata, event.ydata)
        
        
        canvas.draw()

    f.canvas.callbacks.connect('button_press_event', clicked)

    canvas.draw()

    def learningRate(event):
        global lr

        try:
            lr = float(lrEntry.get())
        except ValueError:
            print('El numero ingresado no es correcto')

    lrLabel = Tk.Label(root, text="Learning rate")
    lrLabel.pack(side='left')
    lrEntry = Tk.Entry(root)
    lrEntry.insert(0, lr)
    lrEntry.bind("<Return>", learningRate)
    lrEntry.pack(side='left')

    def maxEpochs(event):
        global epochs
        try:
            epochs = float(epochsEntry.get())
        except ValueError:
            print('El numero ingresado no es correcto')

    epochsLabel = Tk.Label(root, text="Maximo de epocas")
    epochsLabel.pack(side='left')
    epochsEntry = Tk.Entry(root)
    epochsEntry.insert(0, epochs)
    epochsEntry.bind("<Return>", maxEpochs)
    epochsEntry.pack(side='left')

    def maxPresition(event):
        global precision
        try:
            precision = float(presitionEntry.get())
        except ValueError:
            print('El numero ingresado no es correcto')
    presitionLabel = Tk.Label(root, text="Presicion")
    presitionLabel.pack(side="left")
    presitionEntry= Tk.Entry(root)
    presitionEntry.insert(0,precision)
    presitionEntry.bind("<Return>", maxPresition)
    presitionEntry.pack(side='left')



    perceptron = None
        
    def eval(x,y):
        result = 1 if ad.eval([-1,x, y])>=0 else -1
        print(result)
        color = ''
        if result == 1:
            color = 'g'
        else:
            color = 'r'
        a.scatter(x, y, c=color)
        canvas.draw()

    def train():
        global ad,adalineTrained
        epoch = 0
        E = 1.0
        ad =  AdalineGD(3)
        _error = []
        if len(xi) == 0:
            win32api.MessageBox(0, 'Favor de ingresar puntos a evaluar', 'Error', 0x00001000)
            return
        while epoch < epochs and np.abs(E) > precision:
            print('-------------- Epoca {} ----------------'.format(epoch + 1))
            a.title.set_text('Epoca {}'.format(epoch + 1))
            [adjust_w,E] = ad.fit2(np.array(xi),np.array(d))
            _error.append(np.abs(E))
            print('pesos',adjust_w)
            print('presition',E)
            epoch = epoch+1
            errorCuadratico(epoch,_error)
            plot(adjust_w)
            root.update()
            if E < precision:break
        if E < precision:
            message = ('Solo se logro una presicion de {}'.format(E))
            win32api.MessageBox(0, message, 'Adaline entrenado', 0x00001000)
        else:
            message = ('Se logro entrenar adalinea con una presicion de {} '.format(E))
            win32api.MessageBox(0,message, 'Adaline entrenado', 0x00001000) 
        adalineTrained = True
        lrEntry.destroy()
        lrLabel.destroy()
        presitionLabel.destroy()
        presitionEntry.destroy()
        epochsEntry.destroy()
        epochsLabel.destroy()
        trainButton.destroy()
     
    def errorCuadratico(epocas, error):
        x = np.arange(epocas)
        err.plot(x,error, 'r')
        canvas.draw()

    trainButton = Tk.Button(root, text="Entrenar", command=train)
    trainButton.pack(side='left')
    Tk.mainloop()
