# 这是一个焊接chatgpt/gpt3和vits的后端api程序
用api启动的主要目的是搭建lovelive的聊天网站，其实16号就已经把这个项目搞好了。因为lovelive不像邦邦和少歌那样有live2d模型，找各种方案搁置了一周多。看了别的up的视频后发现大家对这种形式的热情很高，就把这个放在文件夹里吃灰的项目拿出来了。
参考用链接http://43.159.36.6:8080/
项目地址https://drive.google.com/drive/folders/1vtootVMQ7wTOQwd15nJe6akzJUYNOw4d
解压live2d_chat-0.6(gpt3+chatgpt).zip，
运行游戏程序，
建议用renpy修改游戏程序，内置配置流程，自定义你的live2d模型和交互方式。

## How to launch API in your windows or server
(Suggestion) Python == 3.8/3.7
## Clone a VITS repository or iSTFT-VITS repository
```sh
git clone https://github.com/CjangCjengh/vits.git
#git clone https://github.com/innnky/MB-iSTFT-VITS
```
## Get the model and config
- See https://github.com/CjangCjengh/TTSModels or other repositorise in Github or huggingface
## Adding cleaners&inference_api.py to your project
- Noticing "text_cleaners" in config.json
- Edit 'text'dictionary in the VITS or iSTFT-VITS
- Remove unnecessary imports from text/cleaners.py
- The path of inference_api.py should be like path/to/vits/inference_api.py
- If you want to launch this project in your server, it is recommended to use iSTFT-VITS for tts: path/to/MB-iSTFT-VITS/inference_api.py
## Install requirements of vits enviornments
```sh
cd vits
#cd MB-iSTFT-VITS
pip install -r requirements.txt
```
## Build Monotonic Alignment Search and run preprocessing
```sh
# Cython-version Monotonoic Alignment Search
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd vits
#cd MB-iSTFT-VITS
```
## Install requirements for using GPT3/CHATGPT in python
```sh
pip install pydub 
pip install openai
#Not recommended due to demanding requirements
#pip install pyChatGPT
```
## Editing the path of configuration file in inference_api.py
```sh
line26:#设定存储各种数据的目录，方便查看，默认C:/project_file
line27:current_work_dir = os.path.dirname(__file__)
line28:weight_path = os.path.join(current_work_dir, '/project_file/')
line34:hps_ms = utils.get_hparams_from_file("path/to/config.json")
line43:_ = utils.load_checkpoint("path/to/checkpoint.pth", net_g_ms, None)
```
## For CPU inference in server or those who do not have cuda installed
```sh
#change this line to dev = torch.device("cpu")
line32:dev = torch.device("cuda:0")
```
## launch
```sh
python inference_api.py
```
## What to do next?
As you can see in the temminal
```sh
 * Serving Flask app 'inference_api'
 * Debug mode: on
INFO:werkzeug: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.[0m
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.0.0.14:8080
INFO:werkzeug: Press CTRL+C to quit
```
Which means you can try it in the game now
## Why using api?
不会真有人想每次都要启动一堆程序，配置个半天，吃电脑一大半内存和显存来跟纸片人聊天吧，反正我调试完之后肯定不会，20块一个月的服务器不香吗？
## Real usage for api
Building chatroom on my website. Now preparing the live2d models.
## Why not chatgpt?
You can edit it in the inference_api.py
```sh
line143:#CHATGPT抓取
line144:#session_token = '参考https://www.youtube.com/watch?v=TdNSj_qgdFk'
line145:#api = ChatGPT(session_token)
#Delate the comment in line200 and line233
```
If you want to chat with it indiscriminately as if it is your waifu, the company will stop you lol.
## What to do with game?
Official website of RenPy https://www.renpy.org/
You can follow the instructions and beautify your game, can take my game given as a reference.

## 极速入门renpy
抛弃那些花里胡哨的设置，只编辑script.rpy。交互式live2d的核心代码
```sh
#定义角色,这个类将会继承我们需要的live2d模型和语音文件这些花里胡哨的东西
define Character1 = Character("Your_Character_Name")
#为游戏配置live2d，你需要在安装renpy后将从live2d官网下载的cublism for native压缩包放到renpy的目录下，之后点开renpy按照指示自动加载。
define config.gl2 = True
#导入live2d模型,大部分live2d模型的文件夹名字和model3文件的名字相同，可以直接将路径名设置为文件夹的名字，保险起见也可直接对应model3文件
image Character1 = Live2D("Path/to/your_model/your_model.model3.json", top=0.0, base=0.7, height=1.0,loop=True)
#一定要有一个"开始"场景，场景用label标记。
label start:
#导入背景图片，在image 处自定义，格式‘bg name.png’,中间要带空格号，我也不知道为什么要这样设定
    show bg name
    #加载live2d动作，参考https://www.renpy.cn/doc/live2d.html
#live2d模型都有自己的动作名，你可以在model3文件中查看，也可以自己用动作捕捉工具(steam里搜vtuber)自定义。
    show Character1 motion1
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
    $ open_api_key = renpy.input("填写你的API keys 网址：https://beta.openai.com/account/api-keys",length=1000)
    $ open_api_key = str(open_api_key)
    $ your_name = renpy.input("你的名字：",length=10)
    $ noise_scale = renpy.input('填写噪声参数，默认输入0.667',length=10)
    $ noise_scale_w = renpy.input('填写噪声参数偏差，默认输入0.8',length=10)
    $ noise_scale_0 = renpy.input('语速设置，默认1',length=10)
    $ spk_id = int(renpy.input("对话角色",length=10))
#renshe这个玩意是用来和gpt3对话用的，实际上有些多余了，chatgpt则完全不需要，直接空输入也行
    $ renshe =  renpy.input("写上人设",length=200)    
    $ web = web_base + "/identity?text=" + renshe + "&mapping=" + str(your_name)
    $ renshe = requests.get(web).text
    jump sense1

label sense1:
#获取当前项目所在路径，创建存储音频文件的路径
    $ current_work_dir = os.path.dirname(__file__)
    $ weight_path = os.path.join(current_work_dir, 'temp.ogg')
    $ weight_path = weight_path.replace("\\","/")
#交互的第一步
    $ your_text = renpy.input('',length=60)
#合成网址用来发送请求(本来只有需传入文本就行了，后来参数越传越多)
    $ webs = web_base + "/gpt?text="+ your_text  + "&speakers_name=" + str(spk_id) +"&api_key=" + str(open_api_key) + "&mapping=" + str(your_name) + "&noise_scale=" + str(noise_scale) + "&noise_scale_w=" + str(noise_scale_w) + "&spd=" + str(noise_scale_0)
#这就是另外一种插入python指令的方法了，用treading实现同步运行
    python:
        def get_voice():
            res = requests.get(webs)
            music = res.content
            with open(weight_path, 'wb') as code:
                code.write(music)
            web2 = web_base + "/word?mapping=" + your_name
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
    show Character1 motion2
    voice weight_path
    Setsuna '[answer]'
    show Character1 motion2
    jump sense1

```
