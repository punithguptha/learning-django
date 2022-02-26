from selenium import webdriver
from selenium.webdriver.firefox.service import Service


service_var=Service("../tdd/bin/geckodriver.exe")
browser=webdriver.Firefox(service=service_var)
browser.get('http://localhost:8000')

assert browser.page_source.find("install")
