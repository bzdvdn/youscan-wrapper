# YouScan Insight RestAPI client

# Installation

Install using `pip`...

    pip install youscan
    

YouScan documentation - https://youscan.docs.apiary.io/

# Usage
```python
from youscan import Client
client = Client('<your_api_key>') # production server usage
mock_server_client = Client('<your_api_key>', mock_server=True) # mockserver usage

# get all topics
topics = client.get_topics()

# get all by topic id
tags = client.get_tags('<topic_id>')

# create tag
new_tag = {
   "name" : "unique_name",
   "note" : "some notes",
   "color" : "red"
}
client.create_tag('<topic_id>', **new_tag)

# fetching mentions
# doc url - https://youscan.docs.apiary.io/#reference/mention-stream/fetching-mentions/list-mentions?console=1
mentions = client.list_mentions(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')
```
```text
# extra params for this endpoint

sentiment: str,
exclude_sentiment: str,
sources: str,
exclude_sources: str,
tags: str,
exclude_tags: str,
auto_categories: str,
exclude_auto_categories: str,
starred: bool,
tagged: bool,
processed: bool,
deleted: bool,
spam: bool,
size: int,
skip: int,
order_by: str
```

# Statistic
```python
# Sentiment
sentiment_stats = client.get_sentiments_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Tags
tags_stats = client.get_tags_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Worldcloud
words_stats = client.get_words_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Sentiment by regions
sent_by_regions_stats = client.get_regions_sentiments_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Sentiment by sources
sent_by_sources = client.get_sources_sentiments_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Sentiment by sources by regions
stats_by_source_regions = client.get_sources_by_regions_sentiments_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Histogram
historam = client.get_histogram_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Trends
trends = client.get_trends_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Genders
genders = client.get_genders_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Ages
ages = client.get_ages_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Links
links = client.get_links_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Authors
authors = client.get_authors_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')

# Publication places
pub = client.get_publication_places_statistic(topic_id='<topic_id>', from_date='2019-10-10',to_date='2019-10-11')
```

#TODO
-
* more examples
* tests