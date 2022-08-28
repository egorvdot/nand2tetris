import argparse


symbol_table = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        **{f'R{i}': i for i in range(16)},
        'SCREEN': 16384,
        'KBD': 24576,
        }
new_symbol_addr=16


comp_map = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        'M': '110000',
        '!D': '001101',
        '!A': '110001',
        '!M': '110001',
        '-D': '001111',
        '-A': '110011',
        '-M': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'M+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'M-1': '110010',
        'D+A': '000010',
        'D+M': '000010',
        'D-A': '010011',
        'D-M': '010011',
        'A-D': '000111',
        'M-D': '000111',
        'D&A': '000000',
        'D&M': '000000',
        'D|A': '010101',
        'D|M': '010101',
        }

dest_map = {
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
        }

jump_map = {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
        }


def parse_type(asm_i: str):
    if asm_i.startswith('//'):
        return 'comment'
    if asm_i == '':
        return 'empty'
    if asm_i.startswith('@'):
        return 'command_a'
    if asm_i.startswith('('):
        return 'label'
    return 'command_c'


def remove_comment(asm_instruction):
    asm_i, *_ = asm_instruction.split('//')
    cleaned = asm_i.rstrip()
    return cleaned

def parse_command_a(asm_instruction):
    global new_symbol_addr
    asm_i = remove_comment(asm_instruction)
    addr_symbols = asm_i[1:]
    is_variable = bool(''.join([i for i in addr_symbols if not addr_symbols.isdigit()]))
    if is_variable:
        if addr_symbols not in symbol_table:
            symbol_table[addr_symbols] = new_symbol_addr
            new_symbol_addr += 1
        dec_addr = symbol_table[addr_symbols]
    else:
        dec_addr = int(addr_symbols)
    bin_addr = bin(dec_addr)[2:]
    bin_addr_15 = bin_addr.zfill(15)
    return f'0{bin_addr_15}'


def parse_command_c(asm_instruction):
    asm_i = remove_comment(asm_instruction)
    dest, comp, jump = None, None, None
    if '=' in asm_i:
        dest, tail = asm_i.split('=')
    else:
        tail = asm_i
    if ';' in tail:
        comp, jump = tail.split(';')
    else:
        comp = tail
    a_bit = 1 if 'M' in comp else 0
    bin_comp = comp_map[comp]
    if dest:
        bin_dest = dest_map[dest]
    else:
        bin_dest = '000'
    if jump:
        bin_jump = jump_map[jump]
    else:
        bin_jump = '000'

    return f'111{a_bit}{bin_comp}{bin_dest}{bin_jump}'


def parse_lable(asm_instruction, label_addr):
    asm_i = remove_comment(asm_instruction)
    label = asm_i[1:-1]
    if label not in symbol_table:
        symbol_table[label] = label_addr
    


def translate_asm_to_hack(asm_instructions):
    asm_instructions_fp = []
    asm_i_counter = 0
    for asm_i in asm_instructions:
        asm_i_type = parse_type(asm_i)
        if asm_i_type == 'label':
            parse_lable(asm_i, asm_i_counter)
        elif asm_i_type == 'empty':
            pass
        elif asm_i_type == 'comment':
            pass
        else:
            asm_i_counter += 1
            asm_instructions_fp.append(asm_i)
    hack_instructions_sp = []
    for asm_i in asm_instructions_fp:
        asm_i_type = parse_type(asm_i)
        hack_i = None
        if asm_i_type == 'command_a':
            hack_i = parse_command_a(asm_i)
        elif asm_i_type == 'command_c':
            hack_i = parse_command_c(asm_i)
        elif asm_i_type == 'label':
            pass
        if hack_i:
            hack_instructions_sp.append(hack_i)
    return hack_instructions_sp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    with open(args.file, 'r') as asm_file:
        asm_instructions = [asm_i.rstrip().lstrip() for asm_i in asm_file.readlines()]
        hack_instructions = [hack_i + '\n' for hack_i in translate_asm_to_hack(asm_instructions)]

    name = args.file.partition('.')[0]
    hack_file_name = f'{name}.hack'
    with open(hack_file_name, 'w') as hack_file:
        hack_file.writelines(hack_instructions)


