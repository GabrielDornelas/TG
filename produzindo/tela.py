import matplotlib

##temporary fix
#import matplotlib.pylab as pylab

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import datetime
import time

import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox
#from tkinter import Combobox

import paho.mqtt.client as mqtt


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize = (5, 5), dpi = 100)
a = f.add_subplot(211)
a.axes.get_xaxis().set_visible(False)
b = f.add_subplot(212)
b.axes.get_xaxis().set_visible(False)
l_choice = []
lista_temper=[]
lista_umid=[]


def animate(i):
    global l_choice,lista_temper,lista_umid

    # Código correspondente ao grafico A
    try:

        if l_choice[0] == "Temperatura":
            dataList = lista_temper
        elif l_choice[0] == "Umidade":
            dataList = lista_umid
        
        xList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x = eachLine.split(",")[0]
                xList.append(int(x))
        a.clear()
        a.set_title(l_choice[0] + ": " + str(xList[-1]))
        a.plot(xList)

        #código correpondente a B
        if len(l_choice) >= 2:
            if l_choice[1] == "Temperatura":
                dataList = lista_temper
            elif l_choice[1] == "Umidade":
                dataList = lista_umid
            
            yList = []
            for eachLine in dataList:
                if len(eachLine) > 1:
                    x = eachLine.split(",")[0]
                    yList.append(int(x))
            b.clear()
            b.set_title(l_choice[1] + ": " + str(yList[-1]))
            b.plot(yList)
        
    except:
        return -1   

class InterfacePlanta(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "WebSensor")

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
        label = ttk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 30, padx = 30)
        but1 = ttk.Button(self, text = "Iniciar", state = tk.DISABLED, command = lambda: controller.show_frame(GraphPage))
        but1.pack(pady = 10, padx = 10)

        label = ttk.Label(self, text = "Selecione os sensores...", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        sensorVar = StringVar(self)
        choices = ['Temperatura', 'Umidade']

        vcmd = (parent.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        entry = tk.Entry(self, validate = 'key', validatecommand = vcmd)
        entry.pack(pady = 10, padx = 10)

        popupMenu = ttk.OptionMenu(self, sensorVar, choices[0], *choices)
        popupMenu.pack(pady = 10, padx = 10)
        
        def opt_callback(*args):
            but1['state'] = 'normal'#enable the button back
            global l_choice
            if len(l_choice) < 2:
                print(sensorVar.get())
                l_choice.append(str(sensorVar.get()))
                label = ttk.Label(self, text = ("Adicionado: " + l_choice[-1]))
                label.pack()
            else:
                messagebox.showinfo("Atenção!", "O número de sensores alcançou o limite")
        sensorVar.trace('w', opt_callback)
        
    def validate(self, action, index, value_if_allowed,
                     prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        global l_choice,lista_umud,lista_temper
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Graphics", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        #os parâmetros de highlight são somente para observação de limites dos frames
        frame1 = tk.Frame(self, highlightbackground = "grey", highlightthickness = 1)
        frame2 = tk.Frame(self, highlightbackground = "grey", highlightthickness = 1)

        lista_temper =[]
        lista_umid =[]

        canvas = FigureCanvasTkAgg(f, frame1)
        toolbar = NavigationToolbar2TkAgg(canvas, frame1)
        canvas.show()

        frame1.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        frame2.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.X)

        client = mqtt.Client()

        def start_supply():

            global lista_umid,lista_temper
            
            #reset measure list
            start_time = time.time()
            lista_temper = []
            lista_umid = []
                
            ani.event_source.start()

            def on_connect(client, userdata, flags, rc):
                print("Connected with result code " + str(rc))

                # Subscribing in on_connect() means that if we lose the connection and
                # reconnect then subions will be renewed.
                client.subscribe("sensorDornelas/temperatura")
                client.subscribe("sensorDornelas/umidade")

            def on_disconnect(client, userdata, flags):
                print("Disconnected...")
                file = open(l_choice[0]+".txt", mode = "a")
                if l_choice[0] == "Temperatura":
                    file.writelines(lista_temper)
                elif l_choice[0] == "Umdade":
                    file.writelines(lista_umid)    
                file.close()
                print("Saving...")
                file = open(l_choice[1]+".txt", mode = "a")
                if l_choice[1] == "Temperatura":
                    file.writelines(lista_temper)
                elif l_choice[1] == "Umdade":
                    file.writelines(lista_umid)
                file.close()
                print("Done")
                

            # The callback for when a PUBLISH message is received from the server.
            def on_message(client, userdata, msg):
                print(msg.topic + " > " + str(msg.payload.decode()))
                if(msg.topic == 'sensorDornelas/temperatura'):
                    lista_temper.append(str(msg.payload.decode()) + ", timestamp -> "+ str(datetime.datetime.now())[:-7]+"\n")
                elif(msg.topic == 'sensorDornelas/umidade'):
                    lista_umid.append(str(msg.payload.decode()) + ", timestamp -> " + str(datetime.datetime.now())[:-7]+"\n")
                if (time.time() - start_time)/60 > final:
                    stop_suply()

            client.on_connect = on_connect
            client.on_message = on_message
            client.on_disconnect = on_disconnect

            client.connect("iot.eclipse.org", 1883, 60)

            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            client.loop_start()

        def stop_supply():
            ani.event_source.stop()
            client.loop_stop()
            client.disconnect()

        but1 = ttk.Button(frame2, text = " <-Home", command = lambda: controller.show_frame(StartPage))
        but1.pack(expand = True, pady = 20, padx = 20)

        but2 = ttk.Button(frame2, text = "Start", command = start_supply)
        but2.pack(expand = True, pady = 20, padx = 20)

        but3 = ttk.Button(frame2, text = "Stop", command = stop_supply)
        but3.pack(expand = True, pady = 20, padx = 20)

        but4 = ttk.Button(frame2, text = "Quit", command = exit)
        but4.pack(expand = True, pady = 20, padx = 20)

        

app = InterfacePlanta()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
