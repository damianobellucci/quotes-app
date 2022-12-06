from parsing_functions import get_indexes_pages, atomic_operation
import random
from time import sleep

path_topics = "./config/topics"

if __name__ == '__main__':
    print("Started.")
    topics = (open(path_topics)).read().split("\n")[:1]
    for topic in topics:
        last_index = get_indexes_pages(topic)
        for index in range(1,last_index+1):
            print(f'topic:{topic}, index:{index}')
            atomic_operation(topic,index)
            delay = random.uniform(0, 3)
            sleep(delay)
    print("Ended.")

