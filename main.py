from tkinter import *
from numpy import *


class GravityWindow:
    def __init__(self, master, width=800, height=800):
        self.master = master
        master.title('Gravity')

        self.massLabel = Label(text='Current Mass')
        self.massLabel.grid(row=0, column=3, stick='E')
        self.clearButton = Button(text='Clear All')
        self.clearButton.grid(row=0, column=5)
        self.clearButton.bind('<Button-1>', self.clear_button_click)
        self.massField = Entry(master)
        self.massField.insert(END, '3')
        self.massField.grid(row=0, column=4, stick='W')
        
        self.canvas = Canvas(root, width=width, height=height, bg="#000000")
        self.canvas.grid(row=1, column=0, columnspan=8)
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.mouse1_click)
        
    def clear_button_click(self, event):
        self.canvas.delete('all')
        for i, obj in enumerate(Planet.list_of_objects):
            obj.r = array([-200. - 10 * i, -200.])
            
    def mouse1_click(self, event):
        Planet(self.canvas, event.x, event.y, float(self.massField.get()))


class Planet:
    list_of_objects = []
    G = 6.67 * 10 ** -11
    stepT = 10.
    afterT = 100
    
    def __init__(self, c, x, y, mass):
        self.mass = mass
        self.r = array([x, y], dtype=float)
        self.v = array([0., 0.])
        self.color = self.random_color()
        self.canvas = c
        r = max(2, min(10, self.mass))
        self.oval = self.canvas.create_oval(self.r[0] - r, self.r[1] - r,
                                            self.r[0] + r, self.r[1] + r,
                                            fill=self.color, outline=self.color)
        Planet.list_of_objects.append(self)
        self.infinite_movement()
        
    def infinite_movement(self):
        acs = array([0., 0.])
        tempr = self.r.copy()
        for obj in Planet.list_of_objects:
            if obj == self:
                continue
            acs += obj.mass * (obj.r - self.r) / linalg.norm(obj.r - self.r) ** 3
        self.v += acs * Planet.stepT
        self.r += self.v * Planet.stepT
        self.canvas.move(self.oval, self.r[0] - tempr[0], self.r[1] - tempr[1])
        if self.r[0] < -20 or self.r[0] > 2000 or self.r[1] < -20 or self.r[0] > 2000:
            Planet.list_of_objects.remove(self)
            del self.oval
            del self
            return
        self.canvas.after(Planet.afterT, self.infinite_movement)
        
    @staticmethod
    def random_color():
        return '#' + ''.join([str(hex(random.randint(2, 15)))[2:].upper() for i in range(6)])


if __name__ == '__main__':
    WIDTH, HEIGHT = 1200, 800
    root = Tk()
    GravityWindow(root, WIDTH, HEIGHT)
    root.mainloop()
