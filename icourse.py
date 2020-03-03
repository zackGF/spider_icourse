import json

import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool


def get_one_page(url, form_data):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }

        response = requests.post(url=url, headers=headers, data=form_data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    expression = re.compile(
        # '<img\sonerror="nofind.*?src="(.*?)">',
        '<img\sonerror=".*?"\ssrc="(.*?)".*?<a\sclass="icourse-desc-title"\shref="(.*?)".*?title="(.*?)"\starget="_blank">.*?title="(.*?)\s\D\s(.*?)">',
        re.S
    )
    result = re.findall(expression, html)
    for item in result:
        yield {
            "image": item[0],
            "link": item[1],
            "title": item[2],
            "teacher": item[3],
            "school": item[4]
        }
    # print(result)


def write_to_file(content):
    with open("icourse.txt", "a", encoding="utf8") as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(pagenum):
    url = "http://www.icourses.cn/web//sword/portal/shareSearchPage"
    form_data = {
        "curPage": pagenum,
        "pageSize": "20",
        "listType": "1"
    }

    html = get_one_page(url, form_data)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # for num in range(5):
    #     main(num)
    pool = Pool()
    pool.map(main, [num for num in range(146)])
