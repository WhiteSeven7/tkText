import tkinter as tk

num_font = ("黑体", 24)
text_font = None


def create_window(title: str, w, h, x=200, y=200):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    return ro


class MyLabel:
    def __init__(self, master, row, column, value: int):
        self.row = row
        self.column = column
        self.value = tk.StringVar(value=str(value))
        self.label = tk.Label(master, font=num_font, textvariable=self.value, relief='raised')
        self.label.config(width=2, height=1)

    def layout(self):
        self.label.grid(row=self.row, column=self.column, padx=1, pady=1)

    def change(self, num: int):
        if num == 0:
            self.value.set(' ')
        else:
            self.value.set(str(num))


class MyFrame:
    def __init__(self, master, row, column):
        self.row = row
        self.column = column
        self.frame = tk.Frame(master, relief='groove', background=self.color())

    def color(self):
        return 'red' if (self.row + self.column) % 2 else 'white'

    def layout(self):
        self.frame.grid(row=self.row, column=self.column, padx=3, pady=3)


class Block:
    def __init__(self, master, row, column, row_num, column_num):
        self.my_frame = MyFrame(master, row, column)
        self.my_label_dict = MyLabelDict(self.my_frame.frame, row_num, column_num)

    def layout(self):
        self.my_label_dict.layout()
        self.my_frame.layout()


class MyLabelDict:
    def __init__(self, master, row_num, column_num):
        self.group = {(row, column): MyLabel(master, row, column, 1)
                      for row in range(row_num)
                      for column in range(column_num)}

    def layout(self):
        for my_Label in self.group.values():
            my_Label.layout()


class FrameDict:
    def __init__(self, master, row_num, column_num, rn, cn):
        self.group = {(row, column): Block(master, row, column, rn, cn)
                      for row in range(row_num)
                      for column in range(column_num)}

    def layout(self):
        for my_frame in self.group.values():
            my_frame.layout()


root = create_window("数独游戏", 600, 600)
frame = tk.Frame(root)
frame_dict = FrameDict(frame, 3, 3, 3, 3)
frame_dict.layout()
frame.pack(side='bottom')
root.mainloop()
