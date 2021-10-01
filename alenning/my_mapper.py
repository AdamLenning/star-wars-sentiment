#!/usr/bin/python3
"""mapper.py"""

import sys
import re

# input comes from STDIN (standard input)
for line in sys.stdin:

    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    # increase counters
    output_word_list = [] #Will hold processed words    
    
    for word in words:
        out_word = ""
        for letter in word:
            if letter.isalpha(): #only keep letters
                out_word = "".join([out_word, letter.lower()]) #transform to lower
        #word = "".join(re.findall("[a-zA-Z]+", word))
        
        
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        if len(out_word) > 0: #We don't want to include any blank strings in our wordcount so the reduce works
            output_word_list.append(out_word)
    for i in range(0, len(output_word_list)-1):
        print( "%s\t%s" % (output_word_list[i] + " " + output_word_list[i+1], 1))

