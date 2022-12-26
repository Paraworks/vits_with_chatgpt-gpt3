# 这是一个焊接chatgpt/gpt3和vits的后端api程序
用api启动的主要目的是搭建lovelive的聊天网站，其实16号就已经把这个项目搞好了，只是因为lovelive不像邦邦和少歌那样有live2d模型，找各种方案搁置了一周多，直到花钱整了个模型想起来()，而且发现大家对这种形式的热情很高，就把这个放在文件夹里吃灰的项目拿出来了。
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
## Adding cleaners&inference_api.py to your project
- Noticing "text_cleaners" in config.json
- Edit 'text'dictionary in the VITS or iSTFT-VITS
- Remove unnecessary imports from text/cleaners.py
- The path of inference_api.py should be like path/to/vits/inference_api.py
- If you want to launch this project in your server, it is recommanded to use iSTFT-VITS for tts: path/to/MB-iSTFT-VITS/inference_api.py
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
