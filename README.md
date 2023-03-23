## 2023/2/10更新 vits-onnx 一键式启动
## 2023/2/17更新 弃用renpy [采用桌面应用版本](https://github.com/Arkueid/Live2DMascot)
## 2023/3/3更新 接入官方的chatgpt
## 2023/3/15更新 完全本地化，采用[清华ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)
# 此分支为vits模型onnx导出版，[原版vits](https://github.com/Paraworks/vits_with_chatgpt-gpt3/tree/main)
# 步骤1，启用前端应用，克隆[Live2DMascot](https://github.com/Arkueid/Live2DMascot)仓库后，修改config.json文件
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
# 下一步：server端启动后端api程序(Windows也可以)
## Combining chatgpt/gpt3&vits as api and launch it（Server suggested）
##将你的onnx导出为onnx模型[colab版](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/onnx_export_colab.ipynb)
[来源](https://gitee.com/ccdesue/vits_web_demo)
[该仓库使用的模型(Onnx model example)](https://huggingface.co/Mahiruoshi/vits_onnx_model/tree/main)
[替换text文件夹以适配不同模型(Change text folder)](https://github.com/Paraworks/vits_with_chatgpt-gpt3/tree/onnx/text)
# 完全本地化,windows部署流程,建议30系以上N卡，或者cpu
## 安装[FFmpeg](https://zhuanlan.zhihu.com/p/118362010)并且添加环境变量
## I.安装[Torch+gpu](https://blog.csdn.net/qq_44173699/article/details/126312680)(如需cpu推理则跳过)
## II.[cmake及pyopenjtalk安装](https://www.bilibili.com/video/BV13t4y1V7DV/?spm_id_from=333.880.my_history.page.click)
## III.下载[model.onnx](https://huggingface.co/Mahiruoshi/vits_onnx_model/tree/main)后放入moe文件夹
# 如果只采用chatgpt则跳过此步
## IV.按照教程，将清华的[开源语音模型](https://github.com/THUDM/ChatGLM-6B)下载下来后全部放进moe文件夹中，[huggingface](https://huggingface.co/THUDM/chatglm-6b)
最后你的moe文件夹应该长这样,纯vits只需model.onnx与config_v.json
![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/moe%202023_3_16%201_13_45.png)
```sh
cd moe
pip install -r requirements.txt
cd ..
#默认最低配置，如有需要可以按照官方教程修改。为了防止炸显存，推荐tts端采用onnx的cpu推理
python local_chat.py 
#python api_launch.py --key your_openai_api_key
```
```sh
修改配置文件来更换模型
def get_args():
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--onnx_model', default = './moe/model.onnx')
    parser.add_argument('--cfg', default="./moe/config_v.json")
    parser.add_argument('--outdir', default="./moe",
                        help='ouput folder')
    parser.add_argument('--ChatGLM',default = "./moe",
                        help='https://github.com/THUDM/ChatGLM-6B')
    args = parser.parse_args()
    return args
```
# chatgpt+服务器部署
```sh
#核心思路:服务器部署api，完成主要工作
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
git clone https://github.com/Paraworks/vits_with_chatgpt-gpt3
cd vits_with_chatgpt-gpt3
pip install -r requirements.txt
#after uploading onnx models and edit it in the api_launch.py, launch
#Reference
#('--onnx_model', default = './moe/model.onnx')
#('--cfg', default="./moe/config_v.json")
#('--outdir', default="./moe",help='ouput directory')
#('--key',default = "你的openai key",help='openai api key')
python api_launch.py --key 'openapikey see: https://openai.com/api/'
#这只是一种思路，建议根据自己的需求自行修改，先实现普通的tts后再去整大活，比如随时随地掏出手机和老婆聊天()。
 #* Running on all addresses (0.0.0.0)
 #* Running on http://127.0.0.1:8080
 #* Running on http://172.16.5.4:8080
#部署到服务器以后的标准网页格式,http://yourhost:8080/
#浏览器键入测试 http://yourhost:8080/chat?Text=测试测试
#旧版本 http://yourhost:8080/gpt?text=测试测试
```
# 接口的具体展示，后者是chatgpt，也就是默认端
```sh
@app.route('/gpt?')
def text_api():
    text = request.args.get('Text','')
    text = gpt3_chat(text)
    text = infer(text)
    text = text.replace('[JA]','').replace('[ZH]','')
    with open(outdir +'/temp2.wav','rb') as bit:
        wav_bytes = bit.read()
    headers = {
        'Content-Type': 'audio/wav',
        'Text': text.encode('utf-8')
    }
    return wav_bytes, 200, headers
if __name__ == '__main__':
   app.run("0.0.0.0", 8080) 


messages = [{"role": "system", "content": "你是温柔体贴的vtuber。"},]
@app.route('/chat')
def text_api():
    openai.api_key = args.key
    message = request.args.get('Text','')
    messages.append({"role": "user", "content": message},)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    text = infer(reply)
    text = text.replace('[JA]','').replace('[ZH]','')
    with open(outdir +'/temp2.wav','rb') as bit:
        wav_bytes = bit.read()
    headers = {
            'Content-Type': 'audio/wav',
            'Text': text.encode('utf-8')}
    return wav_bytes, 200, headers
if __name__ == '__main__':
   app.run("0.0.0.0", 8080) 
```
```sh
#聊天机器人生成回复的代码
tokenizer = AutoTokenizer.from_pretrained(args.ChatGLM, trust_remote_code=True)
#8G GPU
model = AutoModel.from_pretrained(args.ChatGLM, trust_remote_code=True).half().quantize(4).cuda()
history = []
@app.route('/chat')
def text_api():
    global history
    message = request.args.get('Text','')
    t1 = time.time()
    if message == 'clear':
      history = []
    else:
      response, new_history = model.chat(tokenizer, message, history)
      response = response.replace(" ",'').replace("\n",'.')
      text = infer(response)
      text = text.replace('[JA]','').replace('[ZH]','')
      with open(outdir +'/temp2.wav','rb') as bit:
          wav_bytes = bit.read()
      headers = {
            'Content-Type': 'audio/wav',
            'Text': text.encode('utf-8')}
      history = new_history
      t2 = time.time()
      spending_time = "总耗时："+str(t2-t1)+"s" 
      print(spending_time)
      return wav_bytes, 200, headers
if __name__ == '__main__':
   app.run("0.0.0.0", 8080)
```
```sh
#TTS用到的代码，修改sid来更换角色，更换模型
def infer(text):
    #选择你想要的角色
    sid = 3
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    seq = text_to_sequence(text, symbols=hps.symbols, cleaner_names=hps.data.text_cleaners)
    #seq = text_to_sequence(text, cleaner_names=hps.data.text_cleaners)
    if hps.data.add_blank:
        seq = commons.intersperse(seq, 0)
    with torch.no_grad():
        x = np.array([seq], dtype=np.int64)
        x_len = np.array([x.shape[1]], dtype=np.int64)
        sid = np.array([sid], dtype=np.int64)
        scales = np.array([0.667, 0.8, 1], dtype=np.float32)
        scales.resize(1, 3)
        ort_inputs = {
                    'input': x,
                    'input_lengths': x_len,
                    'scales': scales,
                    'sid': sid
                }
        t1 = time.time()
        audio = np.squeeze(ort_sess.run(None, ort_inputs))
        audio *= 32767.0 / max(0.01, np.max(np.abs(audio))) * 0.6
        audio = np.clip(audio, -32767.0, 32767.0)
        t2 = time.time()
        spending_time = "推理时间："+str(t2-t1)+"s" 
        print(spending_time)
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        wavfile.write(outdir + '/temp1.wav',hps.data.sampling_rate, audio.astype(np.int16))
        cmd = 'ffmpeg -y -i ' +  outdir + '/temp1.wav' + ' -ar 44100 '+ outdir + '/temp2.wav'
        os.system(cmd)
    return text
```
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
