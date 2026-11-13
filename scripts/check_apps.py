#!/usr/bin/env python3
"""Use available native parsers and validate the actual Aether highlight output."""
import hashlib,json,os,pathlib,shutil,subprocess,sys
from validate import contrast
ROOT=pathlib.Path(__file__).resolve().parents[1]
results={}
for name,command in {
    'foot':['foot','-C','-c',str(ROOT/'build/generated/foot.ini')],
    'ghostty':['ghostty','+validate-config','--config-file='+str(ROOT/'build/generated/ghostty.conf')],
    'hyprland_lua':['luac','-p',str(ROOT/'build/generated/hyprland.lua')],
    'neovim_lua':['luac','-p',str(ROOT/'build/generated/neovim.lua')],
}.items():
    if not shutil.which(command[0]): results[name]='not installed'; continue
    subprocess.run(command,check=True,capture_output=True,text=True); results[name]='pass'
aether=pathlib.Path.home()/'.local/share/nvim/lazy/aether'
if shutil.which('nvim') and aether.exists():
    env=dict(os.environ,BASEDCODE_ROOT=str(ROOT),XDG_CACHE_HOME=str(ROOT/'build/nvim-cache'))
    subprocess.run(['nvim','--headless','-u','NONE','-i','NONE','-l',str(ROOT/'scripts/check_nvim.lua')],env=env,check=True,capture_output=True,text=True)
    h=json.loads((ROOT/'qa/nvim-highlights.json').read_text())
    pairs={}
    for name,g in h.items():
        fg=g.get('fg',h['Normal'].get('fg',0xffffff)); bg=g.get('bg',h['Normal'].get('bg',0x121014))
        ratio=contrast(f'#{fg:06x}',f'#{bg:06x}'); assert ratio>=4.5,(name,ratio)
        pairs[name]=round(ratio,2)
    results['aether_highlight_contrast']=pairs
else: results['aether_highlight_contrast']='Aether or Neovim not installed'
(ROOT/'qa/app-validation.json').write_text(json.dumps(results,indent=2)+'\n')
font=pathlib.Path(subprocess.check_output(['fc-match','JetBrains Mono:style=Bold','-f','%{file}'],text=True))
build={'python':sys.version.split()[0],'omarchy':subprocess.check_output(['omarchy','version'],text=True).strip(),
       'ffmpeg':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
       'font_file':font.name,'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest(),
       'template_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(pathlib.Path('/usr/share/omarchy/default/themed').glob('*.tpl'))}}
(ROOT/'qa/build-info.json').write_text(json.dumps(build,indent=2)+'\n')
print(json.dumps(results,indent=2))
