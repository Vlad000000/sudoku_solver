from tkinter import *
import collections
from itertools import product

class Sudoku_main_work:
    def __init__(self):
        self.block_starters = [1, 4, 7, 28, 31, 34, 55, 58, 61]
        self.row_starters = [1, 10, 19, 28, 37, 46, 55, 64, 73]
        self.starting_widgets()

    def reset_all(self):
        for widget in tk.winfo_children():
            widget.destroy()
        self.starting_widgets()

    def starting_widgets(self):
        self.enter_numbers = []
        for k in range(1, 82):
            self.enter_numbers.append(Entry(tk, font = ("Calibri", 30), justify = "center"))
            self.enter_numbers[-1].place(x = 5+(k -1 -((k-1)//9)*9)*55, y =  5+((k-1)//9)*55, width = 50, height = 50 )
        self.solve_button = Button(tk, text = "Solve", command = self.solve_sudoku)
        self.solve_button.place(x = 395, y =  500, width = 100, height = 50 )
        self.reset_button = Button(tk, text = "Reset", command = self.reset_all)
        self.reset_button.place(x = 290, y =  500, width = 100, height = 50 )

    def solve_sudoku(self):
        self.sudoku_table = {}
        count_hints = 0
        self.list_of_hints = []
        for k in range(1, 82):
            temp = self.enter_numbers[k-1].get()
            if len(temp)>1:
                sudoku_is_valid = "no"
                reason = "Invalid values!"
                break
            else:
                try:
                    if temp == '':
                        self.sudoku_table[str(k)]=[1, 2, 3, 4, 5, 6, 7, 8, 9]
                    else:
                        self.sudoku_table[str(k)]=int(temp)
                        self.enter_numbers[k-1].place_forget()
                        count_hints += 1
                        temp_label = Label(tk, text = f"{temp}", bg = "light grey", fg = "black", font=("Calibri", 30))
                        temp_label.place(x = 8 +(k -1 -((k-1)//9)*9)*55, y =  8 +((k-1)//9)*55, width = 44, height = 44 )
                        self.list_of_hints.append(str(k))
                    sudoku_is_valid = "yes"
                except:
                    sudoku_is_valid = "no"
                    reason = "Invalid values are in table!"
                    break
        if count_hints < 17:
            sudoku_is_valid = "no"
            reason = "Hints amount must be at least 17!"
        if sudoku_is_valid == "yes":
            for k in self.list_of_hints:
                self.fsob_improved(int(k))
            self.table_is_completed = "no"
            itert = 0
            while self.table_is_completed == "no" and itert < 50:
                self.look_for_one_in_list()
                if self.table_is_completed != "won't ever":
                    self.look_throught_blocks()
                    self.look_throught_rows()
                    self.look_throught_columns()
                    self.blockade_seek()
                    self.x_wing_seek()
                    self.y_wing_seek()
                    self.sword_fish_wing_seek()
                    self.hidden_pair_seek()
                    self.hidden_triple_seek()
                    self.obvious_pair()
                else:
                    break
                itert +=1
            if self.table_is_completed != "won't ever":
                self.list_table = []
                for k in range(1, 10):
                    sub_list_table = []
                    for l in range(1, 10):
                        if str(type(self.sudoku_table[str(l+((k-1)*9))]))=="<class 'list'>":
                            print(self.sudoku_table[str(l+((k-1)*9))], "list")
                            sub_list_table.append(0)
                        elif str(type(self.sudoku_table[str(l+((k-1)*9))]))=="<class 'int'>":
                            print(self.sudoku_table[str(l+((k-1)*9))], "int")
                            sub_list_table.append(self.sudoku_table[str(l+(k-1)*9)])
                    self.list_table.append(sub_list_table)
                self.list_table = self.basic_backtracking(self.list_table)
                self.sudoku_table = {}
                for k in range(1, 10):
                    for l in range(1, 10):
                        self.sudoku_table[f"{l+(k-1)*9}"] = self.list_table[k-1][l-1]
                        if self.sudoku_table[f"{l+(k-1)*9}"] == False:
                            self.table_is_completed = "won't ever"
                            break
            if self.table_is_completed != "won't ever":
                for k in self.sudoku_table:
                    if len(list(set(self.list_of_hints) & set([k]))) == 0:
                        temp_label = Label(tk, text = f"{self.sudoku_table[k]}", bg = "white", fg = "black", font=("Calibri", 30))
                        temp_label.place(x = 8 +(int(k) -1 -((int(k)-1)//9)*9)*55, y =  8 +((int(k)-1)//9)*55, width = 44, height = 44 )
                        try:
                            self.enter_numbers[int(k)-1].place_forget()
                        except:
                            pass
            else:
                self.warn_about_error("There's no possible solution!")
        else:
            self.warn_about_error(reason)

    def warn_about_error(self, mess):
        temp_label = Label(tk, text = f"Warning: {mess}", bg = "black", fg = "white", font=("Calibri", 10))
        temp_label.place(x = 5, y = 500, width = 385, height = 50 )
        self.solve_button.place_forget()
        self.reset_button.place(x = 395, y =  500, width = 100, height = 50 )

    def fsob_improved(self, x):
        vertical_position_floor = ((int(x)-1)//9)*9+1
        for j in range(vertical_position_floor, vertical_position_floor+9):
            if str(type(self.sudoku_table[f"{j}"]))!="<class 'int'>":
                try:
                    self.sudoku_table[f"{j}"].remove(self.sudoku_table[f"{x}"])
                except:
                    pass
        horizontal_position_floor = int(x)-(((int(x)-1)//9)*9)
        for j in range(0, 9):
            if str(type(self.sudoku_table[f"{j*9+horizontal_position_floor}"]))!="<class 'int'>":
                try:
                    self.sudoku_table[f"{j*9+horizontal_position_floor}"].remove(self.sudoku_table[f"{x}"])
                except:
                    pass
        block_position_floor = ((((int(x)-1)//27)*27)+1)+(((horizontal_position_floor-1)//3)*3)
        itert = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if str(type(self.sudoku_table[f"{block_position_floor+j+(i*9)}"]))!="<class 'int'>":
                    try:
                        self.sudoku_table[f"{block_position_floor+j+(i*9)}"].remove(self.sudoku_table[f"{x}"])
                    except:
                        pass
            itert+=1

    def look_for_one_in_list(self):
        sudoku_table_start = self.sudoku_table.copy()
        while True:
            for k in self.sudoku_table:
                temp = self.sudoku_table[f"{k}"]
                if str(type(self.sudoku_table[f"{k}"]))=="<class 'list'>":
                    if len(self.sudoku_table[f"{k}"])==0:
                        print("Sudoku is unsolvable!")
                        self.table_is_completed = "won't ever"
                        break
                    elif len(self.sudoku_table[f"{k}"])==1:
                        self.sudoku_table[f"{k}"] = int(self.sudoku_table[f"{k}"][0])
                        self.enter_numbers[int(f"{k}")-1].place_forget()
                        temp_label = Label(tk, text = f"{temp[0]}", bg = "white", fg = "black", font=("Calibri", 30))
                        temp_label.place(x = 8 +(int(k) -1 -((int(k)-1)//9)*9)*55, y =  8 +((int(k)-1)//9)*55, width = 44, height = 44 )
                        self.fsob_improved(int(k))
                        print(f"The {temp[0]} assigned to {k} cell (one in list)")
            if self.sudoku_table == sudoku_table_start:
                break
            else:
                pass
        



    def look_throught_blocks(self):
        print("Before:", self.sudoku_table)
        for b in self.block_starters:
            for k in range(1, 10):
                temp = []
                for i in range(0, 3):
                    for j in range(0, 3):
                        if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                            try:
                                for n in self.sudoku_table[f"{b+j+(i*9)}"]:
                                    if n == k:
                                        temp.append(f"{b+j+(i*9)}")
                            except:
                                pass
                if len(temp)==1 and type(self.sudoku_table[temp[0]])!="<class 'int'>":
                    self.sudoku_table[temp[0]] = k
                    self.enter_numbers[int(temp[0])-1].place_forget()
                    temp_label = Label(tk, text = f"{k}", bg = "white", fg = "black", font=("Calibri", 30))
                    temp_label.place(x = 8 +(int(temp[0]) -1 -((int(temp[0])-1)//9)*9)*55, y =  8 +((int(temp[0])-1)//9)*55, width = 44, height = 44 )
                    self.fsob_improved(int(temp[0]))
                    print(f"The {k} assigned to {temp[0]} cell (square)")
                    print("After:", self.sudoku_table)

    def look_throught_rows(self):
        print("Before:", self.sudoku_table)
        for r in self.row_starters:
            for k in range(1, 10):
                temp = []
                for j in range(0, 9):
                    if str(type(self.sudoku_table[f"{r+j}"]))!="<class 'int'>":
                        try:
                            for i in self.sudoku_table[f"{r+j}"]:
                                if i == k:
                                    temp.append(f"{r+j}")
                        except:
                            pass
                if len(temp)==1 and type(self.sudoku_table[temp[0]])!="<class 'int'>":
                    self.sudoku_table[temp[0]] = k
                    self.enter_numbers[int(temp[0])-1].place_forget()
                    temp_label = Label(tk, text = f"{k}", bg = "white", fg = "black", font=("Calibri", 30))
                    temp_label.place(x = 8 +(int(temp[0]) -1 -((int(temp[0])-1)//9)*9)*55, y =  8 +((int(temp[0])-1)//9)*55, width = 44, height = 44 )
                    self.fsob_improved(int(temp[0]))
                    print(f"The {k} assigned to {temp[0]} cell (row)")
                    print("After:", self.sudoku_table)

    def look_throught_columns(self):
        for c in range(1, 10):
            for k in range(1, 10):
                count = 0
                temp = []
                for j in range(0, 9):
                    if str(type(self.sudoku_table[f"{c+(j*9)}"]))!="<class 'int'>":
                        try:
                            for i in self.sudoku_table[f"{c+(j*9)}"]:
                                if i == k:
                                    count += 1
                                    temp.append(f"{c+(j*9)}")
                        except:
                            pass
                if len(temp)==1 and type(self.sudoku_table[temp[0]])!="<class 'int'>":
                    self.sudoku_table[temp[0]] = k
                    self.enter_numbers[int(temp[0])-1].place_forget()
                    temp_label = Label(tk, text = f"{k}", bg = "white", fg = "black", font=("Calibri", 30))
                    temp_label.place(x = 8 +(int(temp[0]) -1 -((int(temp[0])-1)//9)*9)*55, y =  8 +((int(temp[0])-1)//9)*55, width = 44, height = 44 )
                    self.fsob_improved(int(temp[0]))
                    print(f"The {k} assigned to {temp[0]} cell (column)")

    def blockade_seek(self):
        for b in self.block_starters:
            for k in range(1, 10):
                line_1, line_2, line_3, line_a, line_b, line_c = 0, 0, 0, 0, 0, 0
                for i in range(0, 3):
                    for j in range(0, 3):
                        if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                            try:
                                for n in self.sudoku_table[f"{b+j+(i*9)}"]:
                                    if n == k:
                                        if i == 0:
                                            line_1 += 1
                                        elif i == 1:
                                            line_2 += 1
                                        elif i == 2:
                                            line_3 += 1
                                        if j == 0:
                                            line_a += 1
                                        elif j == 1:
                                            line_b += 1
                                        elif j == 2:
                                            line_c += 1
                            except:
                                pass
                    
                addic, addicc = "no_need", "no_need"
                
                if line_1 > 1 and line_2 == 0 and line_3 == 0:
                    addic = 0
                elif line_1 == 0 and line_2 > 1 and line_3 == 0:
                    addic = 1
                elif line_1 == 0 and line_2 == 0 and line_3 > 1:
                    addic = 2
                    
                try:
                    vertical_position_floor = ((int(b+addic*9)-1)//9)*9+1
                    for j in range(vertical_position_floor, vertical_position_floor+9):
                        if str(type(self.sudoku_table[f"{j}"]))=="<class 'list'>" and self.delete_needed(j, b)=="yes":
                            try:
                                self.sudoku_table[f"{j}"].remove(int(k))
                                print(f"Blockade of {k} in block enumeration {j} (horizontal)")
                            except:
                                pass
                except:
                    pass

                if line_a > 1 and line_b == 0 and line_c == 0:
                    addicc = 0
                elif line_a == 0 and line_b > 1 and line_c == 0:
                    addicc = 1
                elif line_a == 0 and line_b == 0 and line_c > 1:
                    addicc = 2
                    
                try:
                    horizontal_position_floor = int(b+addicc)-(((int(b+addicc)-1)//9)*9)
                    for j in range(0, 9):
                        if str(type(self.sudoku_table[f"{j*9+horizontal_position_floor}"]))=="<class 'list'>" and self.delete_needed(j*9+horizontal_position_floor, b)=="yes":
                            try:
                                self.sudoku_table[f"{j*9+horizontal_position_floor}"].remove(int(k))
                                print(f"Blockade of {k} in block enumerated {j*9+horizontal_position_floor} (vertical)")
                            except:
                                pass
                except:
                    pass

    def hidden_pair_seek(self):
        for b in self.block_starters:            #9 перевірок (по одній на кожен блок)
            block_double_num = []                #сюди зберігається цифра, що повторюється двічі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 3):
                    for j in range(0, 3):
                        if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{b+j+(i*9)}"]) & set([k])))==1:
                                count += 1
                if count == 2:
                    block_double_num.append(k)
            if len(block_double_num) >= 2:
                for first in range(0, len(block_double_num)-1):
                    for second in range(first+1, len(block_double_num)):
                        cell_index = []
                        for i in range(0, 3):
                            for j in range(0, 3):
                                if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                                    if len(list(set(self.sudoku_table[f"{b+j+(i*9)}"]) & set([block_double_num[first], block_double_num[second]])))==2:
                                        cell_index.append(f"{b+j+(i*9)}")
                        if len(cell_index) == 2:
                            for index in cell_index:
                                if self.sudoku_table[index] != [block_double_num[first], block_double_num[second]]:
                                    self.sudoku_table[index] = [block_double_num[first], block_double_num[second]]      #звужує список дозволених цифр до двох
                                    print(f"{index}: list decresed to {[block_double_num[first], block_double_num[second]]} (square)\n", self.sudoku_table)
                                    
        for r in self.row_starters:            #9 перевірок (по одній на кожну лінію)
            block_double_num = []                #сюди зберігається цифра, що повторюється двічі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 9):
                        if str(type(self.sudoku_table[f"{r+i}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{r+i}"]) & set([k])))==1:
                                count += 1
                if count == 2:
                    block_double_num.append(k)
            if len(block_double_num) >= 2:
                for first in range(0, len(block_double_num)-1):
                    for second in range(first+1, len(block_double_num)):
                        cell_index = []
                        for i in range(0, 9):
                            if str(type(self.sudoku_table[f"{r+i}"]))!="<class 'int'>":
                                if len(list(set(self.sudoku_table[f"{r+i}"]) & set([block_double_num[first], block_double_num[second]])))==2:
                                    cell_index.append(f"{r+i}")
                        if len(cell_index) == 2:
                            for index in cell_index:
                                if self.sudoku_table[index] != [block_double_num[first], block_double_num[second]]:
                                    self.sudoku_table[index] = [block_double_num[first], block_double_num[second]]
                                    print(f"{index}: list decresed to {[block_double_num[first], block_double_num[second]]} (row)\n", self.sudoku_table)

        for c in range(1, 10):            #9 перевірок (по одній на кожен стовпець)
            block_double_num = []                #сюди зберігається цифра, що повторюється двічі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 9):
                        if str(type(self.sudoku_table[f"{c+(i*9)}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{c+(i*9)}"]) & set([k])))==1:
                                count += 1
                if count == 2:
                    block_double_num.append(k)
            if len(block_double_num) >= 2:
                for first in range(0, len(block_double_num)-1):
                    for second in range(first+1, len(block_double_num)):
                        cell_index = []
                        for i in range(0, 9):
                            if str(type(self.sudoku_table[f"{c+(i*9)}"]))!="<class 'int'>":
                                if len(list(set(self.sudoku_table[f"{c+(i*9)}"]) & set([block_double_num[first], block_double_num[second]])))==2:
                                    cell_index.append(f"{c+(i*9)}")
                        if len(cell_index) == 2:
                            for index in cell_index:
                                if self.sudoku_table[index] != [block_double_num[first], block_double_num[second]]:
                                    self.sudoku_table[index] = [block_double_num[first], block_double_num[second]]
                                    print(f"{index}: list decresed to {[block_double_num[first], block_double_num[second]]} (column)\n", self.sudoku_table)

    def hidden_triple_seek(self):
        for b in self.block_starters:            #9 перевірок (по одній на кожен блок)
            block_triple_num = []                #сюди зберігається цифра, що повторюється тричі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 3):
                    for j in range(0, 3):
                        if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{b+j+(i*9)}"]) & set([k])))==1:
                                count += 1
                if count == 3:
                    block_triple_num.append(k)
            if len(block_triple_num) >= 3:
                for first in range(0, len(block_triple_num)-2):
                    for second in range(first+1, len(block_triple_num)-1):
                        for third in range(second+1, len(block_triple_num)):
                            cell_index = []
                            for i in range(0, 3):
                                for j in range(0, 3):
                                    if str(type(self.sudoku_table[f"{b+j+(i*9)}"]))!="<class 'int'>":
                                        if len(list(set(self.sudoku_table[f"{b+j+(i*9)}"]) & set([block_triple_num[first], block_triple_num[second], block_triple_num[third]])))==3:
                                            cell_index.append(f"{b+j+(i*9)}")
                            if len(cell_index) == 3:
                                for index in cell_index:
                                    if self.sudoku_table[index] != [block_triple_num[first], block_triple_num[second], block_triple_num[third]]:
                                        self.sudoku_table[index] = [block_triple_num[first], block_triple_num[second], block_triple_num[third]]       #звужує список дозволених цифр до трьох
                                        print(f"{index}: list decresed to {[block_triple_num[first], block_triple_num[second], block_triple_num[third]]} (square)\n", self.sudoku_table)
                                        
        for r in self.row_starters:              #9 перевірок (по одній на кожну лінію)
            block_triple_num = []                #сюди зберігається цифра, що повторюється тричі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 9):
                        if str(type(self.sudoku_table[f"{r+i}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{r+i}"]) & set([k])))==1:
                                count += 1
                if count == 3:
                    block_triple_num.append(k)
            if len(block_triple_num) >= 3:
                for first in range(0, len(block_triple_num)-2):
                    for second in range(first+1, len(block_triple_num)-1):
                        for third in range(second+1, len(block_triple_num)):
                            cell_index = []
                            for i in range(0, 9):
                                if str(type(self.sudoku_table[f"{r+i}"]))!="<class 'int'>":
                                    if len(list(set(self.sudoku_table[f"{r+i}"]) & set([block_triple_num[first], block_triple_num[second], block_triple_num[third]])))==3:
                                        cell_index.append(f"{r+i}")
                            if len(cell_index) == 3:
                                for index in cell_index:
                                    if self.sudoku_table[index] != [block_triple_num[first], block_triple_num[second], block_triple_num[third]]:
                                        self.sudoku_table[index] = [block_triple_num[first], block_triple_num[second], block_triple_num[third]]
                                        print(f"{index}: list decresed to {[block_triple_num[first], block_triple_num[second], block_triple_num[third]]} (row)\n", self.sudoku_table)

        for c in range(1, 10):                   #9 перевірок (по одній на кожен сповпець)
            block_triple_num = []                #сюди зберігається цифра, що повторюється тричі в списках дозволених цифр
            for k in range(1, 10):               #k - int, цифра, що перевіряється
                count = 0
                for i in range(0, 9):
                        if str(type(self.sudoku_table[f"{c+(i*9)}"]))!="<class 'int'>":
                            if len(list(set(self.sudoku_table[f"{c+(i*9)}"]) & set([k])))==1:
                                count += 1
                if count == 3:
                    block_triple_num.append(k)
            if len(block_triple_num) >= 3:
                for first in range(0, len(block_triple_num)-2):
                    for second in range(first+1, len(block_triple_num)-1):
                        for third in range(second+1, len(block_triple_num)):
                            cell_index = []
                            for i in range(0, 9):
                                if str(type(self.sudoku_table[f"{c+(i*9)}"]))!="<class 'int'>":
                                    if len(list(set(self.sudoku_table[f"{c+(i*9)}"]) & set([block_triple_num[first], block_triple_num[second], block_triple_num[third]])))==3:
                                        cell_index.append(f"{c+(i*9)}")
                            if len(cell_index) == 3:
                                for index in cell_index:
                                    if self.sudoku_table[index] != [block_triple_num[first], block_triple_num[second], block_triple_num[third]]:
                                        self.sudoku_table[index] = [block_triple_num[first], block_triple_num[second], block_triple_num[third]]
                                        print(f"{index}: list decresed to {[block_triple_num[first], block_triple_num[second], block_triple_num[third]]} (column)\n", self.sudoku_table)
                                        
    def sword_fish_wing_seek(self):
        for i in range(1, 7):
            for j in range(i+1, 9):
                for h in range(j+1, 10):
                    if (((((i-1)//3)+1)*3)+1 == ((((j-1)//3)+1)*3)+1 and ((((i-1)//3)+1)*3)+1 != ((((h-1)//3)+1)*3)+1) or (((((h-1)//3)+1)*3)+1 == ((((j-1)//3)+1)*3)+1 and ((((i-1)//3)+1)*3)+1 != ((((j-1)//3)+1)*3)+1):
                        for k in range(0, 6):
                            for n in range(k+1, 8):
                                for m in range(n+1, 9):
                                    if (((k//3)+1)*3)+1 != (((n//3)+1)*3)+1 and (((m//3)+1)*3)+1 != (((n//3)+1)*3)+1 and (((k//3)+1)*3)+1 != (((m//3)+1)*3)+1:
                                        temp = [f"{i+k*9}", f"{j+k*9}", f"{h+k*9}", f"{i+n*9}", f"{j+n*9}", f"{h+n*9}", f"{i+m*9}", f"{j+m*9}", f"{h+m*9}"]                                      
                                        if (str(type(self.sudoku_table[f"{i+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(m*9)}"]))=="<class 'int'>") or (str(type(self.sudoku_table[f"{i+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(m*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(n*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{j+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(m*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{j+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(m*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{h+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(m*9)}"]))=="<class 'int'>") or (str(type(self.sudoku_table[f"{h+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(m*9)}"]))=="<class 'int'>"):
                                            filtered_temp = [d for d in temp if not isinstance(self.sudoku_table[d], int)]
                                            if len(filtered_temp) == 6:
                                                l = list(set(self.sudoku_table[filtered_temp[0]]) & set(self.sudoku_table[filtered_temp[1]]) & set(self.sudoku_table[filtered_temp[2]]) & set(self.sudoku_table[filtered_temp[3]]) & set(self.sudoku_table[filtered_temp[4]]) & set(self.sudoku_table[filtered_temp[5]]))
                                                if len(l) == 1:
                                                    print("B", self.sudoku_table)
                                                    for r in [k, n, m]:
                                                        for f in range(0, 9):
                                                            if str(type(self.sudoku_table[f"{f+(r*9)+1}"]))!="<class 'int'>" and self.delete_needed_sword_fish(f"{f+(r*9)+1}", temp)=='yes':
                                                                if len(list(set(self.sudoku_table[f"{f+(r*9)+1}"]) & set(l)))==1:
                                                                    self.sudoku_table[f"{f+(r*9)+1}"].remove(int(l[0]))
                                                    for c in [i, j, h]:
                                                        for f in range(0, 9):
                                                            if str(type(self.sudoku_table[f"{c+(f*9)}"]))!="<class 'int'>" and self.delete_needed_sword_fish(f"{c+(f*9)}", temp)=='yes':
                                                                if len(list(set(self.sudoku_table[f"{c+(f*9)}"]) & set(l)))==1:
                                                                    self.sudoku_table[f"{c+(f*9)}"].remove(int(l[0]))
                                                    print("A", self.sudoku_table)
                    elif ((((h-1)//3)+1)*3)+1 != ((((j-1)//3)+1)*3)+1 and ((((i-1)//3)+1)*3)+1 != ((((j-1)//3)+1)*3)+1 and ((((h-1)//3)+1)*3)+1 != ((((i-1)//3)+1)*3)+1:
                        for k in range(0, 6):
                            for n in range(k+1, 8):
                                for m in range(n+1, 9):
                                    if ((((k//3)+1)*3)+1 == (((n//3)+1)*3)+1 and (((n//3)+1)*3)+1 != (((m//3)+1)*3)+1) or ((((n//3)+1)*3)+1 == (((m//3)+1)*3)+1 and (((m//3)+1)*3)+1 != (((k//3)+1)*3)+1) or ((((k//3)+1)*3)+1 != (((n//3)+1)*3)+1 and (((m//3)+1)*3)+1 != (((n//3)+1)*3)+1 and (((k//3)+1)*3)+1 != (((m//3)+1)*3)+1):
                                        temp = [f"{i+k*9}", f"{j+k*9}", f"{h+k*9}", f"{i+n*9}", f"{j+n*9}", f"{h+n*9}", f"{i+m*9}", f"{j+m*9}", f"{h+m*9}"]       
                                        if (str(type(self.sudoku_table[f"{i+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(m*9)}"]))=="<class 'int'>") or (str(type(self.sudoku_table[f"{i+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(m*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(n*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{j+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(m*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{j+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{h+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(m*9)}"]))=="<class 'int'>") or(str(type(self.sudoku_table[f"{h+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(m*9)}"]))=="<class 'int'>") or (str(type(self.sudoku_table[f"{h+(k*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{j+(n*9)}"]))=="<class 'int'>" and str(type(self.sudoku_table[f"{i+(m*9)}"]))=="<class 'int'>"):
                                            filtered_temp = [d for d in temp if not isinstance(self.sudoku_table[d], int)]
                                            if len(filtered_temp) == 6:
                                                l = list(set(self.sudoku_table[filtered_temp[0]]) & set(self.sudoku_table[filtered_temp[1]]) & set(self.sudoku_table[filtered_temp[2]]) & set(self.sudoku_table[filtered_temp[3]]) & set(self.sudoku_table[filtered_temp[4]]) & set(self.sudoku_table[filtered_temp[5]]))
                                                if len(l) == 1:
                                                    print("B", self.sudoku_table)
                                                    for r in [k, n, m]:
                                                        for f in range(0, 9):
                                                            if str(type(self.sudoku_table[f"{f+(r*9)+1}"]))!="<class 'int'>" and self.delete_needed_sword_fish(f"{f+(r*9)+1}", temp)=='yes':
                                                                if len(list(set(self.sudoku_table[f"{f+(r*9)+1}"]) & set(l)))==1:
                                                                    self.sudoku_table[f"{f+(r*9)+1}"].remove(int(l[0]))
                                                    for c in [i, j, h]:
                                                        for f in range(0, 9):
                                                            if str(type(self.sudoku_table[f"{c+(f*9)}"]))!="<class 'int'>" and self.delete_needed_sword_fish(f"{c+(f*9)}", temp)=='yes':
                                                                if len(list(set(self.sudoku_table[f"{c+(f*9)}"]) & set(l)))==1:
                                                                    self.sudoku_table[f"{c+(f*9)}"].remove(int(l[0]))
                                                    print("A", self.sudoku_table)
                                                        
    def y_wing_seek(self):
        for i in range(1, 7):
            for j in range(((((i-1)//3)+1)*3)+1, 10):
                for k in range(0, 6):
                    for n in range(((((k)//3)+1)*3)+1, 9):
                        if str(type(self.sudoku_table[f"{i+k*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{j+k*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{i+n*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{j+n*9}"]))=="<class 'list'>":
                            lst = list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"])& set(self.sudoku_table[f"{j+n*9}"]))
                            if len(lst) == 0:
                                if len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"]))) == 0:
                                    if len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(self.sudoku_table[f"{j+k*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2 and len(self.sudoku_table[f"{i+k*9}"]) == 2:
                                        try:
                                            self.sudoku_table[f"{j+n*9}"].remove(int(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))[0]))
                                            print(f"Blockade of {h} in block enumerated {j+n*9} (y wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                        except:
                                            pass
                                elif len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 0:
                                    if len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{j+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(self.sudoku_table[f"{j+k*9}"]) == 2 and len(self.sudoku_table[f"{j+n*9}"]) == 2 and len(self.sudoku_table[f"{i+k*9}"]) == 2:
                                        try:
                                            self.sudoku_table[f"{i+n*9}"].remove(int(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))[0]))
                                            print(f"Blockade of {h} in block enumerated {i+n*9} (y wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                        except:
                                            pass
                                elif len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 0:
                                    if len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{j+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"]))) == 1 and len(self.sudoku_table[f"{j+n*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2 and len(self.sudoku_table[f"{j+k*9}"]) == 2:
                                        try:
                                            self.sudoku_table[f"{i+k*9}"].remove(int(list(set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"]))[0]))
                                            print(f"Blockade of {h} in block enumerated {i+k*9} (y wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                        except:
                                            pass
                                elif len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 0:
                                    if len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{i+k*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))) == 1 and len(list(set(self.sudoku_table[f"{j+n*9}"]) & set(self.sudoku_table[f"{i+k*9}"]))) == 1 and len(self.sudoku_table[f"{j+n*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2 and len(self.sudoku_table[f"{i+k*9}"]) == 2:
                                        try:
                                            self.sudoku_table[f"{j+k*9}"].remove(int(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+n*9}"]))[0]))
                                            print(f"Blockade of {h} in block enumerated {j+k*9} (y wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                        except:
                                            pass
                                            
    def x_wing_seek(self):
        for i in range(1, 7):
            for j in range(((((i-1)//3)+1)*3)+1, 10):
                for k in range(0, 6):
                    for n in range(((((k)//3)+1)*3)+1, 9):
                        if str(type(self.sudoku_table[f"{i+k*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{j+k*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{i+n*9}"]))=="<class 'list'>" and str(type(self.sudoku_table[f"{j+n*9}"]))=="<class 'list'>":
                            if (len(self.sudoku_table[f"{i+k*9}"]) == 2 and len(self.sudoku_table[f"{j+k*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2) or (len(self.sudoku_table[f"{i+k*9}"]) == 2 and len(self.sudoku_table[f"{j+k*9}"]) == 2 and len(self.sudoku_table[f"{j+n*9}"]) == 2) or (len(self.sudoku_table[f"{i+k*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2 and len(self.sudoku_table[f"{j+n*9}"]) == 2) or (len(self.sudoku_table[f"{j+k*9}"]) == 2 and len(self.sudoku_table[f"{i+n*9}"]) == 2 and len(self.sudoku_table[f"{j+n*9}"]) == 2):
                                lst = list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"])& set(self.sudoku_table[f"{j+n*9}"]))
                                if len(lst) > 0 and ((len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{j+k*9}"])))==2 and len(list(set(self.sudoku_table[f"{i+n*9}"]) & set(self.sudoku_table[f"{j+n*9}"])))==2) or (len(list(set(self.sudoku_table[f"{i+k*9}"]) & set(self.sudoku_table[f"{i+n*9}"])))==2 and len(list(set(self.sudoku_table[f"{j+n*9}"]) & set(self.sudoku_table[f"{j+k*9}"])))==2):
                                    for h in lst:
                                        try:
                                            for m in range(0, 9):
                                                if str(type(self.sudoku_table[f"{m*9+i}"]))=="<class 'list'>" and self.delete_needed_x_wing(m*9+i, [i, j, k, n])=="yes" and len(list(set(self.sudoku_table[f"{m*9+i}"]) & set([h])))==1:
                                                    try:
                                                        self.sudoku_table[f"{m*9+i}"].remove(int(h))
                                                        print(f"Blockade of {h} in block enumerated {m*9+i} (x wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                                    except:
                                                        pass
                                        except:
                                            pass
                                        try:
                                            for m in range(0, 9):
                                                if str(type(self.sudoku_table[f"{m*9+j}"]))=="<class 'list'>" and self.delete_needed_x_wing(m*9+j, [i, j, k, n])=="yes" and len(list(set(self.sudoku_table[f"{m*9+j}"]) & set([h])))==1:
                                                    try:
                                                        self.sudoku_table[f"{m*9+j}"].remove(int(h))
                                                        print(f"Blockade of {h} in block enumerated {m*9+j} (x wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                                    except:
                                                        pass
                                        except:
                                            pass
                                        try:
                                            for m in range(1, 10):
                                                if str(type(self.sudoku_table[f"{m+k*9}"]))=="<class 'list'>" and self.delete_needed_x_wing(m+k*9, [i, j, k, n])=="yes" and len(list(set(self.sudoku_table[f"{m+k*9}"]) & set([h])))==1:
                                                    try:
                                                        self.sudoku_table[f"{m+k*9}"].remove(int(h))
                                                        print(f"Blockade of {h} in block enumeration {m+k*9} (x wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                                    except:
                                                        pass
                                        except:
                                            pass
                                        try:
                                            for m in range(1, 10):
                                                if str(type(self.sudoku_table[f"{m+n*9}"]))=="<class 'list'>" and self.delete_needed_x_wing(m+n*9, [i, j, k, n])=="yes" and len(list(set(self.sudoku_table[f"{m+n*9}"]) & set([h])))==1:
                                                    try:
                                                        self.sudoku_table[f"{m+n*9}"].remove(int(h))
                                                        print(f"Blockade of {h} in block enumeration {m+n*9} (x wing) {[i+k*9, j+k*9, i+n*9, j+n*9]}")
                                                    except:
                                                        pass
                                        except:
                                            pass


    def obvious_pair(self):
        for b in self.block_starters:
            block_two_num_lists = []
            for i in range(0, 3):
                for j in range(0, 3):
                    if str(type(self.sudoku_table[f"{b+i+(j*9)}"]))=="<class 'list'>":
                        if len(self.sudoku_table[f"{b+i+(j*9)}"]) == 2:
                            block_two_num_lists.append(f"{b+i+(j*9)}")
            if len(block_two_num_lists) == 2:
                list_of_match = list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]))
                if len(list_of_match) == 2:
                    for num in list_of_match:
                        for k in range(0, 3):
                            for n in range(0, 3):
                                if str(type(self.sudoku_table[f"{b+k+(n*9)}"]))!="<class 'int'>":
                                    if len(list(set(self.sudoku_table[f"{b+k+(n*9)}"]) & set([num])))==1 and f"{b+k+(n*9)}"!=block_two_num_lists[0] and f"{b+k+(n*9)}"!=block_two_num_lists[1]:
                                        self.sudoku_table[f"{b+k+(n*9)}"].remove(int(num))
                                        print(f"{num} has been removed from cell {b+k+(n*9)} (obvious pair)")
            elif len(block_two_num_lists) == 3:
                if len(list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]) & set(self.sudoku_table[f"{block_two_num_lists[2]}"]))) == 0:
                    if len(list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]))) == 1 and len(list(set(self.sudoku_table[f"{block_two_num_lists[2]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]))) == 1 and len(list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[2]}"]))) == 1:               
                        for num in [list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]))[0],
                                    list(set(self.sudoku_table[f"{block_two_num_lists[0]}"]) & set(self.sudoku_table[f"{block_two_num_lists[2]}"]))[0],
                                    list(set(self.sudoku_table[f"{block_two_num_lists[2]}"]) & set(self.sudoku_table[f"{block_two_num_lists[1]}"]))[0]]:
                            for k in range(0, 3):
                                for n in range(0, 3):
                                    if str(type(self.sudoku_table[f"{b+k+(n*9)}"]))!="<class 'int'>":
                                        if len(list(set(self.sudoku_table[f"{b+k+(n*9)}"]) & set([num])))==1 and f"{b+k+(n*9)}"!=block_two_num_lists[0] and f"{b+k+(n*9)}"!=block_two_num_lists[1] and f"{b+k+(n*9)}"!=block_two_num_lists[2]:
                                            self.sudoku_table[f"{b+k+(n*9)}"].remove(int(num))
                                            print(f"{num} has been removed from cell {b+k+(n*9)} (obvious triple pair)")
                                        

    def delete_needed_sword_fish(self, numb, area):
        for k in area:
            if k == numb:
                resp = "no"
                break
            else:
                resp = "yes"
        return resp 
                                                
    def delete_needed_x_wing(self, numb, area):
        area_numbs = [area[0]+area[2]*9, area[1]+area[2]*9, area[0]+area[3]*9, area[1]+area[3]*9]
        for k in area_numbs:
            if k == numb:
                resp = "no"
                break
            else:
                resp = "yes"
        return resp                

    def delete_needed(self, numb, block):
        block_numbs = []
        itert = 0
        while itert <= 2:
            for j in range(0, 3):
                block_numbs.append(block+j+(itert*9))
            itert += 1
        for k in block_numbs:
            if k == numb:
                resp = "no"
                break
            else:
                resp = "yes"
        return resp

    def basic_backtracking(self, lst):
        for (c, r) in product(range(0, 9), repeat=2):
            if lst[c][r] == 0:
                for num in range(1, 10):
                    allowed = "yes"
                    for i in range(0, 9):
                        if (lst[i][r] == num) or (lst[c][i] == num):
                            allowed = "no"
                            break
                    for (i, j) in product(range(0, 3), repeat=2):
                        if lst[c-c%3+i][r-r%3+j] == num:
                            allowed = "no"
                            break
                    if allowed == "yes":
                        lst[c][r] = num
                        if trial := self.basic_backtracking(lst):
                            return trial
                        else:
                            lst[c][r] = 0
                return False
        return lst
                

def list_to_dict(lst):
    dic = {}
    for k in range(0, 81):
        dic[f"k+1"] = lst[k]
    return dic


if __name__=='__main__':
    tk = Tk()
    tk.title('Sudoku Solver')
    tk.geometry('500x555+0+0')
    tk['bg'] = 'black'
    Sudoku_main_work()
    tk.mainloop()
