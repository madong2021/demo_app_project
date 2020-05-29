#filename:page_base.py
from selenium.webdriver.support.wait import WebDriverWait #导入显式等待类WebDriverWait类
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
    def make_xpath_with_unit_feature(self,loc):
        args = loc.split(",")
        feature = ""  # 返回值

        if len(args) == 2:
            feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and"
        elif len(args) == 3:
            if args[2] == "1":
                feature = "@" + args[0] + "='" + args[1] + "'" + "and"
            elif args[2] == "0":
                feature = "contains(@" + args[0] + ",'" + args[1] + "')" + "and"
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
    def make_xpath_with_feature(self,loc):
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

        feature = feature.rstrip("and")  # 删除最右侧的"and"
        ret_loc = feature_start + feature + feature_end
        return ret_loc

    # 辅助函数，被下面的click函数调用
    #函数功能：找满足定位条件loc的单个元素。
    #形参loc：定位元素的条件，loc类似“By.XPATH,"text,Display,1"”、“By.ID,"k001"”。
    #形参time：总共搜索time秒。单位是秒！
    #形参poll：每poll秒搜索一次。单位是秒。
    def find_element(self, loc,time=10,poll=1):
        by = loc[0]
        value = loc[1]
        if by == By.XPATH:
            value = self.make_xpath_with_feature(value)
        # 下面的是“x”是“self.driver”
        return WebDriverWait(self.driver, time, poll).until(lambda x: x.find_element(by, value))

    #辅助函数,本案例中未被调用
    #函数功能：找满足定位条件loc的一组元素。
    #形参loc：定位元素的条件，loc类似“By.XPATH,"text,Display,1"”、“By.ID,"k001"”。
    # 形参time：总共搜索time秒。单位是秒！
    # 形参poll：每poll秒搜索一次。单位是秒。
    def find_elements(self, loc,time=10,poll=1):
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

    # 函数功能：对loc定位的某元素进行输入文本text
    def input_text(self, loc, text):
        self.find_element(loc).send_keys(text)  # 调用辅助函数
