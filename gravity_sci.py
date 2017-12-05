from tkinter import *
from numpy import *
from scipy.integrate import odeint


class GravityWindow:
    pause = False
    
    def __init__(self, master, width=1200, height=800):
        self.width, self.height = width, height
        self.firstClick = 0, 0
        self.pointer, self.velocityText = None, None
        self.master = master
        master.title('Gravity')
        master.resizable(width=False, height=False)
        
        self.massLabel = Label(text='Current Mass')
        self.massLabel.grid(row=0, column=3, stick='E')
        self.massField = Entry(master)
        self.massField.insert(END, '3')
        self.massField.grid(row=0, column=4, stick='W')
        self.clearAllButton = Button(text='Clear All', command=self.clear_button_click)
        self.clearAllButton.grid(row=0, column=5)
        self.initiateButton1 = Button(text='Draw me 8!', command=self.initiate_button1_click)
        self.initiateButton1.grid(row=0, column=6)
        self.challengeButton1 = Button(text='Challenge', command=self.challenge_button_click)
        self.challengeButton1.grid(row=0, column=7)
        self.pauseButton = Button(text='Pause', width=10, command=self.pause_button_click)
        self.pauseButton.grid(row=0, column=2)
        
        self.canvas = Canvas(master, width=width, height=height, bg="#000000")
        self.canvas.grid(row=1, column=0, columnspan=8)
        self.canvas.bind('<Button-1>', self.mouse1_click)
        self.canvas.bind('<ButtonRelease-1>', self.mouse1_release)
        self.canvas.bind('<B1-Motion>', self.mouse1_motion)
    
    def pause_button_click(self):
        if self.pause:
            GravityWindow.pause = False
            self.pauseButton['text'] = 'Pause'
        else:
            GravityWindow.pause = True
            self.pauseButton['text'] = 'Unpause'
    
    def clear_button_click(self):
        self.canvas.delete('all')
        self.massField['state'] = 'normal'
        self.massField.delete(0, END)
        self.massField.insert(END, 3)
        for i, obj in enumerate(Planet.listOfObjects):
            obj.r = array([-200. - 10 * i, -200.])
    
    def mouse1_click(self, event):
        self.firstClick = event.x, event.y
        vx, vy = (event.x - self.firstClick[0]) / 1000, (event.y - self.firstClick[1]) / 1000
        self.pointer = self.canvas.create_line(event.x, event.y, event.x + 1, event.y + 1, fill='gray')
        self.velocityText = self.canvas.create_text(self.firstClick[0], self.firstClick[1], fill='white',
                                                    text='{:1.3}'.format((vx ** 2 + vy ** 2) ** 0.5))
    
    def mouse1_motion(self, event):
        self.canvas.delete(self.pointer)
        self.canvas.delete(self.velocityText)
        vx, vy = (event.x - self.firstClick[0]) / 1000, (event.y - self.firstClick[1]) / 1000
        self.velocityText = self.canvas.create_text(self.firstClick[0], self.firstClick[1], fill='white',
                                                    text='{:1.3}'.format((vx ** 2 + vy ** 2) ** 0.5))
        self.pointer = self.canvas.create_line(self.firstClick[0], self.firstClick[1], event.x, event.y, fill='gray')
    
    def mouse1_release(self, event):
        self.canvas.delete(self.pointer)
        self.canvas.delete(self.velocityText)
        vx, vy = (event.x - self.firstClick[0]) / 1000, (event.y - self.firstClick[1]) / 1000
        Planet(self.canvas, self.firstClick[0], self.firstClick[1], vx, vy, abs(float(self.massField.get())))
    
    def initiate_button1_click(self):
        self.clear_button_click()
        Planet(self.canvas, -1.43250000e+02 + self.width / 2, 0 + self.height / 2,
               -1.70327750e-02, -2.61404295e-02, 0.3333333)
        Planet(self.canvas, 1.43250000e+02 + self.width / 2, 0 + self.height / 2,
               -1.70327750e-02, -2.61404295e-02, 0.3333333)
        Planet(self.canvas, 0 + self.width / 2, 0 + self.height / 2,
               3.40655500e-02, 5.22808591e-02, 0.33333333)
    
    def challenge_button_click(self):
        self.clear_button_click()
        x, y = self.width / 2, self.height / 2
        Planet(self.canvas, x, y, 0., 0., 80)
        self.massField.delete(0, END)
        self.massField.insert(END, 0)
        self.massField['state'] = 'disabled'
        self.canvas.create_oval(x - 200, y - 200, x + 200, y + 200, outline='gray')
        self.canvas.create_oval(x - 300, y - 300, x + 300, y + 300, outline='gray')


class Planet:
    listOfObjects = []
    stepT = 10.
    afterT = 50
    canvas = None
    
    def __init__(self, c, x, y, vx, vy, mass):
        if Planet.canvas is None:
            Planet.canvas = c
        self.mass = mass
        self.r = array([x, y], dtype=float)
        self.v = array([vx, vy], dtype=float)
        self.color = self.random_color()
        r = max(min(self.mass, 10), 3)
        self.oval = Planet.canvas.create_oval(self.r[0] - r, self.r[1] - r,
                                              self.r[0] + r, self.r[1] + r,
                                              fill=self.color, outline=self.color)
        Planet.canvas.tag_raise(self.oval)
        Planet.listOfObjects.append(self)
        if len(Planet.listOfObjects) == 1:
            Planet.infinite_movement()
    
    @staticmethod
    def infinite_movement():
        if GravityWindow.pause:
            Planet.canvas.after(Planet.afterT, Planet.infinite_movement)
            return
        if len(Planet.listOfObjects) == 0:
            Planet.canvas.after(Planet.afterT, Planet.infinite_movement)
            return
        
        def ode_func(vector, _):
            temp = []
            n_obj = len(Planet.listOfObjects)
            for k in range(n_obj):
                temp.append(vector[4 * k + 2:4 * k + 4])
                acs = [0., 0.]
                for j, item in enumerate(Planet.listOfObjects):
                    if k == j:
                        continue
                    acs += (item.mass * (vector[4 * j:4 * j + 2] - vector[4 * k:4 * k + 2])
                            / linalg.norm(vector[4 * j:4 * j + 2] - vector[4 * k:4 * k + 2]) ** 3)
                temp.append(acs)
            return vstack(temp).ravel()
        
        initials = []
        for obj in Planet.listOfObjects:
            initials.append(obj.r)
            initials.append(obj.v)
        initials = vstack(initials).ravel()
        solution = odeint(ode_func, initials, [0, Planet.stepT])
        for i, obj in enumerate(Planet.listOfObjects):
            obj.r = solution[-1, 4 * i:4 * i + 2]
            obj.v = solution[-1, 4 * i + 2:4 * i + 4]
            Planet.canvas.move(obj.oval, obj.r[0] - initials[4 * i], obj.r[1] - initials[4 * i + 1])
            line = Planet.canvas.create_line(initials[4 * i], initials[4 * i + 1], obj.r[0], obj.r[1], fill=obj.color)
            Planet.canvas.tag_lower(line)
        for obj in Planet.listOfObjects:
            if obj.r[0] < -20 or obj.r[0] > 2000 or obj.r[1] < -20 or obj.r[0] > 2000:
                Planet.listOfObjects.remove(obj)
                del obj.oval
                del obj
        Planet.canvas.after(Planet.afterT, Planet.infinite_movement)
    
    @staticmethod
    def random_color():
        return '#{}'.format(''.join([str(hex(random.randint(2, 16)))[2:].upper() for _ in range(6)]))


if __name__ == '__main__':
    root = Tk()
    window = GravityWindow(root)
    root.mainloop()
