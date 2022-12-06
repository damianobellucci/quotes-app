import math
import parsing_functions
from multiprocessing import Pool
from linear_execution import linear_execution
from concurrent_execution import concurrent_execution
from urllib.error import URLError, HTTPError
import urllib.request as urllib
import random
from time import sleep
import json 

'''
if __name__ == '__main__':
    letters = ['x', 'z']

    for letter in letters:
        authors = parsing_functions.lista_autori_lettera(letter)
        parsing_functions.dump_authors_letter_list(letter)
        linear_execution(authors)
        #concurrent_execution(authors)
'''



if __name__ == '__main__':
    topics = [
        'motivational',
        'inspirational',
        'attitude',
        'life',
        'positive',
        'beauty',
        'funny',
        'friendship',
        'dreams',
        'cool'
    ]
    
    topics = (open("./res/topics")).read().split("\n")[:1]


    for topic in topics:
        #get links pages
        last_index = parsing_functions.get_indexes_pages(topic)
        print(last_index)
        for index in range(1,last_index+1):
           parsing_functions.atomic_operation(topic,index)
           delay = random.uniform(0, 3)
           print(delay)
           sleep(delay)
