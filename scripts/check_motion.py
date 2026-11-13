#!/usr/bin/env python3
"""Check periodic continuity and decode first/last compressed frames for seam comparison."""
import importlib.util,json,pathlib,subprocess
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render',ROOT/'scripts/render.py')
render=importlib.util.module_from_spec(spec); spec.loader.exec_module(render)
a=np.asarray(render.frame(0,640,360),dtype=np.float32)
b=np.asarray(render.frame(12,640,360),dtype=np.float32)
c=np.asarray(render.frame(2,640,360),dtype=np.float32)
period=float(np.abs(a-b).max()); change=float(np.abs(a-c).mean())
assert period<=1,period
if render.CFG.get('solid_color'):
    from PIL import Image
    expected=tuple(int(render.CFG['solid_color'][i:i+2],16) for i in (1,3,5))
    still=Image.open(ROOT/'theme/backgrounds/02-basedcode-dark-still.png').convert('RGB')
    assert still.getextrema()==tuple((v,v) for v in expected)
    assert change==0 and period==0
    (ROOT/'qa/motion-validation.json').write_text(json.dumps({'profile':'solid','rgb':expected,'periodic_max_channel_delta':period,'two_second_mean_channel_delta':change,'legacy_animation':'retained as optional alternative'},indent=2)+'\n')
    print('Exact solid wallpaper verified; legacy animation remains optional.')
    raise SystemExit(0)
assert change>.1,change  # Subdued grey ribbons have less luminance change than the purple artwork.
media=ROOT/'theme/backgrounds/03-basedcode-dark-motion.mp4'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(media),'-vf',"select='eq(n,0)+eq(n,1)+eq(n,358)+eq(n,359)',scale=640:360",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(4,360,640,3).astype(np.float32)
seam=float(np.abs(frames[-1]-frames[0]).mean())
adjacent=max(float(np.abs(frames[1]-frames[0]).mean()),float(np.abs(frames[-1]-frames[-2]).mean()))
assert seam<max(adjacent*2,1), (seam,adjacent)
report={'periodic_max_channel_delta':period,'two_second_mean_channel_delta':change,'encoded_seam_mean_delta':seam,'encoded_adjacent_mean_delta':adjacent}
(ROOT/'qa/motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
