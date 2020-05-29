import os, sys
sys.path.append(os.getcwd())
from base.page_base import PageBase  # 导入页面基类
from selenium.webdriver.common.by import By


class PageSearch(PageBase):
    #这里一会放元素特征
    button_fdj=By.ID, "com.android.settings:id/search";
    input_searchText=By.ID, "android:id/search_src_text";

    def __init__(self, driver):
        PageBase.__init__(self, driver)  # 初始化父类的构造函数

    #这里一会放功能函数
    def click_fdj(self):
        self.click(self.button_fdj);

    def input_search(self,data):
        self.input_text(self.input_searchText,data);
