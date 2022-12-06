from topics_scraper import Topics_scraper

path_topics = "./config/topics"

if __name__ == '__main__':
    topic_scraper = Topics_scraper(
        path_topics=path_topics
        )
    topic_scraper.start()
    
