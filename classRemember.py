# программа для записи/удаления вопросов в json и преобразования в txt
# работает в консоли, в интерактивном режиме
# запрашивает команды пользователя
# открывает/закрывает файлы в формате json, кодировка utf-8
# открывает/закрывает файлы в формате txt, кодировки koi8_r, cp1251, cp866

import json
import os.path
import msvcrt # Useful routines from the MS VC++ runtime

class Remember:
    # словарь json вопросов
    dictJ = {}
    # словарь txt вопросов
    dictT = {}
    # кортеж будет содержать указатель на открытый файл json и имя
    fileJ = tuple([None, ""])
    # кортеж будет содержать указатель на открытый файл txt и имя
    fileT = tuple([None, ""])
    


    def __init__(self):
        pass
        
    def help_(self):
        print("Справка по программе")
        for k, v in self.cmd.items():
            print(f"Команда {k} - функция: {v[1]}")
    
    def info(self):
        print("Статус:")
        if self.fileJ[0] is None:
            print("Файл json не открыт")
        else:
            print(f"Файл json открыт: {self.fileJ[1]}")
        if self.fileT[0] is None:
            print("Файл txt не открыт")
        else:
            print(f"Файл txt открыт: {self.fileT[1]}")

    def open_file(self, name: str, mode = "r"):
        if not os.path.exists(name):
            print("Файл не существует!")
            return None
        try:
            file = open(name, mode)
        except OSError:
            print("Файл не открыт!")
            return None
        
        return file

    def load_file(self, file_, type_):
        if file_ is not None:
            print("Файл уже открыт!")
            q = input("Использовать текущий (<y>) или его закрыть и открыть новый (n)?")
            if q == "y" or q == "":
                print("Используем текущий файл")
                return file_
            else:
                print("Закрываем файл")
                file_.close()
        print(f"Загрузка файла {type_}")
        name = input(f"Введите имя файла (по умолчанию data.{type_}): ")
        if name == "":
            name = f"data.{type_}"
        print(f"Файл: {name}")
        file = self.open_file(name, "r")
    
        return file, name

    def load_json(self):
        self.fileJ = self.load_file(self.fileJ[0], "json")
        self.dictJ = json.load(self.fileJ[0])
        print("Закрытие файла")
        self.fileJ[0].close()
        self.fileJ = tuple([None, ""])
        
    def load_txt(self): # не готово!
        self.fileT = self.load_file(self.fileT[0], "txt")

    def save_json(self):
        print("Сохранение файла json")
        if self.dictJ == {}:
            print("Словарь пустой! Выход из функции.")
            return
        name = input("Введите имя файла (по умолчанию data.json):")
        if name == "":
            name = "data.json"
        print(f"Файл: {name}")
        with open(name, "w") as f:
            json.dump(self.dictJ, f)
            print("Закрытие файла")

    def save_txt(self):
        print("Сохранение файла txt")
        if self.dictJ == {}:
            print("Словарь пустой! Выход из функции.")
            return
        name = input("Введите имя файла (по умолчанию data.txt):")
        if name == "":
            name = "data.txt"
        print(f"Файл: {name}")
        encode_ = input("Выберите кодировку (<1> - koi8_r, 2 - cp1251, 3 - cp866):")
        if encode_ == "" or encode_ == "1":
            encode_ = "koi8_r"
        elif encode_ == "2":
            encode_ = "cp1251"
        elif encode_ == "3":
            encode_ = "cp866"
        else:
            print("Неизвестная кодировка! Выход из функции.")
            return
        print(f"Файл: {name}\nКодировка: {encode_}")
        with open(name, "w", encoding = encode_) as f:
            print("Сохранение...")
            for k, v in self.dictJ.items():
                f.write(f"{k}\n")
                if type(v) == dict:
                    for k_, v_ in v.items():
                        if k_.isnumeric():
                            f.write(f"  {k_}. {v_}\n") if int(k_) < 10 else f.write(f" {k_}. {v_}\n")
            print("Закрытие файла")

    def get_number_strings_to_print(self) -> int:
        in_ = input("Введите количество строк вывода на экран (<10>): ")
        if in_ == "":
            count_lines = 10
        elif in_.isnumeric():
            count_lines = int(in_)
        else:
            count_lines = 0
        
        return count_lines

    def view_json(self):
        print("Просмотр словаря json")
        if self.dictJ == {}:
            print("Словарь json пуст! Выход из функции.")
            return
        
        count_lines = self.get_number_strings_to_print()
        if count_lines == 0:
            print("Неизвестное число! Выход из функции.")
            return
    
        printed_lines = 0
        c = ""
        for k, v in self.dictJ.items():
            if c == "q":
                break
            print(k)
            printed_lines += 1
            if printed_lines > count_lines:
                c = input("***Для продолжения нажмите Enter (для выхода - 'q')...***")
                printed_lines = 0
            if type(v) == dict:
                for k_, v_ in v.items():
                    if k_.isnumeric():
                        print(f"  {k_}. {v_}") if int(k_) < 10 else print(f" {k_}. {v_}")
                    printed_lines += 1
                    if printed_lines > count_lines:
                        c = input("Для продолжения нажмите Enter (для выхода - 'q')...")
                        if c == "q":
                            break
                        printed_lines = 0

    def print_exist_courses(self):
        print("Существующие курсы:")
        for k in self.dictJ.keys():
            print(k)
        print()

    def get_char(self):
        return msvcrt.getwch()
        # msvcrt.getwch() - Read a keypress and returning a Unicode value.
        # Nothing is echoed to the console.

    def input_course(self) -> str:
        print("Введите курс: ", end = "", flush = True)
        c = chr(0)
        name_course = ""
        course = ""
        while ord(c) != 13:
            c = self.get_char()
            if ord(c) == 8 and len(name_course) > 0:
                print(f"{c} {c}", end = "", flush = True)
                name_course = name_course[0:-1]
                course = ""
            elif ord(c) == 8:
                course = ""
            else:
                print(c, end = "", flush = True)
                name_course += c
                count_courses = 0
                for k_ in self.dictJ.keys():
                    if k_.find(name_course) > -1:
                        count_courses += 1
                        course = k_
                if count_courses == 1:
                    name_course = course
                    print("\rВведите курс: " + course, end = "", flush = True)
        print()
        return course

    def manage_dictionary(self):
        print("Управление словарём")
        if self.dictJ == {}:
            print("Словарь пустой!")
            in_ = input("Загрузить или создать новый? (<1> - загрузить, 2 - новый) ")
            if in_ == "" or in_ == "1":
                print("Для загрузки словаря выходим из функции")
                return
            elif in_ == "2":
                print("Создаём новый словарь")
            else:
                print("Неизвестная команда! Выход из функции")
                return
        while True:
            print("Команды:\n1 - добавить курс\n2 - добавить вопрос\n3 - удалить курс\n4 - удалить вопрос")
            in_ = input("Введите команду: ")
            if in_ == "1":
                print("Добавление курса")
                self.print_exist_courses()
                course = input("Введите название курса: ")
                self.dictJ[course] = {}
                print(f"Добавлен курс: {course}")
            
            elif in_ == "2":
                print("Добавление вопроса")
                self.print_exist_courses()
                course_ = self.input_course()
                if course_ == "":
                    print("Курс не выбран")
                else:
                    print(f"Выбран курс: {course_}")
                    count_lines = self.get_number_strings_to_print()
                    if count_lines == 0:
                        print("Неизвестное число! Выход из функции.")
                        return
    
                    printed_lines = 0
                    print("Существующие вопросы курса:")
                    if len(self.dictJ[course_]) > 0:
                        for k_, v_ in self.dictJ[course_].items():
                            if k_.isnumeric():
                                print(f"  {k_}. {v_}") if int(k_) < 10 else print(f" {k_}. {v_}")
                                printed_lines += 1
                                if printed_lines > count_lines:
                                    _ = input("***Для продолжения нажмите Enter...***")
                                    printed_lines = 0
                        last_key = max([int(x) for x in self.dictJ[course_].keys()])
                    else:
                        last_key = 0
                    question = input("Введите вопрос: ")
                    print(f"Добавление вопроса: {last_key+1}. {question}")
                    self.dictJ[course_][str(last_key+1)] = question
            
            elif in_ == "3":
                print("Удаление курса")
                self.print_exist_courses()
                course_to_remove = self.input_course()
                if course_to_remove == "" or course_to_remove not in self.dictJ:
                    print("Курс не выбран или выбран с ошибкой!")
                else:
                    print(f"Выбран курс: {course_to_remove}")
                    if len(self.dictJ[course_to_remove]) > 0:
                        query_to_remove = input("Курс не пустой! Удалить? (y - да, <n> - нет) ")
                        if query_to_remove == "" or query_to_remove == "n":
                            print("Курс не удалён")
                        else:
                            del self.dictJ[course_to_remove]
                            print(f"Курс '{course_to_remove}' удалён из словаря")
                    else:
                        del self.dictJ[course_to_remove]
                        print(f"Курс '{course_to_remove}' удалён из словаря")
            
            elif in_ == "4":
                print("Удаление вопроса")
                self.print_exist_courses()
                course_to_remove_question = self.input_course()
                if course_to_remove_question == "" or course_to_remove_question not in self.dictJ:
                    print("Курс не выбран или выбран с ошибкой!")
                else:
                    print(f"Выбран курс: {course_to_remove_question}")
    
                    printed_lines = 0
                    if len(self.dictJ[course_to_remove_question]) > 0:
                        count_lines = self.get_number_strings_to_print()
                        if count_lines == 0:
                            print("Неизвестное число! Выход из функции.")
                            return
                        print("Существующие вопросы курса:")
                        for k_, v_ in self.dictJ[course_to_remove_question].items():
                            if k_.isnumeric():
                                print(f"  {k_}. {v_}") if int(k_) < 10 else print(f" {k_}. {v_}")
                                printed_lines += 1
                                if printed_lines > count_lines:
                                    _ = input("***Для продолжения нажмите Enter...***")
                                    printed_lines = 0
                        num = input("Введите номер удаляемого вопроса: ")
                        if not num.isnumeric() or num not in self.dictJ[course_to_remove_question]:
                            print("Неизвестный номер")
                            continue
                        print(f"Вопрос '{num}. {self.dictJ[course_to_remove_question][num]}' удалён из курса '{course_to_remove_question}'")
                        del self.dictJ[course_to_remove_question][num]
                    else:
                        print("Курс пустой!")
            else:
                print("Неизвестная команда! Выход из функции")
                return
            in_ = input("Продолжить? (y - да, <n> - нет) ")
            if in_ == "" or in_ == "n":
                print("Выход из управления словарём")
                return

    # словарь команд, функций и описаний для справки
    cmd = {"q": [help_, "Выход из программы"], 
           "h": [help_, "Справка по командам"], 
           "i": [info, "Информация по открытым файлам и загруженным словарям"], 
           "lj": [load_json, "Загрузить файл json"],
           "lt": [load_txt, "Загрузить файл txt - не готово!"], 
           "sj": [save_json, "Сохранить файл json"], 
           "st": [save_txt, "Сохранить файл txt"], 
           "vj": [view_json, "Посмотреть словарь json"], 
           "md": [manage_dictionary, "Управление словарём"]}

    def inputCommand(self):
        in_ = input("Введите команду: ")
        while in_ not in self.cmd.keys():
            print("Неизвестная команда!")
            self.help_()
            req = input("Повторить? (<y>/n) ")
            if req == "y" or req == "":
                in_ = input("Введите команду: ")
            else:
                return "q"
    
        return in_

    def main(self):
        command = self.inputCommand()
        while command != "q":
            self.cmd[command][0](self)
            command = self.inputCommand()
    
        # закрываем файлы
        if self.fileJ[0] is not None:
            print("Закрываем файл json")
            self.fileJ[0].close()
        if self.fileT[0] is not None:
            print("Закрываем файл txt")
            self.fileT[0].close()




if __name__ == "__main__":
    A = Remember()
    A.main()
