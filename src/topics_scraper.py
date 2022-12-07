import urllib.request as urllib
from bs4 import BeautifulSoup
import json
import random
from time import sleep
import os

url_topics = 'https://www.brainyquote.com/topics/'

class Topics_scraper:
    def __init__(self,
                 path_topics,
                 path_results,
                 path_output_aggregation
                 ):
        self.url_topics = url_topics
        self.path_topics = path_topics
        self.path_results = path_results
        self.path_output_aggregation = path_output_aggregation
        
    def start(self):
        print("Started.")
        topics = (open(self.path_topics)).read().split("\n")
        for topic in topics:
            last_index = self.__get_indexes_pages(topic)
            for index in range(1,last_index+1):
                print(f'topic:{topic}, index:{index}')
                self.__dump_topic_page(topic,index)
                delay = random.uniform(0, 3)
                sleep(delay)
        print("Ended.")
        
    def __get_page_with_request(self,page_url):  # no scrolling but no lag for webdriver
        req = urllib.Request(page_url, headers={'User-Agent': "Magic Browser"})
        con = urllib.urlopen(req)
        return con.read()

    def __get_page(self,page_url):
        page = self.__get_page_with_request(page_url)
        return page

    def __get_soup_page(self,page):
        soup = BeautifulSoup(self.__get_page(page), 'html.parser')
        return soup

    def __get_author_in_block(self,data, soup_block):
        data['author'] = soup_block.find_all('a', {'title' : 'view author'})[0].get_text()
        return data

    def __get_indexes_pages(self,topic):
        url = self.url_topics+topic+'-quotes'
        soup = self.__get_soup_page(url)
        indexes = soup.find_all(
            'ul', class_='pagination')
        if len(indexes)>0:
            indexes = soup.find_all('a', class_='page-link')
            last = indexes[len(indexes)-2].get_text()
            return int(last)
        
    def __get_quotes_list(self,keyword,index):
        url = self.url_topics+keyword+'-quotes'+"_"+str(index)
        soup = self.__get_soup_page(url)
        quote_list = []
        blocks_list = soup.find_all(
            'div', class_='grid-item qb clearfix bqQt')
        info_author = 'get_info_author(soup)'
        name_author = " ".join(soup.find_all(
            'h1', class_='bq-subnav-h1')[0].get_text().split()[:-1])
        for block in blocks_list:
            # because block is a BeautifulSoup object, we must stringify it for "re"-soup it
            block = str(block)
            soup_block = BeautifulSoup(block, 'html.parser')
            data = {}
            # take quote, input: data = {} , soup_block . output: data = {'text: 'text of the quote'},'text':'...' appended to data
            data = self.__get_quote_in_block(data, soup_block)
            # take keywords of quotes input : data, soup_block . output: data = {'keywords':[]} 'keywords':[] appended to data
            #data = get_keyword_in_block(data, soup_block)
            data['keyword'] = keyword
            data = self.__get_author_in_block(data, soup_block)
            #print(data)
            quote_list.append(data)
        return name_author, info_author, quote_list

    def __get_quote_in_block(self,data, soup_block):
        data['text'] = soup_block.find_all('a', class_='b-qt')[0].get_text().replace("\n","")
        return data

    def __dump_topic_page(self,keyword,index):
        name, info, quote_list = self.__get_quotes_list(keyword,index)
        author_object = {"quotes": quote_list}
        with open(f'{self.path_results}/{keyword}_{str(index)}.json', 'w') as outfile:
            json.dump(author_object, outfile, sort_keys=True, indent=4)
            
    def aggregate_topics_indexes(self):
        topics = os.listdir(self.path_results)
        map = {}

        for el in topics:
            topic, index = el.split(".")[0].split("_")
            if not topic in map.keys():
                map[topic] = [index]
            else:
                map[topic] = map[topic]+[index]
        output_map = {}
        tot = 0
        for topic in map.keys():
            list_quotes_topic  = []
            for index in map[topic]:
                list_quotes_topic += json.load(
                    open(f'{self.path_results}/{topic}_{index}.json')
                    )["quotes"]
                tot += len(list_quotes_topic)
            output_map[topic]=list_quotes_topic
        json_object = json.dumps(output_map, indent=2)
        with open(self.path_output_aggregation, "w") as outfile:
            outfile.write(json_object)
        print(tot)
