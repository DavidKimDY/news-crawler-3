from crawlers import *
from util import *
from text_extractor import text_extractor
# for webclass in All.class_list:

input_date ='2021-02-05'
a = Venturesquare(input_date)

meta = a.crawler()

new_data = get_rid_of_outdated(meta, input_date)
new_data = get_rid_of_duplicated(new_data)
all_text = text_crawler(new_data)  # get text
all_text = check_text_validity(all_text)  # len 10


