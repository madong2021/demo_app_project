# filename:page_base.py
from selenium.webdriver.support.wait import WebDriverWait  # 导入显式等待类WebDriverWait类
from selenium.webdriver.common.by import By


# 页面类的基类,被其他页面类继承
class PageBase:
    # 辅助函数
    '''
    函数功能：拼接XPATH字符串中间部分（不过，后面会多个"and"）。例如：XPATH字符串"//*[contains(@text,'设')]"的中间部分是"contains(@text,'设')"!
    即：
    如果loc 给 "text,设置"或"text,设置,0",函数返回"contains(@text,'设置')and"，情况1！
    如果loc = "text,设置,1",函数返回"@text='设置'and"，情况2！
    '''

    def make_xpath_with_unit_feature(self, loc):
        args = loc.split(",")
        feature = ""  # 返回值

        if len(args) == 2:
            feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and "
        elif len(args) == 3:
            if args[2] == "1":
                feature = "@" + args[0] + "='" + args[1] + "'" + "and "
            elif args[2] == "0":
                feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and "
        return feature

    '''
    函数功能：给简化的xpath，函数返回标准的xpath字符串。
    即:
    如果loc = "text,设置"或"text,设置,0"，函数返回"//*[contains(@text,'设置')]"，情况1。
    如果loc = "text,设置,1"，函数返回"//*[@text='设置']"，情况2。
    如果loc = ["text,设置"] ，函数返回"//*[contains(@text,'设置')]"，情况1。
    如果loc = ["text,设置", "index,20,1", "index1,50"]，函数返回"//*[contains(@text,'设置')and@index='20'andcontains(@index1,'50')]"，情况3。
    如果loc = "//*[contains(@text,'设')]" ，即故意传个正常的xpath字符串，函数返回"//*[contains(@text,'设')]"，情况4。
    '''

    def make_xpath_with_feature(self, loc):
        feature_start = "//*["
        feature_end = "]"
        feature = ""

        # 如果传的是字符串，即情况1和情况2
        if isinstance(loc, str):
            # 如果是正常的xpath，即情况4
            if loc.startswith("//"):
                return loc
            feature = self.make_xpath_with_unit_feature(loc)
        else:  # 如果传的是列表，即情况3
            for i in loc:
                feature += self.make_xpath_with_unit_feature(i)

        feature = feature.rstrip("and ")  # 删除最右侧的"and "
        ret_loc = feature_start + feature + feature_end
        return ret_loc

    # 辅助函数，被下面的click函数调用
    # 函数功能：找满足定位条件loc的单个元素。
    # 形参loc：定位元素的条件，loc类似“By.XPATH,"text,Display,1"”、“By.ID,"k001"”。
    # 形参time：总共搜索time秒。单位是秒！
    # 形参poll：每poll秒搜索一次。单位是秒。
    def find_element(self, loc, time=5.0, poll=1.0):
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:
            value = self.make_xpath_with_feature(value)
        # 下面的是“x”是“self.driver”
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_element(by, value))

    # 辅助函数,本案例中未被调用
    # 函数功能：找满足定位条件loc的一组元素。
    # 形参loc：定位元素的条件，loc类似“By.XPATH,"text,Display,1"”、“By.ID,"k001"”。
    # 形参time：总共搜索time秒。单位是秒！
    # 形参poll：每poll秒搜索一次。单位是秒。
    def find_elements(self, loc, time=5.0, poll=1.0):
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:
            value = self.make_xpath_with_feature(value)
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_elements(by, value))

    def __init__(self, driver):
        self.driver = driver

    # 函数功能：对loc定位的某元素进行单击
    def click(self, loc):
        self.find_element(loc).click()  # 调用辅助函数

    # 函数功能：对按钮loc进行单击（会自动上滑找按钮）
    # 形参loc：某按钮的元素特征！
    def click_scroll(self, loc, time=5.0, poll=1.0):
        while True:
            try:
                self.find_element(loc, time, poll).click();
                break;
            except Exception:
                self.scroll_page_one_time();

    # 函数功能：点击可能存在的弹窗广告.如果弹窗未出现，直接什么都不做
    def click_tancuan(self, loc, time=5.0, poll=1.0):
        try:
            ele = self.find_element(loc, time, poll)
            ele.click();
        except:
            pass

    # 函数功能：对loc定位的某元素进行输入文本text
    def input_text(self, loc, text):
        self.find_element(loc).send_keys(text)  # 调用辅助函数

    # 函数功能：给输入框输入数据data(会自动上滑的找输入框)！
    # 形参loc：该输入框的元素特征。
    # 形参data：要输入的数据，String类型！
    def input_text_scroll(self, loc, time=5.0, poll=1.0, data=None):
        if data is not None:
            while True:
                try:
                    self.find_element(loc, time, poll).send_keys(data);
                    break;
                except Exception:
                    self.scroll_page_one_time();

    # 函数功能：对loc定位的某元素的文本内容进行清空操作！
    def clear(self, loc):
        self.find_element(loc).clear()

    # 自己封装的press_keycode:能同时适用于Uiautomator1框架和Uiautomator2框架
    # 形参keycode：安卓系统的keyCode，例如4，就是返回键
    def press_keycode(self, keycode):
        if "automationName" not in self.driver.capabilities.keys():
            self.driver.keyevent(keycode)
        elif self.driver.capabilities["automationName"] == "Uiautomator2":
            self.driver.press_keycode(keycode)

    # 函数：点击“返回键”
    def press_keycode_back(self):
        self.press_keycode(4)

    # 函数：点击“home”键
    def press_keycode_home(self):
        self.press_keycode(3)

    # find_toast函数的版本1，不太精简
    # 函数功能：根据toast的部分文本内容message找toast，并返回toast的全部文本内容！
    # 形参message: 预期要获取的toast的部分文本内容。比如你toast的文本内容是"登录成功",那么message可以给"成功"。
    # def find_toast(self,message, timeout=3,poll=0.1):
    #     xpath_str = "//*[contains(@text,'" + message + "')]"  # 使用包含的方式定位toast
    #     # toast = driver.find_element(By.XPATH, xpath_str) #不用显式等待时也OK，但是不好
    #     toast = WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(By.XPATH, xpath_str))
    #     return toast.text  # 返回toast的整个文本内容

    # find_toast函数的版本2
    # 函数功能：根据toast的部分文本内容message找toast，并返回toast的全部文本内容！
    # 形参message: 预期要获取的toast的部分文本内容。比如你toast的文本内容是"登录成功",那么message可以给"成功"。
    # 形参is_screenshot：是否截图。默认是不截图。
    # 形参screenshot_name:如果截图，这里给图片名。
    def find_toast(self, message, is_screenshot=False, screenshot_name=None, timeout=3, poll=0.1):
        xpath_str = "//*[contains(@text,'" + message + "')]"  # 使用包含的方式定位
        toast = self.find_element((By.XPATH, xpath_str), timeout, poll)
        if is_screenshot:
            self.screenshot(screenshot_name)
        return toast.text  # 返回toast的整个文本内容

    # is_toast_exist函数的版本1：里面有函数调用，可能增大CPU
    # 函数功能：根据toast的部分文本内容message来判断toast是否存在。如果存在，就返回True。
    # def is_toast_exist(self, message, is_screenshot=False, screenshot_name=None, timeout=3, poll=0.1):
    #     try:
    #         self.find_toast(message, is_screenshot, screenshot_name, timeout, poll)
    #         return True
    #     except Exception:
    #         return False

    # is_toast_exist函数的版本2
    # 函数功能：根据toast的部分文本内容message来判断toast是否存在。如果存在，就返回True。
    def is_toast_exist(self, message, is_screenshot=False, screenshot_name=None, timeout=3, poll=0.1):
        try:
            # 定位toast
            xpath_str = "//*[contains(@text,'" + message + "')]"  # 使用包含的方式定位toast
            toast = self.find_element((By.XPATH, xpath_str), timeout, poll)
            # print(toast.text);#输出toast的整个文本内容
            if is_screenshot:
                self.driver.get_screenshot_as_file("./screen/" + screenshot_name + ".png")
            return True
        except Exception:
            return False

    # 函数功能：截图
    def screenshot(self, file_name):
        self.driver.get_screenshot_as_file("./screen/" + file_name + ".png")

    # 函数功能：滑动本函数一次，滑动一次屏幕。
    # 形参direction:指定滑动的方向！down：由下往上滑，默认值！up:由下往下滑。left：由左往右滑。right：由右往左滑！
    # 形参duration：整个滑动过程的持续时间，单位是毫秒。这个值越大，滑动约准确！
    def scroll_page_one_time(self, direction="down", duration=5000):
        window_size = self.driver.get_window_size()
        window_height = window_size["height"]
        window_width = window_size["width"]
        up_y = window_height * 0.25
        down_y = up_y * 3
        left_x = window_width * 0.25
        rigth_x = left_x * 3
        center_x = window_width * 0.5
        center_y = window_height * 0.5

        if direction == "down":
            self.driver.swipe(center_x, down_y, center_x, up_y, duration)
        elif direction == "up":
            self.driver.swipe(center_x, up_y, center_x, down_y, duration)
        elif direction == "left":
            self.driver.swipe(left_x, center_y, rigth_x, center_y, duration)
        elif direction == "right":
            self.driver.swipe(rigth_x, center_y, left_x, center_y, duration)
        else:
            raise Exception("请输入正确的direction参数：down、up、left、right")

    # 根据元素特征来判断元素是否存在。即墨：所有查找元素都是在当前手机屏幕上操作！
    def is_loc_exist(self, loc):
        try:
            self.find_element(loc)
            return True
        except Exception:
            return False

    # 判断某app的app名（即该app的在桌面上的显示名）是否在安卓系统的这些桌面上存在。即判断这些桌面上是否有该app！
    # 形参num：安卓系统总共几个桌面就给几。这样给值，如果安卓系统总共有N个桌面，那么num=N即可！
    def is_desktop_has_app(self, app_name, num):
        # home键：按一次，回到原来的桌面；再按一次，回到第1桌面（即最左侧的桌面）！
        self.press_keycode_home()  # 点击“Home键”一次
        self.press_keycode_home()  # 再点击“Home键”一次，此时手机屏幕一定是在第1桌面上！

        for i in range(num):
            # 例如：(By.XPATH,"text,交易猫,1")
            if self.is_loc_exist((By.XPATH, "text," + app_name + ",1")):  # 在当前桌面上查找该app的显示名。是精确匹配！
                return True
            else:
                self.scroll_page_one_time("right")  # 滑动屏幕到下一个桌面
        return False
