import json
import re

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

    


if __name__ == '__main__':
    url = "http://sports.qq.com/l/others/2018asiangames/jakartanews/list2018071716110.htm"
    nr = NewsRobot(url)
    nr.get_url_list()
