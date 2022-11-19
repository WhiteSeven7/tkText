import itertools
import tkinter as tk
from typing import Union, Tuple, Dict, List

num_font = ("黑体", 24)
text_font = None


def create_window(title: str, w: int, h: int, x: int = 500, y: int = 150):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    return ro


def click(self: 'MyLabel'):
    def inner_func(event):
        other = app.control.select
        if other is self:
            self.unselect()
            app.control.select = None
            return
        if other:
            other.unselect()
        self.select()
        app.control.select = self

    return inner_func


class MyLabel:
    wrong: Dict[str, bool]

    def __init__(self, master: tk.Misc, row: int, column: int, fr: int, fc: int, value: str):
        self.row = row
        self.column = column
        self.f_row = fr
        self.f_column = fc
        self.value = tk.StringVar(value=value)
        self.label = tk.Label(master, font=num_font, textvariable=self.value, relief='raised', bg='green', width=2,
                              height=1)
        self.label.bind('<Button-1>', click(self))
        self.wrong = {'block': False, 'row': False, 'column': False}

    def get(self):
        return self.value.get()

    def set(self, num: int):
        value = ' ' if num == 0 else str(num)
        self.value.set(value)

    def set_same_dif(self, select: 'MyLabel', range_: str, bool_: bool):
        self.wrong[range_] = bool_
        if select is self:
            self.label['bg'] = 'orange' if self.is_wrong() else 'blue'
        else:
            self.label['bg'] = 'red' if self.is_wrong() else 'green'

    def select(self):
        self.label['bg'] = 'orange' if self.is_wrong() else 'blue'

    def unselect(self):
        self.label['bg'] = 'red' if self.is_wrong() else 'green'

    def layout(self):
        self.label.grid(row=self.row, column=self.column, padx=1, pady=1)

    def is_wrong(self):
        return any(self.wrong.values())


class MyLabelDict:
    group: Dict[Tuple[int, int], 'MyLabel']

    def __init__(self, master: tk.Misc, row_num: int, column_num: int, fr: int, fc: int):
        self.group = {(row, column): MyLabel(master, row, column, fr, fc, ' ')
                      for row in range(row_num)
                      for column in range(column_num)}

    def __getitem__(self, item):
        return self.group[item]

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
        self.my_label_dict = MyLabelDict(self.my_frame.frame, row_num, column_num, row, column)

    def __getitem__(self, item):
        return self.my_label_dict[item]

    def values(self):
        return self.my_label_dict.group.values()

    def layout(self):
        self.my_label_dict.layout()
        self.my_frame.layout()


class FrameDict:
    group: Dict[Tuple[int, int], 'Block']
    row_group: List[List['MyLabel']]
    column_group: List[List['MyLabel']]

    def __init__(self, master: tk.Misc, row_num: int, column_num: int, rn: int, cn: int):
        self.group = {(row, column): Block(master, row, column, rn, cn)
                      for row in range(row_num)
                      for column in range(column_num)}
        self.row_group = []
        self.column_group = []
        self._make_group(row_num, column_num, rn, cn)

    def _make_group(self, row_num: int, column_num: int, rn: int, cn: int):
        # 横表
        for fr, row_ in itertools.product(range(row_num), range(rn)):
            _ = [self[(fr, fc)].my_label_dict.group[(row_, column_)] for fc, column_ in
                 itertools.product(range(column_num), range(cn))]
            self.row_group.append(_)
        # 竖表
        for fc, column_ in itertools.product(range(row_num), range(rn)):
            _ = [self[(fr, fc)].my_label_dict.group[(row_, column_)] for fr, row_ in
                 itertools.product(range(column_num), range(cn))]
            self.column_group.append(_)

    def __getitem__(self, item):
        return self.group[item]

    def values(self):
        return self.group.values()

    def layout(self):
        for my_frame in self.values():
            my_frame.layout()


class Window:
    def __init__(self):
        self.root = create_window("数独游戏", 500, 400)

        self.frame = tk.Frame(self.root)
        self.frame.pack(side='bottom')

        self.frame_dict = FrameDict(self.frame, 3, 3, 3, 3)
        self.frame_dict.layout()

    def run(self):
        self.root.mainloop()


class Control:
    def __init__(self, root: tk.Tk, frame_dict: 'FrameDict'):
        self.select: Union['MyLabel', None] = None
        root.bind('<Key>', self.builder(frame_dict))

    def builder(self, frame_dict: 'FrameDict'):
        def key_press(event: tk.Event):
            if not self.select:
                return
            try:
                num = int(event.keysym)
            except ValueError:
                if event.keysym in ('BackSpace', 'space'):
                    num = 0
                else:
                    return
            self.select.set(num)

        def examine():
            select = self.select
            if not select:
                return
            groups = {'block': frame_dict[(select.f_row, select.f_column)].values(),
                      'row': frame_dict.row_group[select.f_row * 3 + select.row],
                      'column': frame_dict.column_group[select.f_column * 3 + select.column]}
            for range_, group in groups.items():
                all_num = set()
                same_num = set()
                for a_label in group:
                    value = a_label.get()
                    if value == ' ':
                        continue
                    a_set = same_num if value in all_num else all_num
                    a_set.add(value)
                for a_label in group:
                    a_label.set_same_dif(self.select, range_, a_label.get() in same_num)

        def inner(event: tk.Event):
            key_press(event)
            examine()

        return inner


class App:
    def __init__(self):
        self.window = Window()
        self.control = Control(self.window.root, self.window.frame_dict)

    def run(self):
        self.window.run()


app = App()
app.run()
