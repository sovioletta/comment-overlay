import tkinter as tk
import win32api
import win32con
import pywintypes
import threading
import time


class App(threading.Thread):
    def __init__(self):
        self.root = None
        self.label = None
        self.x = 250
        self.y = 250
        threading.Thread.__init__(self)
        self.start()

    def move(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.x += 10
        self.label.master.geometry('+{}+{}'.format(self.x, self.y))
        self.root.after(33, self.move)

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.label = tk.Label(text='Text on the screen', font=('Times New Roman','80'), fg='black', bg='white')
        self.label.master.overrideredirect(True)
        self.label.master.geometry("+{}+{}".format(self.x, self.y))
        self.label.master.lift()
        self.label.master.wm_attributes("-topmost", True)
        self.label.master.wm_attributes("-disabled", True)
        self.label.master.wm_attributes("-transparentcolor", "white")

        h_window = pywintypes.HANDLE(int(self.label.master.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        ex_style = win32con.WS_EX_COMPOSITED \
            | win32con.WS_EX_LAYERED \
            | win32con.WS_EX_NOACTIVATE \
            | win32con.WS_EX_TOPMOST \
            | win32con.WS_EX_TRANSPARENT

        win32api.SetWindowLong(h_window, win32con.GWL_EXSTYLE, ex_style)

        self.label.pack()
        self.move()
        self.label.mainloop()


app = App()

time.sleep(1)

