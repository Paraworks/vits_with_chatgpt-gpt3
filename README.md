## 2023/2/10更新 vits-onnx 一键式启动
## 2023/2/17更新 弃用renpy [采用桌宠版本](https://github.com/Arkueid/Live2DMascot)
# 克隆[Live2DMascot](https://github.com/Arkueid/Live2DMascot)仓库后，修改config.json文件
```sh
"ChatAPI" : 
{
	"ChatSavePath" : "chat",  //聊天音频和文本保存路径
	"CustomChatServer" : 
	{
		"HostPort" : "http://127.0.0.1:8080",  //服务器地址，端口默认8080
		"On" : true,  //开启自定义聊天接口
		"ReadTimeOut" : 114,  //等待响应时间(s)
		"Route" : "/chat"  //路径
	},
```
# 下一步：server端启动后端api程序(Windows也可以)
## Combining chatgpt/gpt3&vits as api and launch it（Server suggested）
将[inference_api.py](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/inference_api.py)丢入你的vits项目或moegoe项目中
```sh
cd vits
mkdir moe
python inference_api.py
```
# 对于 text_to_sequence相关错误
```sh
#在推理中，可能出现symbols相关错误，这主要是由于不同text cleaner之间的冲突导致的
line 85, in infer
seq = text_to_sequence
#需要你在这一行自行修改
#如果需要
symbols seq = text_to_sequence(text, symbols=hps.symbols, cleaner_names=hps.data.text_cleaners)
#如不需要，把 symbols=hps.symbols 删掉
