# 部署流程
## I:启用前端应用，从[Live2DMascot](https://github.com/Arkueid/Live2DMascot)仓库下载后，修改config.json文件
```sh
"ChatAPI" : 
{
	"ChatSavePath" : "chat",  //聊天音频和文本保存路径
	"CustomChatServer" : 
	{
		"HostPort" : "http://yourhost:8080",  //服务器地址，端口默认8080
		"On" : true,  //开启自定义聊天接口
		"ReadTimeOut" : 114,  //等待响应时间(s)
		"Route" : "/chat"  //路径
	},
```
## II:server端启动后端api程序(Windows也可以)
使用pyopenjtalk，如果如何安装cmake?:
在Github自带的codespace或者windows下安装的Visual Studio Code，都可以下载插件![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/moe/VSC.png)
点击install就可以安装了
## Linux
```sh
#Click Code && codespaces and start
#Installing cmake and FFmpeg,showing FFmpeg,since cmake can be installed directly in the Extensions
sudo apt update
sudo apt upgrade
sudo apt install ffmpeg
ffmpeg -version
#Creating enviornments
conda create -n chatbot python=3.8
conda init bash
bash
conda activate chatbot
git clone https://huggingface.co/Mahiruoshi/vits_with_chatbot
cd vits_with_chatbot
pip install -r requirements.txt

# 控制面板兼启动文件
python main.py
# * Running on http://127.0.0.1:8080
# * Running on http://172.16.5.4:8080
#Running on local URL:  http://127.0.0.1:7860
#端口号7860是面板，8080是api
```
## Window
## I 安装[FFmpeg](https://zhuanlan.zhihu.com/p/118362010)并且添加环境变量
## II.安装[Torch+gpu](https://blog.csdn.net/qq_44173699/article/details/126312680)(如需cpu推理则跳过)
## III.[cmake及pyopenjtalk安装(可略过)](https://www.bilibili.com/video/BV13t4y1V7DV/?spm_id_from=333.880.my_history.page.click)
## Iv.使用封装版的Japanese cleaner,用该text[文件夹](https://github.com/Paraworks/vits_with_chatgpt-gpt3/tree/window/text)替换原本的text文件夹,然后从该仓库的release中[下载](https://github.com/NaruseMioShirakana/JapaneseCleaner)，将cleaners压缩包解压至vits项目的路径下
![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/moe/c4.png)

## V.python创建虚拟环境后 
```sh
git clone https://huggingface.co/Mahiruoshi/vits_with_chatbot
cd vits_with_chatbot
pip install -r requirements.txt
python main.py
```
# 面板说明
## 完成chatbot方式选择及vits模型加载
![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/moe/p2.png)
可供选择的方式: gpt3.5/gpt3的api，CHATGLM
方法：将路径或者api key填写进文本框中
## 测试api是否启动
![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/moe/p3.png)
# 对于 text_to_sequence相关错误
```sh
#在推理中，可能出现symbols相关错误，这主要是由于不同text cleaner之间的冲突导致的
line 85, in infer
seq = text_to_sequence
#需要你在这一行自行修改
#如果需要
seq = text_to_sequence(text, symbols=hps.symbols, cleaner_names=hps.data.text_cleaners)
#如不需要，把 symbols=hps.symbols 删掉
```
# 已废弃：从release中下载前端，解压后直接运行
删除 api_launch.py中的注释，恢复相关api
```sh
#Input url after game or setting it in the basic/game/script.rpy: label setting0:
$ web_base = renpy.input("输入后端api的地址，如本地推理为'http://127.0.0.1:8080'，终端运行inference_api.py时查看",length=100)
#Replace it to:
$ web_base = 'your_onw_web'
```
## What to do with game?
[Official website of RenPy](https://www.renpy.org/)
You can follow the instructions and beautify your game, can take my game given as a reference.

## 极速入门renpy
抛弃那些花里胡哨的设置，只编辑script.rpy。交互式live2d的核心代码
```sh
#定义角色,这个类将会继承我们需要的live2d模型和语音文件这些花里胡哨的东西
define Character1 = Character("First Character")
#为游戏配置live2d，你需要在安装renpy后将从live2d官网下载的cublism for native压缩包放到renpy的目录下，之后点开renpy按照指示自动加载。
define config.gl2 = True
#导入live2d模型,大部分live2d模型的文件夹名字和model3文件的名字相同，可以直接将路径名设置为文件夹的名字，保险起见也可直接对应model3文件
image Character1 = Live2D("live2d/hiyori",loop=True)
#一定要有一个"开始"场景，场景用label标记。
label start:
#导入背景图片，在image 处自定义，格式‘bg name.png’,中间要带空格号，我也不知道为什么要这样设定
    show bg name
    #加载live2d动作，参考https://www.renpy.cn/doc/live2d.html
#live2d模型都有自己的动作名，你可以在model3文件中查看，也可以自己用动作捕捉工具(steam里搜vtuber)自定义。
    show Character1 m04
#renpy有两种加载python命令的方式，一种是"$ "+代码，另外一种是"Python:"，下一行缩进后编写，这里先用"$ "
#导入需要的库
    $ import requests
    $ import os
    $ import threading 
#这些参数是我认为适合在应用端设定的
#spk_id是vits模型中的人物id，vits多人模型通过变化spk_id来修改说话人
    $ global spk_id
#your_name是为了增加代入感和gpt3的chatbot聊天用的，chatgpt则不需要
    $ global your_name
#open_api_key则是每个人特有的，你也可以从官网上复制好后直接存储在游戏中
    $ global open_api_key
#web_base就是程序生成的网址，我设定的程序都是host/route_nameX?parameter1=[your_input1]&parameter2=[your_input2]......&parameter3=[your_input3]这种形式，你也可以改成表单
    $ global web_base
#这三个是vits用到的参数，樱花妹说中文还是需要仔细调的，不然很难听进去。特别是轻量化模型，日文也需要()
    $ global noise_scale
    $ global noise_scale_w
    $ global speaking_speed
#jump直接切换至下一场景
    jump setting0
return

label setting0:
#renpy需要在python命令中用renpy.input获取文本输入，这样就可以修改参数了。调试后可以将这些参数存储在游戏文件中。
    $ web_base = renpy.input("输入后端api的地址，如本地推理为'http://127.0.0.1:8080'，终端运行inference_api.py时查看",length=100)
    jump sense1

label sense1:
#获取当前项目所在路径，创建存储音频文件的路径
    $ current_work_dir = os.path.dirname(__file__)
    $ weight_path = os.path.join(current_work_dir, 'temp.ogg')
    $ weight_path = weight_path.replace("\\","/")
#交互的第一步
    $ your_text = renpy.input('',length=60)
#合成网址用来发送请求(本来只有需传入文本就行了，后来参数越传越多)
    $ webs = web_base + "/gpt?text="+ your_text
#这就是另外一种插入python指令的方法了，用treading实现同步运行
    python:
        def get_voice():
            res = requests.get(webs)
            music = res.content
            with open(weight_path, 'wb') as code:
                code.write(music)
            web2 = web_base + "/word"
            answer = requests.get(web2).text
            global answer
#            os.system(weight_path)
        thread = threading.Thread(target=get_voice)
        thread.start()
#这是选择界面，决定是否要remake
menu:
    "查看回复":
        jump reply
    "重新设定":
        jump setting0
#最后的展示阶段，可以自己添加动作，这里选择用voice播放声音而不是简单粗暴的os
label reply:
    show Character1 m02
    voice weight_path
    Character1 '[answer]'
    show Character1 m03
    jump sense1
```
# 由于openai将扩大对非官方api的打压力度，如以盈利为目的，建议采用官方的api key以及openai标准库
(私下里还是建议省钱滴)
