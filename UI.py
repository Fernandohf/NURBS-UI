import matplotlib
import matplotlib.pyplot as plt
import NURBS
import math
import numpy
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Grid, Tk, Canvas, VERTICAL, FALSE, Spinbox, LEFT, BOTH, YES, N, S, E, W, END
import tkinter.ttk as ttk


matplotlib.use('TkAgg')


# UI Class
class UIVariables:
    fig = plt.figure()

    def __init__(self, master, points, weight=None, deg=None, seg=None):
        self.master = master
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.points = points
        if seg is None:
            self.nseg = 200
        else:
            self.nseg = seg
        if seg is None:
            self.ndeg = 2
        else:
            self.ndeg = deg
        self.npoints = points.shape[0]
        if weight is None:
            self.weight = numpy.ones(self.npoints)
        else:
            self.weight = weight
        if points.shape[1] == 3:
            self.dim2d3d = '3D'
        elif points.shape[1] == 2:
            self.dim2d3d = '2D'
        else:
            Exception("Pontos de dimensões inválidas!")
        self.subplot = self.fig.add_subplot(111)
        self.plotGraph()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()

    def plotGraph(self):
        plt.clf()
        if (self.npoints <= 0):
            Exception("Número de Pontos Inválidos")
            return
        data = NURBS.nurbs(self.points, self.ndeg, self.nseg, self.weight)
        if self.dim2d3d == '2D':
            self.subplot = self.fig.add_subplot(111)
            self.subplot.plot(self.points[:, 0], self.points[:, 1], 'ro', )
            self.subplot.plot(data[:, 0], data[:, 1])
            c = 0
            for i, j in zip(self.points[:, 0], self.points[:, 1]):
                c += 1
                self.subplot.annotate('%s' % c, xy=(i, j), xytext=(
                    5, 0), textcoords='offset points')
        elif self.dim2d3d == '3D':
            self.subplot = self.fig.add_subplot(111, projection='3d')
            for i in range(self.npoints):
                self.subplot.scatter(
                    self.points[i, 0], self.points[i, 1], self.points[i, 2])
                self.subplot.text(self.points[i, 0] + 1, self.points[i, 1] + 1, self.points[i, 2], '%s' % (str(i + 1)),
                                  size=15, zorder=3, color='k')
            self.subplot.plot(data[:, 0], data[:, 1], data[:, 2])
        else:
            Exception("Os pontos devem ser 2D ou 3D.")

    def appendPoint(self, P):
        # POINTS ARRAY
        temp = self.points
        temp = numpy.vstack([temp, P])
        self.points = temp

        # WEIGHTS ARRAY
        tempW = self.weight
        tempW = numpy.append(tempW, [1])
        self.weight = tempW

        self.npoints += 1
        # self.updateFunction()

    def removeLastPoint(self):
        try:
            # POINTS ARRAY
            temp = self.points
            temp = numpy.delete(temp, self.npoints - 1, 0)
            self.points = temp

            # WEIGHTS ARRAY
            tempW = self.weight
            tempW = numpy.delete(tempW, self.npoints - 1, 0)
            self.weight = tempW

            self.npoints -= 1
            # self.updateFunction()
        except Exception:
            pass

    def updateFunction(self):
        self.subplot.clear()
        self.plotGraph()
        self.canvas.draw()
        updateSideFrame()


class Examples:
    p = list(range(11))
    d = list(range(11))
    w = list(range(11))

    p[1] = numpy.array([[0, 0], [0, 5], [5, 5], [10, 5], [10, 0]])
    d[1] = 3
    w[1] = numpy.array(
        [1, 1.0 / math.sqrt(2.0), 1.0, 1.0 / math.sqrt(2.0), 1.0])

    p[2] = numpy.array([[0, 0], [1, 1.5], [2, 3], [
                       3, 4.5], [4, 6], [5, 7.5], [6, 9]])
    d[2] = 3
    w[2] = numpy.array([1, 1, 1, 1, 1, 1, 1])

    p[3] = numpy.array([[-10, 0], [-5, 5], [0, 4], [8, 4],
                       [10, 4], [15, 3], [20, 1], [20, 0]])
    d[3] = 4
    w[3] = numpy.array([1, 5, 1, 1, 1, 1, 1, 1])

    p[4] = numpy.array([[0, 0], [5, 10], [10, -10], [15, 10], [20, 0]])
    d[4] = 2
    w[4] = numpy.array([1, 1, 1, 1, 1])

    p[5] = numpy.array([[0, 0], [5, 10], [10, -10], [15, 10], [20, 0]])
    d[5] = 4
    w[5] = numpy.array([1, 5, 15, 1, 1])

    p[6] = numpy.array(
        [[0, 0, 5], [0, 5, 1], [-5, -5, 2], [-8, 10, 5], [-10, 0, -2]])
    d[6] = 3
    w[6] = numpy.array([1, 1, 1, 1, 1])

    p[7] = numpy.array(
        [[0, 0, 5], [0, 5, 1], [-5, -5, 2], [-8, 10, 5], [-10, 0, -2]])
    d[7] = 3
    w[7] = numpy.array([1, 6, 1, 8, 1])

    p[8] = numpy.array(
        [[0, 0, 5], [0, 5, 1], [-5, -5, 2], [-8, 10, 5], [-10, 0, -2]])
    d[8] = 6
    w[8] = numpy.array([1, 6, 1, 8, 1])

    p[9] = numpy.array(
        [[0, 0, 0], [0, 5, 0], [5, 5, 0], [10, 5, 0], [10, 0, 0]])
    d[9] = 2
    w[9] = numpy.array([1, 6, 1, 8, 1])

    p[10] = numpy.array([[0, 0, 0], [0, 5, 0], [5, 5, 0], [
                        10, 0, 0], [10, 5, 5], [5, 0, 0], [0, 0, 0]])
    d[10] = 2
    w[10] = numpy.array([1, 1, 1, 1, 1, 1, 1])

    def __init__(self, n):
        self.number = n

    def updateEx(self, n):
        self.number = n

    def show(self):
        ui.ndeg = self.d[self.number]
        ui.weight = self.w[self.number]
        ui.points = self.p[self.number]
        ui.npoints = self.p[self.number].shape[0]
        if ui.points.shape[1] == 3:
            ui.dim2d3d = '3D'
        else:
            ui.dim2d3d = '2D'
        ui.updateFunction()


class ClickDrag:
    increment = 1
    deltax = 0
    deltay = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDeltaX(self):
        return self.deltax

    def getDeltaY(self):
        return self.deltay

    def addDeltax(self):
        self.deltax += self.increment

    def addDeltay(self):
        self.deltay += self.increment / 1.5

    def subDeltax(self):
        self.deltax -= self.increment

    def subDeltay(self):
        self.deltay -= self.increment / 1.5

    def setDeltaXY(self, deltax, deltay):
        self.deltax = deltax
        self.deltay = deltay


# Settings
root = Tk()
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")
# root.tk.call("set_theme")
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
root.resizable(FALSE, FALSE)

# Styles

# TODO
# style = ttk.Style(root)
# style.theme_use('clam')
# styleFrame = ttk.Style().configure('TFrame', backgroud="white")
# styleEntries = ttk.Style().configure('TFrame', backgroud="white")
# styleButtons = ttk.Style().configure('TFrame', backgroud="white")
# styleLabels = ttk.Style().configure('TFrame', backgroud="white")

# Global Variables
initialPoints3D = numpy.array(
    [(28, 44, 6), (20, 6, 5), (40, -10, 0), (68, 0, 2),
     (6, 5, 10), (-8, 50, 50), (4, -50, 25)],
    float)  # PONTOS INICIAIS
initialPoints2D = numpy.array([(0, 0), (2, 6), (1, 8), (8, 10), (5, 20), (15, 16), (20, 20)],
                              float)  # PONTOS INICIAIS
examplesVar = Examples(1)

initialPointsW = numpy.ones(initialPoints2D.shape[0])

# UI Variables

labelPoints = []
entryPoints = []
labelPointsW = []
entryPointsW = []

root.wm_title("N.U.R.B.S.")

mainFrame = ttk.Frame(root, padding="3")
mainFrame.grid(column=0, row=0, sticky=N + S + W + E)
mainFrame.columnconfigure(0, weight=1)
mainFrame.rowconfigure(0, weight=1)

# MAIN UI CHUNK
sideFrame = ttk.Frame(mainFrame, padding="3")

frameScrollable = ttk.Frame(sideFrame)
canvasPoints = Canvas(frameScrollable, borderwidth=0, width=300, height=400)
labelMainPoints = ttk.Label(
    master=sideFrame, text="Pontos do Polimômio:", padding="2")
framePoints = ttk.Frame(master=canvasPoints)
framePoints.bind("<Configure>", lambda event,
                 canvasPoints=canvasPoints: onFrameConfigure(canvasPoints))

scrollPoints = ttk.Scrollbar(frameScrollable, orient=VERTICAL)
canvasPoints.configure(yscrollcommand=scrollPoints.set)
scrollPoints.configure(command=canvasPoints.yview)

# Classes Initiation
cnd = ClickDrag(0, 0)

ui = UIVariables(mainFrame, initialPoints2D, initialPointsW, 2, 200)
ui.plotGraph()


# UI Functions
def onMousewheel(event):
    canvasPoints.yview_scroll(int(-1 * (event.delta / 120)), "units")


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def minusPoint():
    ui.removeLastPoint()
    updateAll(0)
    return


def plusPoint():
    x = random.randrange(15)
    y = random.randrange(15)
    if ui.dim2d3d == '3D':
        z = random.randrange(15)
        ui.appendPoint([x, y, z])
    else:
        ui.appendPoint([x, y])
    updateAll(0)
    return


def updateSideFrame():
    global labelPoints
    global entryPoints
    global labelPointsW
    global entryPointsW
    # FIRST COLUMN
    for widget in framePoints.winfo_children():
        widget.destroy()
    labelPoints = [None] * (ui.npoints)
    entryPoints = [None] * (ui.npoints)
    labelPointsW = [None] * (ui.npoints)
    entryPointsW = [None] * (ui.npoints)
    for p in range(ui.npoints):
        labelPoints[p] = ttk.Label(
            master=framePoints, text="P%i" % (p + 1), padding="1", width=4)
        entryPoints[p] = ttk.Entry(master=framePoints, width=18)
        entryPoints[p].bind('<Return>', updateAll)
        entryPoints[p].delete(0, END)
        # entryPoints[p].inset(0, ui.points[p])
        if ui.dim2d3d == '2D':
            entryPoints[p].insert(0, ' {0} , {1}'.format(
                ui.points[p, 0], ui.points[p, 1]))
        else:
            entryPoints[p].insert(0, ' {0} , {1} , {2} '.format(
                ui.points[p, 0], ui.points[p, 1], ui.points[p, 2]))
        entryPoints[p].grid(column=1, row=p, sticky=E)
        labelPoints[p].grid(column=0, row=p, sticky=W)
        labelPointsW[p] = ttk.Label(
            master=framePoints, text="W%i" % (p + 1), padding="1", width=4)
        entryPointsW[p] = ttk.Entry(master=framePoints, width=4)
        entryPointsW[p].bind('<Return>', updateAll)
        entryPointsW[p].delete(0, END)
        entryPointsW[p].insert(0, ui.weight[p])
        entryPointsW[p].grid(column=3, row=p, sticky=E)
        labelPointsW[p].grid(column=2, row=p, sticky=W)
    # SECOND COLUMN
    spinboxDegree.delete(0, END)
    spinboxSeg.delete(0, END)
    spinboxDegree.insert(0, ui.ndeg)
    spinboxSeg.insert(0, ui.nseg)
    if ui.dim2d3d == '2D':
        radio2D.state(['!disabled', 'selected'])
        radio3D.state(['!disabled', '!selected'])
    else:
        radio2D.state(['!disabled', '!selected'])
        radio3D.state(['!disabled', 'selected'])
        # sideFrame.update()


def getUIVariables():
    # FIRST COLUMN
    for i in range(ui.npoints):
        try:
            tempstr = entryPoints[i].get()
            num = tempstr.split(',')
            ui.points[i] = [float(j) for j in num]
            tempstring = entryPointsW[i].get()
            ui.weight[i] = float(tempstring)
        except Exception:
            Exception("Cuidado!")

    # SECOND COLUMN
    try:
        ui.nseg = int(spinboxSeg.get())
    except Exception:
        Exception("Valor inválido!")
    try:
        ui.ndeg = int(spinboxDegree.get())
    except Exception:
        Exception("Valor inválido!")
    if radio3D.focus():
        ui.dim2d3d = '3D'
    elif radio2D.focus():
        ui.dim2d3d = '2D'


def changeDim():
    temp = ui.points
    dim = ui.dim2d3d
    if dim == '3D':
        a = numpy.delete(temp, 2, axis=1)
        ui.points = a
        ui.canvas.get_tk_widget().unbind("all")
        ui.canvas.get_tk_widget().bind("<B1-Motion>", onDrag)
        ui.canvas.get_tk_widget().bind("<Button-1>", onLeftClick)
        ui.canvas.get_tk_widget().configure(cursor="hand2")
        ui.dim2d3d = '2D'
    elif dim == '2D':
        b = numpy.hstack((temp, numpy.ones((temp.shape[0], 1))))
        ui.points = b
        ui.canvas.get_tk_widget().configure(cursor="arrow")
        ui.canvas.get_tk_widget().unbind("all")
        ui.dim2d3d = '3D'
    updateAll()

    # Activate Click and Drag


def updateAll(s=None):
    getUIVariables()
    updateSideFrame()
    ui.updateFunction()


def updateView():
    ui.canvas.show()
    return


def onDrag(event):
    if ui.dim2d3d == '3D':
        if cnd.getX() > event.x:
            cnd.addDeltax()
        elif cnd.getX() < event.x:
            cnd.subDeltax()
        if cnd.getY() > event.y:
            cnd.subDeltay()
        elif cnd.getY() < event.y:
            cnd.addDeltay()
        tempx = cnd.getDeltaX()
        tempy = cnd.getDeltaY()
        rotateView(ui.subplot, tempx, tempy)
        cnd.setXY(event.x, event.y)
        updateView()
    else:
        return


def onLeftClick(event):
    cnd.setXY(event.x, event.y)
    cnd.setDeltaXY(0, 0)


def callExButton(n):
    examplesVar.updateEx(n)
    examplesVar.show()


# Changes current plot view position
def rotateView(fig, azim, elev):
    if ui.dim2d3d == '2D':
        return
    else:
        fig.azim += azim
        fig.elev += elev


# UI Settings
if ui.dim2d3d == '3D':
    ui.canvas.get_tk_widget().bind("<B1-Motion>", onDrag)
    ui.canvas.get_tk_widget().bind("<Button-1>", onLeftClick)
    ui.canvas.get_tk_widget().configure(cursor="hand2")
    # ui.canvas.get_tk_widget().bind("<Enter>", changeCursor)
    # ui.canvas.get_tk_widget().bind("<Leave>", changeCursor)
else:
    ui.canvas.get_tk_widget().configure(cursor="arrow")
    ui.canvas.get_tk_widget().unbind("all")

# FIRST COLUMN
framePButtons = ttk.Frame(master=sideFrame, padding="2")
buttonPlusP = ttk.Button(master=framePButtons,
                         text="+ Pontos", command=plusPoint, width=14)
buttonMinusP = ttk.Button(master=framePButtons,
                          text="- Pontos", command=minusPoint, width=14)

# SECOND COLUMN
labelSettings = ttk.Label(master=sideFrame, text="Configurações da NURBS:")
labelDegree = ttk.Label(master=sideFrame, text="Grau:")
spinboxDegree = Spinbox(master=sideFrame, from_=1, to=100,
                        textvariable=ui.ndeg, width=4, command=updateAll)
radio2D = ttk.Radiobutton(master=sideFrame, text='2D',
                          variable=ui.dim2d3d, value='2D', command=changeDim)
radio3D = ttk.Radiobutton(master=sideFrame, text='3D',
                          variable=ui.dim2d3d, value='3D', command=changeDim)

# INITIAL VALUES
spinboxDegree.delete(0, END)
spinboxDegree.insert(0, ui.ndeg)
# spinboxDegree.bind("<Increment>", updateAll)

labelSeg = ttk.Label(master=sideFrame, text="Segmentos:")
spinboxSeg = Spinbox(master=sideFrame, from_=1, to=5000,
                     textvariable=ui.nseg, width=7, command=updateAll)

spinboxDegree.bind('<Return>', updateAll)
spinboxSeg.bind('<Return>', updateAll)
# INITIAL VALUES
spinboxSeg.delete(0, END)
spinboxSeg.insert(0, ui.nseg)
# spinboxSeg.bind("<Increment>", updateAll)

label3D2D = ttk.Label(master=sideFrame, text="Dimensão dos pontos:")

# THIRD COLUMN
labelExamples = ttk.Label(master=sideFrame, text=">>>Exemplos<<<")
labelExamples2D = ttk.Label(master=sideFrame, text="Exemplos 2D:")
buttonEx1 = ttk.Button(master=sideFrame, text="Exemplo 1",
                       command=lambda: callExButton(1))
buttonEx2 = ttk.Button(master=sideFrame, text="Exemplo 2",
                       command=lambda: callExButton(2))
buttonEx3 = ttk.Button(master=sideFrame, text="Exemplo 3",
                       command=lambda: callExButton(3))
buttonEx4 = ttk.Button(master=sideFrame, text="Exemplo 4",
                       command=lambda: callExButton(4))
buttonEx5 = ttk.Button(master=sideFrame, text="Exemplo 5",
                       command=lambda: callExButton(5))
buttonEx6 = ttk.Button(master=sideFrame, text="Exemplo 6",
                       command=lambda: callExButton(6))
buttonEx7 = ttk.Button(master=sideFrame, text="Exemplo 7",
                       command=lambda: callExButton(7))
buttonEx8 = ttk.Button(master=sideFrame, text="Exemplo 8",
                       command=lambda: callExButton(8))
buttonEx9 = ttk.Button(master=sideFrame, text="Exemplo 9",
                       command=lambda: callExButton(9))
buttonEx10 = ttk.Button(master=sideFrame, text="Exemplo 10",
                        command=lambda: callExButton(10))

labelExamples3D = ttk.Label(master=sideFrame, text="Exemplos 3D:")

# Layout Management
ui.canvas.get_tk_widget().pack(side=LEFT)
sideFrame.pack(side=LEFT, fill=BOTH, expand=YES)

frameScrollable.grid(column=0, row=1, rowspan=12, sticky=(N, W))
canvasPoints.bind_all("<MouseWheel>", onMousewheel)
canvasPoints.pack(side=LEFT, fill=BOTH, expand=YES)
scrollPoints.pack(side=LEFT, fill="y")
canvasPoints.create_window((0, 0), window=framePoints, anchor="nw")

labelMainPoints.grid(column=0, row=0, sticky=(W, N), columnspan=3)
framePButtons.grid(column=0, row=13, sticky=(N, W))
# .grid(column=0,row=13,  sticky=(W,S))
buttonPlusP.pack(side=LEFT, fill=BOTH, expand=YES)
# .grid(column=1,row=13, sticky=(E,S))
buttonMinusP.pack(side=LEFT, fill=BOTH, expand=YES)

labelSettings.grid(column=2, row=0, columnspan=2, sticky=(W, N))
labelDegree.grid(column=2, row=1, sticky=(W, N), columnspan=2)
spinboxDegree.grid(column=3, row=1, sticky=(E, N))
labelSeg.grid(column=2, row=2, sticky=(W, N))
spinboxSeg.grid(column=3, row=2, sticky=(E, N))
label3D2D.grid(column=2, row=3, columnspan=2, sticky=(W, N))
radio2D.grid(column=2, row=4, sticky=(W, N))
radio3D.grid(column=3, row=4, sticky=(E, N))

labelExamples.grid(column=4, row=0, columnspan=2)

labelExamples2D.grid(column=4, row=1, sticky=(W, N))
buttonEx1.grid(column=4, row=2, sticky=(W, N))
buttonEx2.grid(column=4, row=3, sticky=(W, N))
buttonEx3.grid(column=4, row=4, sticky=(W, N))
buttonEx4.grid(column=4, row=5, sticky=(W, N))
buttonEx5.grid(column=4, row=6, sticky=(W, N))

labelExamples3D.grid(column=5, row=1, sticky=(E, N))
buttonEx6.grid(column=5, row=2, sticky=(E, N))
buttonEx7.grid(column=5, row=3, sticky=(E, N))
buttonEx8.grid(column=5, row=4, sticky=(E, N))
buttonEx9.grid(column=5, row=5, sticky=(E, N))
buttonEx10.grid(column=5, row=6, sticky=(E, N))

updateSideFrame()

root.mainloop()
