import subprocess, json, wave, struct, math, os, sys
D = sys.argv[1]
os.makedirs(f"{D}/aud", exist_ok=True)
script = [
 ("F","Kamu kenapa sih, dari tadi liatin HP terus?"),
 ("M","Lagi mikir, mau makan apa nih."),
 ("F","Ya ampun! Dari tadi cuma mikirin makan?"),
 ("M","Laper itu serius, tau!"),
 ("F","Ya udah, kita beli bakso aja yuk."),
 ("M","Nah, gitu dong! Kamu emang paling ngerti aku."),
 ("F","Tapi kamu yang bayar, ya."),
 ("M","Hmm... tiba-tiba aku kenyang."),
]
FPS=30; SR=22050; GAP=0.45
clips=[]; t=0.8
for i,(who,txt) in enumerate(script):
    raw=f"{D}/aud/{i}_raw.wav"; out=f"{D}/aud/{i}.wav"
    if who=="F":
        subprocess.run(["espeak-ng","-v","mb-id1","-s","135","-p","70","-w",raw,txt],check=True)
        af="asetrate=16000*1.32,aresample=22050,atempo=0.82,highpass=f=120,volume=1.6"
    else:
        subprocess.run(["espeak-ng","-v","mb-id1","-s","140","-p","40","-w",raw,txt],check=True)
        af="aresample=22050,volume=1.6"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",af,"-ac","1","-ar",str(SR),out],check=True)
    w=wave.open(out); n=w.getnframes(); data=struct.unpack(f"<{n}h",w.readframes(n)); w.close()
    dur=n/SR; step=SR//FPS; env=[]
    for k in range(0,n,step):
        seg=data[k:k+step]; env.append(math.sqrt(sum(x*x for x in seg)/max(1,len(seg)))/32768)
    mx=max(env) or 1; env=[round(min(1,e/mx*1.4),3) for e in env]
    clips.append(dict(who=who,text=txt,start=round(t,3),dur=round(dur,3),env=env,file=out))
    t+=dur+GAP
total=round(t+1.2,2)
# mix audio track
inputs=[];filt=[]
for i,c in enumerate(clips):
    inputs+=["-i",c["file"]]; ms=int(c["start"]*1000); filt.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(clips)))+f"amix=inputs={len(clips)}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(filt),"-map","[out]",f"{D}/voice.wav"],check=True)
json.dump(dict(fps=FPS,total=total,clips=[{k:v for k,v in c.items() if k!='file'} for c in clips]),open(f"{D}/timeline.json","w"))
print("total",total)
