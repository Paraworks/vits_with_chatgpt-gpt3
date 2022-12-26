#需要额外安装的包：pydub、openai pyChatGPT
from pydub import AudioSegment
import matplotlib.pyplot as plt
import IPython.display as ipd
import threading
import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write
from flask import Flask, request
import openai
#from pyChatGPT import ChatGPT

#设定存储各种数据的目录，方便查看，默认C:/project_file
current_work_dir = os.path.dirname(__file__)
weight_path = os.path.join(current_work_dir, '/project_file/')
app = Flask(__name__)
mutex = threading.Lock()
#设置gpu推理
dev = torch.device("cuda:0")
#导入config文件
hps_ms = utils.get_hparams_from_file("path/to/config.json")
#加载多人模型
net_g_ms = SynthesizerTrn(
    len(symbols),
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=hps_ms.data.n_speakers,
    **hps_ms.model).to(dev)
_ = net_g_ms.eval()
#导入模型文件
_ = utils.load_checkpoint("path/to/checkpoint.pth", net_g_ms, None)
#预处理
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm
#修改参数的语音合成
def tts(text,name=1,noise_scale=0.667,noise_scale_w=0.8,speaking_speed=1):
  speaker_id = name
  speaker_id = int(speaker_id)
  stn_tst = get_text(text, hps_ms)
  with torch.no_grad():
      x_tst = stn_tst.unsqueeze(0).to(dev)
      x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(dev)
      sid = torch.LongTensor([speaker_id]).to(dev)
      audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w, length_scale=speaking_speed)[0][0,0].data.cpu().float().numpy()
    #  ipd.display(ipd.Audio(audio, rate=hps_ms.data.sampling_rate))
      return audio

#参考https://github.com/Minami-Yuduru/-ChatGPT_VITS
def friend_chat(text,prompt0,key,mapping,call_name):
  with open(weight_path + mapping + "identity.txt", "r", encoding="utf-8") as f1:
        identity = f1.read()
  call_name = call_name
  openai.api_key = key
  #identity = '女'
  start_sequence = '\n'+str(call_name)+':'
  restart_sequence = "\nYou: "
  all_text = identity + restart_sequence
  if prompt0 == '':
     prompt0 = text #当期prompt
  if prompt0 == 'quit':
     return prompt0
  prompt = identity + prompt0 + start_sequence

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=["\nYou:"]
  )
  return response['choices'][0]['text'].strip()

#定义id和角色名的对照关系  
def selection(speaker):
    if speaker == 0:
        spk = "南小鸟"
        return spk

    elif speaker == 1:
        spk = "园田海未"
        return spk

    elif speaker == 2:
        spk = "小泉花阳"
        return spk

    elif speaker == 3:
        spk = "星空凛"
        return spk

    elif speaker == 4:
        spk = "东条希"
        return spk
    
    elif speaker == 5:
        spk = "矢泽妮可"
        return spk

    elif speaker == 6:
        spk = "绚濑绘里"
        return spk

    elif speaker == 7:
        spk = "西木野真姬"
        return spk
    elif speaker == 8:
        spk = "艾玛.维尔德"
        return spk
    elif speaker == 9:
        spk = "高坂穗乃果"
        return spk
    elif speaker == 10:
        spk = "三船栞子"
        return spk
    elif speaker == 12:
        spk = "米娅.泰勒"
        return spk
    elif speaker == 11:
        spk = "钟岚珠"
        return spk
    else:
        return "高咲侑"
#CHATGPT抓取
#session_token = '参考https://www.youtube.com/watch?v=TdNSj_qgdFk'
#api = ChatGPT(session_token)

#输出文本对应的api
@app.route('/word')
def show():
    mapping = request.args.get('mapping','')
    with open(weight_path + mapping + "temp.txt", "r", encoding="utf-8") as f1:
        text = f1.read()
        return text.replace('[JA]','').replace('[ZH]','')

#用txt记录设定文档
@app.route('/identity')
def writing():
    text = request.args.get('text','')
    mapping = request.args.get('mapping','')
    with open(weight_path+ mapping + "identity.txt", "w", encoding="utf-8") as f1:
        f1.write(text)
    with open(weight_path+ mapping + "identity.txt", "r", encoding="utf-8") as f1:
        text = f1.read()
        return text

#默认GPT3也可自行改成用表格的方式接收数据
@app.route('/gpt')
def gpt_api():
    text = request.args.get('text','')
#    text = friend_chat(text)
#    key = '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'
    api_key = request.args.get('api_key','')
    mapping = request.args.get('mapping','')
    speakers_name = request.args.get('speakers_name','')
    noise_scale = request.args.get('noise_scale','')
    noise_scale_w = request.args.get('noise_scale','')
    speaking_speed =  request.args.get('spd','')
    noise_scale = float(noise_scale)
    noise_scale_w = float(noise_scale_w)
    speaking_speed = float(speaking_speed)
    text = friend_chat(text,'',api_key,mapping,selection(int(speakers_name)))
    text= text.replace("：","。").replace("；","。").replace(":","。").replace(";","。").replace("\n","")
    def is_japanese(string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False    
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    audio = tts(text,speakers_name,noise_scale,noise_scale_w,speaking_speed)
    write(weight_path+mapping+'temp2.wav',22050, audio)
    wav = AudioSegment.from_wav(weight_path+mapping+'temp2.wav')
    wav.export(weight_path+mapping+'now2.ogg', format="ogg")
    with open(weight_path+mapping+"temp.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open(weight_path+mapping+'now2.ogg','rb') as bit:
        wav_bytes = bit.read()
    return wav_bytes, 200, {'Content-Type': 'audio/ogg'}
   # return audio_text

'''chatgpt受限非常多，几乎不能提供稳定的链接，爬几次就给你锁了（），记得删掉144行和145行的注释
@app.route('/chatgpt')
def chatgpt_api():
    text = request.args.get('text','')
#    text = friend_chat(text)
#    key = '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'
#    api_key = request.args.get('api_key','')
    mapping = request.args.get('mapping','')
    speakers_name = request.args.get('speakers_name','')
    noise_scale = request.args.get('noise_scale','')
    noise_scale_w = request.args.get('noise_scale','')
    speaking_speed =  request.args.get('spd','')
    noise_scale = float(noise_scale)
    noise_scale_w = float(noise_scale_w)
    speaking_speed = float(speaking_speed)
    response_from_chatgpt = api.send_message(text)
    text= response_from_chatgpt['message'].replace('\n','').replace(' ','')
    def is_japanese(string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False    
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    audio = tts(text,speakers_name,noise_scale,noise_scale_w,speaking_speed)
    write(weight_path+mapping+'temp2.wav',22050, audio)
    wav = AudioSegment.from_wav(weight_path+mapping+'temp2.wav')
    wav.export(weight_path+mapping+'now2.ogg', format="ogg")
    with open(weight_path+mapping+"temp.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open(weight_path+mapping+'now2.ogg','rb') as bit:
        wav_bytes = bit.read()
    return wav_bytes, 200, {'Content-Type': 'audio/ogg'}
   # return audio_text
'''    

if __name__ == '__main__':
    app.run("0.0.0.0", 8080,debug=True)