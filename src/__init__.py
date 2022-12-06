import parsing_functions
import random
from time import sleep

path_topics = "./config/topics"

if __name__ == '__main__':
    topics = (open(path_topics)).read().split("\n")[:1]
    for topic in topics:
        last_index = parsing_functions.get_indexes_pages(topic)
        for index in range(1,last_index+1):
           parsing_functions.atomic_operation(topic,index)
           delay = random.uniform(0, 3)
           sleep(delay)
