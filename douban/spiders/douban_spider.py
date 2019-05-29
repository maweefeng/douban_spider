# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'#爬虫名
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']#入口url 扔到调度器里面
    #默认的解析方法
    def parse(self, response):
        #循环电影的条目
        html = etree.HTML(response.text)
        movie_list = html.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for item in movie_list:
            #item文件导入
            douban_item = DoubanItem()
            #写详细的xpath 进行数据的解析
            douban_item['serial_number'] = item.xpath('.//div[@class="item"]//em/text()')[0]
            douban_item['movie_name'] = item.xpath('.//div[@class="info"]//a/span[1]/text()')[0]
            content_list = item.xpath('.//div[@class="info"]//div[@class="bd"]/p[1]/text()')
            for content in content_list:
                content_s = "".join(content.split())
                douban_item['introduce'] = content_s

            douban_item['star']= item.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()')[0]
            douban_item['comment'] = item.xpath('.//div[@class="star"]/span[4]/text()')[0]
            douban_item['description'] = item.xpath('.//p[@class="quote"]/span[1]/text()')[0]
            print(douban_item)
            yield douban_item #yeild到piplines里面 进行数据清洗 数据存储
        
        #解析下一页规则 获取后一页的xpath
        next_link = html.xpath('//span[@class="next"]/link/@href')

        if next_link:
            next_link = next_link[0]
            #yeild到调度器当中 后面给了回调函数
            yield scrapy.Request('https://movie.douban.com/top250'+next_link,callback=self.parse)


