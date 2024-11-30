import secrets # предоставляет функции для работы с криптографически безопасными случайными числами
import string # является стандартной библиотекой языка Python и предоставляет набор констант и функций, связанных с обработкой строк
from base64 import * # предоставляет функции для кодирования и декодирования данных в формате Base64
from tkinter import * # является стандартным пакетом для создания графического интерфейса
from base64 import b64encode # метод используется для кодирования данных в формат Base64.
import tkinter.messagebox as mb # предоставляет стандартные диалоговые окна для вывода сообщений и получения подтверждения от пользователя в графическом интерфейсе
from tkinter.ttk import Combobox # представляет собой выпадающий список (комбинированный виджет), который может содержать список опций, из которого пользователь может выбирать
from Crypto.Cipher import AES # импортирует модуль AES из библиотеки Crypto
from Crypto.Util.Padding import pad # предоставляет возможность автоматического дополнения данных в соответствии с определенным стандартом
from Crypto.Util.Padding import unpad # предоставляет возможность автоматического удаления дополнения в соответствии с определенным стандартом
def pokaz_oshibka_klych_dlina(): # для режима шифрования ECB показ ошибки длины ключа
    oshibka_sms = "РАЗМЕР КЛЮЧА ДОЛЖЕН БЫТЬ РАВЕН 16 СИМВОЛОВ!" # текст ошибки
    mb.showerror("ОШИБКА!", oshibka_sms) # название окна
def pokaz_ohibka_klych_i_vector_inicializatcia_dlina(): # для режимов шифрования CBC, CFB, OFB показ ошибки длины ключа и вектора инициализации
    oshibka_sms = "РАЗМЕРЫ КЛЮЧА И ВЕКТОРА ИНИЦИАЛИЗАЦИИ ДОЛЖНЫ БЫТЬ РАВНЫ ПО 16 СИМВОЛОВ!" # текст ошибки
    mb.showerror("ОШИБКА!", oshibka_sms) # название окна
def pokaz_preduprezdenie_vektor_inicializatcia(): # функция показывает окнопредупреждение
    preduprezdenie_sms = "ДЛЯ РЕЖИМА ECB ВЕКТОР ИНИЦИАЛИЗАЦИИ НЕ НУЖЕН!" # текст предупреждения
    mb.showwarning("ОШИБКА!", preduprezdenie_sms) # название окна
    pole_vvod_vektor_inicializatcia.delete(0, END) # удаляется содержимое поля вектора инициализации
def generatcia_klych_i_vektor_inicializatcia(dlina): # генерация ключа и вектора инициализации, передаётся длина
    alfavit = string.ascii_letters + string.digits # алфавит
    sms = ''.join(secrets.choice(alfavit) for i in range(dlina)) # генерация смс
    return sms # возврат сгенерированного смс
def zapusk(): # функционал кнопки запуск
    if (pole_vibor_rezim_shirovaniya.get() == "-" and (pole_vibor_deyistvie.get() == "Зашифровать" or pole_vibor_deyistvie.get() == "Расшифровать" or pole_vibor_deyistvie.get() == "-")) or (pole_vibor_deyistvie.get() == "-" and (pole_vibor_rezim_shirovaniya.get() == "-" or pole_vibor_rezim_shirovaniya.get() == "ECB" or pole_vibor_rezim_shirovaniya.get() == "CBC" or pole_vibor_rezim_shirovaniya.get() == "CFB" or pole_vibor_rezim_shirovaniya.get() == "OFB")): # проверка условий на истину
        pole_vivod.delete(1.0, END) # стирание содержимого
        pole_vivod.insert(1.0, "Для работы программы сначала выберите режим шифрования, а затем действие (Зашифровать или Расшифровать)!") # добавление текста во внутрь поля вывода
    if (pole_vibor_rezim_shirovaniya.get() == "ECB" and (pole_vibor_deyistvie.get() == "Зашифровать" or pole_vibor_deyistvie.get() == "Расшифровать")) and pole_vvod_vektor_inicializatcia.get(): # условие на то, чтобы будет ли показано окно предупреждения что вектор инициализации не нужен в режиме ECB
        pokaz_preduprezdenie_vektor_inicializatcia() # показ окна предупреждения
    if pole_vibor_rezim_shirovaniya.get() == "ECB" and pole_vibor_deyistvie.get() == "Зашифровать": # тут идёт шифрование ECB
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        tekst = bytes(pole_vvod_tekst.get(), "utf-8") # байтовая последовательность текста
        pole_vivod.insert(END, "Ключ: \n" + str(klyuch)) # добавление в поле вывода ключа
        try: # тут происходит зашифрование
            schifr = AES.new(klyuch, AES.MODE_ECB) # то каким ключом шифруем
            schifr_tekst_byte = schifr.encrypt(pad(tekst, AES.block_size)) # то как выглядит в байтовом представлении
            schifr_tekst = b64encode(schifr_tekst_byte).decode("utf-8") # нужная кодировка и зашифровали текст
            pole_vivod.insert(END, "\nЗашифрованный текст: \n" + schifr_tekst) # добавление зашифрованного текста в поле вывода
        except ValueError: # ловим ошибку
            pokaz_oshibka_klych_dlina() # показ ошибки длины ключа
    if pole_vibor_rezim_shirovaniya.get() == "ECB" and pole_vibor_deyistvie.get() == "Расшифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        schifr_tekst_byte = pole_vvod_tekst.get().encode("utf-8") # байтовое представление закодированного текста
        raschifr_tekst_byte = b64decode(schifr_tekst_byte) # байтовое представление раскодированного текста
        raschifr = AES.new(klyuch, AES.MODE_ECB) # процесс расшифрования
        original_tekst = unpad(raschifr.decrypt(raschifr_tekst_byte), AES.block_size) # оригинальный текст в байтовом представлении
        original = original_tekst.decode("utf-8") # оригинальный расшифрованный текст
        pole_vivod.insert(END, "Исходный текст: \n" + original) # добавление расшифрованного оригинального текста в поле вывода
    if pole_vibor_rezim_shirovaniya.get() == "CBC" and pole_vibor_deyistvie.get() == "Зашифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        tekst = bytes(pole_vvod_tekst.get(), "utf-8") # байтовая последовательность текста
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8") # байтовая последовательность вектора инициализации
        pole_vivod.insert(END, "Ключ: \n" + str(klyuch)) # добавление в поле вывода ключа
        pole_vivod.insert(END, "\nIv: \n" + str(Iv)) # добавление в поле вывода вектора инициализации
        try: # тут происходит зашифрование
            schifr = AES.new(klyuch, AES.MODE_CBC, Iv) # то каким ключом и вектором инициализации шифруем
            schifr_tekst_byte = schifr.encrypt(pad(tekst, AES.block_size)) # то как выглядит в байтовом представлении
            schifr_tekst = b64encode(schifr_tekst_byte).decode("utf-8") # нужная кодировка и зашифровали текст
            pole_vivod.insert(END, "\nЗашифрованный текст: \n" + schifr_tekst) # добавление зашифрованного текста в поле вывода
        except ValueError: # ловим ошибку
            pokaz_ohibka_klych_i_vector_inicializatcia_dlina() # показ ошибки длины ключа и вектора инициализации
    if pole_vibor_rezim_shirovaniya.get() == "CBC" and pole_vibor_deyistvie.get() == "Расшифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        schifr_tekst_byte = pole_vvod_tekst.get().encode("utf-8") # байтовое представление закодированного текста
        raschifr_tekst_byte = b64decode(schifr_tekst_byte) # байтовое представление раскодированного текста
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8") # байтовая последовательность вектора инициализации
        raschifr = AES.new(klyuch, AES.MODE_CBC, Iv) # процесс расшифрования
        original_tekst = unpad(raschifr.decrypt(raschifr_tekst_byte), AES.block_size) # оригинальный текст в байтовом представлении
        original = original_tekst.decode("utf-8") # оригинальный расшифрованный текст
        pole_vivod.insert(END, "Исходный текст: \n" + original) # добавление расшифрованного оригинального текста в поле вывода
    if pole_vibor_rezim_shirovaniya.get() == "CFB" and pole_vibor_deyistvie.get() == "Зашифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        tekst = bytes(pole_vvod_tekst.get(), "utf-8") # байтовая последовательность текста
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8") # байтовая последовательность вектора инициализации
        pole_vivod.insert(END, "Ключ: \n" + str(klyuch)) # добавление в поле вывода ключа
        pole_vivod.insert(END, "\nIv: \n" + str(Iv)) # добавление в поле вывода вектора инициализации
        try: # тут происходит зашифрование
            schifr = AES.new(klyuch, AES.MODE_CFB, Iv, segment_size=8) # то каким ключом и вектором инициализации шифруем
            schifr_tekst_byte = schifr.encrypt(tekst) # то как выглядит в байтовом представлении
            schifr_tekst = b64encode(schifr_tekst_byte).decode('utf-8') # нужная кодировка и зашифровали текст
            pole_vivod.insert(END, "\nЗашифрованный текст: \n" + schifr_tekst) # добавление зашифрованного текста в поле вывода
        except ValueError: # ловим ошибку
            pokaz_ohibka_klych_i_vector_inicializatcia_dlina() # показ ошибки длины ключа и вектора инициализации
    if pole_vibor_rezim_shirovaniya.get() == "CFB" and pole_vibor_deyistvie.get() == "Расшифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8")  # байтовая последовательность вектора инициализации
        schifr_tekst_byte = pole_vvod_tekst.get().encode("utf-8") # байтовое представление закодированного текста
        raschifr_tekst_byte = b64decode(schifr_tekst_byte) # байтовое представление раскодированного текста
        raschifr = AES.new(klyuch, AES.MODE_CFB, Iv, segment_size = 8) # процесс расшифрования
        original_tekst = raschifr.decrypt(raschifr_tekst_byte) # оригинальный текст в байтовом представлении
        original = original_tekst.decode("utf-8") # оригинальный расшифрованный текст
        pole_vivod.insert(END, "Исходный текст: \n" + original) # добавление расшифрованного оригинального текста в поле вывода
    if pole_vibor_rezim_shirovaniya.get() == "OFB" and pole_vibor_deyistvie.get() == "Зашифровать":
        steret() # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        tekst = bytes(pole_vvod_tekst.get(), "utf-8") # байтовая последовательность текста
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8") # байтовая последовательность вектора инициализации
        pole_vivod.insert(END, "Ключ: \n" + str(klyuch)) # добавление в поле вывода ключа
        pole_vivod.insert(END, "\nIv: \n" + str(Iv)) # добавление в поле вывода вектора инициализации
        try: # тут происходит зашифрование
            schifr = AES.new(klyuch, AES.MODE_OFB, Iv) # то каким ключом и вектором инициализации шифруем
            schifr_tekst_byte = schifr.encrypt(tekst) # то как выглядит в байтовом представлении
            schifr_tekst = b64encode(schifr_tekst_byte).decode("utf-8") # нужная кодировка и зашифровали текст
            pole_vivod.insert(END, "\nЗашифрованный текст: " + schifr_tekst) # добавление зашифрованного текста в поле вывода
        except ValueError: # ловим ошибку
            pokaz_ohibka_klych_i_vector_inicializatcia_dlina() # показ ошибки длины ключа и вектора инициализации
    if pole_vibor_rezim_shirovaniya.get() == "OFB" and pole_vibor_deyistvie.get() == "Расшифровать":
        steret()  # стирает поле вывода
        klyuch = bytes(pole_vvod_klyuch.get(), "utf-8") # байтовая последовательность ключа
        Iv = bytes(pole_vvod_vektor_inicializatcia.get(), "utf-8") # байтовая последовательность вектора инициализации
        schifr_tekst_byte = pole_vvod_tekst.get().encode("utf-8") # байтовое представление закодированного текста
        raschifr_tekst_byte = b64decode(schifr_tekst_byte) # байтовое представление раскодированного текста
        raschifr = AES.new(klyuch, AES.MODE_OFB, Iv) # процесс расшифрования
        original_tekst = raschifr.decrypt(raschifr_tekst_byte) # оригинальный текст в байтовом представлении
        original = original_tekst.decode("utf-8") # оригинальный расшифрованный текст
        pole_vivod.insert(END, "Исходный текст: " + original) # добавление расшифрованного оригинального текста в поле вывода
def ochistit(): # функция чистит текст, ключ и вектора инициализации
    pole_vvod_tekst.delete(0, END) # очищение содержимого поля текста
    pole_vvod_klyuch.delete(0, END) # очищение содержимого поля ключа
    pole_vvod_vektor_inicializatcia.delete(0, END) # очищение сожержимого вектора инициализации
def steret(): # функция чистит поле вывода
    pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
def spravka(): # функция нажатия кнопки справка
    if pole_vibor_rezim_shirovaniya.get() == "ECB": # условие если режим шифрования ECB
        pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
        pole_vivod.insert(1.0, "Режим электронной кодовой книги (Electronic Codebook, ECB) — один из вариантов использования симметричного блочного шифра, при котором каждый блок открытого текста заменяется блоком шифротекста.\nОсобенность: \nРежим устойчив к ошибкам, связанным с изменением битов блока (ошибка не распространяется на другие блоки), но неустойчив к ошибкам, связанным с потерей или вставкой битов, если не используется дополнительный механизм выравнивания блоков.\nДля данного режима дополнительно необходимо ввести ключ (16 символов).") # вывод текста справки по режиму шифрования ECB
    elif pole_vibor_rezim_shirovaniya.get() == "CBC": # условие если режим шифрования CBC
        pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
        pole_vivod.insert(1.0, "Режим сцепления блоков шифротекста (Cipher Block Chaining, CBC) — один из режимов шифрования для симметричного блочного шифра с использованием механизма обратной связи. Каждый блок открытого текста (кроме первого) побитово складывается по модулю 2 (операция XOR) с предыдущим результатом шифрования.\nОсобенность: \nНаличие механизма распространения ошибки: если при передаче произойдёт изменение одного бита шифротекста, данная ошибка распространится и на следующий блок. Однако на последующие блоки (через один) ошибка не распространится, поэтому режим CBC также называют самовосстанавливающимся.\nДля данного режима дополнительно необходимо ввести ключ (16 символов) и вектор инизиацлизации Iv (16 символов).") # вывод текста справки по режиму шифрования CBC
    elif pole_vibor_rezim_shirovaniya.get() == "CFB": # условие если режим шифрования CFB
        pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
        pole_vivod.insert(1.0, "Режим обратной связи по шифротексту, режим гаммирования с обратной связью (Cipher Feedback Mode, CFB) — один из вариантов использования симметричного блочного шифра, при котором для шифрования следующего блока открытого текста он складывается по модулю 2 с перешифрованным (блочным шифром) результатом шифрования предыдущего блока.\nОсобенность: \nВектор инициализации IV, как и в режиме сцепления блоков шифротекста, можно делать известным, однако он должен быть уникальным.\nДля данного режима дополнительно необходимо ввести ключ (16 символов) и вектор инизиацлизации Iv (16 символов).") # вывод текста справки по режиму шифрования CFB
    elif pole_vibor_rezim_shirovaniya.get() == "OFB": # условие если режим шифрования OFB
        pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
        pole_vivod.insert(1.0, "Режим обратной связи по выходу (Output Feedback, OFB) — один из вариантов использования симметричного блочного шифра. Особенностью режима является то, что в качестве входных данных для алгоритма блочного шифрования не используется само сообщение. Вместо этого блочный шифр используется для генерации псевдослучайного потока байтов, который с помощью операции XOR складывается с блоками открытого текста. Подобная схема шифрования называется потоковым шифром.\nОсобенность: \nЗначение вектора инициализации должно быть уникальным для каждой процедуры шифрования одним ключом. Его необязательно сохранять в секрете и оно может быть передано вместе с шифротекстом.\nДля данного режима дополнительно необходимо ввести ключ (16 символов) и вектор инизиацлизации Iv (16 символов).") # вывод текста справки по режиму шифрования OFB
    else: # условие если режим шифрования не выбран
        pole_vivod.delete(1.0, END) # очищение содержимого поля вывода
        pole_vivod.insert(1.0, "Crypton — симметричный алгоритм блочного шифрования, разработанный южнокорейским криптологом для участия в конкурсе, проводимом NIST. Этот алгоритм хорошо проанализирован и сейчас широко используется.\nВ данной программе представлено несколько режимов работы данного алгоритма шифрования: ECB, CBC, CFB, OFB.")  # вывод текста справки по алгоритму шифрования Crypton
okno_programma = Tk() # окно программы основное
okno_programma.title("Программа Crypton") # название программы
okno_programma.iconbitmap("icon_for_app.ico") # иконка программы
okno_programma.configure(background = "yellow") # цвет фона
okno_programma.geometry("1024x768+200+200") # размеры окна
okno_programma.resizable(False, False) # запрет на увеличение окна
nazvanie_pole_vvod_tekst = Label(foreground= "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Введите текст: ").place(x = 10, y = 5) # название поля ввода текста
pole_vvod_tekst = Entry(width = 45, font = ("Times New Roman", "14", "bold")) # характеристики поля ввода текста
pole_vvod_tekst.place(x = 10, y = 40) # расположение поля ввода текста
nazvanie_pole_vvod_klyuch = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Введите ключ: ").place(x = 10, y = 75) # название поля ввода ключа
pole_vvod_klyuch = Entry(width = 45, font = ("Times New Roman", "14", "bold")) # характеристики поля ввода ключа
pole_vvod_klyuch.place(x = 10, y = 110) # расположение поля ввода ключа
nazvanie_pole_vvod_vektor_inicializatcia = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Введите вектор инициализации (Iv): ").place(x = 10, y = 145) # название поля ввода вектора инициализации
pole_vvod_vektor_inicializatcia = Entry(width = 45, font = ("Times New Roman", "14", "bold")) # характеристики поля ввода вектора инициализации
pole_vvod_vektor_inicializatcia.place(x = 10, y = 180) # расположение поля ввода вектора инициализации
knopka_spravka = Button(text = "Справка", width = 10, border = 5, font = ("Times New Roman", 14, "bold"), command = spravka) # характеристики кпопки Справка
knopka_spravka.place(x = 10, y = 220) # расположение кнопки Справка
knopka_zapusk = Button(text = "Запуск", width = 10, border = 5, font = ("Times New Roman", 14, "bold"), command = zapusk) # характеристики кнопки Запуск
knopka_zapusk.place(x = 150, y = 220) # расположение кнопки Запуск
knopka_ochistit = Button(text = "Очистить", width = 10, border = 5, font = ("Times New Roman", 14, "bold"), command = ochistit) # характеристики кнопки Очистить
knopka_ochistit.place(x = 300, y = 220) # расположение кнопки Очистить
nazvanie_pole_vivod = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Вывод: ").place(x = 10, y = 280) # название поля вывода
pole_vivod = Text(height = 15, width = 60, wrap = WORD, font = ("Times New Roman", 14, "bold")) # характеристики поля вывода
pole_vivod.place(x = 10, y = 320) # расположение поля вывода
knopka_zakryit = Button(text = "Закрыть", width = 10, border = 5, font=("Times New Roman", 14, "bold"), command = okno_programma.quit) # характеристики кнопки Закрыть
knopka_zakryit.place(x = 10, y = 670) # расположение кнопки Закрыть
knopka_steret = Button(text = "Стереть", width = 10, border = 5, font = ("Times New Roman", 14, "bold"), command = steret) # характеристики кнопки Стереть
knopka_steret.place(x = 485, y = 670) # расположение кнопки Стереть
spisok_rezhim_shifrovaniya = ["-", "ECB", "CBC", "CFB", "OFB"] # список режимов шифрования
pervyi_element_spisok_rezhim_shifrovaniya = StringVar(value = spisok_rezhim_shifrovaniya[0]) # первый элемент списка режимов шифрования
pole_vibor_rezim_shirovaniya = Combobox(okno_programma, width = 25, values = spisok_rezhim_shifrovaniya, textvariable = pervyi_element_spisok_rezhim_shifrovaniya, font = ("Times New Roman", 14, "bold"), state = "readonly") # выпадающий список режимов шифрования и его характеристики
nazvanie_pole_vibor_rezim_shirovaniya = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Выберите режим шифрования: ").place(x = 500, y = 5) # название списка режимов шифрования
pole_vibor_rezim_shirovaniya.place(x = 500, y = 40) # расположение названия списка режимов шифрования
pole_vibor_deyistviyi = ["-", "Зашифровать", "Расшифровать"] # список действий
pervyi_element_pole_vibor_deyistviyi = StringVar(value = pole_vibor_deyistviyi[0]) # первый элемент списка действий
pole_vibor_deyistvie = Combobox(okno_programma, width = 25, values = pole_vibor_deyistviyi, textvariable = pervyi_element_pole_vibor_deyistviyi, font = ("Times New Roman", 14, "bold"), state = "readonly") # выпадающий список действий и его характеристики
nazvanie_pole_vibor_deyistvie = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Выберите действие: ").place(x = 500, y = 75) # название списка действий
pole_vibor_deyistvie.place(x = 500, y = 110) # расположение названия списка действий
nazvanie_pole_sluchayini_klyuch = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Случайный ключ: ").place(x = 500, y = 145) # название поля случайного ключа
pole_sluchayini_klyuch = Text(height = 1, width = 45, wrap = WORD, font = ("Times New Roman", 14, "bold")) # характеристики поля случайного ключа
pole_sluchayini_klyuch.place(x = 500, y = 180) # расположение поля случайного ключа
nazvanie_pole_vektor_inicializatcia = Label(foreground = "black", background = "yellow", font = ("Times New Roman", 14, "bold"), text = "Вектор инициализации (Iv): ").place(x = 500, y = 215) # название поля вектора иницилиазации
pole_vektor_inicializatcia = Text(height = 1, width = 45, wrap = WORD, font = ("Times New Roman", 14, "bold")) # характеристи поля вектора инициализации
pole_vektor_inicializatcia.place(x = 500, y = 250) # расположение поля вектора инициализации
pole_sluchayini_klyuch.insert(1.0, generatcia_klych_i_vektor_inicializatcia(16)) # добавление случайного ключа в его поле
pole_vektor_inicializatcia.insert(1.0, generatcia_klych_i_vektor_inicializatcia(16)) # добавления вектора инициализации в его поле
okno_programma.mainloop() # показ главного окна