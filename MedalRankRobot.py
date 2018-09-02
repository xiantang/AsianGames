import json
import re

from lxml import etree

from WebRequest import WebRequest


class MedalRankRobot(WebRequest):
    def __init__(self, start_url):
        super().__init__()
        self.start_url = start_url

    def parse_start_html(self):
        raw_json = self.get(self.start_url).text
        raw_json = re.findall("nkSucc\((.*?)\)", raw_json)[0]
        return raw_json

    def to_local(self, medal_json):
        with open("json/MedalRank.json", "w") as f:
            f.write(medal_json)

    def run(self):
        medal_json = self.parse_start_html()
        self.to_local(medal_json)


if __name__ == '__main__':
    url = "https://2018ag.sports.qq.com/api/rank.php?callback=callbackYayunhuiRankSucc&_=1535865899219"
    mrb = MedalRankRobot(url)
    mrb.run()
