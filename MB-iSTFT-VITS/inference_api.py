import torch
import commons
import utils
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import io
from scipy.io.wavfile import write

from flask import Flask, request
import threading
app = Flask(__name__)
mutex = threading.Lock()

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm
hps = utils.get_hparams_from_file("./configs/ljs_mb_istft_vits.json")
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model)
_ = net_g.eval()

# _ = utils.load_checkpoint("../tempbest.pth", net_g, None)
import time


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

@app.route('/tts')
def text_api():
    text = request.args.get('text','')
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    audio = tts(text)
    if audio is None:
        return "服务器忙"
    write(byte_io, 22050, audio)
    wav_bytes = byte_io.read()

    # audio_data = base64.b64encode(wav_bytes).decode('UTF-8')
    return wav_bytes, 200, {'Content-Type': 'audio/wav'}


if __name__ == '__main__':
   app.run("0.0.0.0", 8080)
