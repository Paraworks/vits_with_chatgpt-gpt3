## 极速入门renpy
抛弃那些花里胡哨的设置，只编辑script.rpy。加载交互式live2d的核心代码
```sh
#定义角色,这个类将会继承我们需要的live2d模型和语音文件这些花里胡哨的东西
define Character1 = Character("Your_Character_Name")
#为游戏配置live2d，你需要在安装renpy后将从live2d官网下载的cublism for native压缩包放到renpy的目录下，之后点开renpy按照指示自动加载。
define config.gl2 = True
#导入live2d模型,大部分live2d模型的文件夹名字和model3文件的名字相同，可以直接将路径名设置为文件夹的名字，保险起见也可直接对应model3文件
image Character1 = Live2D("Path/to/your_model/your_model.model3.json", top=0.0, base=0.7, height=1.0,loop=True)
#一定要有一个"开始"场景，用label展示
label start:
#导入背景图片，在image 处自定义，格式‘bg name.png’
    show bg r
    #加载live2d动作，参考https://www.renpy.cn/doc/live2d.html
    show Character1 daiji_idle_01
    $ import requests
    $ import os
    $ global spk_id
    $ global your_name
    $ global open_api_key
    $ global web_base
    $ global noise_scale
    $ global noise_scale_w
    $ global speaking_speed
    #vits模型中的人物id
    #基础参数设置
menu:
    'GPT3':
        jump setting0
    'CHATGPT':
        jump setting1
return

label setting0:
    $ web_base = renpy.input("输入后端api的地址，如本地推理为'http://127.0.0.1:8080'，终端运行inference_api.py时查看",length=100)
    $ open_api_key = renpy.input("填写你的API keys 网址：https://beta.openai.com/account/api-keys",length=1000)
    $ open_api_key = str(open_api_key)
    $ your_name = renpy.input("你的名字：",length=10)
    jump setting2


```
