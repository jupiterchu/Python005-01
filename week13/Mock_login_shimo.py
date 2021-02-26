import time

from selenium import webdriver

DRI_PATH = 'chromedriver.exe'

chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(options=chrome_option, executable_path=DRI_PATH)

browser.get('https://shimo.im/login?from=home')
username = browser.find_element_by_xpath('//input[@name="mobileOrEmail"]')
username.send_keys('account')
password = browser.find_element_by_xpath('//input[@name="password"]')
password.send_keys('password')
button = browser.find_element_by_xpath('//button[@type="black"]')
button.click()

print('等待用户点击验证码...')
time.sleep(30)
print('登录成功')