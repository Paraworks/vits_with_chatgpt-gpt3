#one speaker only,you can get the model here: https://github.com/innnky/MB-iSTFT-VITS
import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import io
from scipy.io.wavfile import write
from flask import Flask, request
from pydub import AudioSegment
import threading
import openai
app = Flask(__name__)
mutex = threading.Lock()
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm
#using nene, you can find it in the /MB-iSTFT-VITS/tree/main/configs
hps = utils.get_hparams_from_file("path/to/ljs_mb_istft_vits.json")
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
_ = net_g.eval()
#https://huggingface.co/innnky/mb-vits-models/resolve/main/tempbest.pth
_ = utils.load_checkpoint("path/to/model/tempbest.pth", net_g, None)
import time
#Editing your setting here
def friend_chat(text):
  call_name = "her name"
  openai.api_key = "your-openai-key"
  identity = "my waifu"
  start_sequence = '\n'+str(call_name)+':'
  restart_sequence = "\nYou: "
  all_text = identity + restart_sequence
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

def tts(txt):
    audio = None
    if mutex.acquire(blocking=False):
        try:
            stn_tst = get_text(txt, hps)
            with torch.no_grad():
                x_tst = stn_tst.unsqueeze(0)
                x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                t1 = time.time()
                audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8,
                                            length_scale=1)[0][0, 0].data.float().numpy()
                t2 = time.time()
                print("推理时间：", (t2 - t1), "s")
        finally:
            mutex.release()
    return audio

def is_japanese(string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False    

@app.route('/gpt')
def text_api():
    text = request.args.get('text','')
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    Response = friend_chat(text)
    with open("temp.txt", "w", encoding="utf-8") as f:
        f.write(Response)
    text = f"[JA]{Response}[JA]" if is_japanese(Response) else f"[ZH]{Response}[ZH]"
    audio = tts(text)
    write('temp2.wav',22050, audio)
    wav = AudioSegment.from_wav('temp2.wav')
    wav.export('now2.ogg', format="ogg")
    with open("temp.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open('now2.ogg','rb') as bit:
        wav_bytes = bit.read()
    return wav_bytes, 200, {'Content-Type': 'audio/ogg'}
@app.route('/word')
def show():
    with open("temp.txt","r", encoding="utf-8") as f1:
        text = f1.read()
        return text.replace('[JA]','').replace('[ZH]','')
#on your server
if __name__ == '__main__':
   app.run("0.0.0.0", 8080)
