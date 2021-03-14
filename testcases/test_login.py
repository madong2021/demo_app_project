import os, sys
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from app_project.base.base_yaml import yml_data_with_filename_and_key
from app_project.base.base_driver import init_driver
from app_project.page.page_login import PageLogin  # 导入此页面类
from appium import webdriver

sys.path.append(os.getcwd())


# 辅助函数：用于再处理测试数据
def data_with_key(key):
    return yml_data_with_filename_and_key("data_login", key)


class TestLogin:
    def setup(self):
        self.driver = init_driver()
        self.page_login = PageLogin(self.driver)

    def teardown(self):
        self.driver.quit()

    @pytest.mark.parametrize("dict_data", data_with_key("test_login"))
    def test_login(self, dict_data):  # 形参dict_data是字典类型
        username = dict_data["username"];
        pwd = dict_data["pwd"];
        toast = dict_data["toast"];
        screen = dict_data["screen"];
        # 步骤1：点击“我的”选项卡
        self.page_login.click_my();
        # 步骤2：点击“登录/注册”
        self.page_login.click_loginreg();
        # 步骤3：点击“用UC账号登录”或“切换到旧版登录”
        self.page_login.click_uc();
        # 步骤4：输入手机号
        self.page_login.input_zanhao(username)
        # 步骤5：输入密码
        self.page_login.input_pwd(pwd);
        # 步骤6：点击“登录”按钮
        self.page_login.click_login();
        # 步骤7：利用toast来判断是否登录成功
        ret = self.page_login.is_toast_exist(toast, True, screen, 10);
        assert ret;
