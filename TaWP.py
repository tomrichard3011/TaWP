import argparse
import itertools
import time
import tempfile
from random import choice

"""
TaWP - Targeted - Wordlist - Project

Takes biographical information and creates a wordlist
"""
"""
TODO:
Main-Issue:
Algorithm can generated passwords, but it's kind of hard to check if it did it correctly. We need to build some test cases.
This is designed to have output similar to the original, but note that the lists with larger leet and strings can be very long.
Perhaps there's a way to cut this down.

Sub-Issues:
cart_prod and chunk_cart_prod follow strange rules in mixing up the characters. Some teaks were made, but more needs to be done.
File writing is inefficient (last step is copying file from temp). This is done to make switching the order of functions easier, but not faster.
Algorithm could be better optimized, namely to avoid repeats. Check at end is performed to prevent consecutive repeats, but slows down and doesn't check everything
Algorithm behaves strangely towards the minimum string size. Most end up towards the upper end, likely due to cart_prod and chunk_cart_prod
Passwords generated don't always abide by the rules of passwords (Needs at least one upper, lower, digit, special char, etc.)
Variable scope can be complicated, consider revising functions. EDIT: Scope improved, but still weird

Note that portions of the code are commented out instead of out-right deleted. This is meant to make reviewing the code easier.
It should be deleted upon review. (Note that old code can be restored with git).
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
# leet transformation dictionaries
leet_1 = {
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
    return string.isalpha()

def alpha_only(string):
    '''
    Returns a string with only alphabetical characters
    @param <string> string: The string that's being checked
    return: The string with only alphabetical characters
    '''
    # Treat the string as a list and remove the non-alphabetical characters O(n)
    test_str = ''
    for c in string:
        if(c.isalpha()):
            test_str += c
    return test_str

# dob validity check
def date_check(date):
    '''
    Checks if date string is valid (numerically, not logically)
    @param <string> date: The string to be checked
    return: True if valid, false if not
    '''

    # Check length first
    if len(date) != 10:
        return False

    # Check if the correct format is used
    filter_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    format = iter('XX/XX/XXXX')
    date_iter = iter(date)
    for i in range(10):
        if(next(format) == '/'):
            if(next(date_iter) != '/'):
                return False
        else:
            if not (next(date_iter) in filter_list):
                return False
    return True

# character replace, return array with words with each possible combination - transformation accepts tuple with char as key and array value
def char_transform(string, transformation, min_val, max_val):
    '''
    Creates a list of all leet code variations
    @param <str> string: The word be converted to leet
    @param <dict><str:str> transformation: The dictionary guide for converting to leet
    '''
    
    # Early escape if there is no leet level
    if not transformation:
        return [string]
    
    # turn string into array
    char = list(string)
    new_list = []
    if len(string) > 8 and transformation == leet_3:
        ''' This function references values outside of its scope: leet_3.'''
        # TODO: Fix this condition and possibly this limit
        print("Name is too long for this leet level!")
        exit()
    # relate char to leet equivalent in map
    for j in range(len(string)):
        if char[j] in transformation:
            char[j] = transformation[char[j]]
    # find the cartesian product
    for t in itertools.product(*char):
        new_word = ("".join(list(t)))
        if int(min_val) <= len(new_word) <= int(max_val):
            # This comparison is weird, you're cutting before you need to cut it.
            new_list.append(new_word)
    return new_list

def cart_prod_helper(array_storage, chunk_size=20, min_val=6, max_val=8):
    """
    Take a tempfile and returns the cartesian product in another tempfile
    
    Since array can be indefinitely large, tempfiles are used to store the
    array and the product it creates. The input file is destroyed afterwards,
    so the original is not safe for threading. Larger chunk sizes lead to faster
    runtimes, at the cost of more memory. Feel free to modify it, but be careful.
    
    @param TemporaryFile array_storage: The word_array made into temp file
    @param int chunk_size: The size of the array for cartesian multiplication (i.e. String[chunk_size] x String[chunk_size])
    @param int min_val: The minimum size of the password generated
    @param int max_val: The maximum size of the password generated
    @return TemporaryFile: The product array with all the words
    """
    # Prep for new cart prod method
    all_combinations = tempfile.TemporaryFile(mode="r+t")
    line_num = 0
    index = -1
    chunk = []
    array_storage.seek(0)
    
    while index < array_storage.tell():
        # Track where we are in the file
        index = array_storage.tell()
        chunk.append(array_storage.readline()[:-1])
        # Once we meet the chunk size, then iterate over the whole file
        if len(chunk) >= chunk_size:
            # Go through and take the product
            prev = array_storage.tell()
            array_storage.seek(0)
            sec_chunk = []
            
            # Get another chunk from the file
            for line in array_storage:
                sec_chunk.append(line[:-1])
                if len(sec_chunk) >= chunk_size:
                    sec_chunk = chunk_cart_prod(chunk, sec_chunk, min_val, max_val)
                    for part in sec_chunk:
                        all_combinations.write(part + "\n")
                    sec_chunk = []
            # If the chunk isn't empty at the end, then add it to the all_comb
            if len(sec_chunk) > 0:
                sec_chunk = chunk_cart_prod(chunk, sec_chunk, min_val, max_val)
                for part in sec_chunk:
                    all_combinations.write(part + "\n")
            # Prepare to return
            array_storage.seek(prev)
            line_num = 0
    
    # If the chunk isn't empty at the end, then add it to the all_comb
    if len(chunk) > 0:
        # Get another chunk from the file
        array_storage.seek(0)
        sec_chunk = []
        for line in array_storage:
            sec_chunk.append(line[:-1])
            if len(sec_chunk) >= chunk_size:
                sec_chunk = chunk_cart_prod(chunk, sec_chunk, min_val, max_val)
                for part in sec_chunk:
                    all_combinations.write(part + "\n")
                sec_chunk = []
        # If the chunk isn't empty at the end, then add it to the all_comb
        if len(sec_chunk) > 0:
            sec_chunk = chunk_cart_prod(chunk, sec_chunk, min_val, max_val)
            for part in sec_chunk:
                all_combinations.write(part + "\n")
    
    # Finally done, destroy original temp and return original
    array_storage.close()
    return all_combinations

# cartesian product of array of arrays
def cart_prod(arr, min_val, max_val):
    new_list = []
    temp_list = [arr, arr]
    # This part is eating a lot of memory, you're keeping two copies of an array
    # For long lists, this is likely where the memory issue stems from
    for t in itertools.product(*temp_list):
        new_word = ("".join(list(t)))
        if len(new_word) < int(min_val):
            new_list.append(new_word)
            continue
        elif len(new_word) >= int(max_val):
            '''Wouldn't this be creating duplicates if the beginning is the same?'''
            new_list.append(new_word[:int(max_val)])
        else:
            new_list.append(new_word)
    return new_list

def chunk_cart_prod(chunk, file_chunk, min_val, max_val):
    '''Used for cartesian products over chunks'''
    new_list = []
    temp_list = [chunk, file_chunk]
    for t in itertools.product(*temp_list):
        new_word = ("".join(list(t)))
        if len(new_word) < int(min_val):
            # Opting to add smaller words as they can become larger words later
            new_list.append(new_word)
            continue
        elif len(new_word) >= int(max_val):
            new_list.append(new_word[:int(max_val)])
        else:
            new_list.append(new_word)
    return new_list

def dob_transform(num_array, min_val, max_val):
    temp = [""]
    for num in num_array:
        temp.append(num)
        temp.append(num[::-1])
    temp = cart_prod(temp, min_val, max_val)
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

# Header fix, prevents error when trying to load without charmap
repeat = True
while repeat:
    try:
        label = choice(header)
        print(label)
        repeat = False
    except UnicodeEncodeError:
        header.remove(label)
        repeat = True
print(choice(label))
print("")

# fill out basic info if not filled in arguments
if not fname:
    fname = input('Enter first name: ')
    # Exiting early, helps with debugging
    if not fname:
        exit()
if not lname:
    lname = input('Enter Surname: ')
if not dob:
    dob = input('Enter date of birth MM/DD/YYYY: ')
if not info:
    info = input('Enter any extra words separated by a comma: ')
if leet_num == 0:
    leet_num = int(input("Enter leet level, 0 for none, 3 is max (may cause memory issues). 2 is suggested: "))
    while leet_num < 0 or leet_num > 3:
        leet_num = int(input("Invalid leet level, enter a number between 0 and 3: "))
if not args.min:
    args.min = input("Enter minimum character length: ")
    if args.min == "":
        args.min = 6
    min_val = int(args.min)
if not args.max:
    args.max = input("Enter maximum character length: ")
    if args.max == "":
        args.max = 13
    max_val = int(args.max)

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
if not date_check(dob):
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
word_array = cart_prod(word_array, min_val, max_val)
word_array = list(set(word_array))
# reverse and cart_product of date, filter number, and filter unique values
word_array.extend(set(filter(lambda x: x != "", dob_transform(dob.split("/"), min_val, max_val))))
# Make the first temp file for handling long arrays
array_storage = tempfile.TemporaryFile("r+t")
for word in word_array:
    array_storage.write(word + "\n")
# handle extra words, if digit string is present, will flip the digits as well
extras = info.replace(" ", "").split(",")
for i in range(len(extras)):
    array_storage.write(extras[i] + "\n")
    if extras[i].isdigit():
        array_storage.write(extras[i][::-1] + "\n")
print("List of words built, now getting combinations")
# word_array.extend(extras)

# Early exit, testing only. Uncomment to see what I mean.
# print(word_array)
# exit()

# New early exit
#array_storage.seek(0)
#for line in array_storage:
#    print(line, end="")
#exit()

"""
Order of operations is being changed.
Original: Leet swap => Case swap => Cartesian product => File write
New: Cartesian product => Leet swap => Case Swap => File write

Both should have the same result. The cartesian product is done earlier to
reduce computational need, especially since the combinations are going to 
be the same pretty much throughout. I don't see too much wrong with this
approach, but if I'm incorrect, please let me know. -NG
"""

# Regular cartesian product as a tempfile
array_storage.seek(0)
word_comb = cart_prod_helper(array_storage, 20, min_val, max_val)
print("List of combinations built. Now translating to leet")

# Check to see if word_comb is working
#word_comb.seek(0)
#for line in word_comb:
#    print(line, end="")
#exit()

# Leet swap
leet_list = tempfile.TemporaryFile("r+t")
word_comb.seek(0)
for line in word_comb:
    leet_variants = char_transform(line[:-1], leet_set, min_val, max_val)
    for variant in leet_variants:
        leet_list.write(variant + "\n")
word_comb.close()
print("Leet list translated. Now transforming cases")

# Check to see if leet_list is working
#leet_list.seek(0)
#for line in leet_list:
#    print(line, end="")
#exit()

# Case swap
case_list = tempfile.TemporaryFile("r+t")
leet_list.seek(0)
previous = ""
for line in leet_list:
    case_variants = char_transform(line[:-1], case_set, min_val, max_val)
    for variant in case_variants:
        if variant != previous:
            case_list.write(variant + "\n")
        previous = variant
leet_list.close()
print("Cases finalized. Proceeding to save list...")

# Check to see if case_list is working
# case_list.seek(0)
# for line in case_list:
    # print(line, end="")
# exit()

'''
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
word_array = cart_prod(word_array, min_val, max_val)

# filter out empty strings and uniques
# This handles duplicates, but can waste quite a bit of memory and some time
word_array = set(filter(lambda x: x != "", word_array))
'''

# write to file
if not filename:
    filename = fname + lname + "_wordlist.txt"

# create file with write permissions
file = open(filename, "w+")

# Copy the temp file
# Note that this could be optimized, but it should do for now
case_list.seek(0)
for line in case_list:
    if min_val <= len(line[:-1]) and len(line[:-1]) <= max_val:
        file.write(line)
file.close()

'''
# write each word from array to file
for word in word_array:
    file.write(word + "\r\n")
file.close()
'''

print("It took {:.3f} seconds to generate a wordlist of length {}".format((time.time() - start_time), len(word_array)))
print("New file created in present directory: " + filename)
