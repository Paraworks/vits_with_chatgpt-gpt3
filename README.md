# [无ui版及ChatGLM部署流程](https://github.com/Paraworks/vits_with_chatgpt-gpt3/tree/window)
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
如需使用pyopenjtalk，则需要先安装好cmake。
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
## (Alternative).使用封装版的Japanese cleaner,用该text[文件夹](https://github.com/Paraworks/vits_with_chatgpt-gpt3/tree/window/text)替换原本的text文件夹,然后从该仓库的release中[下载](https://github.com/NaruseMioShirakana/JapaneseCleaner)，将cleaners压缩包解压至vits项目的路径下
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
# [添加vits模型](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/checkpoints/README.md)
# [onnx导出程序，克隆该仓库后运行](https://huggingface.co/Mahiruoshi/vits_with_chatbot/blob/main/export_onnx.py)
# 由于openai将扩大对非官方api的打压力度，如以盈利为目的，建议采用官方的api key以及openai标准库
