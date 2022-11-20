import itertools
import tkinter as tk
from typing import Union, Tuple, Dict, List, Callable

num_font = ("黑体", 24)
text_font = ("宋体", 20)
Pos = Tuple[int, int]


def create_window(title: str, w: int, h: int, x: int = 500, y: int = 150):
    ro = tk.Tk()
    ro.title(title)
    ro.resizable(False, False)
    ro.geometry(f'{w}x{h}+{x}+{y}')
    return ro


def click(self: 'MyLabel'):
    def inner_func(event):
        other = app.select
        if other is self:
            self.unselect()
            app.select = None
            return
        if other:
            other.unselect()
        self.select()
        app.select = self

    return inner_func


def next_num(fr: int, fc: int, row: int, column: int) -> Tuple[int, int, int, int]:
    # sourcery skip: assign-if-exp, reintroduce-else
    if column < 2:
        return fr, fc, row, column + 1
    if fc < 2:
        return fr, fc + 1, row, 0
    if row < 2:
        return fr, 0, row + 1, 0
    if fr < 2:
        return fr + 1, 0, 0, 0
    return -1, -1, -1, -1


class MyLabel:
    wrong: Union[Dict[str, bool], None]

    def __init__(self, master: tk.Misc, row: int, column: int, fr: int, fc: int, value: str):
        self.row = row
        self.column = column
        self.f_row = fr
        self.f_column = fc
        self.value = tk.StringVar(value=value)
        self.label = tk.Label(master, font=num_font, textvariable=self.value, relief='raised', width=2, height=1)
        if value == ' ':
            self.label.bind('<Button-1>', click(self))
            self.normal = 'green'
            self.wrong_color = 'red'
        else:
            self.normal = 'white'
            self.wrong_color = 'darkRed'
        self.label['bg'] = self.normal
        self.wrong = {'block': False, 'row': False, 'column': False}

    def get(self):
        return self.value.get()

    def set(self, num: int):
        value = ' ' if num == 0 else str(num)
        self.value.set(value)

    def get_poss(self) -> Tuple[int, int, int, int]:
        return self.f_row, self.f_column, self.row, self.column

    def set_same_dif(self, select: 'MyLabel', range_: str, bool_: bool):
        self.wrong[range_] = bool_
        if select is self:
            self.label['bg'] = 'orange' if self.is_wrong() else 'blue'
        elif self.is_wrong():
            self.label['bg'] = self.wrong_color
        else:
            self.label['bg'] = self.normal

    def select(self):
        self.label['bg'] = 'orange' if self.is_wrong() else 'blue'

    def unselect(self):
        self.label['bg'] = 'red' if self.is_wrong() else 'green'

    def layout(self):
        self.label.grid(row=self.row, column=self.column, padx=1, pady=1)

    def is_wrong(self):
        return any(self.wrong.values())


class MyLabelDict:
    group: Dict[Pos, 'MyLabel']

    def __init__(self, master: tk.Misc, data: Dict[Pos, str], row_num: int, column_num: int, fr: int, fc: int):
        self.group = {(row, column): MyLabel(master, row, column, fr, fc, data[row, column])
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
    def __init__(self, master: tk.Misc, data: Dict[Pos, str], row: int, column: int, row_num: int, column_num: int):
        self.my_frame = MyFrame(master, row, column)
        self.my_label_dict = MyLabelDict(self.my_frame.frame, data, row_num, column_num, row, column)

    def __getitem__(self, item):
        return self.my_label_dict[item]

    def values(self):
        return self.my_label_dict.group.values()

    def layout(self):
        self.my_label_dict.layout()
        self.my_frame.layout()


class FrameDict:
    group: Dict[Pos, 'Block']
    row_group: List[List['MyLabel']]
    column_group: List[List['MyLabel']]

    def __init__(self, master: tk.Misc, level: Dict[Pos, Dict[Pos, str]], row_num: int, column_num: int, rn: int,
                 cn: int):
        self.group = {(row, column): Block(master, level[(row, column)], row, column, rn, cn)
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

    def set_same_dif(self, select):
        groups = {'block': self.group[(select.f_row, select.f_column)].values(),
                  'row': self.row_group[select.f_row * 3 + select.row],
                  'column': self.column_group[select.f_column * 3 + select.column]}
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
                a_label.set_same_dif(select, range_, a_label.get() in same_num)

    def layout(self):
        for my_frame in self.values():
            my_frame.layout()


class Window:
    frame: tk.Frame
    frame_dict: 'FrameDict'

    def __init__(self, func: Callable[[], None]):
        self.root = create_window("数独游戏", 500, 500)
        # 大部分构造在fun里
        self.func = func
        self.button = tk.Button(self.root, text='下一关', font=text_font, command=func)
        self.button.pack()

    def load_next(self, level):
        if hasattr(self, 'frame'):
            self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame_dict = FrameDict(self.frame, level, 3, 3, 3, 3)
        self.frame_dict.layout()
        self.frame.pack(side='bottom')


class Levels:
    data: List[Dict[Pos, Dict[Pos, str]]]

    def __init__(self, path: str):
        self.index = -1
        self.data = []
        self._create_data(path)

    def _create_data(self, path: str):
        self.data = []
        with open(path, mode='r', encoding='utf-8') as f:
            txt = f.read()
        levels = txt.split('\n\n')
        for level in levels:
            a_dict = {}
            fr = fc = row = column = 0
            for char in level:
                if char not in '123456789 ':
                    continue
                if (fr, fc) not in a_dict:
                    a_dict[(fr, fc)] = {}
                a_dict[(fr, fc)][(row, column)] = char
                fr, fc, row, column = next_num(fr, fc, row, column)
            self.data.append(a_dict)

    def index_add(self):
        self.index += 1
        if self.index >= len(self.data):
            self.index = 0


class App:
    select: Union['MyLabel', None]

    def __init__(self):
        self.levels = Levels('sudoku.txt')
        self.window = Window(self.next_level())
        self.select = None
        self.window.func()
        self.window.root.bind('<Key>', self.builder())

    def next_level(self):
        def inner():
            self.levels.index_add()
            self.window.load_next(self.levels.data[self.levels.index])
            self.select = None

        return inner

    def builder(self):

        def move(select: 'MyLabel', face: str) -> Tuple[int, int, int, int]:
            fr, fc, row, column = select.get_poss()
            if face == 'Up':
                if row > 0:
                    return fr, fc, row - 1, column
                return (fr - 1, fc, 2, column) if fr > 0 else (2, fc, 2, column)
            if face == 'Down':
                if row < 2:
                    return fr, fc, row + 1, column
                return (fr + 1, fc, 0, column) if fr < 2 else (0, fc, 0, column)
            if face == 'Left':
                if column > 0:
                    return fr, fc, row, column - 1
                return (fr, fc - 1, row, 2) if fc > 0 else (fr, 2, row, 2)
            if face == 'Right':
                if column < 2:
                    return fr, fc, row, column + 1
                return (fr, fc + 1, row, 0) if fc < 2 else (fr, 0, row, 0)
            return fr, fc, row, column

        def set_move(face):
            if not self.select:
                self.select = self.window.frame_dict[(0, 0)].my_label_dict[(0, 0)]
            else:
                self.select.unselect()
                while True:
                    fr, fc, row, column = move(self.select, face)
                    self.select = self.window.frame_dict[(fr, fc)].my_label_dict[(row, column)]
                    if self.select.normal == 'green':
                        break
            self.select.select()

        def inner(event: tk.Event):
            if event.keysym in ('Up', 'Down', 'Left', 'Right'):
                set_move(event.keysym)
                return
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
            self.window.frame_dict.set_same_dif(self.select)

        return inner

    def run(self):
        self.window.root.mainloop()


app = App()
app.run()
