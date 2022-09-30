import sys, time
import requests
from bs4 import BeautifulSoup

header = {
        'accept':
        'application/json',
        'origin':
        'https://ani.gamer.com.tw',
        'authority':
        'ani.gamer.com.tw',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }

class Episode:
    def __init__(self, url):
        #url = "https://httpbin.org/status/404"
        self.__url          = url
        self.__series_title = None
        self.__title        = None
        self.__cover_data   = None
        self.__cover_url    = None
        self.__visual_data  = None
        self.__visual_url   = None
        self.__time         = None
        self.__agency       = None

        self.soup = get_soup(url)
        if "動畫瘋" not in self.soup.title.string:
            raise FileNotFoundError

    def metadata_as_dict(self):
        data = {"網址":self.url,
                "此季標題":self.series_title,
                "標題":self.title,
                "上架時間":self.time,
                "台灣代理":self.agency,
                "視覺圖網址":self.visual_url
               }
        if self.cover_url != self.visual_url:
            data["封面網址"] = self.cover_url
        return data

    def whole_season_url(self):
        multi_ep = self.soup.find("section", class_="season")
        if not multi_ep:
            yield self.url
            return
        # example v: "?sn=31322"
        for v in multi_ep.find_all("a"):
            yield "https://ani.gamer.com.tw/animeVideo.php" + v["href"]

    @property
    def agency(self):
        if self.__agency:
            return self.__agency

        print("開始尋找台灣代理")
        t = self.soup.find("ul", class_="data_type").find_all("li")
        self.__agency = t[3].next_element.next_element.next_element
        return self.__agency

    @property
    def time(self):
        if self.__time:
            return self.__time
        # 上架時間：2022/09/25 02:00
        # 5 == len("上架時間：")
        print("開始尋找上架時間")
        self.__time = self.soup.find("div", class_="anime_info_detail").p.string[5:]
        return self.__time

    @property
    def url(self):
        return self.__url

    @property
    def series_title(self):
        if self.__series_title:
            return self.__series_title

        print("開始尋找此季動畫標題")
        detail_url = "https:" + self.soup.find_all('a', class_="bluebtn")[-1].get("href")
        detail_soup = get_soup(detail_url)
        self.__series_title = detail_soup.h1.string
        return self.__series_title

    @property
    def title(self):
        if self.__title:
            return self.__title

        print("開始尋找此集標題")
        self.__title = self.soup.h1.string
        print(f"標題：{self.__title}")
        return self.__title

    @property
    def visual_url(self):
        if self.__visual_url:
            return self.__visual_url

        print("開始尋找視覺圖網址")
        visual = self.soup.find("meta", attrs={"name": "thumbnail"})
        self.__visual_url = visual["content"]
        return self.__visual_url

    @property
    def cover_url(self):
        if self.__cover_url:
            return self.__cover_url

        print("開始尋找封面圖網址")
        cover = self.soup.find_all("script")
        last_script = str(cover[-1])
        cover_url_start = last_script.find("https")
        if cover_url_start == -1:
            print(f"網址：{self.url}")
            print("找不到封面！請開 issue 回報。")
            print("退出程式")
            sys.exit(1)

        cover_url_end = last_script.find("\'", cover_url_start)
        self.__cover_url = last_script[cover_url_start : cover_url_end]
        return self.__cover_url

    @property
    def visual_data(self):
        if self.__visual_data:
            return self.__visual_data

        print("開始下載視覺圖")
        self.__visual_data = requests_get(self.visual_url, headers=header).content
        return self.__visual_data

    @property
    def cover_data(self):
        if self.__cover_data:
            return self.__cover_data

        print("開始下載封面")
        self.__cover_data = requests_get(self.cover_url, headers=header).content
        return self.__cover_data


def get_soup(url):
    content = requests_get(url, headers=header)
    return BeautifulSoup(content.text, "html.parser")

def requests_get(url, **kwargs):
    for try_cnt in range(1, 4):
        try:
            content = requests.get(url, timeout=10, **kwargs)
            if content.status_code != requests.codes.ok:
                content.raise_for_status()
        except requests.exceptions.RequestException as err:
            print("連線到動畫瘋網站時出錯，詳情：")
            print(err)
            if try_cnt == 3:
                print("\n連續錯誤 3 次，退出程式。")
                print("建議確認網路連線狀況。")
                sys.exit(1)
            #else:
            try:
                print("3 秒後再試一次……\n")
                time.sleep(3)
            except KeyboardInterrupt:
                print("\n使用者按了 Ctrl + C 中斷程式")
                sys.exit(1)
        else:
            return content


# url = "https://ani.gamer.com.tw/animeVideo.php?sn=31069"


# use offline file to test (code is old, and hasn't been updated)
#
# print(get_cover(soup))
#
# pic = requests.get(get_cover(soup))
# with open("cover.jpg", 'wb') as fn:
#     fn.write(pic.content)
