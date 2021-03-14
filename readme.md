# 接口自动化测试框架之ddt数据驱动
本框架主要用python语言实现，采用po的设计思想，以pytest单元测试框架为基础，采用yaml文件来管理测试用例。
## 项目框架说明
- base：自己封装的公共方法类
   - base_driver.py 
   - base_yaml.py 
   - page_base.py 
- data:用来管理用例
   - data_login.yaml
- page:po层，用来封装各个页面或模块
   - page_login.py
- report:日志存放
- screen:失败截图存放
- testcases:测试用例存放层，用例采用链式调用
## 使用说明
先拉取到本地，然后导入依赖包:

`pip install -r requirements.txt`

## 什么样的项目适合此框架
- 1.app端ui自动化
---
注意： 使用的过程中遇到什么问题，请发邮件到qq邮箱：1067164043@qq.com