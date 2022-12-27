define nengdai = Character("能代")
define config.gl2 = True
image nengdai = Live2D("nengdai_2", top=0.3, base=0.7, height=1,loop=True)
label start:
    #加载live2d动作，参考https://www.renpy.cn/doc/live2d.html
    show nengdai idle
    $ import requests
    $ import os
    $ import threading
    $ from time import sleep
    $ global your_text
    jump sense1

label sense1:
    show nengdai main_1
    $ current_work_dir = os.path.dirname(__file__)
    $ weight_path = os.path.join(current_work_dir, 'temp.ogg')
    $ weight_path = weight_path.replace("\\","/")
    $ your_text = renpy.input('',length=60)
    $ webs = "http://127.0.0.1:8080/gpt?text=" + your_text
    python:
        def get_voice():
            res = requests.get(webs)
            music = res.content
            with open(weight_path, 'wb') as code:
                code.write(music)            
            response = requests.get("http://127.0.0.1:8080/word").text
            global response
        thread = threading.Thread(target=get_voice)
        thread.start()
    jump speak 

label speak:
    nengdai '等待合成'
    voice weight_path
    nengdai '[response]'
    jump sense1


    

