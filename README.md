## 2023/2/10更新 vits-onnx 一键式启动
## 2023/2/17更新 弃用renpy [采用桌宠版本](https://github.com/Arkueid/Live2DMascot)
# live2d启动器发生1：克隆[Live2DMascot](https://github.com/Arkueid/Live2DMascot)仓库后，修改config.json文件
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
# 启动器方式2：live2dviewer
# 选择1：server端启动后端api程序(Windows也可以)
## Combining chatgpt/gpt3&vits as api and launch it（Server suggested）
将[inference_api.py](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/inference_api.py)丢入你的vits项目或moegoe项目中
```sh
cd vits
mkdir moe
python inference_api.py
```
# 选择2：[绿皮思路chat](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/inference_ork.py)
支持从外部启动任何正在运行的live2d模型，比如说修改点击事件的对应音频来实现。只需在你的vits项目中加入inference_ork.py这个小文件，然后启动它。注意，需要你能够在自己的windows上部署vits项目，推荐安装好cuda，[教程
](https://www.bilibili.com/video/BV13t4y1V7DV/?spm_id_from=333.337.search-card.all.click&vd_source=7e8cf9f5c840ec4789ccb5657b2f0512)
```sh
#example Nijigasaki
git clone https://huggingface.co/spaces/Mahiruoshi/Lovelive_Nijigasaki_VITS
cd Lovelive_Nijigasaki_VITS
pip install -r requirements.txt
python inference_ork.py
```
许多live2d都有触碰事件，那么，只需要有一个装载有完整cubism for native功能的live2d播放器,其可以支持点击事件并且支持对口型功能。
此时只需要启动 inference_ork.py
![Image text](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/T9B%25SY%7B%7BGY5I%600K5P7A4AUC.png)
```sh
#在程序中将audio参数修改为触碰动作的音频路径
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
          "Sound": "sounds/temp2.wav",
          "Text": "ﾋﾄﾘﾀﾞｹﾅﾝﾃｴﾗﾍﾞﾅｲﾖｰ"
        }，
	{
          "File": "motions/a.motion3.json",
          "Sound": "sounds/temp3.wav",
          "Text": "ﾋﾄﾘﾀﾞｹﾅﾝﾃｴﾗﾍﾞﾅｲﾖｰ"
        }
	......]
	
```
这样做的本质是让这个绿皮程序不断修改音频文件
```sh
#绿皮启动器的核心
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
# 如何为gpt-3.5添加设定
```sh
#比如说我需要和珠绪学姐玩跑团游戏
messages = [
    {"role": "system", "content": "你是超级ai，名字叫巴珠绪。接下来我们将进行一个克苏鲁跑团游戏，你负责扮演守密人，我负责扮演调查员。接下来你会加载一个名叫《幽暗之门》的模组，作为守密人，你需要基于“克苏鲁神话角色扮演游戏规则第七版（Call of Cthulhu 7th Edition）”，我会给你剧本的开头部分，然后基于你对它的理解自由发挥。投掷骰子的环节将由你来模拟，用两个1d10的骰子来生成0-100的随机数。比如说我的某一项属性点是80，当骰子的数目小于80时就判定为成功，0-5为大成功，95-100为大失败等等。整个游戏过程将类似于你来描述故事，我来投骰子并且做出决定来推动剧情的走向。"},
    {'role': 'assistant', 'content': '我明白了，现在我将扮演守密人。'},
    ]
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
```
