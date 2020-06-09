import argparse
import itertools
import time
from random import choice
from typing import Dict, List

"""
TaWP - Targeted - Wordlist - Project

Takes biographical information and creates a wordlist
"""
#############################################################################################################
# case transformation definitions
#############################################################################################################
case_set = {
    'a': ['a', 'A'],
    'b': ['b', 'B'],
    'c': ['c', 'C'],
    'd': ['d', 'D'],
    'e': ['e', 'E'],
    'f': ['f', 'F'],
    'g': ['g', 'G'],
    'h': ['h', 'H'],
    'i': ['i', 'I'],
    'j': ['j', 'J'],
    'k': ['k', 'K'],
    'l': ['l', 'L'],
    'm': ['m', 'M'],
    'n': ['n', 'N'],
    'o': ['o', 'O'],
    'p': ['p', 'P'],
    'q': ['q', 'Q'],
    'r': ['r', 'R'],
    's': ['s', 'S'],
    't': ['t', 'T'],
    'u': ['u', 'U'],
    'v': ['v', 'V'],
    'w': ['w', 'W'],
    'x': ['x', 'X'],
    'y': ['y', 'Y'],
    'z': ['z', 'Z'],
}
# leet transformation tuples
leet_1: Dict[str, List[str]] = {
    'a': ['a', '4'],
    'e': ['e', '3'],
    'i': ['i', '1'],
    'o': ['o', '0'],
    'u': ['u', '(_)']
}
leet_2 = {
    'a': ['a', '4', '@'],
    'b': ['b', '8', '13', '6'],
    'e': ['e', '3'],
    'f': ['f', 'ph'],
    'g': ['g', '6', '9'],
    'h': ['h', '#'],
    'i': ['i', '1', '!'],
    'l': ['l', '1', '7'],
    'o': ['o', '0'],
    's': ['s', '5', '$', 'z'],
    't': ['t', '7']
}
leet_3 = {
    'a': ['a', '4', '/\\', '@', '/-\\', '^', 'aye', '(L'],
    'b': ['b', 'I3', '8', '13', '| 3', 'ß', '!3', '(3', '/3', ')3', '|-]', 'j3', '6'],
    'c': ['c', '{', '<', '('],
    'd': ['d', ')', '|)', '(|', '[)', 'I>', '|>', '?', 'T)', 'I7', 'cl', '|}', '>', '|]'],
    'e': ['e', '3', '&', '[-', '|=-'],
    'f': ['f', '|=', '|#', 'ph', '/=', 'v'],
    'g': ['g', '&', '6', '(_+', '9', 'C-', 'gee', '(?,', '[,', '{,', '<-', '(.'],
    'h': ['h', '#', '/-/', '[-]', ']-[', ')-(', '(-)', ':-:', '|~|', '|-|', ']~[', '}{', '!-!', '1-1', '\\-/', 'I+I', '/-\\'],
    'i': ['i', '1', '[]', '|', '!', 'eye', '3y3', ']['],
    'j': ['j', ',_|', '_|', '._|', '._]', '_]', ',_]', ']', ';', '1'],
    'k': ['k', '>|', '|<', '/<', '1<', '|c', '|(', '|{', ],
    'l': ['l', '1', '7', '|_', '|'],
    'm': ['m', '/\\/\\', '/V\\', 'JVI', '[V]', '[]V[]', '|\\/|', '^^', '<\\/>', '{V}', '(v)', '(V)', '|V|', 'nn', 'IVI', '|\\|\\', ']\\/[', '1^1', 'ITI', 'JTI'],
    'n': ['n', '^/', '|\\|', '/\\/', '[\\]', '<\\>', '{\\}', '|V', '/V', '^'],
    'o': ['o', '0', 'Q', '()', 'oh', '[]', 'p', '<>'],
    'p': ['p', '|*', '|o', '?', '|^', '|>', '|"', '9', '[]D', '|7'],
    'q': ['q', '(_,)', '9', '()_', '2', '0_', '<|', '&'],
    'r': ['r', 'I2', '|`', '|~', '|?', '/2', '|^', 'lz', '|9', '2', '12', '[z', '.-', '|2', '|-'],
    's': ['s', '5', '$', 'z', 'ehs', 'es', '2'],
    't': ['t', '7', '+', '-|-', '\'][\'', '"|"', '~|~'],
    'u': ['u', '(_)', '|_|', 'v', 'L|'],
    'v': ['v', '\\/', '|/', '\\|'],
    'w': ['w', '\\/\\/', 'VV', '\\N', '\'//', '\\\\\'', '\\^/', '(n)', '\\V/', '\\X/', '\\|/', '\\_|_/', '\\_:_/', 'uu', '2u', '\\\\//\\\\//'],
    'x': ['x', '><', '}{', 'ecks', '×', '?', ')(', ']['],
    'y': ['y', 'j', '`/', '7', '\\|/', '\\//'],
    'z': ['z', '2', '7_', '-/_', '%', '>_', 's', '~/_', '-\\_', '-|_']
}

#############################################################################################################
# header array - holds different ascii art headers
#############################################################################################################

header = [("""\u001b[37m
__\u001b[36m/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\u001b[37m___________________\u001b[36m/\\\\\\\u001b[37m______________\u001b[36m/\\\\\\\u001b[37m___\u001b[36m/\\\\\\\\\\\\\\\\\\\\\\\\\\\u001b[37m___        
 _\u001b[36m\\///////\\\\\\/////\u001b[37m___________________\u001b[36m\\/\\\\\\\u001b[37m_____________\u001b[36m\\/\\\\\\\u001b[37m__\u001b[36m\\/\\\\\\/////////\\\\\\\u001b[37m_       
  _______\u001b[36m\\/\\\\\\\u001b[37m________________________\u001b[36m\\/\\\\\\\u001b[37m_____________\u001b[36m\\/\\\\\\\u001b[37m__\u001b[36m\\/\\\\\\\u001b[37m_______\u001b[36m\\/\\\\\\\u001b[37m_      
   _______\u001b[36m\\/\\\\\\\u001b[37m_________\u001b[36m/\\\\\\\\\\\\\\\\\\\u001b[37m_____\u001b[36m\\//\\\\\\\u001b[37m____\u001b[36m/\\\\\\\u001b[37m____\u001b[36m/\\\\\\\u001b[37m___\u001b[36m\\/\\\\\\\\\\\\\\\\\\\\\\\\\\/\u001b[37m__     
    _______\u001b[36m\\/\\\\\\\u001b[37m________\u001b[36m\\////////\\\\\\\u001b[37m_____\u001b[36m\\//\\\\\\\u001b[37m__\u001b[36m/\\\\\\\\\\\u001b[37m__\u001b[36m/\\\\\\\u001b[37m____\u001b[36m\\/\\\\\\/////////\u001b[37m____    
     _______\u001b[36m\\/\\\\\\\u001b[37m__________\u001b[36m/\\\\\\\\\\\\\\\\\\\\\u001b[37m_____\u001b[36m\\//\\\\\\/\\\\\\/\\\\\\/\\\\\\\u001b[37m_____\u001b[36m\\/\\\\\\\u001b[37m_____________   
      _______\u001b[36m\\/\\\\\\\u001b[37m_________\u001b[36m/\\\\\\/////\\\\\\\u001b[37m______\u001b[36m\\//\\\\\\\\\\\\//\\\\\\\\\\\u001b[37m______\u001b[36m\\/\\\\\\\u001b[37m_____________  
       _______\u001b[36m\\/\\\\\\\u001b[37m________\u001b[36m\\//\\\\\\\\\\\\\\\\/\\\\\u001b[37m______\u001b[36m\\//\\\\\\\u001b[37m__\u001b[36m\\//\\\\\\\u001b[37m_______\u001b[36m\\/\\\\\\\u001b[37m_____________ 
        _______\u001b[36m\\///\u001b[37m__________\u001b[36m\\////////\\//\u001b[37m________\u001b[36m\\///\u001b[37m____\u001b[36m\\///\u001b[37m________\u001b[36m\\///\u001b[37m______________
"""), "\u001b[35m" + """
    ███        ▄████████  ▄█     █▄     ▄███████▄ 
▀█████████▄   ███    ███ ███     ███   ███    ███ 
   ▀███▀▀██   ███    ███ ███     ███   ███    ███ 
    ███   ▀   ███    ███ ███     ███   ███    ███ 
    ███     ▀███████████ ███     ███ ▀█████████▀  
    ███       ███    ███ ███     ███   ███        
    ███       ███    ███ ███ ▄█▄ ███   ███        
   ▄████▀     ███    █▀   ▀███▀███▀   ▄████▀      
""" + "\u001b[0m", "\u001b[31m" + """
▄▄▄█████▓ ▄▄▄       █     █░ ██▓███  
▓  ██▒ ▓▒▒████▄    ▓█░ █ ░█░▓██░  ██▒
▒ ▓██░ ▒░▒██  ▀█▄  ▒█░ █ ░█ ▓██░ ██▓▒
░ ▓██▓ ░ ░██▄▄▄▄██ ░█░ █ ░█ ▒██▄█▓▒ ▒
  ▒██▒ ░  ▓█   ▓██▒░░██▒██▓ ▒██▒ ░  ░
  ▒ ░░    ▒▒   ▓▒█░░ ▓░▒ ▒  ▒▓▒░ ░  ░
    ░      ▒   ▒▒ ░  ▒ ░ ░  ░▒ ░     
  ░        ░   ▒     ░   ░  ░░       
               ░  ░    ░             
""" + "\u001b[0m", "\u001b[33m" + """
 _____       _    _ ______ 
|_   _|     | |  | || ___ \\
  | |  __ _ | |  | || |_/ /
  | | / _` || |/\\| ||  __/ 
  | || (_| |\\  /\\  /| |    
  \\_/ \\__,_| \\/  \\/ \\_|                                           
""" + "\u001b[0m", """
_        ______  _____    ____    _     ___\u001b[34m
(__    __)    /  \\    |  |    |  | |    \\  
   |  |      /    \\   |  |    |  | |     ) 
   |  |     /  ()  \\  |  |    |  | |  __/  
   |  |    |   __   |  \\  \\/\\/  /  | |   \u001b[0m  
___\u001b[34m|  |\u001b[0m____\u001b[34m|  (\u001b[0m__\u001b[34m)  |\u001b[0m___\u001b[34m\\      /\u001b[0m___\u001b[34m| |\u001b[0m_____
""", "\u001b[32m" + """                            
@@@@@@@   @@@@@@   @@@  @@@  @@@  @@@@@@@   
@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@@@@@@  
  @@!    @@!  @@@  @@!  @@!  @@!  @@!  @@@  
  !@!    !@!  @!@  !@!  !@!  !@!  !@!  @!@  
  @!!    @!@!@!@!  @!!  !!@  @!@  @!@@!@!   
  !!!    !!!@!!!!  !@!  !!!  !@!  !!@!!!    
  !!:    !!:  !!!  !!:  !!:  !!:  !!:       
  :!:    :!:  !:!  :!:  :!:  :!:  :!:       
   ::    ::   :::   :::: :: :::    ::       
   :      :   : :    :: :  : :     :        
""" + "\u001b[0m", "\u001b[37m" + """
 ____  ____  ____  ____ 
||T ||||A ||||W ||||P ||
||__||||__||||__||||__||
|/__\\||/__\\||/__\\||/__\\|
""", "\u001b[34m" + """
████████╗ █████╗ ██╗    ██╗██████╗ 
╚══██╔══╝██╔══██╗██║    ██║██╔══██╗
   ██║   ███████║██║ █╗ ██║██████╔╝
   ██║   ██╔══██║██║███╗██║██╔═══╝ 
   ██║   ██║  ██║╚███╔███╔╝██║     
   ╚═╝   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝     
""" + "\u001b[0m", """\u001b[31m                                   
                            \u001b[31m_________   _...._      
               \u001b[33m      _     _\u001b[31m\\        |.'      '-.   
\u001b[35m     .|        \u001b[33m/\\    \\\\   // \u001b[31m\\        .'```'.    '. 
\u001b[35m   .' |_     \u001b[34m__\u001b[33m`\\\\  //\\\\ //   \u001b[31m\\      |       \\     \\
\u001b[35m .'     | \u001b[34m.:--.'.\u001b[33m\\`//  \\'/     \u001b[31m|     |        |    |
\u001b[35m'--.  .-'\u001b[34m/ |   \\ |\u001b[33m\\|   |/      \u001b[31m|      \\      /    . 
\u001b[35m   |  |  \u001b[34m`" __ | | \u001b[33m'           \u001b[31m|     |\\`'-.-'   .'  
\u001b[35m   |  |   \u001b[34m.'.''| |             \u001b[31m|     | '-....-'`    
\u001b[35m   |  '. \u001b[34m/ /   | |_           \u001b[31m.'     '.             
\u001b[35m   |   / \u001b[34m\\ \\._,\\ '/         \u001b[31m'-----------'           
\u001b[35m   `'-'   \u001b[34m`--'  `"                                  
\u001b[0m
"""]


#############################################################################################################
# Functions
#############################################################################################################
# alpha validity check
def alpha_check(string):
    test_str = ''.join(filter(str.isalpha, string))
    return test_str


# dob validity check
def num_check(num):
    filter_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/']
    test_str = ''.join(filter(lambda k: k not in filter_list, dob))
    if len(num) != 10:
        return True
    return str(test_str)


# character replace, return array with words with each possible combination - transformation accepts tuple with char as key and array value
def char_transform(string, transformation):
    # turn string into array
    char = list(string)
    new_list = []
    if len(string) > 8 and transformation == leet_3:
        print("Name is too long for !")
        exit()
    # relate char to leet equivalent in map
    for j in range(len(string)):
        if char[j] in transformation:
            char[j] = transformation[char[j]]
    # find the cartesian product
    for t in itertools.product(*char):
        new_word = ("".join(list(t)))
        if int(args.min) <= len(new_word) <= int(args.max):
            new_list.append(new_word)
    return new_list


# cartesian product of array of arrays
def cart_prod(arr):
    new_list = []
    temp_list = [arr, arr]
    for t in itertools.product(*temp_list):
        new_word = ("".join(list(t)))
        if int(args.min) <= len(new_word) <= int(args.max):
            new_list.append(new_word)
    return new_list


def dob_transform(num_array):
    temp = [""]
    for num in num_array:
        temp.append(num)
        temp.append(num[::-1])
    temp = cart_prod(temp)
    return temp


#############################################################################################################
# arg parse
#############################################################################################################
parser = argparse.ArgumentParser(description="Takes biographical information and creates a wordlist", epilog="Example: TaWP.py -f john -l doe -d 01/10/2010 -i lakers,basketball,ucla,24 --leet 1 -c -o output.txt -m 6 -M 13")
parser.add_argument("-f", "--first")
parser.add_argument("-s", "--sur")
parser.add_argument("-d", "--dob", help="date of birth - MM/DD/YYYY")
parser.add_argument("-i", "--info", help="Extra info, separated by comma")
parser.add_argument("-m", "--min", help="minimum password length, default is 6")
parser.add_argument("-M", "--max", help="Maximum password length, default is 12")
parser.add_argument("-l", "--leet", help="Enable leet character replacement, max level 3, can run into memory problems on max; 2 provides good coverage", default=0)
parser.add_argument("-c", "--case", help="Disable capitalization substitution", action="store_false", default=True)
parser.add_argument("-o", "--output", help="Output File name")

args = parser.parse_args()

# args to variable translation
fname = args.first
lname = args.sur
dob = args.dob
info = args.info
leet_num = int(args.leet)
case_bool = args.case
filename = args.output

#############################################################################################################
# output
#############################################################################################################

# header - random.choice randomly chooses header
print("Welcome to TaWP")
print(choice(header))
print("")

# fill out basic info if not filled in arguments
if not fname:
    fname = input('Enter first name: ')
if not lname:
    lname = input('Enter Surname: ')
if not dob:
    dob = input('Enter date of birth MM/DD/YYYY: ')
if not info:
    info = input('Enter any extra words separated by a comma: ')
if leet_num == 0:
    leet_num = int(input("Enter leet level, 0 for none, 3 is max (may cause memory issues). 2 is suggested: "))
    while 0 > leet_num > 3:
        leet_num = input("Invalid leet level, enter a number between 0 and 3: ")
if not args.min:
    args.min = input("Enter minimum character length: ")
    if args.min == "":
        args.min = 6
if not args.max:
    args.max = input("Enter maximum character length: ")
    if args.max == "":
        args.max = 13

# set all to lowercase
fname = str.lower(fname)
lname = str.lower(lname)
info = str.lower(info)

# switch statement for setting leet level and set
leet_set = [""]
leet_num = int(leet_num)
if leet_num == 0:
    leet_set = [""]
elif leet_num == 1:
    leet_set = leet_1
elif leet_num == 2:
    leet_set = leet_2
elif leet_num == 3:
    print("leet 3 is most likely to fail due to limited stack space. Only for small amount and short length of terms.")
    leet_set = leet_3
else:
    print("Invalid leet level")
    exit()


#############################################################################################################
# validity checks
#############################################################################################################
if not alpha_check(fname):
    print("Invalid firstname - check alphabetical characters")
    exit()
if not alpha_check(lname):
    print("Invalid surname - Only alphabetical characters")
    exit()
if num_check(dob):
    print("Invalid Date - check format")
    exit()
#############################################################################################################
# Main Program
#############################################################################################################
# mark start time
print("Generating wordlist...")
start_time = time.time()
# cleanup / separate data / join words into array / begin manipulation
word_array = ["", fname, lname]
word_array = cart_prod(word_array)
# reverse and cart_product of date, filter number, and filter unique values
word_array.extend(set(filter(lambda x: x != "", dob_transform(dob.split("/")))))
# handle extra words, if digit string is present, will flip the digits as well
extras = info.replace(" ", "").split(",")
for i in range(len(extras)):
    if extras[i].isdigit():
        extras.append(extras[i][::-1])
word_array.extend(extras)

# leet swap
if leet_num != -1:
    # empty temp_arr
    temp_arr = []
    # for every word, append leet variations
    for word in word_array:
        temp_arr.extend(char_transform(word, leet_set))
    word_array.extend(temp_arr)
# case swap
if case_bool:
    # empty temp_arr
    temp_arr = []
    # for every word, append lowercase and uppercase variations
    for word in word_array:
        temp_arr.extend(char_transform(word, case_set))
    word_array.extend(temp_arr)

# regular cartesian product
word_array = cart_prod(word_array)

# filter out empty strings and uniques
word_array = set(filter(lambda x: x != "", word_array))

# write to file
if not filename:
    filename = fname + lname + "_wordlist.txt"

# create file with write permissions
file = open(filename, "w+")
# write each word from array to file
for word in word_array:
    file.write(word + "\r\n")
file.close()

print("It took {:.3f} seconds to generate a wordlist of length {}".format((time.time() - start_time), len(word_array)))
print("New file created in present directory: " + filename)
