# 这是一个焊接chatgpt/gpt3和vits的后端api程序
**搭建流程
**1.克隆一个vits库或iSTFT VITS库
**2.搭建vits环境，准备好模型
**3.把inference_api.py丢进去
**4.按照inference_api.py内指示创建用于保存生成的各种文件的文件夹
**5.$pip install openai pyChatGPT openai
**6.修改inference_api中的模型路径和配置路径
**7.cd /path/to/vits
**8.python inference_api.py
**9.留意running on http://yourhost:8080 这是最基础的网址。
**最基础的前端应用项目地址https://drive.google.com/drive/folders/1vtootVMQ7wTOQwd15nJe6akzJUYNOw4d
**解压live2d_chat-0.6(gpt3+chatgpt).zip
**运行游戏程序
**你也可以用renpy修改游戏程序，自定义你的live2d模型和交互方式。

## How to use
(Suggestion) Python == 3.7
## Clone a VITS repository or iSTFT-VITS repository
```sh
git clone https://github.com/CjangCjengh/vits.git
#git clone https://github.com/innnky/MB-iSTFT-VITS
```
## Adding cleaners inference_api.py to your project
- The path of inference_api.py should be like path/to/vits/inference_api.py
- If you want to launch this project in your server, it is recommanded to use iSTFT-VITS for tts: path/to/MB-iSTFT-VITS/inference_api.py
## Install requirements of vits enviornments
```sh
cd vits
#cd MB-iSTFT-VITS
pip install -r requirements.txt
```
## Install requirements for using GPT3/CHATGPT in python
```sh
pip install pydub 
pip install openai
#Not recommended due to demanding requirements
#pip install pyChatGPT
```
## Editing 
