import tkinter as tk
import win32api
import win32con
import pywintypes
import threading
import time
import queue
import random


class App(threading.Thread):
    class Comment:
        def __init__(self, label, x, y, size):
            self.label = label
            self.x = x
            self.y = y
            self.size = size

    def __init__(self, q):
        self.root = None
        self.input_queue = q
        self.comment_list = []

        self.width = 1280
        self.height = 800
        self.pos_x = 250
        self.pos_y = 250

        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def create_comment(self, text):
        size = 40
        y = random.choice(range(0, self.height - size))
        label = tk.Label(text=text, font=('Times New Roman', str(size)), fg='white', bg='black')
        label.pack()
        return self.Comment(label, 0, y, size)

    def check_and_move(self):
        while not self.input_queue.empty():
            try:
                text = self.input_queue.get()
            except queue.Empty:
                continue

            comment = self.create_comment(text)
            self.comment_list.append(comment)
            self.input_queue.task_done()

        for i in self.comment_list:
            i.x += 6
            i.label.place(x=i.x, y=i.y)
            self.root.wm_attributes("-transparentcolor", "black")

        self.root.configure(background='black')
        self.root.after(33, self.check_and_move)

    def run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("800x800+{}+{}".format(250, 250))
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-disabled", True)
        self.root.wm_attributes("-transparentcolor", "black")

        h_window = pywintypes.HANDLE(int(self.root.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        ex_style = win32con.WS_EX_COMPOSITED \
            | win32con.WS_EX_LAYERED \
            | win32con.WS_EX_NOACTIVATE \
            | win32con.WS_EX_TOPMOST \
            | win32con.WS_EX_TRANSPARENT

        win32api.SetWindowLong(h_window, win32con.GWL_EXSTYLE, ex_style)

        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.check_and_move()
        self.root.mainloop()


q = queue.Queue()
app = App(q)
q.put('test100')

for i in range(0, 40):
    q.put('testtestestestestestst')
    time.sleep(0.2)



