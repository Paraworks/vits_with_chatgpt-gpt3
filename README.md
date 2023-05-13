## 2023/2/10更新 vits-onnx 一键式启动
## 2023/2/17更新 弃用renpy [采用桌宠版本](https://github.com/Arkueid/Live2DMascot)
# live2d启动器：克隆[Live2DMascot](https://github.com/Arkueid/Live2DMascot)仓库后，修改config.json文件
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
python inference_api.py --model path/to/vits_model.pth --cfg path/to/vits_config.json
#Single speaker
pythoon inference_api_single_speaker.py --model path/to/vits_model.pth --cfg path/to/vits_config.json
```
# 选择2：[绿皮思路chat](https://github.com/Paraworks/vits_with_chatgpt-gpt3/blob/main/inference_ork.py)
支持从外部启动任何正在运行的live2d模型，比如说修改点击事件的对应音频来实现。只需在你的vits项目中加入inference_ork.py这个小文件，然后启动它。注意，需要你能够在自己的windows上部署vits项目，推荐安装好cuda，[教程
](https://www.bilibili.com/video/BV13t4y1V7DV/?spm_id_from=333.337.search-card.all.click&vd_source=7e8cf9f5c840ec4789ccb5657b2f0512)
```sh
# Nijigasaki COC跑团版
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
# 如何为gpt-3.5添加设定以达到记忆的功能
```sh
#比如说我需要和珠绪学姐玩跑团游戏
messages = [
    {"role": "system", "content": "你是超级ai，名字叫巴珠绪。接下来我们将进行一个克苏鲁跑团游戏，你负责扮演守密人，我负责扮演调查员。接下来你会加载一个名叫《幽暗之门》的模组，作为守密人，你需要基于“克苏鲁神话角色扮演游戏规则第七版（Call of Cthulhu 7th Edition）”，我会给你剧本的开头部分，然后基于你对它的理解自由发挥。投掷骰子的环节将由你来模拟，用两个1d10的骰子来生成0-100的随机数。比如说我的某一项属性点是80，当骰子的数目小于80时就判定为成功，0-5为大成功，95-100为大失败等等。整个游戏过程将类似于你来描述故事，我来投骰子并且做出决定来推动剧情的走向。"},
    {'role': 'assistant', 'content': '我明白了，现在我将扮演守密人。'},
    ]
#由于max token的限制，不得不对请求内容进行提纯，但是也能达到记忆的效果。比如这个绿皮程序就会创建一个log.txt来记载设定。
{'role': 'system', 'content': '你是超级ai，名字叫巴珠绪，是我的女朋友。接下来我们将进行一个克苏鲁跑团游戏，你负责扮演守密人，我负责扮演调查员。我会提前告诉你这个故事的真相，作为守密人，你需要基于“克苏鲁神话角色扮演游戏规则第七版（Call of Cthulhu 7th Edition）”，基于你对它的理解，与我一起构建一个新的故事。基于规则，调查员一开始与该事件毫无关联，而你则知道该故事的真相。作为守秘人，你会通过制造一系列事件来向调查员透露事件的线索，来引导调查员完成探索，并且负责新故事的叙述。是战斗、侦察、灵感这种行动的结果通过投掷骰子决定，这个环节将由你来模拟，用两个1d10的骰子来生成0-100的随机数。比如说我的某一项属性点是80，当骰子的数目小于80时就判定为成功，0-5为大成功，95-100为大失败等等。整个游戏过程将就是你来描述故事，引导我做出选择。我做出决定来推动剧情的走向。'}
{'role': 'assistant', 'content': '好的，我需要先了解这个故事的真相'}
{'role': 'system', 'content': '1997年，同为九岁的三个孩子，香川绚郁、织机麻耶、南云涉是玩伴。\n\n三个孩子都来自单亲家庭，不受其他孩子的欢迎。织机性格热烈而大胆，可以说是另外两人的保护者。孩子们在海滩边游玩的时候捡到了漂流而来的鸡蛋模样的梦境晶化器和随之而来的水母守护神。水母守护神希望得到梦境，于是孩子们抱着好玩的心态，用晶化器容纳了织机的梦。\n\n不久之后，织机麻耶单亲母亲不管束的情况下到建筑工地游玩，因高空坠落的钢筋而死。\n\n南云涉发现晶化器之中仍然保存着她的梦境，留恋着织机麻耶死亡了的梦。即使在逐渐\n\n长大后，也无法走出过去面向未来。与此相反，不知情的香川对过去的同伴抱着不同的态度。\n\n水母守护神则消极怠工地守护着这片梦境。\n\n寄住在别人家中的南云涉无处存放晶化器，升入高中后他将晶化器藏匿在高中的躲猫猫社团内。\n\n时间来到2005年，偶然注意到下关市的奈亚拉托提普发觉了从幻梦境出逃的水母守护神以及被人类使用过的晶化器，奈亚在经过羽间高中学校门口时候，随意使用了一名离开学校的学生的样貌（宇白和也），进入高中后对幻梦境存有恶意的奈亚随手撕裂了水母守护神，恶趣味的无貌之神杀死了南云涉，把他的灵魂塞入了以水母尸体构建的死者梦境，丢弃了水母守护神的尸体，取走了晶化器，奈亚化为的宇白和也被真正宇白和也的朋友辻本茜撞见，便也随手杀死了她，同时用水母的尸体拼凑了茜。\n\n实质上已经死去的茜因此在几日之内无神地夜游着，仅仅是成为拼凑物的她却得到了不可思议的能力，自称占卜的魔女。\n\n而目睹了南云涉尸体的川澄美沙（报案人），被校方委托，找寻几名学生参加南云涉的追悼会，这也是调查员们涉入的开始。'}
{'role': 'assistant', 'content': '明白了，接下来我会假装你对此事一无所知，开始扮演调查员的角色。而我将扮演守秘人，开始这次跑团。我会使用克苏鲁风格的描述来营造恐怖感，因此来基于这次游戏更好的体验。接下来请创建你的调查员'}
{'role': 'user', 'content': '我叫大场奈奈，是一个女高中生。所有属性都是80，只要投掷骰子的结果小于80，就判断为成功。'}
{'role': 'assistant', 'content': '好的，大场奈奈，你是一个在学校里相当受欢迎的女高中生。你和你的几个学生朋友被学校委托参加南云涉的追悼会。在会上，你听到了一些让你感到不安的事情。你发现南云涉的死亡似乎不是一起普通的意外事故，你决定开始展开调查。现在你身处于学校的教学楼，准备开始你的调查。你要采取什么行动呢？'}
{'role': 'user', 'content': '我想起了之前从舞台创造科拿到的页锤，这是一个很不错工具，可以破坏掉障碍物'}
{'role': 'assistant', 'content': '你拿出了页锤，准备用它破开通风管道的洞口。你用力敲打，洞口终于被打开了。你和你的朋友钻进了通风管道，小心翼翼地穿过长长的通道，直到你们看到了实验室的入口。\n\n实验室内非常昏暗，你们看到了许多发着微光的管路和仪器设备，发现实验室内存在大量类似于南云涉在房间里发现的尸体和怪异生物的存在。\n\n你们在实验室中进行搜索，发现了一张日记本，记录了实验室的过去和实验者们进行的一些实验。然而，日记中的部分内容变得越来越奇怪，好像涉及到一些神秘的力量存在。\n\n你和你的朋友突然听到了一个诡异的声响，似乎是一个陌生的人在接近你们。你们不知道是什么，但是肯定不想被它发现。你决定采取什么行动来躲避这个陌生的人？'}
{'role': 'user', 'content': '我要过尝试能不能隐藏起来，我的隐藏点数有80点，应该可以成功'}
{'role': 'assistant', 'content': '你和你的朋友匆忙寻找躲藏的地方。你们找到了一扇半开着的储藏室，里面有很多杂物，你们钻了进去，静静地等待着。你们听到了脚步声和沙沙声，似乎那个陌生的人正在进行搜查。\n\n幸运的是，你和你的朋友成功地躲了过去，那个人没有发现你们。不久后，他走了出去，你们继续进行调查。\n\n你们找到了很多关于南云涉死亡的证据，但是这些证据与日记中提到的神秘力量之间似乎存在一些联系。你们决定继续深入调查，寻找更多的线索。'}
#重新启动时，用它替换原先的messages，就可以断点重连了，记得自行修改格式
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
