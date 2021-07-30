import itertools
import time
import configparser
import random

# function that creates a new empty crossword
# depending on crossword_size
def new_array():

    default_array =["/"] * crossword_size*crossword_size   

    temp_array = [[] for _ in range(20)] # creates a base for all the crosswords 

    temp_array[0].append(default_array) # the first empty crossword is placed in the first place of temp_array

    return temp_array

# function that given an array prints it in the terminal 
# in a crossword form
def print_array(given_array):        
    x = 0
    y = crossword_size

    while x != crossword_size*crossword_size:
        print(given_array[x:y])  # prints the first line of the crossword of lenght crossword_size
        x = x + crossword_size
        y = y + crossword_size
    print("\n")

# function that places a given word in a crossword vertically
# given the initial position of that word and the crossword
# it should be placed in
def place_vertically(word, i_position, given_array):  # iposition is the coordinate of the first letter in the word
    
    word_len = len(word)
    msg = 0 # in case it gives an error when the word is placed
            # if msg equals none the crossword is aborted

    if i_position + (word_len*crossword_size) <= crossword_size*crossword_size and i_position >= 0: 
        # this is necessary so that the word isn't placed outside of the array 

        letters = []
        for letter in word:
            letters.append(letter)  # all the letters of the word are appended to an array

        counter = 0        # a counter is used insted of a for loop because of indexes
        while counter != word_len : 

            if  given_array[i_position] == letters[counter] or given_array[i_position] == '/':  
            # the letter is placed only if there is an empty space     

                given_array[i_position] = letters[counter]    # the letter is placed 
                i_position = i_position + crossword_size
                
            else:
                msg = 'None'
                
            counter = counter + 1


        if msg != 'None':
            return given_array    

    if msg == 'None':    
        return msg

    # the msg == None thing is here to avoid errors and wrong made crosswords


# function that places a given word in a crossword horizzontally
# given the initial position of that word and the crossword
# it should be placed in
def place_horizzontally(word, i_position, given_array):  # i_position vuol dire posizione della prima lettera nell'array
    
    word_len = len(word) 
    msg = 0 # in case it gives an error when the word is placed
            # if msg equals none the crossword is aborted

    if i_position + word_len - 1 <= (i_position // crossword_size) * crossword_size + crossword_size-1: 
        # this to avoid words placed outside of the array (error) and so that
        # the word isn't split in two lines

        letters = []

        for letter in word:
            letters.append(letter)    # all the letters of the word are appended to an array  
        
        counter = 0  # a counter is used insted of a for loop because of indexes
        
        while counter != word_len :  

            if  given_array[i_position] == letters[counter] or given_array[i_position] == '/':
            # the letter is placed only if there is an empty space

                given_array[i_position] = letters[counter]  # the letter is placed  
                i_position = i_position + 1
                
            else:
                msg = 'None'
                
            counter = counter + 1


        if msg != 'None':
            return given_array   

    if msg == 'None':    
        return msg
    # the msg == None thing is here to avoid errors and wrong made crosswords    
  
# a completely unoptimized function that searches where
# there are similar letters between a word and a crossword
def find_same_letters(array,word): 

    same_letters = []

    letters = []
    for letter in word:
        letters.append(letter)     
    
    letters_len = len(letters)
    counter = 0
    array_counter = 0

    while counter != letters_len:   # brute searches similarities

        while array_counter != crossword_size*crossword_size-1:

            if letters[counter] == array[array_counter]:

                same_letters.append([letters[counter], array_counter, counter ])

            array_counter = array_counter + 1    
        counter = counter + 1 
        array_counter = 0
    
    return same_letters 
    # output example: ['letter of the word','where is that letter equal','position of that letter in the word']

# function that places the first word horizzontally in the empty crossword
# it's possible to delete it and integrate it in main() if necessary
def first_word_place(array,word,all_words):    
    
    word_len = len(word)
    i_position = int(first_word_coord - (word_len/2))   
    # the word is placed in the 'center' of the crossword
    
    array = place_horizzontally(word,i_position,array)
    
    # this is a thing that places symbols before and after the word if it's possible
    # and if it doesn't break any crossword rule like going to the next line or 
    # outside the array
    try:
        if (i_position // crossword_size) * crossword_size != i_position:
            array[i_position-1] = '$'

        if (i_position // crossword_size) * crossword_size + crossword_size-1 != i_position + len(word)-1:  
            array[i_position+len(word)] = '$'
    
    except Exception:
        pass
    
    # exeption handling in case of error 
    if array != 'none' and array != None:   

        # coords is where and how the word is placed
        # in this case is ['position of the word in the list of given words at the beginning',
        # 'position in the array of the first letter of the word','horizzontal or vertical,]
        coords = [all_words.index(word)+1,i_position,"hrz"] 

        return [array,[coords]]
    else:
        print('Error During First Word Place Function, the word is too big')

# function that decides if a word should be placed horizzontally or vertically
def how_to_place(array,coord):              
    
    # basically given a coord in the array it sees if above, below, right and left there is an empty space,
    # all of that considering not going to the next line or outside of the array
    # aka i don't know why it works but it does
    if coord <= crossword_size*crossword_size-2-crossword_size and coord >= crossword_size+1:

        if array[coord+crossword_size+1] == '/'and array[coord+crossword_size-1] == '/' and array[coord-crossword_size-1] == '/'and array[coord-crossword_size+1] == '/':

            if array[coord+1] == '/' or array[coord+1] == '$' and array[coord-1] == '/' or array[coord-1] == '$':
                orientation = "hrz" 
                return orientation
            
            elif array[coord+crossword_size] == '/' or array[coord+crossword_size] == '$' and array[coord-crossword_size] == '/' or array[coord-crossword_size] == '$':
                orientation = "vrt"
                return orientation

            else:
                orientation = "none"    
                return orientation    
    else:
        orientation = "none"    
        return orientation

# a function that is used at the end to sort coordinates
def sortArray(val): 
    return val[0]

# this is the main core that binds together all the other functions to create a finished product
# what is does is that it creates (when there is no how_many_crossword) all the possible crosswords
# with the given words and a given crossword size
# to do this it creates all the possible permutation with the given words and then tries to place 
# them in all the possible ways one by one
# when how_many_crosswords isn't infinite this function creates a user wanted number of crosswords
# it works in a repetitive way, it places the first word, sees for example that the next word can
# be placed in two different ways and it places them, now there are two crossword in which the next
# word can be placed in and so on
# when the last word of a permutation of words is placed in the crossword, that crossword become a 
# finished one and it's appended to the end_crosswords array and then prompted at the end to the user
# during all this procedure the place where the words are placed is also saved with the crossword
def main(all_words,how_many_crosswords):        

    # the longest_word variable is needed in first_word_place() funtion, that's why it's global
    global longest_word 

    # finds the longest word so that in theory because it will be the first one to be placed
    # the overall alghoritm speed will be faster idk
    longest_word = max(all_words, key=len)  

    all_words1 = all_words.copy()

    all_words.remove(longest_word)

    # uncomment this if you want to have different crosswords every time you run the alghorithm
    #random.shuffle(all_words)  

    words_len = len(all_words)          

    # permutations of all the words are created
    permutation = itertools.permutations(all_words)
    
    # how many finished crosswords were created
    end_crosswords_counter = 0

    # if it is necessary to break all the loops because end_crosswords_counter
    # reached how_many_crosswords
    to_break = False

    # a main array is created with at the beginning of it an empry crossword
    temp_crosswords = new_array()
    
    empty_crossword = temp_crosswords[0][0].copy()

    # the longest word of the given words is placed in the middle of the empty crossword
    first_array = first_word_place(empty_crossword, longest_word,all_words1)

    # uncomment if for some reason an error appears
    #first_array.append([])

    # the crossword made with the first word is appended to the skeleton array
    temp_crosswords[1].append(first_array)    

    # for permutation of words
    for words in permutation:

        print(words)
        
        words_counter = 1

        # for every word in the permutation of wprds
        while words_counter != words_len  :  

            # this variable is how many crosswords were created with the precedent word
            last_created_crosswords_len = len(temp_crosswords[words_counter])       

            # variable now resetted
            last_created_crossword = 0
            
            # for every crossword created with the precedent word
            while last_created_crossword != last_created_crosswords_len:    

                # the variable similarity contains where a letter of a word and a crossword are similar
                # so that the script will try to place that word in a way to make those letters combine in a crossword way
                similarity = find_same_letters(temp_crosswords[words_counter][last_created_crossword][0], words[words_counter])
                
                # uncomment for free epilepsy
                #print(similarity)
                
                similarity_len = len(similarity)

                similarity_element = 0  

                # for every simiarity found above
                while  similarity_element != similarity_len :
                    
                    # sees if the word needs to be placed horizzontally or vertically
                    how_to_place_word = how_to_place(temp_crosswords[words_counter][last_created_crossword][0], similarity[similarity_element][1])

                    # a temporary array that is reset every time
                    temp_array = 0
                    where = 0
                    
                    # the previous made crossword is copied 
                    temp_array = temp_crosswords[words_counter][last_created_crossword][0].copy()                  
                    
                    # also the previous made crossword words coordinates are copied
                    where = temp_crosswords[words_counter][last_created_crossword][1].copy()
                    
                    # if an error happens to_discard will be set t True and the crossword will be discarded
                    to_discard = False

                    if how_to_place_word == "vrt":
                        
                        # coords is the initial position of the word to match the similarity
                        # for example if the second letter of the word is the same as the one 
                        # in the position 56 of the crossword the initial position of the word in case
                        # crossword_size is 10 will be 56 - 10 = 46
                        coords = similarity[similarity_element][1] - crossword_size * similarity[similarity_element][2]  
                        
                        # the word is placed vertically in the crossword
                        temp_array = place_vertically(words[words_counter], coords, temp_array)   
                        
                        # the following part is here so that unwanted crosswords are discarded
                        # it tries to place a $ before and after the word if it is possible
                        # if those spaces are already occupied by other letters the crossword 
                        # wont work anymore and needs to be discarded
                        try:
                            # checks for letters before and after the word
                            if temp_array[coords-crossword_size].isalpha()==True or temp_array[coords+(len(words[words_counter]))*crossword_size].isalpha()==True:
                                
                                # if found crossword is discarded
                                to_discard = True
                                
                        except Exception:
                            pass
                                    
                        try:
                            # tries to place a $ before the word if that space is empty
                            if temp_array[coords-crossword_size] == '/' and coords>crossword_size-1:

                                temp_array[coords-crossword_size] = '$'

                        except Exception:
                            pass
                        
                        try:
                            # tries to place a $ after the word if that place is empty
                            if temp_array[coords+(len(words[words_counter]))*crossword_size]  == '/':

                                temp_array[coords+(len(words[words_counter]))*crossword_size] = '$'

                        except Exception:
                            pass


                    # almost same thing as if how_to_place_word == 'vrt'
                    elif how_to_place_word == "hrz":        
                        
                        # check how_to_place_word == 'vrt' for coord explanation
                        coords = similarity[similarity_element][1] - similarity[similarity_element][2]

                        # the word is placed horizzontally in the crossword
                        temp_array = place_horizzontally(words[words_counter], coords, temp_array) 
                        
                        # ckecks for letters before and after the word
                        try:
                            # unlike the other check for letters in this one there is the need to see
                            # if the position that is checked is in the same line
                            if (coords // crossword_size) * crossword_size != coords and temp_array[coords-1].isalpha() == True or temp_array[coords+len(words[words_counter])].isalpha()==True: 
                                
                                # if is equal crossword is discarded
                                to_discard = True
                        
                        except Exception:
                            pass
                        
                        # if before the word is empty a $ is placed
                        try:
                            
                            if (coords // crossword_size) * crossword_size != coords and temp_array[coords-1] == '/':
                                temp_array[coords-1] = '$'
                        
                        except Exception:
                            pass

                        # if after the word is empty a $ is placed  
                        try:

                            if (coords // crossword_size) * crossword_size + crossword_size - 1 != coords + len(words[words_counter])-1 and temp_array[coords+len(words[words_counter])] == '/':  
                                temp_array[coords+len(words[words_counter])] = '$'

                        except Exception:
                            pass

                    # if there is no way to place the word the crossword is discarded
                    elif how_to_place_word == None or how_to_place_word == 'none':
                        
                        to_discard = True
                        
                        
                    if to_discard == False:
                        
                        # this variable stores where is the current word placed in the array
                        # it saves it like this: ['position of the word in the list of given words',
                        # 'initial position of the first letter','vertical or horizzontal']
                        where_this_word = [all_words.index(words[words_counter])+1,coords,how_to_place_word]

                        # the coordinates of this word are appended to the list of coordinates
                        # of the previous words in a list
                        where.append(where_this_word)
                        
                        # the thing to append to temp_array
                        to_append = [temp_array,where]

                        # if no errors occur
                        if temp_array != 'None' and temp_array != None:
                            
                            # the crossword and the coordinates of the word are appended 
                            temp_crosswords[words_counter+1].append(to_append)

     

                    similarity_element = similarity_element + 1

                last_created_crossword = last_created_crossword + 1

            words_counter = words_counter + 1

        # check to see if all the words of the permutation of words have been placed 
        # this check is poorly made but it works
        crosswords_len = 0
        for i in temp_crosswords:
            if i != []:
                crosswords_len = crosswords_len + 1

        # if all the words have been placed
        if crosswords_len == len(words) + 1:
            
            # i dont know what and how it works
            counter = 0
            while counter != crosswords_len + 1:
                
                if to_break == True:
                    break

                if temp_crosswords[counter] == []:

                    for crossword in temp_crosswords[counter-1]:      
                        
                        # the finished crosswords are appended to end_crosswords
                        end_crosswords.append(crossword)

                        # the counter increases until how_many_crosswords is reached
                        # then everything will break and the crosswords will be prompted
                        end_crosswords_counter = end_crosswords_counter + 1

                        if end_crosswords_counter >= how_many_crosswords:
                            to_break = True
                            break 

                counter = counter + 1

        if to_break == True:
            break

# time thing
start = time.time()

# configs are imported
config = configparser.ConfigParser()
config.read('config.ini')

# variables are assigned from the config file to local
words_string = config['DEFAULT']['words']
how_many_crosswords = int(config['DEFAULT']['how_many_crosswords'])
crossword_size = int(config['DEFAULT']['size'])

# the next part is necessary for transforming a string in an array
# because for some reason configparser keeps giving me strings as output
words_string = words_string[1:-1]
bad_chars = ["'",',']
for i in bad_chars :
    words_string = words_string.replace(i, '')
words = words_string.split()

# end_crossword is initialized
end_crosswords = []
 
# used to calculate the center of a crosswords with a given lenght
first_word_coord = int(crossword_size/2)+crossword_size*int(crossword_size/2)

# main function is called
main(words,how_many_crosswords)

#print crosswords to user
end_crosswords_counter = 0
for j in end_crosswords:
    
    j[1].sort(key=sortArray)

    # coords are split to vertical or horizzontal
    vertical_coords = []
    horizzontal_coords = []
        
    counter = 0
    for coord in j[1]:

        if j[1][counter][2] == 'hrz':
            horizzontal_coords.append(j[1][counter])

        if j[1][counter][2] == 'vrt':
            vertical_coords.append(j[1][counter])    

        counter = counter + 1

    # everything is printed to the terminal
    print(horizzontal_coords)
    print(vertical_coords)
    print_array(j[0])
    end_crosswords_counter = end_crosswords_counter + 1

print('I have made ',end_crosswords_counter, ' crosswords with those words. Enjoy!\n')

# time is stopped and printed
end = time.time()

end_time = round(end - start,2)

print("This algorithm took",end_time," seconds to run\n")

# the end



        



