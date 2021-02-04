from NewsCrawler3.crawlers import *

input = {
    "Startup": "2021-01-18",
    "Trends": "2021-01-19",
    "Investment": "2021-01-06",
    "Main": "2021-01-19",
    "Business": "2021-01-19",
    "Event": "2021-01-19",
    "China": "2021-01-19",
    "Blockchain": "2021-01-18",
    "Marketing": "2021-01-11",
    "Workinsight": "2020-12-30",
    "Entrepreneur": "2021-01-12",
    "Report": "2020-08-14",
    "ALL TECH KOREA": "2019-12-14",
    "Uncategorized": "2019-08-03",
    "Greater China": "2015-01-21"}

a = Platum(input)
for i in a.crawler():
    print(i['day'], i['category'], i['title'], i['url'])