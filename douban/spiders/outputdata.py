#数据导出 也可以使用terminal 直接运行
from scrapy import cmdline
#数据导出到json
# cmdline.execute('scrapy crawl douban_spider -o output.json'.split())

#数据导出到csv格式
cmdline.execute('scrapy crawl douban_spider -o output.csv'.split())