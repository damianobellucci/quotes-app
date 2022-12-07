from topics_scraper import Topics_scraper

path_topics = "./config/topics"
path_results = "./res/topic_index"
path_output_aggregation = "./res/topics/result.json"

if __name__ == '__main__':
    topic_scraper = Topics_scraper(
        path_topics=path_topics,
        path_results=path_results,
        path_output_aggregation=path_output_aggregation
        )
    topic_scraper.start()
    #topic_scraper.aggregate_topics_indexes()
    
