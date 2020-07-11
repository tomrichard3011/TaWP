import itertools, tempfile

"""
This file was where I tested the alogrithms in isolation. I considered
removing them from the directory, but I thought it was worth sharing
to help with testing. NG
"""

max_val = 10
min_val = 8

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

def main():
    # Generate the temp file
    array_storage = tempfile.TemporaryFile(mode="r+t")
    # Generate list of words
    words = ["hear"]
    # Add words to temp file
    for word in words:
        current_word = word_generate(word, 12)
        for variant in current_word:
            # print(variant)
            array_storage.write(variant + "\n")
    
    # Use readline to access the elements
    # Combine all the words together
    word_comb = ng_cart_prod_helper(array_storage, chunk_size=20, min_val=4, max_val=6)
    word_comb.seek(0)
    for line in word_comb:
        print(line, end="")
    word_comb.seek(0)
    print("----------------------------------------")
    
    # Covert to leet
    transformation = leet_2
    leet_temp = tempfile.TemporaryFile(mode="r+t")
    for line in word_comb:
        word_list = char_transform(line[:-2], transformation, 4, 6)
        for word in word_list:
            leet_temp.write(word + "\n")
    word_comb.close()
    leet_temp.seek(0)
    
    # Check to see if the file came out as desired
    for line in leet_temp:
        print(line, end="")
        
    # Final conversion for capitals and lowercase
    
# Consider removing
def word_generate(word, max_val):
    # Create a list of word variations
    size = len(word)
    result = []
    for i in range(size):
        if size - i <= max_val:
            #print(word[i:size])
            #print(word[0:size - i])
            result.append(word[i:size])
            result.append(word[0:size - i])
            result.append(rev(word[i:size]))
            result.append(rev(word[0:size - i]))
    return set(filter(lambda x: x != "", result))
    
def ng_cart_prod_helper(array_storage, chunk_size=20, min_val=6, max_val=8):
    # Prep for new cart prod method
    all_combinations = tempfile.TemporaryFile(mode="r+t")
    line_num = 0
    index = -1
    chunk = []
    array_storage.seek(0)
    
    # While the line keeps moving down
    while index < array_storage.tell():
        # Track where we are in the file
        index = array_storage.tell()
        # We have to go through and read the lines
        chunk.append(array_storage.readline()[:-2])
        # Once we meet the chunk size, then iterate over the whole file
        if len(chunk) >= chunk_size:
            # Go through and take the product
            prev = array_storage.tell()
            array_storage.seek(0)
            sec_chunk = []
            
            # Get another chunk from the file
            for line in array_storage:
                sec_chunk.append(line[:-2])
                if len(sec_chunk) >= chunk_size:
                    sec_chunk = ng_cart_prod(chunk, sec_chunk, min_val, max_val)
                    for part in sec_chunk:
                        all_combinations.write(part + "\n")
                    sec_chunk = []
            # If the chunk isn't empty at the end, then add it to the all_comb
            if len(sec_chunk) > 0:
                sec_chunk = ng_cart_prod(chunk, sec_chunk, min_val, max_val)
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
            sec_chunk.append(line[:-2])
            if len(sec_chunk) >= chunk_size:
                sec_chunk = ng_cart_prod(chunk, sec_chunk, min_val, max_val)
                for part in sec_chunk:
                    all_combinations.write(part + "\n")
                sec_chunk = []
        # If the chunk isn't empty at the end, then add it to the all_comb
        if len(sec_chunk) > 0:
            sec_chunk = ng_cart_prod(chunk, sec_chunk, min_val, max_val)
            for part in sec_chunk:
                all_combinations.write(part + "\n")
    
    # Finally done, destroy original temp and return original
    array_storage.close()
    return all_combinations
    

def rev(word):
    return word[::-1]

# character replace, return array with words with each possible combination - transformation accepts tuple with char as key and array value
def char_transform(string, transformation, min_val, max_val):
    '''
    TODO: What is even happening here?
    '''
    
    # turn string into array
    char = list(string)
    new_list = []
    
    '''
    if len(string) > 8 and transformation == leet_3:
        # This function references values outside of its scope: leet_3
        print("Name is too long for this leet level!")
        exit()
    '''
    # relate char to leet equivalent in map
    # print(char)
    # print("-----------------")
    for j in range(len(string)):
        if char[j] in transformation:
            char[j] = transformation[char[j]]
    # print(char)
    # print("-----------------")
    # find the cartesian product
    for t in itertools.product(*char):
        new_word = ("".join(list(t)))
        if int(min_val) <= len(new_word) <= int(max_val):
            '''This function references values outside of its scope: args'''
            new_list.append(new_word)
    return new_list

# cartesian product of array of arrays
def cart_prod(arr):
    min = 4
    max = 6
    new_list = []
    temp_list = [arr, arr]
    # This part is eating a lot of memory, you're keeping two copies of an array
    # For long lists, this is likely where the memory issue stems from
    for t in itertools.product(*temp_list):
        print(t)
        new_word = ("".join(list(t)))
        if len(new_word) < int(min):
            continue
        elif len(new_word) >= int(max):
            new_list.append(new_word[:int(max)])
        else:
            new_list.append(new_word)
    return new_list
    
# cartesian product of array of arrays
def ng_cart_prod(chunk, file_chunk, min_val, max_val):
    new_list = []
    temp_list = [chunk, file_chunk]
    # This part is eating a lot of memory, you're keeping two copies of an array
    # For long lists, this is likely where the memory issue stems from
    for t in itertools.product(*temp_list):
        # print(t)
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
    
# print(char_transform(input("Please enter a string here: "), leet_2))
# print(cart_prod(["", "nick", "guer"]))
main()

