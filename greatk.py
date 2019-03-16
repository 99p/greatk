import tkinter as tk
from ctypes import windll

class GreaTK(tk.Tk):
    def __init__(self, width=480, height=280, title='The Great App', title_fg='ghostwhite', title_bg='turquoise', title_accent='aquamarine'):
        self.Init()
        self.Geometry(width, height)
        self.Title(title, title_fg, title_bg, title_accent)

    def Init(self):
        super().__init__()
        self.entire_multi_screen_x, self.entire_multi_screen_y = windll.user32.GetSystemMetrics(78), windll.user32.GetSystemMetrics(79)
        self.bind('q', lambda e:self.destroy())
        self.bind('<Alt-m>', self.Iconify)
        self.b1 = self.bind("<ButtonPress-1>", self.StartMove)
        self.b2 = self.bind("<ButtonRelease-1>", self.StopMove)
        self.b3 = self.bind("<B1-Motion>", self.MoveWindow)
        self.overrideredirect(True)
        self.after(10, lambda: self.SetAppwindow())
        self.after(11, lambda:windll.user32.SetForegroundWindow(windll.user32.GetParent(self.winfo_id())))

    def Title(self, title='The Great App', fg='ghostwhite', bg='turquoise', grips='aquamarine', setButton=False):
        self.title_bg_color = bg
        if not setButton:
            self.title(title)
            self.title_frame = tk.Frame(self, height=22, bg=bg)
            self.title_frame.pack(fill='both')
            self.title_label = tk.Label(self.title_frame, text=title, fg=fg, bg=bg, font='Tahoma 10 bold')
            self.title_label.pack(fill='both')
            self.title_label.bind('<Double-Button-1>', self.MaximizeWindow)
            self.update()
            self.quit_button = tk.Canvas(self.title_frame, width=16, height=16 , bg=bg, highlightthickness=0)
            self.quit_button.create_oval(0,0,13,13, fill='darkred', activefill='red', outline='')
            self.quit_button.bind("<ButtonPress-1>", lambda e:self.destroy())
            self.maximize_button = tk.Canvas(self.title_frame, width=16, height=16 , bg=bg, highlightthickness=0)
            self.maximize_button.create_oval(0,0,13,13, fill='forestgreen', activefill='greenyellow', outline='')
            self.maximize_button.bind("<ButtonPress-1>", self.MaximizeWindow)
            self.iconify_button = tk.Canvas(self.title_frame, width=16, height=16 , bg=bg, highlightthickness=0)
            self.iconify_button.create_oval(0,0,13,13, fill='goldenrod', activefill='gold', outline='')
            self.iconify_button.bind("<ButtonPress-1>", self.Iconify)
            self.SetGrips(grips)
        self.quit_button.place(anchor='ne', x=self.title_frame.winfo_width()-5, y=3)
        self.maximize_button.place(anchor='ne', x=self.title_frame.winfo_width()-25, y=3)
        self.iconify_button.place(anchor='ne', x=self.title_frame.winfo_width()-45, y=3)

    def Geometry(self, x, y):
        self.initialX = x
        self.initialY = y
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2 - x/2)
        positionDown = int(self.winfo_screenheight()/2 - windowHeight/2 - y/2)
        self.geometry(f"{x}x{y}+{positionRight}+{positionDown}")

    def MaximizeWindow(self, event):
        if self.winfo_height() != self.winfo_screenheight() and self.winfo_width() != self.winfo_screenwidth():
            self.before_geometry = self.geometry()
            if self.winfo_rootx() > self.winfo_screenwidth():
                self.geometry(f"{self.entire_multi_screen_x - self.winfo_screenwidth()}x{self.entire_multi_screen_y}+{self.winfo_screenwidth()}+0")
            else:
                self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self.update()
            self.Title(setButton=True)
        elif hasattr(self, 'before_geometry'):
            self.geometry(self.before_geometry)
            self.update()
            self.Title(setButton=True)
        else:
            self.Geometry(self.initialX, self.initialY)
            self.update()
            self.Title(setButton=True)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def MoveWindow(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def StartResize(self, event):
        self.unbind("<ButtonPress-1>", self.b1)
        self.unbind("<ButtonRelease-1>", self.b2)
        self.unbind("<B1-Motion>", self.b3)
        self.b4 = self.bind("<B1-Motion>", self.ResizeWindow)
        self.update()
        self.west = self.winfo_rootx()
        self.north = self.winfo_rooty()
        self.east = self.winfo_rootx() + self.winfo_width()
        self.south = self.winfo_rooty() + self.winfo_height()

    def StopResize(self, event):
        self.unbind("<B1-Motion>", self.b4)
        self.b1 = self.bind("<ButtonPress-1>", self.StartMove)
        self.b2 = self.bind("<ButtonRelease-1>", self.StopMove)
        self.b3 = self.bind("<B1-Motion>", self.MoveWindow)

    def ResizeWindow(self, e):
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        x_mid = ((self.east-self.west)//2)+self.west
        y_mid = ((self.south-self.north)//2)+self.north
        if   str(e.widget) == '.grip_nw' :
            W = 250 if (self.east-x) < 250 else (self.east-x)
            H = 150 if (self.south-y) < 150 else (self.south-y)
            X, Y = (self.east-self.winfo_width()), (self.south-self.winfo_height())
        elif str(e.widget) == '.grip_ne':
            W = 250 if (x-self.west) < 250 else (x-self.west)
            H = 150 if (self.south-y) < 150 else (self.south-y)
            X, Y = self.west, (self.south-self.winfo_height())
        elif str(e.widget) == '.grip_sw':
            W = 250 if (self.east-x) < 250 else (self.east-x)
            H = 150 if (y-self.north) < 150 else (y-self.north)
            X, Y = (self.east-self.winfo_width()), self.north
        elif str(e.widget) == '.grip_se':
            W = 250 if (x-self.west) < 250 else (x-self.west)
            H = 150 if (y-self.north) < 150 else (y-self.north)
            X, Y = self.west, self.north
        self.geometry(f"{W}x{H}+{X}+{Y}")
        self.Title(setButton=True)

    def SetGrips(self, grips="aquamarine"):
        self.grip_nw = tk.Canvas(name="grip_nw", width=3, height=22, cursor="ul_angle",highlightthickness=0)
        self.grip_nw.create_rectangle(0,0,3,22,fill=grips,outline="")
        self.grip_nw.place(relx=0, rely=0, anchor="nw")
        self.grip_nw.bind("<ButtonPress-1>", self.StartResize)
        self.grip_nw.bind("<ButtonRelease-1>", self.StopResize)
        self.grip_ne = tk.Canvas(name="grip_ne", width=3, height=22, cursor="ur_angle",highlightthickness=0)
        self.grip_ne.create_rectangle(0,0,3,22,fill=grips,outline="")
        self.grip_ne.place(relx=1.0, rely=0, anchor="ne")
        self.grip_ne.bind("<ButtonPress-1>", self.StartResize)
        self.grip_ne.bind("<ButtonRelease-1>", self.StopResize)
        self.grip_sw = tk.Canvas(name="grip_sw", width=15, height=15, cursor="ll_angle",highlightthickness=0)
        self.grip_sw.create_rectangle(0,0,15,15,fill="",outline="")
        self.grip_sw.place(relx=0, rely=1.0, anchor="sw")
        self.grip_sw.bind("<ButtonPress-1>", self.StartResize)
        self.grip_sw.bind("<ButtonRelease-1>", self.StopResize)
        self.grip_se = tk.Canvas(name="grip_se", width=15, height=15, cursor="lr_angle",highlightthickness=0)
        self.grip_se.create_rectangle(0,0,15,15,fill="",outline="")
        self.grip_se.place(relx=1.0, rely=1.0, anchor="se")
        self.grip_se.bind("<ButtonPress-1>", self.StartResize)
        self.grip_se.bind("<ButtonRelease-1>", self.StopResize)

    def SetAppwindow(self):
        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080

        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        self.wm_withdraw()
        self.after(10, lambda: self.wm_deiconify())

    def Iconify(self, event):
        windll.user32.ShowWindow(windll.user32.GetParent(self.winfo_id()),6)
