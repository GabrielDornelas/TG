from tkinter import *
import matplotlib
import matplotlib.pyplot as plt

telaInicial = Tk()
w, h = telaInicial.winfo_screenwidth(), telaInicial.winfo_screenheight()
telaInicial.geometry("%dx%d+0+0" % (w - 20, h - 75))
telaInicial.resizable(width = False, height = False)

lTitulo = Label(text = 'WebSensor')
lTitulo.grid(row = 0, column = 1)

fGrafico = Frame(telaInicial)
fGrafico.grid(row = 1, column = 0)

lSensor = Label(fGrafico, text = 'Sensor: ')
lSensor.grid(row = 0, column = 0)
lValor = Label(fGrafico, text = 'Último valor: ')
lValor.grid(row = 0, column = 1)

fPainel = Frame(telaInicial)
fPainel.grid(row = 1, column = 2)

bSalvaGrafico = Button(fPainel, text = 'Salva gráfico')
bSalvaGrafico.grid(row = 0)
bSalvaDados = Button(fPainel, text = 'Salva dados')
bSalvaDados.grid(row = 1)

#v = StringVar()
#l1 = Label(textvariable = v)
#l1.grid(row = 0)


def aa():
    #print('oe')
    v.set("New Text!")
    plt.plot(a)
    plt.show()
    
#bSalvaGrafico = Button(text = 'gráfico', command = aa)
#bSalvaDados = Button()
#bTeste = Button()
#bTeste.grid(row = 2)

