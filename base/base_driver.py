# fileName:base_driver.py
from appium import webdriver


# 函数功能：封装了前置代码，并返回driver对象
def init_driver():
    # server 启动参数
    desired_caps = dict()
    # 设备信息
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1.1'
    desired_caps['deviceName'] = '192.168.164.101:5555'
    # app信息
    desired_caps['appPackage'] = 'com.jym.mall'  # 交易猫app
    desired_caps['appActivity'] = '.home.ui.HomeActivity'  # 首页"交易"选项卡的UI名
    # 中文
    desired_caps['unicodeKeyboard'] = True
    desired_caps['resetKeyboard'] = True
    # toast
    desired_caps['automationName'] = 'Uiautomator2'
    # True,不重置应用。默认Appium每次运行时都会重置app，即清除app中所有使用的数据，即回到app刚安装完的状态！
    # desired_caps['noReset'] = True
    # 声明对象
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver
