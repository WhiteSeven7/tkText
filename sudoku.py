import tkinter as tk
from typing import Union, Tuple, Dict

num_font = ("黑体", 24)
text_font = None


def create_window(title: str, w, h, x=500, y=150):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    return ro


def click(self: 'MyLabel'):
    def inner_func(event):
        if app.control.select is self:
            app.control.set(None)
            self.label.config(background='green')
            return
        if app.control.select:
            app.control.select.label.config(background='green')
        app.control.set(self)
        self.label.config(background='red')

    return inner_func


class MyLabel:
    def __init__(self, master: tk.Misc, row: int, column: int, value: int):
        self.row = row
        self.column = column
        self.value = tk.StringVar(value=str(value))
        self.label = tk.Label(master, font=num_font, textvariable=self.value, relief='raised', bg='green')
        self.label.config(width=2, height=1)
        self.label.bind('<Button-1>', click(self))

    def change(self, num: int):
        if num == 0:
            self.value.set(' ')
        else:
            self.value.set(str(num))

    def layout(self):
        self.label.grid(row=self.row, column=self.column, padx=1, pady=1)


class MyLabelDict:
    def __init__(self, master: tk.Misc, row_num: int, column_num: int):
        self.group = {(row, column): MyLabel(master, row, column, 0)
                      for row in range(row_num)
                      for column in range(column_num)}

    def layout(self):
        for my_Label in self.group.values():
            my_Label.layout()


class MyFrame:
    def __init__(self, master: tk.Misc, row: int, column: int):
        self.row = row
        self.column = column
        self.frame = tk.Frame(master, relief='groove')

    def layout(self):
        self.frame.grid(row=self.row, column=self.column, padx=3, pady=3)


class Block:
    def __init__(self, master: tk.Misc, row: int, column: int, row_num: int, column_num: int):
        self.my_frame = MyFrame(master, row, column)
        self.my_label_dict = MyLabelDict(self.my_frame.frame, row_num, column_num)

    def layout(self):
        self.my_label_dict.layout()
        self.my_frame.layout()


class FrameDict:
    group: Dict[Tuple[int, int], 'Block']

    def __init__(self, master: tk.Misc, row_num: int, column_num: int, rn: int, cn: int):
        self.group = {(row, column): Block(master, row, column, rn, cn)
                      for row in range(row_num)
                      for column in range(column_num)}

    def layout(self):
        for my_frame in self.group.values():
            my_frame.layout()


class Window:
    def __init__(self):
        self.root = create_window("数独游戏", 500, 400)
        self.frame = tk.Frame(self.root)
        self.frame_dict = FrameDict(self.frame, 3, 3, 3, 3)
        self.frame_dict.layout()
        self.frame.pack(side='bottom')

    def run(self):
        self.root.mainloop()


class Control:
    def __init__(self):
        self.select: Union['MyLabel', None] = None

    def bind(self, window: 'Window'):
        window.root.bind('<Key>', self.key_press())

    def set(self, my_label: Union['MyLabel', None]):
        self.select = my_label

    def key_press(self):
        def inner_func(event: tk.Event):
            if not self.select:
                return
            try:
                num = int(event.keysym)
            except ValueError:
                if event.keysym in ('BackSpace', 'space'):
                    num = 0
                else:
                    return
            self.select.change(num)

        return inner_func


class App:
    def __init__(self):
        self.window = Window()
        self.control = Control()
        self.control.bind(self.window)

    def run(self):
        self.window.run()


app = App()
app.run()
