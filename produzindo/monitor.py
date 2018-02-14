import matplotlib

#temporary fix
import matplotlib.pylab as pylab

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize = (5, 5), dpi = 100)
a = f.add_subplot(211)
b = f.add_subplot(212)
l_choice = []


def write_slogan():
    print(l_choice)

def animate(i):
    global l_choice

    # Código correspondente ao grafico A
    pullData = open("Temperatura.txt", mode = "r").read()#open("Sampledata.txt", mode = "r").read()
    dataList = pullData.split("\n")
    #if len(dataList) >= 10:
    #    dataList = dataList[len(dataList) - 20::] #isso filtra pra utilizar somente os ultimos 20 valores
    xList = []
    #yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x = eachLine.split("º")[0]
            xList.append(int(x))
            #yList.append(int(y))
    a.clear()
    a.plot(xList)

    #código correpondente a B
    #ainda não foi configurado para ler o segundo arquivo
    if len(l_choice) >= 2:
        # Código correspondente ao grafico A
        pullData = open("Umidade.txt", mode = "r").read()
        dataList = pullData.split("\n")
        # if len(dataList) >= 10:
        #    dataList = dataList[len(dataList) - 20::] #isso filtra pra utilizar somente os ultimos 20 valores
        xList = []
        # yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x = eachLine.split("%")[0]
                xList.append(int(x))
                # yList.append(int(y))
        b.clear()
        b.plot(xList)
    

class InterfacePlanta(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default = "icon.ico")
        tk.Tk.wm_title(self, "Título")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for f in (StartPage, GraphPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 30, padx = 30)
        but1 = ttk.Button(self, text = "Iniciar", state = tk.DISABLED, command = lambda: controller.show_frame(GraphPage))
        but1.pack(pady = 10, padx = 10)

        label = tk.Label(self, text = "Selecione os sensores...", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        sensor = StringVar(self)
        choices = ['Temperatura', 'Umidade']

        popupMenu = ttk.OptionMenu(self, sensor, choices[0], *choices)
        popupMenu.pack(pady = 10, padx = 10)

        def change_dropdown(*args):
            but1['state'] = 'normal'#enable the button back
            global l_choice
            if len(l_choice) < 2:
                l_choice.append(str(sensor.get()))
                aux = "Adicionado: " + l_choice[-1]
                label = tk.Label(self, text = aux)
                label.pack()
            else:
                messagebox.showinfo("Atenção!", "O número de sensores alcançou o limite")
        sensor.trace('w', change_dropdown)

class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        global l_choice
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Graphics", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)       

        #os parâmetros de highlight são somente para observação de limites dos frames
        frame1 = tk.Frame(self, highlightbackground = "grey", highlightthickness = 1)
        frame2 = tk.Frame(self, highlightbackground = "grey", highlightthickness = 1)

        canvas = FigureCanvasTkAgg(f, frame1)
        toolbar = NavigationToolbar2TkAgg(canvas, frame1)
        canvas.show()

        frame1.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        frame2.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.X)

        but1 = ttk.Button(frame2, text = " <-Home", command = lambda: controller.show_frame(StartPage))
        but1.pack(expand = True, pady = 20, padx = 20)

        but2 = ttk.Button(frame2, text = "Start", command = lambda: ani.event_source.start())
        but2.pack(expand = True, pady = 20, padx = 20)

        but3 = ttk.Button(frame2, text = "Stop", command = lambda: ani.event_source.stop())
        but3.pack(expand = True, pady = 20, padx = 20)

        but4 = ttk.Button(frame2, text = "Quit", command = exit)
        but4.pack(expand = True, pady = 20, padx = 20)

        slogan = tk.Button(self, text="Hello", command = write_slogan)
        slogan.pack(side = tk.LEFT)

app = InterfacePlanta()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()