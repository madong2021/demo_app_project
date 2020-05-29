import os, sys
sys.path.append(os.getcwd())

from base.base_driver import init_driver
from appium import webdriver
from pages.page_search import PageSearch
import time

class TestDisplay:
    def setup(self):
        self.driver = init_driver();
        self.page_search=PageSearch(self.driver);

    def teardown(self):
        time.sleep(5);
        self.driver.quit()

    def test_search(self):
        #步骤1：找到并点击“放大镜”
        self.page_search.click_fdj();
        #步骤2: 找到搜索框并输入"张三"
        self.page_search.input_search("张三");

