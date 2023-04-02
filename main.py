import logging
logging.getLogger('numba').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
from text import text_to_sequence
import numpy as np
from scipy.io import wavfile
import torch
import json
import commons
import utils
import sys
import pathlib
import onnxruntime as ort
import gradio as gr
import argparse
import time
import os
import io
from scipy.io.wavfile import write
from flask import Flask, request
from threading import Thread
import openai
import requests
class VitsGradio:
    def __init__(self):
        self.lan = ["中文","日文","自动"]
        self.chatapi = ["gpt-3.5-turbo","gpt3"]
        self.modelPaths = []
        for root,dirs,files in os.walk("checkpoints"):
            for dir in dirs:
                self.modelPaths.append(dir)
        with gr.Blocks() as self.Vits:
            with gr.Tab("调试用"):
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            with gr.Column():
                                self.text = gr.TextArea(label="Text", value="你好")
                                with gr.Accordion(label="测试api", open=False):
                                    self.local_chat1 = gr.Checkbox(value=False, label="使用网址+文本进行模拟")
                                    self.url_input = gr.TextArea(label="键入测试", value="http://127.0.0.1:8080/chat?Text=")
                                    butto = gr.Button("测试从网页端获取文本")
                                btnVC = gr.Button("测试tts+对话程序")
                            with gr.Column():
                                output2 = gr.TextArea(label="回复")
                                output1 = gr.Audio(label="采样率22050")
                                output3 = gr.outputs.File(label="44100hz: output.wav")
                butto.click(self.Simul, inputs=[self.text, self.url_input], outputs=[output2,output3])
                btnVC.click(self.tts_fn, inputs=[self.text], outputs=[output1,output2])
            with gr.Tab("控制面板"):
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            with gr.Column():
                                self.api_input1 = gr.TextArea(label="输入api-key或本地存储说话模型的路径", value="https://platform.openai.com/account/api-keys")
                                with gr.Accordion(label="chatbot选择", open=False):
                                                self.api_input2 = gr.Checkbox(value=True, label="采用gpt3.5")
                                                self.local_chat1 = gr.Checkbox(value=False, label="启动本地chatbot")
                                                self.local_chat2 = gr.Checkbox(value=True, label="是否量化")
                                                res = gr.TextArea()
                                Botselection = gr.Button("确认模型")
                                Botselection.click(self.check_bot, inputs=[self.api_input1,self.api_input2,self.local_chat1,self.local_chat2], outputs = [res])
                                self.input1 = gr.Dropdown(label = "模型", choices = self.modelPaths, value = self.modelPaths[0], type = "value")
                                self.input2 = gr.Dropdown(label="Language", choices=self.lan, value="自动", interactive=True)
                            with gr.Column():
                                btnVC = gr.Button("Submit")
                                self.input3 = gr.Dropdown(label="Speaker", choices=list(range(101)), value=0, interactive=True)
                                self.input4 = gr.Slider(minimum=0, maximum=1.0, label="更改噪声比例(noise scale)，以控制情感", value=0.267)
                                self.input5 = gr.Slider(minimum=0, maximum=1.0, label="更改噪声偏差(noise scale w)，以控制音素长短", value=0.7)
                                self.input6 = gr.Slider(minimum=0.1, maximum=10, label="duration", value=1)
                                statusa = gr.TextArea()
                btnVC.click(self.create_tts_fn, inputs=[self.input1, self.input2, self.input3, self.input4, self.input5, self.input6], outputs = [statusa])

    def Simul(self,text,url_input):
        web = url_input + text
        res = requests.get(web)
        music = res.content
        with open('output.wav', 'wb') as code:
            code.write(music)
        file_path = "output.wav"
        return web,file_path


    def chatgpt(self,text):
        self.messages.append({"role": "user", "content": text},)
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages= self.messages)
        reply = chat.choices[0].message.content
        return reply
    
    def ChATGLM(self,text):
        if text == 'clear':
            self.history = []
        response, new_history = self.model.chat(self.tokenizer, text, self.history)
        response = response.replace(" ",'').replace("\n",'.')
        self.history = new_history
        return response
    
    def gpt3_chat(self,text):
        call_name = "Waifu"
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
    
    def check_bot(self,api_input1,api_input2,local_chat1,local_chat2):
        if local_chat1:
            from transformers import AutoTokenizer, AutoModel
            self.tokenizer = AutoTokenizer.from_pretrained(api_input1, trust_remote_code=True)
            if local_chat2:
                self.model = AutoModel.from_pretrained(api_input1, trust_remote_code=True).half().quantize(4).cuda()
            else:
                self.model = AutoModel.from_pretrained(api_input1, trust_remote_code=True)
            self.history = []
        else:
            self.messages = []
            openai.api_key = api_input1
        return "Finished"
    
    def is_japanese(self,string):
        for ch in string:
            if ord(ch) > 0x3040 and ord(ch) < 0x30FF:
                return True
        return False
    
    def is_english(self,string):
        import re
        pattern = re.compile('^[A-Za-z0-9.,:;!?()_*"\' ]+$')
        if pattern.fullmatch(string):
            return True
        else:
            return False

    def get_symbols_from_json(self,path):
        assert os.path.isfile(path)
        with open(path, 'r') as f:
            data = json.load(f)
        return data['symbols']

    def sle(self,language,text):
        text = text.replace('\n','。').replace(' ',',')
        if language == "中文":
            tts_input1 = "[ZH]" + text + "[ZH]"
            return tts_input1
        elif language == "自动":
            tts_input1 = f"[JA]{text}[JA]" if self.is_japanese(text) else f"[ZH]{text}[ZH]"
            return tts_input1
        elif language == "日文":
            tts_input1 = "[JA]" + text + "[JA]"
            return tts_input1

    def get_text(self,text,hps_ms):
        text_norm = text_to_sequence(text,hps_ms.data.text_cleaners)
        if hps_ms.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def create_tts_fn(self,path, input2, input3, n_scale= 0.667,n_scale_w = 0.8, l_scale = 1 ):
        self.symbols = self.get_symbols_from_json(f"checkpoints/{path}/config.json")
        self.hps = utils.get_hparams_from_file(f"checkpoints/{path}/config.json")
        phone_dict = {
                symbol: i for i, symbol in enumerate(self.symbols)
            }
        self.ort_sess = ort.InferenceSession(f"checkpoints/{path}/model.onnx")
        self.language = input2
        self.speaker_id = input3
        self.n_scale = n_scale
        self.n_scale_w = n_scale_w
        self.l_scale = l_scale
        print(self.language,self.speaker_id,self.n_scale)
        return 'success'
    
    def tts_fn(self,text):
        if self.local_chat1:
            text = self.chatgpt(text)
        elif self.api_input2:
            text = self.ChATGLM(text)
        else:
            text = self.gpt3_chat(text)
        print(text)
        text =self.sle(self.language,text)
        seq = text_to_sequence(text, cleaner_names=self.hps.data.text_cleaners)
        if self.hps.data.add_blank:
            seq = commons.intersperse(seq, 0)
        with torch.no_grad():
            x = np.array([seq], dtype=np.int64)
            x_len = np.array([x.shape[1]], dtype=np.int64)
            sid = np.array([self.speaker_id], dtype=np.int64)
            scales = np.array([self.n_scale, self.n_scale_w, self.l_scale], dtype=np.float32)
            scales.resize(1, 3)
            ort_inputs = {
                        'input': x,
                        'input_lengths': x_len,
                        'scales': scales,
                        'sid': sid
                    }
            t1 = time.time()
            audio = np.squeeze(self.ort_sess.run(None, ort_inputs))
            audio *= 32767.0 / max(0.01, np.max(np.abs(audio))) * 0.6
            audio = np.clip(audio, -32767.0, 32767.0)
            t2 = time.time()
            spending_time = "推理时间："+str(t2-t1)+"s" 
            print(spending_time)
            bytes_wav = bytes()
            byte_io = io.BytesIO(bytes_wav)
            wavfile.write('moe/temp1.wav',self.hps.data.sampling_rate, audio.astype(np.int16))
            cmd = 'ffmpeg -y -i '  + 'moe/temp1.wav' + ' -ar 44100 ' + 'moe/temp2.wav'
            os.system(cmd)    
        return (self.hps.data.sampling_rate, audio),text.replace('[JA]','').replace('[ZH]','')

app = Flask(__name__)
print("开始部署")
grVits = VitsGradio()

@app.route('/chat')
def text_api():
    message = request.args.get('Text','')
    audio,text = grVits.tts_fn(message)
    text = text.replace('[JA]','').replace('[ZH]','')
    with open('moe/temp2.wav','rb') as bit:
        wav_bytes = bit.read()
    headers = {
            'Content-Type': 'audio/wav',
            'Text': text.encode('utf-8')}
    return wav_bytes, 200, headers

def gradio_interface():
    return grVits.Vits.launch()

if __name__ == '__main__':
    api_thread = Thread(target=app.run, args=("0.0.0.0", 8080))
    gradio_thread = Thread(target=gradio_interface)
    api_thread.start()
    gradio_thread.start()
