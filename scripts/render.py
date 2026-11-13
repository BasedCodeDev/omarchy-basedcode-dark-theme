#!/usr/bin/env python3
"""Deterministic, periodic colour fields. Original procedural artwork, no external imagery.
Render a text-free low-frequency field at 1280x720 and upscale.
"""
import argparse, json, math, pathlib, subprocess
import numpy as np
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGN = json.loads((ROOT/'src/design.json').read_text())
CFG = DESIGN['wallpaper']
def rgb(hex_value): return np.array([int(hex_value[i:i+2],16) for i in (1,3,5)],dtype=np.float32)
X,Y = np.meshgrid(np.linspace(0,1,1280,dtype=np.float32),np.linspace(0,1,720,dtype=np.float32))
NOISE = np.random.default_rng(CFG['seed']).uniform(-0.65,0.65,(*X.shape,1)).astype(np.float32)
def frame(t, width=3840, height=2160):
    if CFG.get('solid_color'):
        return Image.new('RGB', (width, height), CFG['solid_color'])
    p = 2*math.pi*t/CFG['seconds']
    # Two broad ribbons, their centres and light travelling periodically.
    curve = .64 - .23*np.sin(X*3.4-.6) + .045*np.sin(X*5+p)
    envelope = np.exp(-((X-.53)/.65)**4)
    body = np.exp(-((Y-curve)/.18)**2)*envelope
    edge = np.exp(-((Y-curve+.055)/.033)**2)*envelope
    second = np.exp(-((Y-(.75-.32*X+.025*np.cos(p+X*6)))/.11)**2)
    travel = .5+.5*np.cos(X*5-p)
    # Feather the base grey at the top for a transparent bar and at the lower edge.
    mask = np.clip(Y/.22,0,1) * np.clip((1-Y)/.19,0,1)
    carbon = rgb('#1D221D')
    a = np.broadcast_to(carbon,(*X.shape,3)).copy()
    def layer(col, amount):
        nonlocal a
        alpha = np.clip(amount*mask,0,1)[...,None]
        a = a*(1-alpha)+rgb(col)*alpha
    layer('#1D221D',np.full_like(X,.6))
    layer('#1E231E',body*.86)
    layer('#1F241F',second*.52)
    layer('#202420',body*(.2+.25*travel))
    layer('#232623',edge*(.16+.30*travel))
    a = np.clip(a+NOISE,0,255).astype(np.uint8)
    im = Image.fromarray(a).resize((width,height),Image.Resampling.BICUBIC)
    return im
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--video',action='store_true'); ap.add_argument('--width',type=int,default=3840); ap.add_argument('--height',type=int,default=2160)
    args=ap.parse_args(); out=ROOT/'theme/backgrounds'; out.mkdir(exist_ok=True)
    frame(0).save(out/'02-basedcode-still.png')
    qa=ROOT/'qa'; qa.mkdir(exist_ok=True)
    frame(0,1280,720).save(qa/'wallpaper-review.png')
    frames=[frame(t,640,360) for t in (0,2,4,6,8,10)]
    sheet=Image.new('RGB',(1920,720))
    for i,im in enumerate(frames): sheet.paste(im,((i%3)*640,(i//3)*360))
    sheet.save(qa/'motion-contact-sheet.png')
    master=frame(0)
    portrait=master.crop((1312,0,2528,2160)).resize((608,1080),Image.Resampling.LANCZOS)
    portrait.save(qa/'portrait-review.png')
    if args.video:
        cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{args.width}x{args.height}','-r',str(CFG['fps']),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart','-threads','4',str(out/'03-basedcode-motion.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for i in range(CFG['fps']*CFG['seconds']):
                proc.stdin.write(frame(i/CFG['fps'],args.width,args.height).tobytes())
                if i%60==0: print(f'Rendered {i}/360 frames',flush=True)
            proc.stdin.close()
            if proc.wait(): raise RuntimeError('Video encode failed')
        except BaseException:
            proc.kill(); proc.wait(); raise
    metadata={'wordmark':False,
              'still_size':[3840,2160],'video_size':[args.width,args.height] if args.video else None,
              'fps':CFG['fps'],'seconds':CFG['seconds'],'seed':CFG['seed']}
    (ROOT/'qa/render-inputs.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('Wallpaper assets ready',flush=True)
if __name__=='__main__': main()
