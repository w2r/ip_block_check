# IP_Block_Check

#### 简介：

迫于墙时不时发飙，自己的小鸡又比较多，特意写了一个tg机器人定时检测ip/port是否被墙(端口查询调用了www.toolsdaquan.com的api，在此表示十分感谢)。

#### 使用方法 ：

##### 快餐：      

关注tg机器人@ip_block_check_bot

==注意：若使用机器人，机器人会暂时你的ip，可以自己选择删除==

具体操作指令如下：

~~~shell
# 域名或者ip格式必须是IP/Port
# 默认机器人会每天12:00:00推送已保存ip的查询结果
# 查询域名www.google.com
&ip_check www.google.com/80
# 查询140.238.33.201/22
&ip_check 140.238.33.201/22
# 查询已保存域名
&ip_saved
# 删除域名记录140.238.33.201/22
&ip_delete 140.238.33.201/22
~~~

##### 自我搭建：

###### 第一步：

telegram自建机器人，并获得机器人的botapi，api格式如下：

~~~
981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3ZA********
~~~

###### 第二步：

从github拉取代码，并修改代码bot api部分，具体修改如下：

~~~
# ip_block_check第12行，请替换为自己的botapi
https://api.telegram.org/bot981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3**********
# post2tg第16行，请替换为自己的botapi
https://api.telegram.org/bot981790366:AAHPBpLzVZXzvRiAV4jx7HHJ3**********
~~~

###### 第三步：

服务器配置，本代码运用环境为python3，同时需要自行安装MongoDB(我的服务器配置centos7.7 + python3 + mongodb 3.4)

python3需要安装的依赖库：

~~~
pip3 install requests
pip3 install torequests
pip3 install pymongo
~~~

效果图：

![](https://i.postimg.cc/QN0tYBzD/cherbim-2019-10-05-20-56-16.jpg)

