import os, threading, time, io, requests, fitz, subprocess, traceback
from PIL import Image, ImageOps, ImageEnhance
from flask import Flask, send_file, jsonify

BASE="/tmp/aevrilo"
os.makedirs(BASE, exist_ok=True)
OUT=os.path.join(BASE,"Aevrilo_Civil_Servant_Ch1-5_1080p.mp4")
STATUS={"state":"starting","progress":0,"message":"Booting renderer"}

URLS={
"audio":os.environ["AUDIO_URL"],
"galaxy":os.environ["GALAXY_URL"],
1:os.environ["CH1_URL"],
2:os.environ["CH2_URL"],
3:os.environ["CH3_URL"],
4:os.environ["CH4_URL"],
5:os.environ["CH5_URL"],
}

SHOTS=[
(1,3,.72),(1,2,.5),(1,9,.5),(1,10,.5),(1,(3,4),.78),(1,5,.5),(1,11,.5),(1,(13,14),.76),
(1,17,.5),(1,18,.5),(1,19,.5),(1,21,.5),(1,22,.5),(1,23,.5),(1,26,.5),(1,27,.5),(1,28,.5),(1,29,.5),
(1,30,.5),(1,32,.5),(1,33,.5),(1,35,.5),(1,36,.5),(1,37,.5),(1,38,.5),(1,39,.5),(1,41,.5),(1,42,.5),
(1,43,.5),(1,44,.5),(1,45,.5),
(2,2,.5),(2,21,.5),(2,22,.5),(2,23,.5),(2,24,.5),(2,25,.5),(2,26,.5),(2,27,.5),(2,28,.5),(2,(29,30),.62),
(2,31,.5),(2,34,.5),(2,37,.5),(2,38,.5),(2,39,.5),
(3,2,.5),(3,3,.5),(3,5,.5),(3,8,.5),(3,10,.5),(3,13,.5),(3,18,.5),(3,24,.5),(3,27,.5),(3,29,.5),(3,31,.5),(3,37,.5),
(4,9,.5),(4,13,.5),(4,18,.5),(4,21,.5),(4,23,.5),(4,25,.5),(4,26,.5),(4,28,.5),(4,30,.5),(4,31,.5),(4,33,.5),(4,34,.5),(4,35,.5),(4,38,.5),(4,41,.5),(4,42,.5),
(5,4,.5),(5,8,.5),(5,9,.5),(5,10,.5),(5,12,.5),(5,14,.5),(5,15,.5),(5,16,.5),(5,17,.5),(5,19,.5),(5,21,.5),(5,24,.5),(5,28,.5),(5,30,.5),(5,33,.5),(5,37,.5),(5,41,.5),(5,41,.72),(5,42,.5),(5,44,.5),(5,45,.5),(5,46,.5),(5,47,.5),(5,48,.5)
]

anchors={1:0.0,9:23.78,16:88.02,19:115.30,23:140.12,24:153.88,31:205.96,34:230.80,37:270.86,41:300.22,43:315.46,46:321.46,49:340.44,54:407.74,62:433.74,66:459.52,74:493.38,76:511.66,81:540.88,85:575.88,92:609.28,93:611.08,94:613.48,97:641.68,98:646.54,99:655.0,100:690.275}

def make_times():
    times=[0.0]*100
    keys=sorted(anchors)
    for a,b in zip(keys[:-1],keys[1:]):
        ta,tb=anchors[a],anchors[b]
        span=b-a
        for i in range(a,b):
            times[i-1]=ta+(tb-ta)*(i-a)/span
    times[99]=anchors[100]
    return times
TIMES=make_times()

def dl(url,path):
    with requests.get(url,stream=True,allow_redirects=True,timeout=120) as r:
        r.raise_for_status()
        with open(path,"wb") as f:
            for c in r.iter_content(1024*1024):
                if c: f.write(c)

def extract_page_image(doc,pageno):
    page=doc[pageno-1]
    imgs=page.get_images(full=True)
    best=None
    for im in imgs:
        try:
            info=doc.extract_image(im[0])
            pic=Image.open(io.BytesIO(info["image"])).convert("RGB")
            area=pic.width*pic.height
            if best is None or area>best[0]: best=(area,pic.copy())
        except Exception:
            pass
    if best: return best[1]
    pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

def crop_window(img,focus=.5,target_ratio=.72):
    w,h=img.size
    ch=min(h,int(w/target_ratio))
    ch=max(min(h,int(w*1.15)),ch)
    cy=int(max(ch/2,min(h-ch/2,focus*h)))
    top=max(0,min(h-ch,cy-ch//2))
    crop=img.crop((0,top,w,top+ch))
    gray=crop.convert("L")
    mask=gray.point(lambda p: 0 if p>247 else 255)
    bbox=mask.getbbox()
    if bbox:
        l,t,r,b=bbox
        pad=12
        l=max(0,l-pad); t=max(0,t-pad); r=min(crop.width,r+pad); b=min(crop.height,b+pad)
        if (r-l)>crop.width*.45 and (b-t)>crop.height*.35:
            crop=crop.crop((l,t,r,b))
    return crop

def panel_to_canvas(panel,path):
    panel=panel.convert("RGB")
    maxw,maxh=1180,1000
    scale=min(maxw/panel.width,maxh/panel.height,1.35)
    nw=max(2,int(panel.width*scale)); nh=max(2,int(panel.height*scale))
    panel=panel.resize((nw,nh),Image.Resampling.LANCZOS)
    panel=ImageEnhance.Sharpness(panel).enhance(1.08)
    canv=Image.new("RGBA",(1920,1080),(0,0,0,0))
    x=(1920-nw)//2; y=(1080-nh)//2
    shadow=Image.new("RGBA",(nw,nh),(0,0,0,150))
    canv.alpha_composite(shadow,(x+10,y+10))
    canv.alpha_composite(panel.convert("RGBA"),(x,y))
    canv.save(path,optimize=True)

def render_worker():
    try:
        STATUS.update(state="working",progress=2,message="Preparing native Chapter 1-5 panels")
        needed={ch:set() for ch in range(1,6)}
        for ch,p,f in SHOTS:
            if isinstance(p,tuple): needed[ch].update(p)
            else: needed[ch].add(p)
        panel_cache={}
        for ch in range(1,6):
            pdf=os.path.join(BASE,f"ch{ch}.pdf")
            STATUS.update(progress=3+ch*4,message=f"Downloading Chapter {ch}")
            dl(URLS[ch],pdf)
            doc=fitz.open(pdf)
            for p in sorted(needed[ch]):
                panel_cache[(ch,p)]=extract_page_image(doc,p)
            doc.close()
            os.remove(pdf)

        STATUS.update(progress=26,message="Building clean static panels")
        fgdir=os.path.join(BASE,"fg"); os.makedirs(fgdir,exist_ok=True)
        for idx,(ch,p,focus) in enumerate(SHOTS,1):
            if isinstance(p,tuple):
                a=panel_cache[(ch,p[0])]; b=panel_cache[(ch,p[1])]
                if ch==1 and p==(3,4):
                    ca=a.crop((0,int(a.height*.68),a.width,a.height)); cb=b.crop((0,0,b.width,int(b.height*.32)))
                elif ch==1 and p==(13,14):
                    ca=a.crop((0,int(a.height*.62),a.width,a.height)); cb=b.crop((0,0,b.width,int(b.height*.36)))
                else:
                    ca=a.crop((0,int(a.height*.66),a.width,a.height)); cb=b.crop((0,0,b.width,int(b.height*.38)))
                W=max(ca.width,cb.width)
                comb=Image.new("RGB",(W,ca.height+cb.height),"white")
                comb.paste(ca,((W-ca.width)//2,0)); comb.paste(cb,((W-cb.width)//2,ca.height))
                panel=crop_window(comb,.5,.72)
            else:
                panel=crop_window(panel_cache[(ch,p)],focus,.72)
            panel_to_canvas(panel,os.path.join(fgdir,f"{idx:03d}.png"))
            if idx%10==0: STATUS["progress"]=26+int(idx/99*34)

        concat=os.path.join(BASE,"panels.txt")
        with open(concat,"w") as f:
            for i in range(99):
                dur=max(.12,TIMES[i+1]-TIMES[i])
                f.write(f"file '{fgdir}/{i+1:03d}.png'\n")
                f.write(f"duration {dur:.6f}\n")
            f.write(f"file '{fgdir}/099.png'\n")

        import imageio_ffmpeg
        ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
        STATUS.update(progress=62,message="Downloading permanent galaxy background and narration")
        gal=os.path.join(BASE,"galaxy.mp4"); aud=os.path.join(BASE,"narration.wav")
        dl(URLS["galaxy"],gal); dl(URLS["audio"],aud)

        STATUS.update(progress=70,message="Rendering 1080p video")
        cmd=[ffmpeg,"-y","-stream_loop","-1","-i",gal,"-f","concat","-safe","0","-i",concat,"-i",aud,
             "-filter_complex","[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=2:1,eq=brightness=-0.20:saturation=0.82[bg];[1:v]format=rgba[fg];[bg][fg]overlay=0:0:format=auto[v]",
             "-map","[v]","-map","2:a:0","-t","690.275","-r","24","-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",OUT]
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        for line in p.stdout:
            if "time=" in line: STATUS["progress"]=min(98,STATUS["progress"]+1)
        rc=p.wait()
        if rc!=0 or not os.path.exists(OUT): raise RuntimeError("FFmpeg render failed")
        STATUS.update(state="done",progress=100,message="Chapter 1-5 1080p recap ready")
    except Exception as e:
        STATUS.update(state="error",message=str(e),trace=traceback.format_exc()[-4000:])

app=Flask(__name__)
@app.get("/")
def home():
    return jsonify({"project":"Aevrilo Chapter 1-5","status":STATUS,"download":"/download" if STATUS.get("state")=="done" else None})
@app.get("/status")
def status(): return jsonify(STATUS)
@app.get("/download")
def download():
    if STATUS.get("state")!="done": return jsonify(STATUS),409
    return send_file(OUT,as_attachment=True,download_name="Aevrilo_Civil_Servant_Ch1-5_1080p.mp4",mimetype="video/mp4")

def monitor_status():
    while True:
        print("AEVRILO_STATUS", STATUS, flush=True)
        time.sleep(10)

threading.Thread(target=monitor_status,daemon=True).start()
threading.Thread(target=render_worker,daemon=True).start()
app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
