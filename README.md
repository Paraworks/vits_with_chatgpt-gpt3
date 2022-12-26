## 极速入门renpy
抛弃那些花里胡哨的设置，加载交互的核心代码
```sh
define Character1 = Character("Your_Character_Name")
define config.gl2 = True
image Setsuna = Live2D("normal", top=0.0, base=0.7, height=1.0,loop=True)
# '游戏'在此开始。

label start:
#导入背景图片，在image 处自定义，格式‘bg name.png’
    show bg r
    #加载live2d动作，参考https://www.renpy.cn/doc/live2d.html
    show Setsuna daiji_idle_01
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
