import json
import re
from lxml import etree

from WebRequest import WebRequest


class NewsRobot(WebRequest):
    def __init__(self, start_url):
        super().__init__()
        self.start_url = start_url

    def get_url_list(self):
        raw_html = self.get(self.start_url).text

        json_url_list = re.findall("""listInfo:(.*?)
                    }
                </script>""", raw_html, re.S)[0]
        json_url_list = json_url_list.replace('\'', '"').replace("title", '"title"') \
            .replace("imgurl:", '"imgurl":'). \
            replace("imgurl2", '"imgurl2"'). \
            replace("abstract", '"abstract"') \
            .replace("source", '"source"'). \
            replace("pubtime", '"pubtime"').replace(",url:", ',"url":')

        # print(json_url_list)
        dict_url_list = json.loads(json_url_list)
        return dict_url_list

    def deal_dict_data(self, detail):
        data_list = []

        for item in detail:
            # print(item)
            data = self.get_detail(item)

            if data is not None:
                data['imgurl'] = item['imgurl']
                data['pubtime'] = item['pubtime']
                data_list.append(data)
        with open("json/News.json","w") as f:
            data_list_json = json.dumps(data_list)
            f.write(data_list_json)
    def get_detail(self, item):
        detail = item["url"]
        # print(detail)
        raw_detail_html = self.get(detail).text
        return self.parse_detail(raw_detail_html)

    def parse_detail(self, raw_detail_html):
        # print(len(raw_detail_html))
        selector = etree.HTML(raw_detail_html)
        title = selector.xpath('//div[@class="hd"]/h1/text()|//meta[@name="Description"]/@content')[0]
        content = selector.xpath('//p[@class="text"]/text()|//div[@class="infoTxt"]/p/text()')
        if len(content) == 0:
            return None

        else:
            item = {}
            item['title'] = title
            item['content'] = content
            imgs = selector.xpath('//p[@align="center"]/img/@src')
            for i in range(len(imgs)):
                imgs[i] = "http:"+imgs[i]
            item["imgs"] = imgs
            return  item

    def run(self):
        detail = self.get_url_list()
        self.deal_dict_data(detail)


if __name__ == '__main__':
    url = "http://sports.qq.com/l/others/2018asiangames/jakartanews/list2018071716110.htm"
    nr = NewsRobot(url)
    nr.run()
