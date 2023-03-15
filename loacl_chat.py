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
import onnxruntime as ort
import time
from pydub import AudioSegment
import io
import os
from transformers import AutoTokenizer, AutoModel
app = Flask(__name__)
mutex = threading.Lock()
def get_args():
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--onnx_model', default = './moe/model.onnx')
    parser.add_argument('--cfg', default="./moe/config_v.json")
    parser.add_argument('--outdir', default="./moe",
                        help='ouput folder')
    parser.add_argument('--ChatGLM',default = "./moe",
                        help='https://github.com/THUDM/ChatGLM-6B')
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

#注意:对于不同的cleaner，需要自行修改symbols
def infer(text):
    #选择你想要的角色
    sid = 3
    text = f"[JA]{text}[JA]" if is_japanese(text) else f"[ZH]{text}[ZH]"
    seq = text_to_sequence(text, symbols=hps.symbols, cleaner_names=hps.data.text_cleaners)
    #seq = text_to_sequence(text, cleaner_names=hps.data.text_cleaners)
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
        wavfile.write(outdir + '/temp1.wav',hps.data.sampling_rate, audio.astype(np.int16))
        cmd = 'ffmpeg -y -i ' +  outdir + '/temp1.wav' + ' -ar 44100 '+ outdir + '/temp2.wav'
        os.system(cmd)
    return text
tokenizer = AutoTokenizer.from_pretrained(args.ChatGLM, trust_remote_code=True)
#8G GPU
model = AutoModel.from_pretrained(args.ChatGLM, trust_remote_code=True).half().quantize(4).cuda()
history = []
@app.route('/chat')
def text_api():
    global history
    message = request.args.get('Text','')
    t1 = time.time()
    if message == 'clear':
      history = []
    else:
      response, new_history = model.chat(tokenizer, message, history)
      response = response.replace(" ",'').replace("\n",'.')
      text = infer(response)
      text = text.replace('[JA]','').replace('[ZH]','')
      with open(outdir +'/temp2.wav','rb') as bit:
          wav_bytes = bit.read()
      headers = {
            'Content-Type': 'audio/wav',
            'Text': text.encode('utf-8')}
      history = new_history
      t2 = time.time()
      spending_time = "总耗时："+str(t2-t1)+"s" 
      print(spending_time)
      return wav_bytes, 200, headers
if __name__ == '__main__':
   app.run("0.0.0.0", 8080) 
