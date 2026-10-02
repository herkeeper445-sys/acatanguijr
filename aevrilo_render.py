import os, threading, time, io, requests, fitz, subprocess, traceback, multiprocessing
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
(5,4,.5),(5,8,.5),(5,9,.5),(5,10,.5),(5,12,.5),(5,14,.5),(5,15,.5),(5,16,.5),(5,17,.5),(5,19,.5),(5,21,.5),(5,24,.5),(5,28,.5),(5,28,.62),(5,30,.5),(5,33,.5),(5,37,.5),(5,41,.5),(5,41,.72),(5,42,.5),(5,44,.5),(5,45,.5),(5,46,.5),(5,47,.5),(5,48,.5)
]

# Hard narration-to-visual sync points from the user's actual 690.275s narrator track.
# Each key is the shot that MUST begin when that named character/event is spoken.
SEMANTIC_CUES={
    1:(0.00,"betrayal / poisoning opening"),
    5:(9.76,"Alex Morgan, Suzuki Endo, Isabella and Hex Hood"),
    9:(24.12,"Suzuki poison affecting Suho"),
    10:(29.34,"Isabella the healer"),
    13:(61.10,"Suho attacks"),
    16:(88.28,"Intangible Sword"),
    19:(115.66,"player Suho rebooting"),
    23:(140.82,"Sindorim dungeon break"),
    24:(153.96,"returned to the past"),
    31:(206.14,"awakening conditions fulfilled"),
    34:(231.12,"chooses Healer"),
    37:(271.08,"Healing Light"),
    41:(300.40,"Beginner Sword"),
    43:(315.70,"abnormal gate"),
    46:(321.58,"Green Red Gate"),
    49:(340.78,"Hobgoblins"),
    54:(407.58,"Dodge / Parry / sword techniques"),
    62:(433.84,"Magic Stones"),
    66:(459.46,"Hobgoblin horde"),
    74:(493.46,"Chief Hobgoblin"),
    76:(512.02,"Fear"),
    81:(541.60,"Pain"),
    85:(576.36,"Healing Light during boss fight"),
    92:(609.52,"Diagonal Slash"),
    93:(611.60,"Horizontal Slash"),
    94:(613.70,"Stab"),
    95:(614.96,"Basic Swordsmanship"),
    97:(641.92,"Intimidation"),
    98:(647.18,"final attack on Chief Hobgoblin"),
    99:(655.20,"gate conquered"),
    100:(690.275,"narration end"),
}
anchors={k:v[0] for k,v in SEMANTIC_CUES.items()}

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

def process_chapter_worker(ch, pdf, fgdir):
    # Run in a fresh process so PyMuPDF/Pillow allocations are returned to the OS
    # after every chapter. This keeps the 512 MB Render free instance below its RAM limit.
    import gc
    doc=fitz.open(pdf)
    chapter_shots=[(idx,p,focus) for idx,(c,p,focus) in enumerate(SHOTS,1) if c==ch]
    for idx,p,focus in chapter_shots:
        if isinstance(p,tuple):
            a=extract_page_image(doc,p[0])
            b=extract_page_image(doc,p[1])
            if ch==1 and p==(3,4):
                ca=a.crop((0,int(a.height*.68),a.width,a.height))
                cb=b.crop((0,0,b.width,int(b.height*.32)))
            elif ch==1 and p==(13,14):
                ca=a.crop((0,int(a.height*.62),a.width,a.height))
                cb=b.crop((0,0,b.width,int(b.height*.36)))
            else:
                ca=a.crop((0,int(a.height*.66),a.width,a.height))
                cb=b.crop((0,0,b.width,int(b.height*.38)))
            W=max(ca.width,cb.width)
            comb=Image.new("RGB",(W,ca.height+cb.height),"white")
            comb.paste(ca,((W-ca.width)//2,0))
            comb.paste(cb,((W-cb.width)//2,ca.height))
            panel=crop_window(comb,.5,.72)
            del a,b,ca,cb,comb
        else:
            src=extract_page_image(doc,p)
            panel=crop_window(src,focus,.72)
            del src

        panel=panel.convert("RGB")
        # Keep the manga crisp without unnecessary upscaling.
        maxw,maxh=1120,900
        scale=min(maxw/panel.width,maxh/panel.height,1.25)
        nw=max(2,int(panel.width*scale)); nh=max(2,int(panel.height*scale))
        panel=panel.resize((nw,nh),Image.Resampling.LANCZOS)
        panel=ImageEnhance.Sharpness(panel).enhance(1.06)

        # Smaller transparent foreground; centered by FFmpeg over the permanent galaxy BG.
        canv=Image.new("RGBA",(1200,960),(0,0,0,0))
        x=(1200-nw)//2; y=(960-nh)//2
        sh=Image.new("RGBA",(nw,nh),(0,0,0,145))
        canv.alpha_composite(sh,(x+8,y+8))
        canv.alpha_composite(panel.convert("RGBA"),(x,y))
        canv.save(os.path.join(fgdir,f"{idx:03d}.png"),compress_level=5)
        del panel,canv,sh
        gc.collect()
    doc.close()
    gc.collect()

def render_worker():
    try:
        import gc, imageio_ffmpeg
        STATUS.update(state="working",progress=2,message="Preparing Chapter 1-5 source panels")
        fgdir=os.path.join(BASE,"fg")
        os.makedirs(fgdir,exist_ok=True)

        # Process each chapter in a fresh child process to prevent native-memory buildup.
        for ch in range(1,6):
            pdf=os.path.join(BASE,f"ch{ch}.pdf")
            STATUS.update(progress=3+ch*5,message=f"Downloading Chapter {ch}")
            dl(URLS[ch],pdf)

            STATUS.update(progress=5+ch*5,message=f"Extracting Chapter {ch} native panels")
            proc=subprocess.run([os.sys.executable,"aevrilo_chapter.py",str(ch),pdf,fgdir],
                                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if proc.returncode!=0:
                raise RuntimeError(f"Chapter {ch} panel extraction failed: {proc.stdout[-2500:]}")
            os.remove(pdf)
            gc.collect()
            STATUS["progress"]=20+ch*8

        # Verify all 99 expected static frames exist before encoding.
        missing=[i for i in range(1,100) if not os.path.exists(os.path.join(fgdir,f"{i:03d}.png"))]
        if missing:
            raise RuntimeError(f"Missing prepared panels: {missing[:12]}")

        concat=os.path.join(BASE,"panels.txt")
        with open(concat,"w") as ftxt:
            for i in range(99):
                dur=max(.12,TIMES[i+1]-TIMES[i])
                ftxt.write(f"file '{fgdir}/{i+1:03d}.png'\n")
                ftxt.write(f"duration {dur:.6f}\n")
            ftxt.write(f"file '{fgdir}/099.png'\n")

        ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()

        # Download the user's exact background and narration with Python first.
        # The bundled ffmpeg build is more reliable with local media than redirected HTTPS URLs.
        STATUS.update(progress=61,message="Downloading permanent galaxy background")
        gal=os.path.join(BASE,"galaxy.mp4")
        dl(URLS["galaxy"],gal)
        STATUS.update(progress=63,message="Downloading original narration")
        aud=os.path.join(BASE,"narration.wav")
        dl(URLS["audio"],aud)

        # Pre-normalize the long 4K/60fps galaxy source once. Rendering every chunk
        # directly from the original background was the remaining memory spike on Render Free.
        # This keeps the final composition 1920x1080 while greatly reducing per-chunk RAM.
        STATUS.update(progress=64,message="Preparing low-memory 1080p galaxy master")
        gal1080=os.path.join(BASE,"galaxy_1080p.mp4")
        bg_cmd=[
            ffmpeg,"-y","-nostats","-loglevel","error",
            "-i",gal,
            "-t","30",
            "-vf","scale=1920:1080:force_original_aspect_ratio=increase:flags=fast_bilinear,"
                  "crop=1920:1080,fps=24,eq=brightness=-0.18:saturation=0.86,format=yuv420p",
            "-an","-threads","1","-c:v","libx264","-preset","ultrafast","-crf","24",
            "-bf","0","-refs","1","-g","48",
            "-x264-params","threads=1:lookahead_threads=1:rc-lookahead=0:sync-lookahead=0:sliced-threads=1",
            "-movflags","+faststart",gal1080
        ]
        proc=subprocess.run(bg_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if proc.returncode!=0 or not os.path.exists(gal1080):
            raise RuntimeError("Galaxy 1080p preparation failed: "+proc.stdout[-2500:])

        STATUS.update(progress=65,message="Rendering narration-synced 1080p chunks with permanent galaxy background")
        chunk_dir=os.path.join(BASE,"chunks")
        os.makedirs(chunk_dir,exist_ok=True)
        chunk_paths=[]
        # Smaller chunks reduce native FFmpeg allocations and make the 512 MB service safer.
        chunk_size=3

        # Render only a few shots per FFmpeg process. Each process exits before the
        # next one starts, returning scaler/overlay/x264 native allocations to the OS.
        # This preserves true 1920x1080 composition while staying below Render Free RAM.
        for chunk_no,start in enumerate(range(0,99,chunk_size),1):
            end=min(99,start+chunk_size)
            cconcat=os.path.join(BASE,f"chunk_{chunk_no:02d}.txt")
            with open(cconcat,"w") as cf:
                for i in range(start,end):
                    dur=max(.12,TIMES[i+1]-TIMES[i])
                    cf.write(f"file '{fgdir}/{i+1:03d}.png'\n")
                    cf.write(f"duration {dur:.6f}\n")
                cf.write(f"file '{fgdir}/{end:03d}.png'\n")

            cpath=os.path.join(chunk_dir,f"chunk_{chunk_no:02d}.mp4")
            cdur=max(.12,TIMES[end]-TIMES[start])
            cmd=[
                ffmpeg,"-y","-nostats","-loglevel","error",
                "-stream_loop","-1","-i",gal1080,
                "-f","concat","-safe","0","-i",cconcat,
                "-filter_complex",
                "[0:v]format=yuv420p[bg];"
                "[1:v]format=yuva420p[fg];"
                "[bg][fg]overlay=(W-w)/2:(H-h)/2:format=yuv420,format=yuv420p[v]",
                "-map","[v]","-an",
                "-t",f"{cdur:.6f}","-r","24",
                "-filter_complex_threads","1","-threads","1",
                "-c:v","libx264","-preset","ultrafast","-tune","zerolatency",
                "-crf","16","-pix_fmt","yuv420p",
                "-bf","0","-refs","1","-g","48",
                "-x264-params","threads=1:lookahead_threads=1:rc-lookahead=0:sync-lookahead=0:sliced-threads=1",
                "-movflags","+faststart",cpath
            ]
            proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if proc.returncode!=0 or not os.path.exists(cpath):
                raise RuntimeError(f"1080p chunk {chunk_no} failed: {proc.stdout[-2500:]}")
            chunk_paths.append(cpath)
            STATUS["progress"]=65+int((chunk_no/((99+chunk_size-1)//chunk_size))*28)
            STATUS["message"]=f"Rendered 1080p chunk {chunk_no}/{(99+chunk_size-1)//chunk_size}"
            gc.collect()

        STATUS.update(progress=94,message="Joining 1080p chunks without re-encoding")
        chunk_list=os.path.join(BASE,"chunks.txt")
        with open(chunk_list,"w") as lf:
            for cp in chunk_paths:
                lf.write(f"file '{cp}'\n")
        video_only=os.path.join(BASE,"video_1080p.mp4")
        join_cmd=[ffmpeg,"-y","-f","concat","-safe","0","-i",chunk_list,
                  "-c","copy","-movflags","+faststart",video_only]
        proc=subprocess.run(join_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if proc.returncode!=0 or not os.path.exists(video_only):
            raise RuntimeError("Chunk join failed: "+proc.stdout[-2500:])

        STATUS.update(progress=97,message="Adding original narration to finished 1080p video")
        mux_cmd=[ffmpeg,"-y","-i",video_only,"-i",aud,
                 "-map","0:v:0","-map","1:a:0","-c:v","copy",
                 "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",OUT]
        proc=subprocess.run(mux_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if proc.returncode!=0 or not os.path.exists(OUT):
            raise RuntimeError("Final narration mux failed: "+proc.stdout[-2500:])

        STATUS.update(state="done",progress=100,message="Chapter 1-5 1080p recap ready")
    except Exception as e:
        STATUS.update(state="error",progress=0,message=str(e),trace=traceback.format_exc()[-4000:])

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

def keep_alive():
    # Render Free web services can spin down after inactivity even while a background
    # render thread is busy. Periodically hit the public status endpoint so this
    # long FFmpeg job can finish in one run.
    url=os.environ.get("RENDER_EXTERNAL_URL","").rstrip("/")
    if not url:
        url="https://aevrilo-ch1-5-render.onrender.com"
    time.sleep(120)
    while STATUS.get("state") in ("starting","working"):
        try:
            requests.get(url+"/status",timeout=20)
        except Exception:
            pass
        time.sleep(240)

threading.Thread(target=monitor_status,daemon=True).start()
threading.Thread(target=keep_alive,daemon=True).start()
threading.Thread(target=render_worker,daemon=True).start()
app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
