# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class QidianPipeline(object):
    def process_item(self, item, spider):
        return item

class QidianXiaoshuoPipeline(object):



    def process_item(self, item, spider):
        paper_file = item["fiction_name"]
        file_name = item["chapter_name"]
        content = item["content"]
        with open(paper_file+"/"+file_name+".txt","w",encoding="utf-8") as file:
            file.write(content)
        print(item["fiction_name"],item["chapter_name"])
        return item
