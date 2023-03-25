import csv
import pickle
from copy import deepcopy


def is_int(st):
    try:
        int(st)
        return True
    except ValueError:
        return False


def is_float(st):
    try:
        float(st)
        return True
    except ValueError:
        return False


class Table:

    def __init__(self, name, values=None, headlines=None, headlines_num=None, column_types=None,
                 column_types_by_num=None, width_table=0, height_table=0
                 , old_self=None, con=False):
        if not ('.' in name):
            raise ValueError('Наверное имя таблицы. Пример правильного имени: input.csv')
        if old_self is None:
            old_self = ''
        if column_types_by_num is None:
            column_types_by_num = {}
        if column_types is None:
            column_types = {}
        if headlines is None:
            headlines = []
        if values is None:
            values = []
        if headlines_num is None:
            headlines_num = {}
        self.__connected_table = old_self
        self.__is_connected = con
        self.__name = name
        self.__values = values
        self.__headlines = headlines
        self.__headlines_num = headlines_num
        self.__width_table = width_table
        self.__height_table = height_table
        self.__column_types = column_types
        self.__column_types_by_num = column_types_by_num

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_value):
        if self.__is_connected:
            self.__connected_table.__name = new_value
        self.__name = new_value

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, new_value):
        if self.__is_connected:
            arr = self.__connected_table.values
            for j in range(1, self.height_table):
                ind = new_value[0][j] + 1
                for i in range(self.width_table):
                    arr[i][ind] = new_value[i][j]
            self.__connected_table.values = arr
        self.__values = new_value

    @property
    def headlines(self):
        return self.__headlines

    @headlines.setter
    def headlines(self, new_value):
        if self.__is_connected:
            self.__connected_table.__headlines = new_value
        self.__headlines = new_value

    @property
    def headlines_num(self):
        return self.__headlines_num

    @headlines_num.setter
    def headlines_num(self, new_value):
        if self.__is_connected:
            self.__connected_table.__headlines_num = new_value
        self.__headlines_num = new_value

    @property
    def width_table(self):
        return self.__width_table

    @width_table.setter
    def width_table(self, new_value):
        if self.__is_connected:
            self.__connected_table.__width_table = new_value
        self.__width_table = new_value

    @property
    def height_table(self):
        return self.__height_table

    @height_table.setter
    def height_table(self, new_value):
        if self.__is_connected:
            self.__connected_table.__height_table = new_value
        self.__height_table = new_value

    @property
    def column_types(self):
        return self.__column_types

    @column_types.setter
    def column_types(self, new_value):
        if self.__is_connected:
            self.__connected_table.__column_types = new_value
        self.__column_types = new_value

    @property
    def column_types_by_num(self):
        return self.__column_types_by_num

    @column_types_by_num.setter
    def column_types_by_num(self, new_value):
        if self.__is_connected:
            self.__connected_table.__column_types_by_num = new_value
        self.__column_types_by_num = new_value

    @staticmethod
    def type_el(self, el, ind):
        type_el = self.column_types_by_num[ind]
        if type_el == 'int':
            return int(el)
        elif type_el == 'float':
            return float(el)
        elif type_el == 'bool':
            return bool(el)
        else:
            return str(el)

    def load_table(self):
        if self.name.split('.')[1] == 'pickle':
            with open('input.pickle', 'rb') as f:
                arr = pickle.load(f)
                with open('input.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(arr)

        if self.name.split('.')[1] == 'csv' or self.name.split('.')[1] == 'pickle':
            try:
                with open(self.name.split('.')[0] + '.csv', 'r') as csvfile:
                    file = csv.reader(csvfile)
                    headline = file.__next__()
                    table_get = [[i] for i in headline]
                    table_get[0][0] = 'index'
                    row = file.__next__()
                    le = len(table_get)

                    for i in range(le):
                        if is_int(row[i]):
                            self.column_types[table_get[i][0]] = 'int'
                            self.column_types_by_num[i] = 'int'
                        elif is_float(row[i]):
                            self.column_types[table_get[i][0]] = 'float'
                            self.column_types_by_num[i] = 'float'
                        elif row[i] == 'True' or row[i] == 'False':
                            self.column_types[table_get[i][0]] = 'bool'
                            self.column_types_by_num[i] = 'bool'
                        else:
                            self.column_types[table_get[i][0]] = 'str'
                            self.column_types_by_num[i] = 'str'
                        table_get[i].append(row[i])

                    for row in file:
                        for i in range(le):
                                table_get[i].append(Table.type_el(self, row[i], i))
            except:
                raise ValueError('Введено неверное имя для таблицы или имя файла записано неверно')
        for i in range(len(headline)):
            self.headlines_num[headline[i]] = i
        self.values = table_get
        self.headlines = headline
        self.width_table = len(table_get)
        self.height_table = len(table_get[0])

    def save_table(self):
        output = [[] for _ in range(self.height_table)]
        for j in range(self.height_table):
            for i in range(self.width_table):
                output[j].append(self.values[i][j])

        if self.name.split('.')[1] == 'csv':
            with open('output.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(output)
        elif self.name.split('.')[1] == 'pickle':
            with open('output.pickle', 'wb') as f:
                pickle.dump(output, f)
        elif self.name.split('.')[1] == 'txt':
            with open('output.txt', 'w') as f:
                for row in output:
                    for el in row:
                        f.write(str(el) + ' ')
                    f.write('\n')
        else:
            raise ValueError('Выбран неверный формат у таблицы')

    def print_table(self):
        try:
            for j in range(self.height_table):
                for i in range(self.width_table):
                    print(self.values[i][j], end=' ')
                print()
        except:
            raise ValueError('Неверное представление таблицы, проверьте загруженные данные')

    def get_rows_by_number(self, start: int, stop=0, copy_table=False):
        if stop > self.height_table or start < 0 or start > stop:
            raise ValueError('Введены некорректные значения для чисел start и stop')
        new_table = [[self.values[i][0]] for i in range(self.width_table)]
        start += 1
        stop += 1
        if not stop:
            stop = start + 1
        for j in range(start, stop + 1):
            for i in range(self.width_table):
                new_table[i].append(self.values[i][j])
        if copy_table:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table,
                         stop - start + 2)
        else:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table, stop - start + 2, con=True,
                         old_self=self)

    def get_rows_by_index(self, *args, copy_table=False):
        new_table = [[self.values[i][0]] for i in range(table.width_table)]
        for j in sorted(args):
            if type(j) != int:
                raise ValueError('Введенные индексы должны быть целочисленными')
            elif j >= self.height_table or j < 0:
                raise ValueError('Индекс out of range')

        for j in sorted(args):
            for i in range(table.width_table):
                new_table[i].append(self.values[i][j + 1])

        if copy_table:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table, len(args) + 1)
        else:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table, len(args) + 1, con=True, old_self=self)

    def get_column_types(self, by_number=True):
        if type(by_number) != bool:
            raise TypeError('Значение by_number может принимать значения только True или False')
        if not by_number:
            return self.column_types
        else:
            return self.column_types_by_num

    def set_column_types(self, types_dict: dict, by_number=True):
        if type(types_dict) != dict:
            raise TypeError('На вход подаетя словарь')
        if type(by_number) != bool:
            raise TypeError('Значение by_number может принимать значения только True или False')
        key_list_new = list(types_dict.keys())
        key_list = list(self.column_types.keys())
        d = self.column_types
        d_n = self.column_types_by_num
        if by_number:
            for key_new in key_list_new:
                d[key_new] = types_dict[key_new]
                d_n[key_list[key_new]] = types_dict[key_new]
        else:
            for key_new in key_list_new:
                d_n[key_list.index(key_new)] = types_dict[key_new]
                d[key_new] = types_dict[key_new]
        self.column_types_by_num = d_n
        self.column_types = d

    def get_values(self, column=0):
        if not (column in self.headlines_num.values() or column in self.headlines):
            raise ValueError('Введено неверное значение для столбца')
        list_values = []
        if not is_int(column):
            column = self.headlines_num[column]
        for j in range(1, self.height_table):
            list_values.append(Table.type_el(self, self.values[column][j], column))
        return list_values

    def get_value(self, column=0):
        if not (column in self.headlines_num.values() or column in self.headlines):
            raise ValueError('Введено неверное значение для столбца')
        if not is_int(column):
            column = self.headlines_num[column]
        return Table.type_el(self, self.values[column][1], column)

    def set_values(self, values_arr: list, column=0):
        if not (column in self.headlines_num.values() or column in self.headlines):
            raise ValueError('Введено неверное значение для столбца')
        arr = self.values
        if not is_int(column):
            column = self.headlines_num[column]
        for j in range(len(values_arr)):
            arr[column][j + 1] = Table.type_el(self, values_arr[j], column)
        self.values = arr

    def set_value(self, new_value, column=0):
        if not (column in self.headlines_num.values() or column in self.headlines):
            raise ValueError('Введено неверное значение для столбца')
        arr = self.values
        if not is_int(column):
            column = self.headlines_num[column]
        arr[column][1] = Table.type_el(self, new_value, column)
        self.values = arr

    def column_to_int(self, column):
        if is_int(column):
            return column
        return int(self.headlines_num[column])

    def error_column(self, column1, column2, column_w=None):
        if not (column1 in self.headlines_num.values() or column1 in self.headlines):
            raise ValueError('Введено неверное значение для столбца 1')
        if not (column2 in self.headlines_num.values() or column2 in self.headlines):
            raise ValueError('Введено неверное значение для столбца 2')
        if not (column1 in self.headlines_num.values() or column1 in self.headlines):
            raise ValueError('Введено неверное значение для столбца 1')
        if not (column_w is None) and not (column_w in self.headlines_num.values() or column_w in self.headlines):
            raise ValueError('Введено неверное значение для столбца куда происходит запись')

    def add(self, column1, column2, column_w):
        Table.error_column(self, column1, column2, column_w)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        for j in range(1, self.height_table):
            arr[column_w][j] = arr[column1][j] + arr[column2][j]
        self.values = arr

    def sub(self, column1, column2, column_w):
        Table.error_column(self, column1, column2, column_w)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        for j in range(1, self.height_table):
            arr[column_w][j] = arr[column1][j] - arr[column2][j]
        self.values = arr

    def mul(self, column1, column2, column_w):
        Table.error_column(self, column1, column2, column_w)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        for j in range(1, self.height_table):
            arr[column_w][j] = arr[column1][j] * arr[column2][j]
        self.values = arr

    def div(self, column1, column2, column_w):
        Table.error_column(self, column1, column2, column_w)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        for j in range(1, self.height_table):
            arr[column_w][j] = arr[column1][j] / arr[column2][j]
        self.values = arr

    def eq(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] == arr[column2][j])
        return bool_list

    def gr(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] > arr[column2][j])
        return bool_list

    def ls(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] < arr[column2][j])
        return bool_list

    def ge(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] >= arr[column2][j])
        return bool_list

    def le(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] <= arr[column2][j])
        return bool_list

    def ne(self, column1, column2):
        Table.error_column(self, column1, column2)
        arr = self.values
        column1 = Table.column_to_int(self, column1)
        column2 = Table.column_to_int(self, column2)
        bool_list = []
        for j in range(1, self.height_table):
            bool_list.append(arr[column1][j] != arr[column2][j])
        return bool_list

    def filter_rows(self, bool_list, copy_table=False):
        new_table = [[self.values[i][0]] for i in range(table.width_table)]
        if len(bool_list) != self.height_table - 1:
            raise ValueError('Длинна списка bool должна совпадать с количеством строк в таблице')
        arr = self.values
        for j in range(1, self.height_table):
            for i in range(self.width_table):
                if bool_list[j - 1]:
                    new_table[i].append(arr[i][j])

        if copy_table:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table, len(new_table[0]))
        else:
            return Table(deepcopy(self.name), deepcopy(new_table), deepcopy(self.headlines),
                         deepcopy(self.headlines_num), deepcopy(self.column_types),
                         deepcopy(self.column_types_by_num), self.width_table, len(new_table[0]), con=True,
                         old_self=self)


table = Table('inputcsv')
table.load_table()

table2 = table.get_rows_by_index(1, 3, 5, 8, copy_table=False)
table2.print_table()
table2.set_values([20, 30, 4], 2)
table2.set_value('1978-11-12', 1)
print()
table2.name = 'lol.txt'
print(table2.name, table.name)
print(table2.le('salary_from_rub', 3))
table3 = table2.filter_rows(table2.le('salary_from_rub', 3), copy_table=True)
table3.print_table()
# print(table.get_values('published_at'))
# print(table2.get_values('published_at'))
