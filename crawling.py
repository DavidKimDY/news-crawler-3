from util import *
from news_site_class_list import class_list

# input_date = input("Enter the date (ex 2021-01-01) or just hit the enter key : ")
input_date = ''
if input_date == '':
    with open('time_stamp.json', 'r') as f:
        time_stamp = json.load(f)
    user_input_date = False
else:
    assert datetime.strptime(input_date, '%Y-%m-%d')
    user_input_date = True


for news_class in class_list:
    news_site = news_class.__name__

    if not user_input_date:
        input_date = time_stamp[news_site]  # edit

    print(news_site, ': ', input_date)
    if input_date == datetime.today().__str__().split()[0]:
        continue

    news_instance = news_class(input_date)
    meta = news_instance.crawler()

    meta_data = get_rid_of_outdated(meta, input_date)
    meta_data = get_rid_of_duplicated(meta_data)


    post_data = getattr(news_instance, 'post_data', None)
    text_data = text_crawler(meta_data, post_data)  # get text
    meta_data, text_data = filter_wrong_data(meta_data, text_data, news_site)  # len 20


    print(news_site, meta_data[0].get('time', None))
    #save_data(meta_data, news_site)
    #save_data(text_data, news_site, text=True)

    #update_time_stamp(meta_data, news_site)
