#basic enviornments & openai
import romajitable
import re
import os
import numpy as np
import logging
logging.getLogger('numba').setLevel(logging.WARNING)
import IPython.display as ipd
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import openai
import tkinter as tk
from tkinter import scrolledtext
import argparse
import time
from scipy.io.wavfile import write
def get_args():
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--model', default = 'lovelive/G_817000.pth')
    parser.add_argument('--audio',
                    type=str,
                    help='the sound file of live2d to be replace,assuming they are temp1.wav,temp2.wav,temp3.wav......',
                    default = 'path/to/temp.wav')
    parser.add_argument('--cfg', default="lovelive/config.json")
    parser.add_argument('--key',default = "openai key",
                        help='platform.openai.com')
    args = parser.parse_args()
    return args
args = get_args()
dev = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
dev = torch.device("cuda:0")
hps_ms = utils.get_hparams_from_file(args.cfg)
#mult-speakers
net_g_ms = SynthesizerTrn(
    len(symbols),
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=hps_ms.data.n_speakers,
    **hps_ms.model).to(dev)
_ = net_g_ms.eval()
_ = utils.load_checkpoint(args.model, net_g_ms, None)
# detecting japanese
def is_japanese(string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False 
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm
def ttv(text):
    text = text.replace('\n','').replace(' ','')
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    speaker_id = 7
    stn_tst = get_text(text,hps_ms)
    t1 = time.time()
    with torch.no_grad():
        x_tst = stn_tst.unsqueeze(0).to(dev)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(dev)
        sid = torch.LongTensor([speaker_id]).to(dev)
        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=0.467, noise_scale_w=0.5, length_scale=1)[0][0,0].data.cpu().float().numpy()
    write(args.audio + '.wav',22050,audio)
    i = 0
    while i < 19:
        i +=1
        cmd = 'ffmpeg -y -i ' +  args.audio + '.wav' + ' -ar 44100 '+ args.audio.replace('temp','temp'+str(i))
        os.system(cmd)
    t2 = time.time()
    print("推理耗时:",(t2 - t1),"s")
openai.api_key = args.key
result_list = []
'''
messages = [
    {"role": "system", "content": "你是超级ai，名字叫巴珠绪。接下来我们将进行一个克苏鲁跑团游戏，你负责扮演守密人，我负责扮演调查员。接下来你会加载一个名叫《幽暗之门》的模组，作为守密人，你需要基于“克苏鲁神话角色扮演游戏规则第七版（Call of Cthulhu 7th Edition）”，我会给你剧本的开头部分，然后基于你对它的理解自由发挥。投掷骰子的环节将由你来模拟，用两个1d10的骰子来生成0-100的随机数。比如说我的某一项属性点是80，当骰子的数目小于80时就判定为成功，0-5为大成功，95-100为大失败等等。整个游戏过程将类似于你来描述故事，我来投骰子并且做出决定来推动剧情的走向。"},
    {'role': 'assistant', 'content': '我明白了，现在我将扮演守密人。'},
    ]
'''
messages = []
read_log = input('Loading log?(y/n)')
if read_log == 'y':
    messages = []
    with open('log.pickle', 'rb') as f:
        messages = pickle.load(f)
    print('Most recently log:\n'+str(messages[-1]))
def send_message():
    text = input_box.get("1.0", "end-1c") # 获取用户输入的文本
    messages.append({"role": "user", "content": text},)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    ttv(reply)
    messages.append({"role": "assistant", "content": reply})
    print(messages[-1])
    if len(messages) == 12:
        messages[6:10] = messages[8:]
        del messages[-2:]
    with open('log.pickle', 'wb') as f:
         pickle.dump(messages, f)
    chat_box.configure(state='normal') 
    chat_box.insert(tk.END, "You: " + text + "\n") 
    chat_box.insert(tk.END, "Tamao: " + reply + "\n") 
    chat_box.configure(state='disabled') 
    input_box.delete("1.0", tk.END) 

root = tk.Tk()
root.title("Tamao")

chat_box = scrolledtext.ScrolledText(root, width=50, height=10)
chat_box.configure(state='disabled')
chat_box.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
input_box = tk.Text(input_frame, height=3, width=50)
input_box.pack(side=tk.LEFT, fill=tk.X, padx=10, expand=True)
send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()
