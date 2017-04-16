# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

class JudgementPipeline(object):
    def process_item(self, item, spider):
        fid = re.findall("\d+", item["url"])[0]
        f = open("docs/%s.txt" % fid, "w")
        f.write(item["url"])
        f.write("\n")
        f.write(str(item["publish_date"]))
        f.write("\n")
        f.write(item["title"].encode('utf-8'))
        f.write("\n")
        f.write(item["content"].encode('utf-8'))
        f.close()
        return item
