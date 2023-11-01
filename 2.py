import re

# Define regular expressions for different token types
keyword_pattern = re.compile(r'def|int|if|else|write_console|max|min|abs|print|len')  # 3
constant_pattern = re.compile(r'\d+(\.\d+)?')  # 2
operator_pattern = re.compile(r'==|>|\.')  # 4
delimiter_pattern = re.compile(r'[(),\[\].]')  # 4 (Added comma ,)
string_literal_pattern = re.compile(r'"[^"]*"')  # 5

python_builtin_functions = ["max", "min", "abs", "print", "len"]

# Define the SymbolTable class

class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, key, value):
        if key not in self.table:
            # If the key doesn't exist, create a new list with the (token, position) pair
            self.table[key] = [(value[0], value[1])]
        else:
            # If the key already exists, append the (token, position) pair to the list
            self.table[key].append((value[0], value[1]))

    def __getitem__(self, key):
        return self.table[key]

    def __contains__(self, key):
        return key in self.table

    def __str__(self):
        return str(self.table)


symbol_table = SymbolTable()
fip_table = []

current_position = 1

def hash_function(token):
    # For simplicity, we'll use Python's built-in hash function
    return hash(token)


def add_token_to_symbol_table(token):
    global current_position
    hash_value = hash_function(token)

    if hash_value not in symbol_table:
        symbol_table.add(hash_value, (token, current_position))
        current_position += 1
    else:
        symbol_table.add(hash_value, (token, current_position))


def add_token_to_fip(code):
    global current_position
    if code == 0 or code == 2:
        fip_table.append((code, current_position))
    else:
        fip_table.append((code, ""))

def is_python_builtin_function(token):
    return token in python_builtin_functions

def lexical_analysis(source_code):
    i = 0

    while i < len(source_code):
        char = source_code[i]

        if char.isalpha() or char == '_':
            token = ""
            while i < len(source_code) and (char.isalnum() or char == '_'):
                token += char
                i += 1
                if i < len(source_code):
                    char = source_code[i]

            if is_python_builtin_function(token):
                add_token_to_fip(3)  # Use code 3 for keywords
            else:
                if len(token) > 13:
                    print_red(f"Eroare: Identificatorul are lungimea > 13 '{token}' la poziția {i}.")
                    return
                else:
                    add_token_to_symbol_table(token)
                    add_token_to_fip(0)

        elif char.isdigit() or char == '-':
            token = ""
            while i < len(source_code) and (char.isdigit() or char == '-'):
                token += char
                i += 1
                if i < len(source_code):
                    char = source_code[i]

            if constant_pattern.match(token):
                add_token_to_symbol_table(token)
                add_token_to_fip(2)  # Use code 2 for constants
            else:
                print_red(f"Eroare: Constantă nevalidă '{token}' la poziția {i}.")
                return

        elif char in "+-*/=><(){}.,":
            token = char
            i += 1
            add_token_to_fip(4)

        elif char in '[]':
            token = char
            i += 1
            add_token_to_fip(4)  # You may want to define a different code for '[' and ']' in your language

        elif char == ';':
            print_red(f"Eroare: Caracterul ';' nu este permis la poziția {i}.")
            return

        elif char == "\n" or char.isspace():
            i += 1

        elif char == '"':
            match = string_literal_pattern.match(source_code[i:])
            if match:
                token = match.group(0)
                add_token_to_fip(5)
                i += len(token)

        else:
            print_red(f"Eroare: Caracter necunoscut '{char}' la poziția {i}.")
            return

    return fip_table


def print_fip(output_file):
    with open(output_file, 'w') as file:
        file.write("Cod atom | Pozitie in TS\n")
        for code, atom in fip_table:
            file.write(f"{code}   | {atom}\n")

def read_source_code(input_file):
    with open(input_file, 'r') as file:
        source_code = file.read()
    return source_code

def print_red(text):
    red = "\033[91m"
    reset = "\033[0m"
    print(f"{red}{text}{reset}")

input_file = "p2.txt"
output_fip_file = "output_fip.txt"

source_code = read_source_code(input_file)

lexical_analysis(source_code)
print_fip(output_fip_file)


