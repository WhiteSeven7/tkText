import tkinter as tk


def create_window(title: str, w, h, x=200, y=200):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    return ro


root = create_window("计算器", 300, 400)
label = tk.Label(root, text='你好', relief='sunken', background='#D4D265')
label.pack()
root.mainloop()
