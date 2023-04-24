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
# 合成日语时要安装pyopenjtalk或者编译好的日语cleaner文件(效果不一定好)，所以你完全可以选择忽视该模块的安装。
在cleaner程序中，也就是text文件下的[cleaners.py](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/onnx/text/cleaners.py),注释掉所有的japanese模块，比如说:
```sh
#第3行
from text.japanese import japanese_to_romaji_with_accent, japanese_to_ipa, japanese_to_ipa2, japanese_to_ipa3
```
在你所采用的config.json文件中，找到对应的cleaner，比如说zh_ja_mixture_cleaners,然后注释掉这一段
``sh
#第50行开始
for japanese_text in japanese_texts:
        cleaned_text = japanese_to_romaji_with_accent(
            japanese_text[4:-4]).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')
        text = text.replace(japanese_text, cleaned_text+' ', 1)
```
## II:server端启动后端api程序(Windows也可以)
如需使用pyopenjtalk，则需要先安装好cmake, 结合自己的系统搜索相关安装教程
## Linux
```sh
#Installing cmake and FFmpeg,showing FFmpeg
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
(较为复杂，建议参考另一个分支部署)如需使用chatglm,需提前部署好环境[在自己的环境下安装好依赖](https://github.com/THUDM/ChatGLM-6B)。建议protobuf==3.20.0，
transformers>=4.26.1，否则会有奇怪报错
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
