import argparse
from text import text_to_sequence
import numpy as np
from scipy.io import wavfile
import torch
import json
import commons
import utils
import sys
import pathlib
from flask import Flask, request
import threading
import openai
import onnxruntime as ort
import time
from pydub import AudioSegment
import io
app = Flask(__name__)
mutex = threading.Lock()
def get_args():
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--onnx_model', default = '../moe/model.onnx')
    parser.add_argument('--cfg', default="../moe/config.json")
    parser.add_argument('--outdir', default="../moe",
                        help='ouput directory')
    args = parser.parse_args()
    return args

def to_numpy(tensor: torch.Tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad \
        else tensor.detach().numpy()

def get_symbols_from_json(path):
    import os
    assert os.path.isfile(path)
    with open(path, 'r') as f:
        data = json.load(f)
    return data['symbols']

args = get_args()
symbols = get_symbols_from_json(args.cfg)
phone_dict = {
        symbol: i for i, symbol in enumerate(symbols)
    }
hps = utils.get_hparams_from_file(args.cfg)
ort_sess = ort.InferenceSession(args.onnx_model)
outdir = args.outdir
def is_japanese(string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False 

def friend_chat(text):
  call_name = "派蒙"
  openai.api_key = "your openai key"
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

def infer(text):
    sid = 16
    text = friend_chat(text)
    with open(outdir + "/temp.txt", "w", encoding="utf-8") as f:
        f.write(text)
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    seq = text_to_sequence(text, cleaner_names=hps.data.text_cleaners
                                   )
    if hps.data.add_blank:
        seq = commons.intersperse(seq, 0)
    with torch.no_grad():
        x = np.array([seq], dtype=np.int64)
        x_len = np.array([x.shape[1]], dtype=np.int64)
        sid = np.array([sid], dtype=np.int64)
        scales = np.array([0.667, 0.8, 1], dtype=np.float32)
        scales.resize(1, 3)
        ort_inputs = {
                    'input': x,
                    'input_lengths': x_len,
                    'scales': scales,
                    'sid': sid
                }
        t1 = time.time()
        audio = np.squeeze(ort_sess.run(None, ort_inputs))
        audio *= 32767.0 / max(0.01, np.max(np.abs(audio))) * 0.6
        audio = np.clip(audio, -32767.0, 32767.0)
        t2 = time.time()
        spending_time = "推理时间："+str(t2-t1)+"s" 
        print(spending_time)
        bytes_wav = bytes()
        byte_io = io.BytesIO(bytes_wav)
        wavfile.write(outdir + '/temp2.wav',hps.data.sampling_rate, audio.astype(np.int16))
        wav = AudioSegment.from_wav(outdir + '/temp2.wav')
        wav.export(outdir +'/now2.ogg', format="ogg")


@app.route('/gpt')
def text_api():
    text = request.args.get('text','')
    infer(text)
    with open(outdir +'/now2.ogg','rb') as bit:
        wav_bytes = bit.read()
    return wav_bytes, 200, {'Content-Type': 'audio/ogg'}
@app.route('/word')
def show():
    with open(outdir + "/temp.txt","r", encoding="utf-8") as f1:
        text = f1.read()
        return text.replace('[JA]','').replace('[ZH]','')
#on your server
if __name__ == '__main__':
   app.run("0.0.0.0", 8080)