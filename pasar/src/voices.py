"""Bikin audio + timeline. Kalau ada file voices/NN.mp3 (dari ElevenLabs), file itu dipakai;
kalau tidak, pakai TTS lokal (espeak-ng + MBROLA)."""
import subprocess, json, wave, struct, math, os, sys
P = sys.argv[1]; B = sys.argv[2]  # P = folder proyek, B = folder build
os.makedirs(f"{B}/aud", exist_ok=True)
# (pembicara, teks tampil, teks TTS, jeda sebelum baris)
LINES = [
 ("SUAMI","Aku pergi dulu, ya.","Aku pergi dulu, ya.",1.0),
 ("ISTRI","Mau ke mana?","Mau ke mana?",0.3),
 ("SUAMI","Ke pasar.","Ke pasar.",0.3),
 ("ISTRI","Aku ikut.","Aku ikut.",0.3),
 ("SUAMI","Ngapain kamu ikut segala?","Ngapain kamu ikut segala?",0.3),
 ("ISTRI","Please...","Pliiis.",0.3),
 ("SUAMI","Ya udah, oke.","Ya udah, oke.",0.4),
 ("ISTRI","Tunggu dua menit ya, aku pakai sandal dulu.","Tunggu dua menit ya, aku pakai sandal dulu.",0.3),
 ("SUAMI","Oke.","Oke.",0.4),
 ("ISTRI","Ayo!","Ayo!",1.8),
 ("ISTRI","Tuh kan, pergi duluan, dasar anjing! Awas aja nanti kalau pulang, aku kasih 'makan' yang enak.","Tuh kan, pergi duluan, dasar anjing! Awas aja nanti kalau pulang, aku kasih makan yang enak.",1.6),
 ("ISTRI","Nunggu dua menit aja nggak bisa.","Nunggu dua menit aja nggak bisa.",0.3),
 ("SUAMI","Ada apa nih?","Ada apa nih?",1.0),
 ("ISTRI","Ayo, baby~","Ayo, bebi.",0.4),
 ("ANAK","(tertawa) Wah, mantap!","Ha ha ha ha! Wah, mantap!",1.0),
]
FPS=30; SR=22050
TTS = {"SUAMI":(["-s","150","-p","35"],"aresample=22050"),
       "ISTRI":(["-s","140","-p","70"],"asetrate=16000*1.32,aresample=22050,atempo=0.82,highpass=f=120"),
       "ANAK":(["-s","150","-p","80"],"asetrate=16000*1.5,aresample=22050,atempo=0.75,highpass=f=150")}
clips=[]; t=0
for i,(who,disp,say,gap) in enumerate(LINES):
    t+=gap
    src=f"{P}/voices/{i+1:02d}.mp3"; out=f"{B}/aud/{i}.wav"
    if os.path.exists(src):
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse","-ac","1","-ar",str(SR),out],check=True)
    else:
        raw=f"{B}/aud/{i}_raw.wav"; args,af=TTS[who]
        subprocess.run(["espeak-ng","-v","mb-id1",*args,"-w",raw,say],check=True,stderr=subprocess.DEVNULL)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",af+",volume=1.6","-ac","1","-ar",str(SR),out],check=True)
    w=wave.open(out); n=w.getnframes(); data=struct.unpack(f"<{n}h",w.readframes(n)); w.close()
    step=SR//FPS; env=[]
    for k in range(0,n,step):
        seg=data[k:k+step]; env.append(math.sqrt(sum(x*x for x in seg)/max(1,len(seg)))/32768)
    mx=max(env) or 1; env=[round(min(1,e/mx*1.4),3) for e in env]
    dur=n/SR
    clips.append(dict(who=who,text=disp,s=round(t,3),e=round(t+dur,3),env=env,file=out))
    t+=dur
total=round(t+1.8,2)
inputs=[];filt=[]
for i,c in enumerate(clips):
    inputs+=["-i",c["file"]]; ms=int(c["s"]*1000); filt.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(clips)))+f"amix=inputs={len(clips)}:normalize=0,apad,atrim=0:{total}[out]")
subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(filt),"-map","[out]",f"{B}/voice.wav"],check=True)
json.dump(dict(fps=FPS,total=total,clips=[{k:v for k,v in c.items() if k!='file'} for c in clips]),open(f"{B}/timeline.json","w"))
print("total",total)
