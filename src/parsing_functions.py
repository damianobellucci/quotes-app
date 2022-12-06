import urllib.request as urllib
from bs4 import BeautifulSoup
import json

url_topics = 'https://www.brainyquote.com/topics/'

def get_page_with_request(page_url):  # no scrolling but no lag for webdriver
    req = urllib.Request(page_url, headers={'User-Agent': "Magic Browser"})
    con = urllib.urlopen(req)
    return con.read()

def get_page(page_url):
    page = get_page_with_request(page_url)
    return page

def get_soup_page(page):
    soup = BeautifulSoup(get_page(page), 'html.parser')
    return soup

def get_author_in_block(data, soup_block):
    data['author'] = soup_block.find_all('a', {'title' : 'view author'})[0].get_text()
    return data

def get_indexes_pages(topic):
    url = url_topics+topic+'-quotes'
    soup = get_soup_page(url)
    indexes = soup.find_all(
        'ul', class_='pagination')
    if len(indexes)>0:
        indexes = soup.find_all('a', class_='page-link')
        last = indexes[len(indexes)-2].get_text()
        return int(last)
      
def refactor_test_get_quotes_list(keyword,index):
    url = url_topics+keyword+'-quotes'+"_"+str(index)
    soup = get_soup_page(url)
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
        data = get_quote_in_block(data, soup_block)
        # take keywords of quotes input : data, soup_block . output: data = {'keywords':[]} 'keywords':[] appended to data
        #data = get_keyword_in_block(data, soup_block)
        data['keyword'] = keyword
        data = get_author_in_block(data, soup_block)
        #print(data)
        quote_list.append(data)
    return name_author, info_author, quote_list

def get_quote_in_block(data, soup_block):
    data['text'] = soup_block.find_all('a', class_='b-qt')[0].get_text().replace("\n","")
    return data

def atomic_operation(keyword,index):
    name, info, quote_list = refactor_test_get_quotes_list(keyword,index)
    author_object = {"quotes": quote_list}
    with open('./res/'+keyword+"_"+str(index)+'.json', 'w') as outfile:
        json.dump(author_object, outfile, sort_keys=True, indent=4)