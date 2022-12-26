define Setsuna = Character("HK416")
define config.gl2 = True
image Setsuna = Live2D("normal", top=0.0, base=0.7, height=1.0,loop=True)
# ‘游戏’在此开始。

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

label setting1:
    $ web_base = renpy.input("输入后端api的地址，如本地推理为'http://127.0.0.1:8080'，终端运行inference_api.py时查看",length=100)
#    $ open_api_key = renpy.input("填写你的API keys 网址：https://beta.openai.com/account/api-keys",length=1000)
#    $ open_api_key = str(open_api_key)
    $ your_name = renpy.input("你的名字：",length=10)
    jump setting3

label setting2:
    $ noise_scale = renpy.input('填写噪声参数，默认输入0.667',length=10)
    $ noise_scale_w = renpy.input('填写噪声参数偏差，默认输入0.8',length=10)
    $ noise_scale_0 = renpy.input('语速设置，默认1',length=10)
    $ spk_id = int(renpy.input("对话角色",length=10))
    #    open_api_path = open_api_path.replace("\\","/").replace(,"/")
    #    with open(open_api_path, "r", encoding="utf-8") as f1:
    #        open_api_key = f1.read()
    $ renshe =  renpy.input("写上人设",length=200)    
    $ web = web_base + "/identity?text=" + renshe + "&mapping=" + str(your_name)
    $ renshe = requests.get(web).text
    jump sense1

label setting3:
    $ noise_scale = renpy.input('填写噪声参数，默认输入0.667',length=10)
    $ noise_scale_w = renpy.input('填写噪声参数偏差，默认输入0.8',length=10)
    $ noise_scale_0 = renpy.input('语速设置，默认1',length=10)
    $ spk_id = int(renpy.input("对话角色",length=10))
    #    open_api_path = open_api_path.replace("\\","/").replace(,"/")
    #    with open(open_api_path, "r", encoding="utf-8") as f1:
    #        open_api_key = f1.read()
    $ renshe =  renpy.input("写上人设",length=200)    
    $ web = web_base + "/identity?text=" + renshe + "&mapping=" + str(your_name)
    $ renshe = requests.get(web).text
    jump sense2


label sense1:
    $ import requests     
    $ import os
    $ import threading    
    $ current_work_dir = os.path.dirname(__file__)
    $ weight_path = os.path.join(current_work_dir, 'temp.ogg')
    $ weight_path = weight_path.replace("\\","/")
    $ your_text = renpy.input('',length=60)
        #webs = "http://43.159.36.6:8080/tts?text=[ZH]" + povname + "[ZH]&speakers_name=歩夢"
    $ webs = web_base + "/gpt?text="+ your_text  + "&speakers_name=" + str(spk_id) +"&api_key=" + str(open_api_key) + "&mapping=" + str(your_name) + "&noise_scale=" + str(noise_scale) + "&noise_scale_w=" + str(noise_scale_w) + "&spd=" + str(noise_scale_0)
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
menu:
    "查看回复":
        jump reply
    "重新设定":
        jump setting2

label reply:
    show Setsuna daiji_idle_01
    voice weight_path
    Setsuna '[answer]'
    show Setsuna daiji_idle_01
    jump sense1

label sense2:
    $ import requests     
    $ import os
    $ import threading    
    $ current_work_dir = os.path.dirname(__file__)
    $ weight_path = os.path.join(current_work_dir, 'temp.ogg')
    $ weight_path = weight_path.replace("\\","/")
    $ your_text = renpy.input('',length=60)
        #webs = "http://43.159.36.6:8080/tts?text=[ZH]" + povname + "[ZH]&speakers_name=歩夢"
    $ webs = web_base + "/chatgpt?text="+ your_text  + "&speakers_name=" + str(spk_id) + "&mapping=" + str(your_name) + "&noise_scale=" + str(noise_scale) + "&noise_scale_w=" + str(noise_scale_w) + "&spd=" + str(noise_scale_0)
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
menu:
    "查看回复":
        jump reply2
    "重新设定":
        jump setting3


label reply2:
    show Setsuna daiji_idle_01
    voice weight_path
    Setsuna '[answer]'
    show Setsuna daiji_idle_01
    jump sense2