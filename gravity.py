from tkinter import *
from numpy import *


class GravityWindow:
    def __init__(self, master, width=800, height=800):
        self.firstClick = 0, 0
        self.master = master
        master.title('Gravity')
        master.resizable(width=False, height=False)

        self.massLabel = Label(text='Current Mass')
        self.massLabel.grid(row=0, column=3, stick='E')
        self.massField = Entry(master)
        self.massField.insert(END, '3')
        self.massField.grid(row=0, column=4, stick='W')
        self.clearAllButton = Button(text='Clear All')
        self.clearAllButton.grid(row=0, column=5)
        self.clearAllButton.bind('<Button-1>', self.clear_button_click)
        self.initiateButton1 = Button(text='Draw me 8!')
        self.initiateButton1.grid(row=0, column=6)
        self.initiateButton1.bind('<Button-1>', self.initiate_button1_click)

        self.canvas = Canvas(master, width=width, height=height, bg="#000000")
        self.canvas.grid(row=1, column=0, columnspan=8)
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.mouse1_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse1_release)
        
    def clear_button_click(self, event):
        Planet.afterT = 100
        self.canvas.delete('all')
        for i, obj in enumerate(Planet.listOfObjects):
            obj.r = array([-200. - 10 * i, -200.])
            
    def mouse1_click(self, event):
        self.firstClick = event.x, event.y
        
    def mouse1_release(self, event):
        vx = (event.x - self.firstClick[0]) / 1000
        vy = (event.y - self.firstClick[1]) / 1000
        Planet(self.canvas, self.firstClick[0], self.firstClick[1], vx, vy, abs(float(self.massField.get())))
    
    def initiate_button1_click(self, event):
        self.clear_button_click(event)
        Planet.afterT = 50
        Planet(self.canvas, -1.43250000e+02 + 400, 0 + 400,
               -1.70327750e-02, -2.61404295e-02, 0.3333333)
        Planet(self.canvas, 1.43250000e+02 + 400, 0 + 400,
               -1.70327750e-02, -2.61404295e-02, 0.3333333)
        Planet(self.canvas, 0 + 400, 0 + 400,
               3.40655500e-02, 5.22808591e-02, 0.333333)


class Planet:
    listOfObjects = []
    stepT = 10.
    afterT = 100
    
    def __init__(self, c, x, y, vx, vy, mass):
        self.mass = mass
        self.r = array([x, y], dtype=float)
        self.v = array([vx, vy], dtype=float)
        self.color = self.random_color()
        self.canvas = c
        r = max(min(self.mass, 10), 3)
        self.oval = self.canvas.create_oval(self.r[0] - r, self.r[1] - r,
                                            self.r[0] + r, self.r[1] + r,
                                            fill=self.color, outline=self.color)
        self.canvas.tag_raise(self.oval)
        Planet.listOfObjects.append(self)
        self.infinite_movement()
        
    def infinite_movement(self):
        acs = array([0., 0.])
        tempr = self.r.copy()
        for obj in Planet.listOfObjects:
            if obj == self:
                continue
            acs += obj.mass * (obj.r - self.r) / linalg.norm(obj.r - self.r) ** 3
        self.v += acs * Planet.stepT
        self.r += self.v * Planet.stepT
        self.canvas.move(self.oval, self.r[0] - tempr[0], self.r[1] - tempr[1])
        line = self.canvas.create_line(tempr[0], tempr[1], self.r[0], self.r[1], fill=self.color)
        self.canvas.tag_lower(line)
        if self.r[0] < -20 or self.r[0] > 2000 or self.r[1] < -20 or self.r[0] > 2000:
            Planet.listOfObjects.remove(self)
            del self.oval
            del self
            return
        self.canvas.after(Planet.afterT, self.infinite_movement)
        
    @staticmethod
    def random_color():
        return '#{}'.format(''.join([str(hex(random.randint(2, 16)))[2:].upper() for i in range(6)]))


if __name__ == '__main__':
    WIDTH, HEIGHT = 1200, 800
    root = Tk()
    window = GravityWindow(root, WIDTH, HEIGHT)
    root.mainloop()
