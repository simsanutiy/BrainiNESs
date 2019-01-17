import argparse #Модуль парсинга аргументов командной строки
import headfoot #Начало и конец вывода на C вынесен в другой файл

def input_parse():
    """Парсим аргументы из командной строки"""
    parser = argparse.ArgumentParser()  #Создаём парсер
    parser.add_argument('source_file_name', type=open)  #Аргументы: входной файл
    parser.add_argument('output_file_name', type=argparse.FileType('w'))#И выходной
    args = parser.parse_args()  #И парсим

    """Раскидываем аргументы по переменным"""
    inp = args.source_file_name.read()  #Входной файл строкой
    output = args.output_file_name  #И имя ывходного файла
    return (inp, output)

def bf_parse(inp):
    """Убираем лишние символы и комментарии"""
    code = ''   #Берём пустую строку
    comm_flag = 0   #А это флаг комментария
    for sym in inp:
        if sym == '#': comm_flag = 1    #Дальше коммент
        elif sym == '\n': comm_flag = 0   #Коммент кончился
        elif comm_flag == 0:  #Если это не коммент
            if sym in '><+-.,[]':   #И это символ брейнфака
                code += sym #То добавляем этот символ в строку
    code += '}'
    return code

def c_process(code):
    """Переводим это говно в C"""
    output.write(headfoot.header)
    tab = 1
    order = 0
    while order < len(code):

        if code[order] == '+':
            sum = 0
            while code[order] == '+':
                sum += 1
                order += 1
            output.write('\t'*tab+'a[a_pointer]=a[a_pointer]+'+str(sum)+';\n')

        elif code[order] == '-':
            sum = 0
            while code[order] == '-':
                sum += 1
                order += 1
            output.write('\t'*tab+'a[a_pointer]=a[a_pointer]-'+str(sum)+';\n')

        elif code[order] == '>':
            sum = 0
            while code[order] == '>':
                sum += 1
                order += 1
            output.write('\t'*tab+'a_pointer=a_pointer+'+str(sum)+';\n')

        elif code[order] == '<':
            sum = 0
            while code[order] == '<':
                sum += 1
                order += 1
                if order >= len(code): break
            output.write('\t'*tab+'a_pointer=a_pointer-'+str(sum)+';\n')

        elif code[order] == '[':
            output.write('\t' * tab + 'while (a[a_pointer] != 0) {\n')
            tab += 1
            order += 1

        elif code[order] == ']':
            tab -= 1
            output.write('\t' * tab + '}\n')
            order += 1

        elif code[order] == '.':
            output.write('\t' * tab + 'PPU_DATA = a[a_pointer];\n')
            order += 1

        elif code[order] == ',':
            output.write('#\n')
            order += 1

        elif code[order] == '}':
            output.write(headfoot.footer)
            order += 1
            
        #order += 1



inp, output = input_parse()
c_process(bf_parse(inp))
output.close
