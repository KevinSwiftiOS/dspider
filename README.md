dspider
========

一个基于Selenium的以Django为爬虫框架的爬虫系统.

- 用Python编写
- Web管理界面包含任务监控、项目管理、结果查看
- 数据库使用MongoDB(注意：不要设置密码)
- Python版本3.4以上

[![Demo]


Installation
------------

* `pip install -r requirements.txt`
* run command `python manage.py runserver`, visit [http://localhost:8000/spider/](http://localhost:8000/spider/)

**WARNING:** WebUI is open to the public by default, it can be used to execute any command which may harm your system. Please use it in an internal network or [enable `need-auth` for webui](http://docs.pyspider.org/en/latest/Command-Line/#-config).

Quickstart: [http://docs.pyspider.org/en/latest/Quickstart/](http://docs.pyspider.org/en/latest/Quickstart/)


License
-------
Licensed under the Apache License, Version 2.0
