## WFRobertQL

>  这是WF·Robert的脚本库，暂时只适配青龙使用。

### 青龙

#### 依赖管理

点击青龙面板的依赖管理——>新建依赖——>选择Python3、自动拆分选择是、复制以下的依赖填到名称里——>点击确定，等待安装完成，已经有的依赖就不用安装了。

<details>
<summary>Python3依赖</summary>


```tex
beautifulsoup4
bs4
fake_useragent
requests
canvas
ping3
jieba
PyExecJS
aiohttp
```

</details>

![image-20230413142448646](https://fastly.jsdelivr.net/gh/HeiDaotu/img-bucket/img/202304131425904.png)

#### 订阅管理

我们需要把仓库的脚本添加到订阅里，这样可以获取脚本，同样可以不定时获取到最新的脚本(取决于你是否禁用)。

点击青龙面板的订阅管理——>新建订阅

- **名称：** 随便写，自己看得懂就行，或者直接写`WFRobert脚本库`
- **类型：** 公开仓库
- **链接：** `https://github.com/HeiDaotu/WFRobertQL.git`
- **定时类型：** crontab
- **定时规则：** 随意，或者写`0 0 6 * * ? `，每天6点自动拉取仓库。

其他值默认，点击确定即可。

最后点击订阅管理里面新增的这条信息，点击`运行`即可，这时候我们就可以在定时任务中看到拉取下来的脚本了，如果不想自动更新，自己禁用该订阅管理就行了。

#### 环境变量

环境变量每个脚本的变量名字不同，具体请查看文档：[参考文档](https://heidaotu.github.io/ScriptDocument/reference/)

#### 成品挂机平台

[WFRobert挂机平台](https://script.heitu.eu.org/#/)这我自己搭建的成品脚本站，可以直接在里面运行脚本，同样具体请查看文档：[参考文档](https://heidaotu.github.io/ScriptDocument/reference/)