# -*- coding: utf-8 -*-
import scrapy
import os
from qidian.items import QidianXiaoshuoItem


class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    #allowed_domains = ['qidian.com']
    start_urls = []
    #print(start_urls)
    base_url = "https://www.qidian.com/all?orderId=&page=%d&vip=0"
    for i in range(1,41466):
        start_urls.append(base_url%i)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(start_urls)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    #请求免费小说的页面
    def parse(self, response):
        #输出请求地址
        #print(response.url)
        #查找第n页中的每部小说的url，存入列表
        fiction_list = response.xpath('//ul[@class="all-img-list cf"]/li/div[@class="book-img-box"]/a/@href').extract()
        #循环输出url列表
        for fiction in fiction_list:
            fiction = "https:" + fiction + "#Catalog"
            #print(fiction)
            yield scrapy.Request(url=fiction,callback=self.parse_chapter)

    #请求每个小说的页面（含有章节）
    def parse_chapter(self,response):
        #print(response.url)
        item = QidianXiaoshuoItem()

        #获取小说的名字
        fiction_name = response.xpath('//div[@class="book-info "]/h1/em/text()').extract()[0]
        item["fiction_name"] = fiction_name
        #print("小说名字：",fiction_name)

        #用小说名字创建一个文件夹
        try:
            os.mkdir(fiction_name)
        except:
            pass

        #查找每一个小说的章节url
        chapter_list = response.xpath('//div[@class="volume-wrap"]/div[@class="volume"]/ul[@class="cf"]/li')


        for chapter in chapter_list:
            #print("------------------")
            chapter_url = "https:" + chapter.xpath('./a/@href').extract()[0]
            yield scrapy.Request(url=chapter_url,callback=self.parse_content,meta={"data":item})

    #请求每个小说的第n章节
    def parse_content(self,response):
        print(response.url)
        item = response.meta["data"]
        #获取章节名字，章节的名字一定要在这个函数中获取，如果在上一个函数中获取，在创建章节文件时，
        #就会覆盖原有文件
        #后来发现,有点小说章节的名字含有"/",这样在存储时会报错,因为系统会认为"/"之后是下一个文件夹,找不到路径
        #所以要把章节名中含有"/"的换成别的符号
        chapter_name = response.xpath('//h3[@class="j_chapterName"]/text()').extract()[0]
        item["chapter_name"] = chapter_name.replace("/","-")

        #获取章节内容，由于内容在多个p标签里，所以就先定义了一个空字符串变量content
        content = ""
        content_p_list = response.xpath('//div[@class="read-content j_readContent"]/p')
        for content_p in content_p_list:
            #每一段落加一个回车换行
            content += content_p.xpath('./text()').extract()[0] + "\n"
        #将内容存入item中
        item["content"] = content

        yield item






