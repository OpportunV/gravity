from tkinter import *
from numpy import *


class GravityWindow:
    def __init__(self, master, width=800, height=800):
        self.master = master
        master.title('Gravity')

        self.massLabel = Label(text='Current Mass')
        self.massLabel.grid(row=1, column=3, stick='E')
        self.massField = Entry(master)
        self.massField.insert(END, '1')
        self.massField.grid(row=1, column=4, stick='W')
        
        self.canvas = Canvas(root, width=width, height=height, bg="#000000")
        self.canvas.grid(row=0, column=0, columnspan=8)
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.mouse1_click)
            
    def mouse1_click(self, event):
        Oval(self.canvas, event.x, event.y, float(self.massField.get()))


class Oval:
    list_of_objects = []
    
    def __init__(self, c, x, y, mass):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = self.random_color()
        self.canvas = c
        self.oval = self.canvas.create_oval(self.x - self.mass, self.y - self.mass,
                                            self.x + self.mass, self.y + self.mass,
                                            fill=self.color, outline=self.color)
        Oval.list_of_objects.append(self)
        self.infinite_movement()
        
    def infinite_movement(self):
        x = random.randint(-1, 2)
        y = random.randint(-1, 2)
        self.canvas.move(self.oval, x, y)
        self.canvas.after(10, self.infinite_movement)
        
    @staticmethod
    def random_color():
        return '#' + ''.join([str(hex(random.randint(0, 15)))[2:].upper() for i in range(6)])


if __name__ == '__main__':
    WIDTH, HEIGHT = 800, 800
    root = Tk()
    GravityWindow(root)
    root.mainloop()
