import fnmatch
import os

PROVINCES_PATH = "base_game\provinces"
CONTINENT_FILE = "base_game\map\continent.txt"
MOD_PATH = "mod\provinces"

def remove_comment(line):
    return line.lstrip().split("#", 1)[0].rstrip()


def pdx_read_lines(file):
    with open(file) as f:
        lines = f.read().splitlines()
        lines = [remove_comment(l) for l in lines if not l.startswith("#")]
    
    return lines


def get_continent_lines():
    return pdx_read_lines(CONTINENT_FILE)


def get_province_numbers(continent_lines, continent):
    continent_provinces = []

    is_continent = False
    
    for l in continent_lines:
        if l.find("}") != -1 and is_continent:
            break

        if l.replace(" ", "").startswith(f'{continent}={{'):
            is_continent = True
        elif is_continent:
            continent_provinces.extend(l.split())

    return continent_provinces

def get_province_files(provinces):
    return [f for f in os.listdir(PROVINCES_PATH) if f.split("-", 1)[0].rstrip() in provinces]


def half_production_and_add_half_tax(province_file):
    with open(PROVINCES_PATH + '\\' + province_file) as f:
        lines = f.read().splitlines(True)

    base_tax_tuple = ()
    base_production_tuple = ()
    
    is_city = False
    for i, line in enumerate(lines):
        line_without_comment = remove_comment(line)

        if line_without_comment.startswith("base_tax") and base_tax_tuple == ():
            tokens = line_without_comment.replace(' ', '').split('=', 1)
            base_tax = int(tokens[1])
            base_tax_tuple = (i, base_tax)

        if line_without_comment.startswith("base_production") and base_production_tuple == ():
            tokens = line_without_comment.replace(' ', '').split('=', 1)
            base_production = int(tokens[1])
            base_production_tuple = (i, base_production)
        
        if line_without_comment.startswith("is_city"):
            if line_without_comment.replace(' ', '').split('=', 1)[1] == 'yes':
                is_city = True

    if not is_city:
        return


    tax_line, base_tax = base_tax_tuple

    if base_tax % 2 == 0:
        new_tax = int(base_tax/2) + base_tax
    else:
        if int(province_file.split("-", 1)[0].rstrip()) % 2 != 0:
            new_tax = int((base_tax+1)/2) + base_tax
        else:
            new_tax = int((base_tax-1)/2) + base_tax
    

    production_line, base_production = base_production_tuple

    if base_production % 2 == 0:
        new_production = int(base_production/2)
    else:
        if int(province_file.split("-", 1)[0].rstrip()) % 2 == 0:
            new_production = int((base_production+1)/2)
        else:
            new_production = int((base_production-1)/2)
    
    
    lines[tax_line] = lines[tax_line].replace(str(base_tax), str(new_tax), 1)
    
    lines[production_line] = lines[production_line].replace(str(base_production), str(new_production), 1)

    with open(MOD_PATH + "\\" + province_file, 'w') as f:
        f.writelines(lines)


def double_production(province_file):
    with open(PROVINCES_PATH + '\\' + province_file) as f:
        lines = f.read().splitlines(True)

    base_production_tuple = ()
    
    is_city = False
    for i, line in enumerate(lines):
        line_without_comment = remove_comment(line)

        if line_without_comment.startswith("base_production") and base_production_tuple == ():
            tokens = line_without_comment.replace(' ', '').split('=', 1)
            base_production = int(tokens[1])
            base_production_tuple = (i, base_production)
        
        if line_without_comment.startswith("is_city"):
            if line_without_comment.replace(' ', '').split('=', 1)[1] == 'yes':
                is_city = True

    if not is_city:
        return
    
    production_line, base_production = base_production_tuple

    new_production = int(base_production * 2)

    lines[production_line] = lines[production_line].replace(str(base_production), str(new_production), 1)

    with open(MOD_PATH + "\\" + province_file, 'w') as f:
        f.writelines(lines)


def main():
    
    continent_lines = get_continent_lines()

    europe_province_numbers = get_province_numbers(continent_lines, "europe")
    asia_province_numbers = get_province_numbers(continent_lines, "asia")

    europe_province_files = get_province_files(europe_province_numbers)
    asia_province_files = get_province_files(asia_province_numbers)

    for f in europe_province_files:
        half_production_and_add_half_tax(f)

    for f in asia_province_files:
        double_production(f)


if __name__ == '__main__':
    main()
