from retrying import  retry
from urllib import request
from http import cookiejar
import re
import os
import requests
from http.cookiejar import LWPCookieJar
import time
from selenium import webdriver
import sys
from  bs4 import BeautifulSoup
def saveCookie(url, savepath):
    '''
    保存cookie - Netscape格式
    :param url: 
    :param savepath: 
    :return: 
    '''
    cookie = cookiejar.MozillaCookieJar(filename=savepath)
    cookie_hander = request.HTTPCookieProcessor(cookie)

    opener = request.build_opener( cookie_hander)
    response = opener.open(url)
    cookie.save(ignore_expires=True, ignore_discard=True)




# open the url and read


def getHtml(url):  #获取html

    # filename = r'C:\Users\class\Desktop\TIP-2018\TIP_cookie.txt'
    # cookie = cookiejar.MozillaCookieJar()
    # cookie.load(filename, ignore_discard=True, ignore_expires=True)
    # handler = request.HTTPCookieProcessor(cookie)
    # openner = request.build_opener(handler)
    # with openner.open(url) as web:
    #     print(type(web))

    # s = requests.Session()
    # headers = {}
    # headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    # headers['Accept-Encoding']='gzip, deflate, sdch'
    # headers['Accept-Language']='zh-CN,zh;q=0.8'
    # headers['Cache-Control']='max-age=0'
    # headers['Connection']='keep-alive'
    # headers['Upgrade-Insecure-Requests']='1'
    # headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    # headers['Host']='hr.tencent.com'
    # s.headers=headers
    # scont = s.get(url)
    # html=BeautifulSoup(scont.text, 'lxml', from_encoding="utf-8")
    #

    attempts = 0
    success = False

    while attempts < 3 and not success:
        try:
            page = request.urlopen(url)
            html = page.read()
            success=True
        except:
            attempts+=1
            if attempts == 3:
                break
    if success==False:
        return None
    return html.decode('UTF-8')



    # html = requests.get(url)
    # # print("网页编码：" + html.encoding)
    # # print("系统默认编码 " + sys.getdefaultencoding())
    # html = html.text
    #
    #
    #
    # return html


def getJsHtml(url):
    driver = webdriver.Chrome()
    driver.get(url)  # 请求页面，会打开一个浏览器窗口
    # html_text = driver.page_source
    # driver.quit()
    try:
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
    except:
        print("error--continue!!")
        html_text = None
    else:
        html_text = driver.page_source

    driver.quit()
    return html_text
# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    reg = r'arnumber=\d{7}'
    url_re = re.compile(reg)
    url_lst = re.findall(url_re, html.decode('utf-8'))
    return url_lst

def download(issue, new_url, paper_num, save_path):
    '''
    :param issue:  论文期号  （用于创建文件夹）
    :param new_url:  论文完整下载URL
    :param paper_num:  论文编号 （arnumber）
    :param save_path: 保存根目录
    :return:
    '''
    filename = r'C:\Users\class\Desktop\TIP-2018\TIP_cookie.txt'
    save_path = save_path+'/'+str(issue)+'/'  # 每期一个文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path = save_path+paper_num+'.pdf'

    web = requests.get(new_url)
    outfile = open(save_path, 'wb')

    outfile.write(web.content)
    outfile.close()


    # cookie = cookiejar.MozillaCookieJar()
    # cookie.load(filename, ignore_discard=True, ignore_expires=True)
    # handler = request.HTTPCookieProcessor(cookie)
    # openner = request.build_opener(handler)
    # with openner.open(new_url) as web:
    #     with open(save_path, 'wb') as outfile:
    #         outfile.write(web.read())
    # print("Sucessful to download" + " " +paper_num)



# IEEE
isnumbers = ['7825595','7815535','7859508','7888652','7932287','7947374','7972763','7995182','8031505','8068786','8089499','8128624'] #期号
'https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=7825595&punumber=4149689' #2017 issue1
'https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=7815535&punumber=4149689' #2017 issue2
'https://ieeexplore.ieee.org/ielx7/4149689/7825595/07826713.pdf?tp=&arnumber=7826713&isnumber=7825595'  #download url
'https://ieeexplore.ieee.org/ielx7/4149689/7825595/07825882.pdf?tp=&arnumber=7825882&isnumber=7825595'
'https://ieeexplore.ieee.org/ielx7/4149689/8128624/08128863.pdf?tp=&arnumber=8128863&isnumber=8128624'
#print(url_lst[0][9:])

# save_path = r'C:/Users/class/Desktop/IEEEpaper/IET Image Processing/2017'  #下载论文保存路径
#
#
# root_url_1 = r'https://ieeexplore.ieee.org/ielx7/4149689/'  #下载url  +isnumber
# root_url_2 = r'/0'   # +arnumber
# root_url_3 = r'.pdf?tp=&arnumber='  # +arnumber
# root_url_4 = r'&isnumber='   #+isnumber
# for issue in range(11,12):#1~12期
#
#     url = r'https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber='+str(isnumbers[issue])+r'&punumber=4149689'  #每期首页 用于爬取论文号
#     html = getHtml(url)
#     url_lst = getUrl(html)  #'arnumber='  提取论文编号
#     print(url_lst)
#
#     filename = r'C:\Users\class\Desktop\cookie.txt'  # 存放cookies的路径
#     cookie = cookiejar.MozillaCookieJar(filename)  # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
#     handler = request.HTTPCookieProcessor(cookie)  # cookie处理器
#     opener = request.build_opener(handler)  # 创建opener
#     respnse = opener.open(url)
#     cookie.save(ignore_discard=True, ignore_expires=True)
#
#     for each_arnumber in url_lst[:]:  #each_arnumber[9:]为arnumber
#         new_url = root_url_1 + isnumbers[issue] +root_url_2 + each_arnumber[9:] +root_url_3+each_arnumber[9:]+root_url_4+isnumbers[issue]
#         print(new_url)
#         download(issue+1,new_url,each_arnumber[9:],save_path)



# TIP
'''
https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8167422&filter=issueId%20EQ%20%228167422%22&pageNumber=1
https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8167422&filter=issueId%20EQ%20%228167422%22&pageNumber=2
https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8167422&punumber=83

  + {isnumber} + %22&rowsPerPage=100&pageNumber=1&resultAction=REFINE&resultAction=ROWS_PER_PAGE&isnumber= + {isnumber}

https://ieeexplore.ieee.org/xpl/tocresult.jsp?filter=issueId%20EQ%20%228167422%22&rowsPerPage=100&pageNumber=1&resultAction=REFINE&resultAction=ROWS_PER_PAGE&isnumber=8167422
'''

'''
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8255675  # 2018 -1
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8036263

https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8417897

https://ieeexplore.ieee.org/ielx7/83/8071125/08255675.pdf?tp=&arnumber=8255675&isnumber=8071125
https://ieeexplore.ieee.org/ielx7/83/8071125/08255675.pdf?tp=&amp;arnumber=8255675&amp;isnumber=8071125

https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8071125&punumber=83
https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8071125&punumber=83#

https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8103362&punumber=83

https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=8453260&punumber=83  # isuue12
'''



if __name__=='__main__':
    homeUrl = 'https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=7855880&punumber=83'
    # saveCookie(url='https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8255675', savepath=r'C:\Users\class\Desktop\TIP-2018\TIP_cookie.txt')
    html = getHtml(homeUrl)

    reg =r'<ul id="pi-2018"(.*?)</ul>'
    list_all_issues = re.findall(reg, html, re.S | re.M)[0]
    reg = r'<a href="(/xpl/tocresult.jsp?.*?)">'
    list_all_issues = re.findall(reg, list_all_issues, re.S | re.M)  # 每期的首页URL

    savepath = r'C:\Users\class\Desktop\TIP-2018'
    # 对每期首页爬取文章编号
    root_issue_url_1 = 'https://ieeexplore.ieee.org/xpl/tocresult.jsp?filter=issueId%20EQ%20%22'
    root_issue_url_2 = '%22&rowsPerPage=200&pageNumber=1&resultAction=REFINE&resultAction=ROWS_PER_PAGE&isnumber='

    for issue in range(1, 13):
        single_url = list_all_issues[issue-1]

        isnumber = re.split(r'[?|&|=]', single_url)[2]  # 期编号

        issue_complete_url = root_issue_url_1+isnumber+root_issue_url_2+isnumber
        html = getHtml(issue_complete_url)  # 获取每期首页的html
        reg_paper_numbers = r'arnumber=\d{7}'
        reg_paper_titles = r'"Download or View the PDF:(.*?)"'
        all_paper_numbers = re.findall(reg_paper_numbers, html, re.M|re.S)  # 文章编号
        all_paper_titles = re.findall(reg_paper_titles, html, re.M|re.S)    # 文章对应title
        root_pdf_url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&'
        for paper_num in range(len(all_paper_numbers)):
            single_paper_number = all_paper_numbers[paper_num]
            single_paper_title = all_paper_titles[paper_num]

            single_paper_url = root_pdf_url+single_paper_number


            html = getJsHtml(single_paper_url)
            if html== None:
                continue
            html = html.replace("amp;", "")
            true_url_list = re.findall(r'src="(https://ieeexplore.ieee.org/ielx7.*?\.pdf?.*?)"', html, re.M|re.S)
            if len(true_url_list) == 0:
                true_url = re.findall(r'pdfUrl":"(/stamp/stamp.jsp?tp=.*?)"', html, re.M|re.S)
                if len(true_url) == 0:
                    continue
                else:
                    true_url = 'https://ieeexplore.ieee.org'+true_url

            else:
                true_url = true_url_list[0]

            attempts = 0
            success = False

            while attempts < 3 and not success:
                try:
                    download(issue, true_url, single_paper_title, savepath)
                    success = True
                except:
                    attempts += 1
                    if attempts == 3:
                        break
            if success==False:
                print('！！！！！！！！！！！！！！！！%d！！！！！！！！%s下载失败！！！！！！！！！！！！！！！！！！' % (issue, true_url))
                continue
            print('--%d---%s已完成---'%(issue, true_url))
    print(list_all_issues)



