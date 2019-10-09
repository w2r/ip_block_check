# 自主搭建查询api接口

#### 简介：

迫于不会php，之前一直偷偷摸摸调用别人的api接口，正好论坛有mjj分享了php源码，就决定自行搭建自己的api接口了。（开源地址：https://gitee.com/KIENG_S/jianchaipshifouzuduan，感谢mjj开源）

##### 操作步骤

##### 第一步：

首先你要有两台小鸡，一台国内机A，一台国外机B，配置至少512M内存，测试环境为:宝塔面板 PHP7.0 + nginx1.15（比较吃内存），exec()默认禁用状态，需要自行开启（具体位置，php设置，禁用函数，把exec删除），然后下载源码，源码地址如下：https://gitee.com/KIENG_S/jianchaipshifouzuduan

##### 第二步：

在小鸡上分别新建网站，然后把源码解压到网站根目录，直接覆盖即可，然后编辑index.html文件，把get请求改成你的网站域名地址，如下图：

![](https://mjj.today/temp/1910/ec034efc07983847.png)

第一个要改成国内网站域名，第二个改成国外网站域名，然后打开网站即可访问，若是不想让别人访问你的站点，直接删除index.html文件，附上测试站点：

http://api.qingyushop.ml/

##### 第三步：

替换文件1——check.php

为了适配主程序，对返回结果进行修改，大家可自主修改，或者直接用修改完的文件

主要修改内容：返回结果open替换为success，close和timeout替换成fail

替换文件2——result_update.py

需要自己抓取curl链接，具体操作步骤：

1. 谷歌浏览器打开你的测试站点，F12审查，然后打开network

2. 然后随意查询网址/端口，network会生成两个连接，鼠标右键点击，copy， copy as curl （bash），然后你会得到两个连接，格式如下

   ~~~
    # 注意国内和国外连接
    # 国内连接
    curl 'http://www.cherbim.com/check.php' -H 'Accept: */*' -H 'Referer: http://api.qingyushop.ml/' -H 'Origin: http://api.qingyushop.ml' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' --data 'ip=195.133.146.64&port=22' --compressed --insecure
    # 国外连接
    curl 'http://api.qingyushop.ml/check.php' -H 'Cookie: __cfduid=dcda57671c2ae2a72ce54d68367ec16001565742656' -H 'Origin: http://api.qingyushop.ml' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://api.qingyushop.ml/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'ip=195.133.146.64&port=22' --compressed --insecure
    # 替换result_update中连接（第16行和18行）替换过程如下：
    # 把ip地址换成{0},端口号改成{1}，然后辅助，替代脚本中""""""中内容
    # 国内 curl_3 = r"""替换内容"""format.(site, port),只需要更改替换内容即可
    # 国外 curl_4 = r"""替换内容"""format.(site, port),只需要更改替换内容即可
~~~
   
3，将result_update.py，改为result.py，直接覆盖原本的result.py
   
   



