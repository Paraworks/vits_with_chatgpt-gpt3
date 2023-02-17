#需要额外安装的包：、openai pyChatGPT
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
import argparse
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

#设定存储各种数据的目录，方便查看，默认/moe/
app = Flask(__name__)
mutex = threading.Lock()
def get_args():
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--model', default = './moe/model.pth')
    parser.add_argument('--audio',
                    type=str,
                    help='你要替换的音频文件',
                    default = 'path/to/temp.wav')
    parser.add_argument('--cfg', default="./moe/config.json")
    parser.add_argument('--outdir', default="./moe",
                        help='ouput directory')
    parser.add_argument('--key',default = "see openai key",
                        help='see openai')
    args = parser.parse_args()
    return args
args = get_args()
#设置gpu推理
dev = torch.device("cuda:0")
#导入config文件
hps_ms = utils.get_hparams_from_file(args.cfg)
#加载多人模型
net_g_ms = SynthesizerTrn(
    len(symbols),
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=hps_ms.data.n_speakers,
    **hps_ms.model).to(dev)
_ = net_g_ms.eval()
#导入模型文件
_ = utils.load_checkpoint(args.model, net_g_ms, None)
#语言检测
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
#修改参数的语音合成
def infer(text):
  #CHATGPT抓取
  #session_token = '参考https://www.youtube.com/watch?v=TdNSj_qgdFk'
  #api = ChatGPT(session_token)
  #response_from_chatgpt = api.send_message(text)
  text = gpt3_chat(text)
  text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
  speaker_id = 1
  stn_tst = get_text(text, hps_ms)
  with torch.no_grad():
      x_tst = stn_tst.unsqueeze(0).to(dev)
      x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(dev)
      sid = torch.LongTensor([speaker_id]).to(dev)
      audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=0.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
    #  ipd.display(ipd.Audio(audio, rate=hps_ms.data.sampling_rate))
      write(args.outdir + '/temp1.wav',22050,audio)
      cmd = 'ffmpeg -y -i ' +  args.outdir + '/temp1.wav' + ' -ar 44100 '+ args.audio
      os.system(cmd)
      return text

#记得修改indentity
def gpt3_chat(text):
  call_name = "宁宁"
  openai.api_key = args.key
  identity = ""
  start_sequence = '\n'+str(call_name)+':'
  restart_sequence = "\nYou: "
  if 1 == 1:
     prompt0 = text #当期prompt
  if text == 'quit':
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

def main():
    while True:
      text = input("You:")
      text = infer(text)
      print('Waifu:'+text.replace("[ZH]","").replace("[JA]",""))
