import requests
import re
import json
import xlwt
from bs4 import  BeautifulSoup
from requests.exceptions import RequestException


def get_one_url(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return  None

def parse_one_url(html):
    pattern = re.compile('<li class.*?_blank.*?<span.*?">(\d+)</span>.*?"num">(\d+)</strong>(.*?)'
                         + '</span>.*?<a alt.*?" href="(.*?)" pos="2".*?">(.*?)</a>.*?<p.*?site-piclist_info_describe">'
                         + '(.*?)</p>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'idex': item[0],
            'name': item[4],
            'score': item[1] + item[2],
            'comments': item[5],
            'url': item[3]
        }

def write_to_txtfile(content,bangdan):
    with open('results' + bangdan + '.txt','a',encoding='utf-8') as f:
        f.truncate()
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def write_to_xlsfile(content,bangdan):
    fopen = open('results' + bangdan + '.txt','r')
    lines = fopen.readlines()
    #新建一个excel文件
    file=xlwt.Workbook(encoding='utf-8',style_compression=0)
    #新建一个sheet
    sheet = file.add_sheet(bangdan)
    #写入写入txt文件
    i = 0
    for key in eval(lines[0]):
        sheet.write(0,i,key)
        i += 1
    i = 1
    for line in lines:
        dic_line = eval(line)
        values = []
        for value in dic_line.values():
            values.append(value)
        k = 0
        for value in values:
            sheet.write(i,k,value)
            k += 1
        i += 1
    file.save('results' + bangdan + '.xls')


def main():
    url = 'http://www.iqiyi.com/dianying_new/i_list_paihangbang.html?type=2'
    prehtml = get_one_url(url)
    htmlsoup = BeautifulSoup(prehtml,'html.parser')
    html_array = htmlsoup.find_all('div',class_="wrapper-piclist")
    bangdan = ["热播榜","高分榜"]
    for i in range(2):
        html = str(html_array[i])
        for item in parse_one_url(html):
            print(item)
            write_to_txtfile(item,bangdan[i])
            write_to_xlsfile(item,bangdan[i])

if __name__ == '__main__':
    main()




