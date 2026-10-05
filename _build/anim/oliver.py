# Oliver 全身版（Q 版）向量零件。座標系 viewBox 0 0 640 760；頭中心 (320,300) r175。
HEAD='''<g class="head"><circle cx="320" cy="300" r="175" fill="#FFFFFF" stroke="#D5DED9" stroke-width="5"/><path d="M320 133 Q 317 115 327 103" fill="none" stroke="#7BB661" stroke-width="9" stroke-linecap="round"/><path d="M324 119 C 330 83, 360 61, 400 59 C 396 97, 366 119, 324 119 Z" fill="#7BB661"/><g class="eyes"><ellipse cx="262" cy="276" rx="17" ry="22" fill="#17332B"/><ellipse cx="378" cy="276" rx="17" ry="22" fill="#17332B"/></g><circle class="mono" cx="378" cy="276" r="42" fill="none" stroke="#F2A541" stroke-width="10"/><path d="M418 292 Q 446 360 426 430" fill="none" stroke="#F2A541" stroke-width="4"/><ellipse cx="220" cy="328" rx="22" ry="13" fill="#F2A541" opacity="0.6"/><ellipse cx="420" cy="328" rx="22" ry="13" fill="#F2A541" opacity="0.6"/><g class="stache"><path d="M320 336 C 300 312, 262 312, 246 338 C 262 330, 278 338, 284 348 C 296 356, 314 350, 320 340 Z" fill="#17332B"/><path d="M320 336 C 340 312, 378 312, 394 338 C 378 330, 362 338, 356 348 C 344 356, 326 350, 320 340 Z" fill="#17332B"/></g></g>'''
SHOES='''<g class="shoes"><ellipse cx="276" cy="688" rx="48" ry="22" fill="#0E201B"/><ellipse cx="364" cy="688" rx="48" ry="22" fill="#0E201B"/><ellipse cx="262" cy="684" rx="14" ry="6" fill="#fff" opacity=".35"/><ellipse cx="350" cy="684" rx="14" ry="6" fill="#fff" opacity=".35"/></g>'''
BODY='''<g class="body"><ellipse cx="320" cy="560" rx="150" ry="118" fill="#17332B"/><ellipse cx="320" cy="556" rx="68" ry="88" fill="#FFFFFF"/><circle cx="320" cy="560" r="6" fill="#17332B"/><circle cx="320" cy="596" r="6" fill="#17332B"/><path d="M320 494 L 270 470 L 270 518 Z" fill="#17332B"/><path d="M320 494 L 370 470 L 370 518 Z" fill="#17332B"/><rect x="306" y="480" width="28" height="28" rx="8" fill="#17332B"/></g>'''
def ARM(x,y,rot,cls="",extra=""):
    return f'<g class="arm {cls}" style="transform-origin:{x}px {y}px;transform:rotate({rot}deg)"><rect x="{x-22}" y="{y}" width="44" height="62" rx="22" fill="#17332B"/><circle cx="{x}" cy="{y+66}" r="30" fill="#FFFFFF" stroke="#D5DED9" stroke-width="4"/>{extra}</g>'
TABLET='''<g class="tablet"><g transform="rotate(-5 320 600)"><rect x="240" y="560" width="160" height="112" rx="14" fill="#17332B"/><rect x="251" y="571" width="138" height="90" rx="8" fill="#FFFFFF"/>__CELLS__</g><circle cx="248" cy="640" r="28" fill="#fff" stroke="#D5DED9" stroke-width="4"/><circle cx="392" cy="640" r="28" fill="#fff" stroke="#D5DED9" stroke-width="4"/></g>'''
_cells="".join(f'<rect x="{262+j*40}" y="{582+i*24}" width="34" height="14" rx="4" fill="{c}"/>' for i,r in enumerate([["#2E7D5B","#F2A541","#8FC4B5"],["#8FC4B5","#2E7D5B","#E6EEE9"],["#F2A541","#E6EEE9","#2E7D5B"]]) for j,c in enumerate(r))
TABLET=TABLET.replace("__CELLS__",_cells)
THUMB='<rect x="441" y="568" width="22" height="36" rx="10" fill="#fff" stroke="#D5DED9" stroke-width="4"/>'

POSES={
 "wave":  lambda: SHOES+BODY+ARM(190,540,30,"l")+ARM(452,520,-150,"r")+HEAD,
 "tablet":lambda: SHOES+BODY+'<rect x="178" y="548" width="44" height="62" rx="22" fill="#17332B" transform="rotate(-40 200 548)"/><rect x="418" y="548" width="44" height="62" rx="22" fill="#17332B" transform="rotate(40 440 548)"/>'+TABLET+HEAD,
 "thumb": lambda: SHOES+BODY+ARM(190,540,20,"l")+ARM(452,520,-200,"r",THUMB)+HEAD+'<circle cx="520" cy="520" r="8" fill="#F2A541"/><circle cx="548" cy="488" r="6" fill="#F2A541"/><circle cx="530" cy="462" r="5" fill="#F2A541"/>',
 "stand": lambda: SHOES+BODY+ARM(190,540,20,"l")+ARM(450,540,-20,"r")+HEAD,
 "point": lambda: SHOES+BODY+ARM(190,540,20,"l")+ARM(452,520,-110,"r")+HEAD,
}
def svg(pose="stand",w=640,cls=""):
    return f'<svg class="oliver {cls}" viewBox="100 40 440 680" width="{w}" height="{int(w*680/440)}" role="img" aria-label="Oliver">{POSES[pose]()}</svg>'
if __name__=="__main__":
    import os
    os.makedirs("img/oliver",exist_ok=True)
    for k in POSES: open(f"img/oliver/oliver-{k}.svg","w").write('<?xml version="1.0" encoding="UTF-8"?>'+svg(k))
    print("ok",list(POSES))
