import json
import random
path_output_aggregation = "./res/topics/result.json"

def test():
    topics = json.load(open(path_output_aggregation))
    seed_topics = random.choice(list(topics.keys()))
    return random.choice(topics[seed_topics])

res = test()
text, author = res["text"],res["author"]


while (len(text)>100 and len(text)<30):
    res = test()
    text, author = res["text"],res["author"]
    
print(author," \n", text)
