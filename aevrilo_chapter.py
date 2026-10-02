import os, sys, io, gc, fitz
from PIL import Image, ImageOps, ImageEnhance

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

def extract_page_image(doc,pageno):
    page=doc[pageno-1]
    best=None
    for im in page.get_images(full=True):
        try:
            info=doc.extract_image(im[0])
            pic=Image.open(io.BytesIO(info["image"])).convert("RGB")
            area=pic.width*pic.height
            if best is None or area>best[0]:
                best=(area,pic.copy())
            pic.close()
        except Exception:
            pass
    if best:
        return best[1]
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

def save_panel(panel,path):
    panel=panel.convert("RGB")
    maxw,maxh=1120,900
    scale=min(maxw/panel.width,maxh/panel.height,1.25)
    nw=max(2,int(panel.width*scale)); nh=max(2,int(panel.height*scale))
    panel=panel.resize((nw,nh),Image.Resampling.LANCZOS)
    panel=ImageEnhance.Sharpness(panel).enhance(1.06)
    canv=Image.new("RGBA",(1200,960),(0,0,0,0))
    x=(1200-nw)//2; y=(960-nh)//2
    sh=Image.new("RGBA",(nw,nh),(0,0,0,145))
    canv.alpha_composite(sh,(x+8,y+8))
    canv.alpha_composite(panel.convert("RGBA"),(x,y))
    canv.save(path,compress_level=5)
    panel.close(); canv.close(); sh.close()

def main():
    ch=int(sys.argv[1]); pdf=sys.argv[2]; fgdir=sys.argv[3]
    doc=fitz.open(pdf)
    chapter_shots=[(idx,p,focus) for idx,(c,p,focus) in enumerate(SHOTS,1) if c==ch]
    for idx,p,focus in chapter_shots:
        if isinstance(p,tuple):
            a=extract_page_image(doc,p[0]); b=extract_page_image(doc,p[1])
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
            for x in (a,b,ca,cb,comb): x.close()
        else:
            src=extract_page_image(doc,p)
            panel=crop_window(src,focus,.72)
            src.close()
        save_panel(panel,os.path.join(fgdir,f"{idx:03d}.png"))
        panel.close()
        gc.collect()
    doc.close()
    print(f"chapter {ch} complete", flush=True)

if __name__=="__main__":
    main()
