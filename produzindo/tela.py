import matplotlib
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
import paho.mqtt.client as mqtt

matplotlib.use("TkAgg")

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
final=None
start_time=None


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

    controller = None

    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 30, padx = 30)
        but1 = ttk.Button(self, text = "Iniciar", state = tk.DISABLED, command = self.segue)
        but1.pack(pady = 10, padx = 10)

        label = ttk.Label(self, text = "Selecione os sensores:", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        sensorVar = StringVar(self)
        choices = ['Temperatura', 'Umidade']

        vcmd = (parent.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        label = ttk.Label(self, text = "Minutos")
        label.pack(pady = 2, padx = 10)
        self.entry = tk.Entry(self, validate = 'key', validatecommand = vcmd, width=7)
        self.entry.pack(pady = 2, padx = 10)

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

    def segue(self):
        global final
        final = float(self.entry.get())
        self.controller.show_frame(GraphPage)

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
        global l_choice,lista_umud,lista_temper,final
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

        but1 = ttk.Button(frame2, text=" <-Home", command=lambda: controller.show_frame(StartPage))
        but1.pack(expand=True, pady=20, padx=20)

        but2 = ttk.Button(frame2, text="Start", command=self.start_supply)
        but2.pack(expand=True, pady=20, padx=20)

        but3 = ttk.Button(frame2, text="Stop", command=self.stop_supply)
        but3.pack(expand=True, pady=20, padx=20)

    def start_supply(self):

        global lista_umid,lista_temper,start_time

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connect("iot.eclipse.org", 1883, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_start()

        #reset measure list
        start_time = time.time()
        lista_temper = []
        lista_umid = []

        ani.event_source.start()

    def on_connect(self, client, userdata, flags, rc):
        # print("Connected with result code bleh" + str(rc))
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        client.subscribe("sensorDornelas/temperatura")
        client.subscribe("sensorDornelas/umidade")

    def on_disconnect(self, client, userdata, flags):
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
    def on_message(self, client, userdata, msg):
        global start_time, final
        print(msg.topic + " > " + str(msg.payload.decode()))
        if(msg.topic == 'sensorDornelas/temperatura'):
            lista_temper.append(str(msg.payload.decode()) + ", timestamp -> "+ str(datetime.datetime.now())[:-7]+"\n")
        elif(msg.topic == 'sensorDornelas/umidade'):
            lista_umid.append(str(msg.payload.decode()) + ", timestamp -> " + str(datetime.datetime.now())[:-7]+"\n")
        if (time.time() - start_time) >= final*60:
            self.stop_supply()

    def stop_supply(self):
        ani.event_source.stop()
        self.client.loop_stop()
        self.client.disconnect()

app = InterfacePlanta()
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
