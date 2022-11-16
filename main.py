import tkinter as tk
import tkinter.messagebox as ms


class Time:
    def __init__(self, h=0, m=0, s=0):
        self.h = h
        self.m = m
        self.s = s
        self.running = False

    def tick(self):
        if self.s > 0:
            self.s -= 1
        elif self.m > 0:
            self.m -= 1
            self.s += 59
        elif self.h > 0:
            self.h -= 1
            self.m += 59
            self.s += 59
        else:
            func_stop()
            ms.showinfo('提示', '倒计时结束')

    def set(self, h, m, s):
        self.h = int(h)
        self.m = int(m)
        self.s = int(s)

    def zero(self):
        self.h = self.m = self.s = 0

    def __repr__(self):
        return f'{self.h}时:{self.m}分:{self.s}秒'


def create_window(title: str, w, h, x=200, y=200):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    ro.iconbitmap('myIcon.ico')
    return ro


def create_label(master, v):
    return tk.Label(master, font=('Aril', 24), textvariable=v)


def func_start():
    time.running = True
    time.set(entry1.get(), entry2.get(), entry3.get())
    value.set(str(time))
    b1.config(state='disabled')
    b2.config(state='active')
    b3.config(state='active')
    label.pack()


def func_pause():
    time.running = False
    b2.config(text='回复', command=func_reply)


def func_reply():
    time.running = True
    b2.config(text='暂停', command=func_pause)


def func_stop():
    time.running = False
    time.zero()
    value.set(str(time))
    b1.config(state='active')
    b2.config(state='disabled')
    b3.config(state='disabled')


def time_func():
    if time.running:
        time.tick()
        value.set(str(time))
    root.after(1000, time_func)


def change_num(iv: tk.IntVar, com: int):
    def inner_func():
        iv.set(iv.get() + com)

    return inner_func


root = create_window('倒计时', 400, 300)
time = Time(1, 1, 1)
value = tk.StringVar(value='在下面设计倒数时间')
label = tk.Label(root, font=('Aril', 24), textvariable=value, relief='groove', bd=4)
label.pack(pady=20)

frame2 = tk.Frame(root)
b1 = tk.Button(frame2, text='开始', font=('Aril', 16), command=func_start)
b1.pack(side='left', padx=10)
b2 = tk.Button(frame2, text='暂停', font=('Aril', 16), command=func_pause, state='disabled')
b2.pack(side='left', padx=10)
b3 = tk.Button(frame2, text='终止', font=('Aril', 16), command=func_stop, state='disabled')
b3.pack(side='left', padx=10)
frame2.pack(pady=(0, 20))

frame3 = tk.Frame(root)
label_top = tk.Label(frame3, text='倒计时', font=('Aril', 20))
label_top.pack(side='left', padx=(0, 5))

value1 = tk.IntVar(value=0)
entry1 = tk.Spinbox(frame3, width=4, from_=0, to=23, textvariable=value1)
entry1.pack(side='left')
label_h = tk.Label(frame3, text='h', font=('Aril', 20))
label_h.pack(side='left', padx=(0, 10))

entry2 = tk.Spinbox(frame3, width=4, from_=0, to=59, textvariable=tk.IntVar(value=0))
entry2.pack(side='left')
label_m = tk.Label(frame3, text='m', font=('Aril', 20))
label_m.pack(side='left', padx=(0, 10))

entry3 = tk.Spinbox(frame3, width=4, from_=0, to=59, textvariable=tk.IntVar(value=0))
entry3.pack(side='left')
label_s = tk.Label(frame3, text='s', font=('Aril', 20))
label_s.pack(side='left', padx=(0, 10))

frame3.pack()

time_func()

root.mainloop()
