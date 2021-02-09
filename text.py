from crawlers import *
from util import *
from text_extractor import text_extractor
# for webclass in All.class_list:

input_date ='2021-02-05'
a = Venturesquare(input_date)

meta = a.crawler()

new_data = get_rid_of_outdated(meta, input_date)
new_data.extend(new_data)
#for i in new_data:
#    print(i['day'], i['title'], i['corp'])

print('*'*100)

new_data = get_rid_of_duplicated(new_data)

#for i in new_data:
#    print(i['day'], i['title'])

all_text = text_crawler(new_data)
all_text.append({'text': 'what the'})
all_text = check_text_validity(all_text)

for i in all_text:
    print(i)

