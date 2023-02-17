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
# [绿皮思路chat](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/inference_ork.py)
许多live2d都有触碰事件，那么，只需要有一个装载有完整cubism for native功能的live2d播放器
```sh
#将audio参数修改为触碰动作的音频路径
#比如
parser.add_argument('--audio',
                    type=str,
                    help='中途生成的语音存储路径',
                    default = '110Yuki-Setsuna/sounds/temp.wav')
#其在live2d的model3.json文件中对应的是
"TapBody": [
        {
          "File": "motions/a.motion3.json",
          "Sound": "sounds/temp.wav",
          "Text": "ﾋﾄﾘﾀﾞｹﾅﾝﾃｴﾗﾍﾞﾅｲﾖｰ"
        },
        {
          "File": "motions/a.motion3.json",
          "Sound": "sounds/temp.wav",
          "Text": "ﾋﾄﾘﾀﾞｹﾅﾝﾃｴﾗﾍﾞﾅｲﾖｰ"
        }
```
这样做的本质是让这个绿皮程序不断修改音频文件
```sh
#在infer函数中直接用os调用命令覆盖旧音频
cmd = 'ffmpeg -y -i ' +  args.outdir + '/temp1.wav' + ' -ar 44100 '+ args.audio
#主程序就长这样
def main():
    while True:
      text = input("You:")
      text = infer(text)
      print('Waifu:'+text.replace("[ZH]","").replace("[JA]",""))
    
if __name__ == '__main__':
    main()
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
