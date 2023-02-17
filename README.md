## WFRobertQL

这是WF·Robert的脚本库，暂时只适配青龙使用

### ddnsto-renewal.py

这是DDNSTO自动续费7天的脚本，在青龙里搭建

#### 环境变量：

**名称:** `DDNSTO_COOKIE` 

**值:** 自己从ddnsto的控制台F12获取

![image-20230217095158313](https://cdn.jsdelivr.net/gh/HeiDaotu/img-bucket/img/202302170953921.png)

#### 依赖管理：

**名称:** `pip install fake_useragent`

![image-20230217100516407](https://cdn.jsdelivr.net/gh/HeiDaotu/img-bucket/img/202302171005288.png)

#### 订阅管理：

**链接输入:** `https://github.com/HeiDaotu/WFRobertQL.git`

其他字段随意填写

![image-20230217094726090](https://cdn.jsdelivr.net/gh/HeiDaotu/img-bucket/img/202302170953031.png)

#### 定时任务：

**名称:** 随意

**命令行输入:**`task HeiDaotu_WFRobertQL_main/ddnsto-renewal.py` 

**定时规则:** 推荐一周运行2次即可，可参照我的`34 30 7 * * 1,5 `

![image-20230217095019008](https://cdn.jsdelivr.net/gh/HeiDaotu/img-bucket/img/202302170953427.png)