# Oliver 全身版（Q 版）向量零件。座標系 viewBox 0 0 640 760；頭中心 (320,300) r175。
HEAD='''<g class="head"><circle cx="320" cy="300" r="178" fill="#FFFFFF" stroke="#D5DED9" stroke-width="5"/><ellipse cx="320" cy="440" rx="86" ry="22" fill="#EEF3F0" opacity=".9"/><path d="M320 126 Q 316 108 328 96" fill="none" stroke="#7BB661" stroke-width="10" stroke-linecap="round"/><path d="M326 112 C 334 72, 368 50, 412 48 C 408 92, 374 114, 326 112 Z" fill="#7BB661"/><path d="M332 108 C 350 84, 376 70, 404 56" fill="none" stroke="#5E9B49" stroke-width="4" stroke-linecap="round"/><g class="eyes"><ellipse cx="258" cy="282" rx="24" ry="32" fill="#17332B"/><ellipse cx="382" cy="282" rx="24" ry="32" fill="#17332B"/><circle cx="250" cy="270" r="9" fill="#fff"/><circle cx="374" cy="270" r="9" fill="#fff"/><circle cx="266" cy="296" r="4" fill="#fff" opacity=".8"/><circle cx="390" cy="296" r="4" fill="#fff" opacity=".8"/></g><circle class="mono" cx="382" cy="282" r="48" fill="none" stroke="#F2A541" stroke-width="9"/><path d="M424 304 Q 450 360 432 420" fill="none" stroke="#F2A541" stroke-width="4" stroke-linecap="round"/><ellipse cx="208" cy="338" rx="28" ry="16" fill="#F7B3A3" opacity="0.7"/><ellipse cx="432" cy="338" rx="28" ry="16" fill="#F7B3A3" opacity="0.7"/><g class="stache"><path d="M320 350 C 306 332, 278 330, 266 348 C 276 342, 290 348, 296 356 C 304 362, 316 358, 320 352 Z" fill="#17332B"/><path d="M320 350 C 334 332, 362 330, 374 348 C 364 342, 350 348, 344 356 C 336 362, 324 358, 320 352 Z" fill="#17332B"/></g><path d="M304 372 Q 320 384 336 372" fill="none" stroke="#17332B" stroke-width="5" stroke-linecap="round"/></g>'''
SHOES='''<g class="shoes"><ellipse cx="320" cy="700" rx="150" ry="16" fill="#17332B" opacity=".10"/><ellipse cx="278" cy="684" rx="46" ry="24" fill="#0E201B"/><ellipse cx="362" cy="684" rx="46" ry="24" fill="#0E201B"/><ellipse cx="266" cy="678" rx="14" ry="6" fill="#fff" opacity=".35"/><ellipse cx="350" cy="678" rx="14" ry="6" fill="#fff" opacity=".35"/></g>'''
BODY='''<g class="body"><ellipse cx="320" cy="572" rx="140" ry="108" fill="#17332B"/><ellipse cx="250" cy="540" rx="40" ry="60" fill="#fff" opacity=".06"/><ellipse cx="320" cy="570" rx="62" ry="80" fill="#FFFFFF"/><circle cx="320" cy="576" r="6" fill="#17332B"/><circle cx="320" cy="608" r="6" fill="#17332B"/><path d="M320 500 L 276 480 L 276 520 Z" fill="#17332B"/><path d="M320 500 L 364 480 L 364 520 Z" fill="#17332B"/><rect x="308" y="488" width="24" height="24" rx="7" fill="#17332B"/></g>'''
def ARM(x,y,rot,cls="",extra=""):
    return f'<g class="arm {cls}" style="transform-origin:{x}px {y}px;transform:rotate({rot}deg)"><rect x="{x-20}" y="{y}" width="40" height="50" rx="20" fill="#17332B"/><circle cx="{x}" cy="{y+54}" r="27" fill="#FFFFFF" stroke="#D5DED9" stroke-width="4"/>{extra}</g>'
TABLET='''<g class="tablet"><g transform="rotate(-5 320 600)"><rect x="240" y="560" width="160" height="112" rx="14" fill="#17332B"/><rect x="251" y="571" width="138" height="90" rx="8" fill="#FFFFFF"/>__CELLS__</g><circle cx="248" cy="640" r="28" fill="#fff" stroke="#D5DED9" stroke-width="4"/><circle cx="392" cy="640" r="28" fill="#fff" stroke="#D5DED9" stroke-width="4"/></g>'''
_cells="".join(f'<rect x="{262+j*40}" y="{582+i*24}" width="34" height="14" rx="4" fill="{c}"/>' for i,r in enumerate([["#2E7D5B","#F2A541","#8FC4B5"],["#8FC4B5","#2E7D5B","#E6EEE9"],["#F2A541","#E6EEE9","#2E7D5B"]]) for j,c in enumerate(r))
TABLET=TABLET.replace("__CELLS__",_cells)
THUMB='<rect x="441" y="560" width="20" height="32" rx="9" fill="#fff" stroke="#D5DED9" stroke-width="4"/>'

POSES={
 "wave":  lambda: SHOES+BODY+ARM(200,550,30,"l")+ARM(446,530,-150,"r")+HEAD,
 "tablet":lambda: SHOES+BODY+'<rect x="186" y="556" width="40" height="50" rx="20" fill="#17332B" transform="rotate(-40 206 556)"/><rect x="414" y="556" width="40" height="50" rx="20" fill="#17332B" transform="rotate(40 434 556)"/>'+TABLET+HEAD,
 "thumb": lambda: SHOES+BODY+ARM(200,550,20,"l")+ARM(446,530,-200,"r",THUMB)+HEAD+'<circle cx="516" cy="520" r="8" fill="#F2A541"/><circle cx="542" cy="490" r="6" fill="#F2A541"/><circle cx="524" cy="464" r="5" fill="#F2A541"/>',
 "stand": lambda: SHOES+BODY+ARM(200,550,20,"l")+ARM(440,550,-20,"r")+HEAD,
 "point": lambda: SHOES+BODY+ARM(200,550,20,"l")+ARM(446,530,-110,"r")+HEAD,
}
def svg(pose="stand",w=640,cls=""):
    return f'<svg class="oliver {cls}" viewBox="100 40 440 680" width="{w}" height="{int(w*680/440)}" role="img" aria-label="Oliver">{POSES[pose]()}</svg>'
if __name__=="__main__":
    import os
    os.makedirs("img/oliver",exist_ok=True)
    for k in POSES: open(f"img/oliver/oliver-{k}.svg","w").write('<?xml version="1.0" encoding="UTF-8"?>'+svg(k))
    print("ok",list(POSES))
