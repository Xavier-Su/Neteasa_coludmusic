from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree

bro = webdriver.Chrome(executable_path='./chromedriver.exe')
bro.get('https://music.163.com/')
search_input = bro.find_element_by_id('srch')
search_input.send_keys('刘珂矣')
search_input.send_keys(Keys.ENTER)

page_text = bro.page_source
print(page_text)
tree = etree.HTML('page_text')
id_num = tree.xpath('//div[@class="text"]/a')
#id_num = tree.xpath('//span[@class="s-fc7"]//text()')
print(id_num)
