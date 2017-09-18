import time
from selenium import webdriver

import urllib.request

from bs4 import BeautifulSoup

import html.parser


def main():
    """open chrome driver and get the target websites"""
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.zhihu.com/question/26037846")

    def execute_times(times):
        for i in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()
                print("page: " + str(i))
                time.sleep(1)
            except:
                break

    execute_times(1)

    result_raw = driver.page_source
    result_soup = BeautifulSoup(result_raw, 'html.parser')
    result_bf = result_soup.prettify()

    with open('./output/rawfile/raw_result.txt', 'w') as girls:
        girls.write(result_bf)
    girls.close()
    print('store raw data successfully!!!')

    with open('./output/rawfile/noscript_meta.txt', 'w') as noscript_meta:
        noscript_nodes = result_soup.find_all('noscript')

        noscript_inner_all = ''
        for noscript in noscript_nodes:
            noscript_inner = noscript.get_text()
            noscript_inner_all += noscript_inner + '\n'

        noscript_all = html.parser.unescape(noscript_inner_all)
        noscript_meta.write(noscript_all)
    noscript_meta.close()
    print("Store noscript meta data successfully!!!")

    img_soup = BeautifulSoup(noscript_all, 'html.parser')
    img_nodes = img_soup.find_all('img')
    with open('./output/rawfile/img_meta.txt', 'w') as img_meta:
        count = 0
        for img in img_nodes:
            if img.get('src') is not None:
                img_url = img.get('src')
                line = str(count) + '\t' + img_url + '\n'
                img_meta.write(line)
                urllib.request.urlretrieve(img_url, "./output/img/" + str(count) + ".jpg")
                count += 1
    img_meta.close()
    print("Store meta data and images successfully!!!")

    driver.close()

if __name__ == '__main__':
    main()
