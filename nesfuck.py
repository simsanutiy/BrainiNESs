import argparse

def input_parse():
    """Парсим аргументы из командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file_name', type=open)
    parser.add_argument('output_file_name', type=argparse.FileType('w'))
    args = parser.parse_args()

    """Раскидываем аргументы по переменным"""
    inp = args.source_file_name.read()
    global output
    output = args.output_file_name
    return inp

def bf_parse(inp):
    """Убираем лишние символы и комментарии"""
    code = ''
    comm_flag = 0
    for sym in inp:
        if sym == '#': comm_flag = 1
        if sym == '\n': comm_flag = 0
        if comm_flag == 0:
            if sym in '><+-.,[]':
                code += sym
    code += '}'
    return code

def c_process(code):
    """Переводим это говно в C"""
    output.write(header)
    tab = 1
    order = 0
    print(code)
    while order < len(code):
        #print(code[order])

        if code[order] == '+':
            sum = 0
            while code[order] == '+':
                print(order)
                sum += 1
                order += 1
            output.write('\t'*tab+'a[a_pointer]=a[a_pointer]+'+str(sum)+';\n')
            #print(sum, ' ', order, code[order])

        if code[order] == '-':
            sum = 0
            while code[order] == '-':
                sum += 1
                order += 1
            output.write('\t'*tab+'a[a_pointer]=a[a_pointer]-'+str(sum)+';\n')

        if code[order] == '>':
            sum = 0
            while code[order] == '>':
                sum += 1
                order += 1
            output.write('\t'*tab+'a_pointer=a_pointer+'+str(sum)+';\n')

        if code[order] == '<':
            sum = 0
            while code[order] == '<':
                sum += 1
                order += 1
                if order >= len(code): break
            output.write('\t'*tab+'a_pointer=a_pointer-'+str(sum)+';\n')

        if code[order] == '[':
            output.write('\t' * tab + 'while (a[a_pointer] != 0) {\n')
            tab += 1
            order += 1

        if code[order] == ']':
            tab -= 1
            output.write('\t' * tab + '}\n')
            order += 1

        if code[order] == '.':
            output.write('\t' * tab + 'PPU_DATA = a[a_pointer];\n')
            order += 1

        if code[order] == ',':
            output.write('#\n')
            order += 1

        if code[order] == '}':
            output.write(footer)
            order += 1
            
        #order += 1

header = """#define PPU_CTRL		*((unsigned char*)0x2000)
#define PPU_MASK		*((unsigned char*)0x2001)
#define PPU_STATUS		*((unsigned char*)0x2002)
#define SCROLL			*((unsigned char*)0x2005)
#define PPU_ADDRESS		*((unsigned char*)0x2006)
#define PPU_DATA		*((unsigned char*)0x2007)

unsigned char a[512];
unsigned char a_pointer = 0;
unsigned char index;
const unsigned char PALETTE[]={
0x1f, 0x00, 0x10, 0x20
}; //	black, gray, lt gray, white

void main (void) {
		//	turn off the screen
	PPU_CTRL = 0;
	PPU_MASK = 0;
	
	//	load the palette
	PPU_ADDRESS = 0x3f; 	//	set an address in the PPU of 0x3f00
	PPU_ADDRESS = 0x00;
"""

footer = """
//	reset the scroll position	
	PPU_ADDRESS = 0;
	PPU_ADDRESS = 0;
	SCROLL = 0;
	SCROLL = 0;
	
	//	turn on screen
	PPU_CTRL = 0x90; 	//	screen is on, NMI on
	PPU_MASK = 0x1e;
	
	//	infinite loop
	while (1);
}"""

c_process(bf_parse(input_parse()))
#output.write('#' + code)
output.close
