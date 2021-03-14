import os, sys
from demo_app_prject.base.page_base import PageBase # 导入页面基类
from selenium.webdriver.common.by import By

sys.path.append(os.getcwd())

class PageLogin(PageBase):
    # 这些是抽取元素特征
    button_my = By.XPATH, ["text,我的,1", "resource-id,com.jym.mall:id/indicator_tab_tv,1"]  # "我的"选项卡
    text_loginreg = By.XPATH, ["text,登录/注册,1", "resource-id,com.jym.mall:id/user_account,1"]  # “我的”选项卡中的“登录/注册”按钮
    button_uc = By.XPATH, "resource-id,com.jym.mall:id/btn_login_uc,1"  # 用“UC”账号登录
    text_zanhao = By.XPATH, "text,手机/邮箱/用户名/UC号,1"  # “账号”文本框
    text_pwd = By.XPATH, ["resource-id,com.jym.mall:id/login_input,1", "password,true,1"]  # “密码”文本框
    button_login = By.XPATH, ["text,登录,1", "resource-id,com.jym.mall:id/login_normal,1"]  # 登录按钮

    def __init__(self, driver):
        PageBase.__init__(self, driver)

    # 这里写各种被脚本类调用的各种功能函数
    # 函数功能：找到并点击“我的”选项卡
    def click_my(self):
        self.click(self.button_my)

    # 函数功能：找到并点击“登录/注册”
    def click_loginreg(self):
        self.click(self.text_loginreg);

    # 函数功能：找到点击“用UC账号登录”
    def click_uc(self):
        self.click(self.button_uc);

    # 函数功能：输入手机号
    def input_zanhao(self, zanhao):
        self.input_text(self.text_zanhao, zanhao);

    # 函数功能：输入密码
    def input_pwd(self, pwd):
        self.input_text(self.text_pwd, pwd)

    # 函数功能：点击“登录”按钮
    def click_login(self):
        self.click(self.button_login)
