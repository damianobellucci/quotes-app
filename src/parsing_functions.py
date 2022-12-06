import urllib.request as urllib
from bs4 import BeautifulSoup
import json

url_topics = 'https://www.brainyquote.com/topics/'

def get_info_author(block):

    info_html = str(block.find_all(
        'div', class_='subnav-below-p')[0])
    info_string = (block.find_all(
        'div', class_='subnav-below-p')[0]).get_text().split('\n')
    info_string_2 = ""
    for element in info_string:
        if(len(element) != 0):
            info_string_2 += element + " "
    return {'info_html': info_html, 'info_string': info_string_2}

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


def max_index_page(page):
    soup = get_soup_page(page)
    page_numbers = []
    if soup.find('ul', class_='pagination bqNPgn pagination-sm'):
        for link in soup.find('ul', class_='pagination bqNPgn pagination-sm').find_all('a'):
            href_string = link.get('href')
            if href_string and href_string.find('/authors/') != -1:
                href_string = href_string[len('/authors/')+1:]
                page_numbers.append(int(href_string))
        pages = max(page_numbers)
    else:
        pages = 1
    return pages


def get_quote_in_block(data, soup_block):
    data['text'] = soup_block.find_all('a', class_='b-qt')[0].get_text().replace("\n","")
    return data

def get_keyword_in_block(data, soup_block):
    keywords = []
    # per ogni citazione prendo le keywords
    for keyword in soup_block.find_all('a', class_='qkw-btn btn btn-xs oncl_klc'):
        keywords.append(keyword.get_text())
    data['keywords'] = keywords
    return data

def atomic_operation(keyword,index):
    name, info, quote_list = refactor_test_get_quotes_list(keyword,index)
    author_object = {"quotes": quote_list}
    with open('./res/'+keyword+"_"+str(index)+'.json', 'w') as outfile:
        json.dump(author_object, outfile, sort_keys=True, indent=4)

