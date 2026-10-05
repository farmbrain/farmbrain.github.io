#!/usr/bin/env python3
"""Generate the inline SVG diagrams in _includes/diagrams/.

Edit this script (not the .svg files), then run:  python3 scripts/gen_diagrams.py
Colors and font sizes come from the .dg* rules in assets/css/main.css, so the
diagrams follow the site theme, including dark mode.
"""
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_includes", "diagrams")

def marker(id_, cls, ref=8, size=6):
    return f'<marker id="{id_}" viewBox="0 0 10 10" refX="{ref}" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="{cls}"/></marker>'

def loop(cx, cy, r, cls, mk):
    return f'<path class="{cls}" d="M{cx+r},{cy} A{r},{r} 0 1 1 {cx},{cy-r}" marker-end="url(#{mk})"/>'

def tower(cx, top, h, s=1.0):
    b = top + h; w = 26*s; t0 = top + 6*s
    o = f'<g>\n    <line class="ic-line" x1="{cx}" y1="{t0}" x2="{cx-w}" y2="{b}"/>\n    <line class="ic-line" x1="{cx}" y1="{t0}" x2="{cx+w}" y2="{b}"/>'
    pts = []
    for f in (0.35, 0.62, 0.86):
        y = t0 + (h-6*s)*f; dx = w*f
        o += f'\n    <line class="ic-thin" x1="{cx-dx:.1f}" y1="{y:.1f}" x2="{cx+dx:.1f}" y2="{y:.1f}"/>'
        pts.append((y, dx))
    (y1,d1),(y2,d2),(y3,d3) = pts
    o += f'''
    <polyline class="ic-thin" points="{cx-d1:.1f},{y1:.1f} {cx+d2:.1f},{y2:.1f} {cx-d3:.1f},{y3:.1f}"/>
    <circle class="ic" cx="{cx}" cy="{top}" r="{5*s}"/>
    <path class="wave" d="M{cx-12*s},{top-9*s} a{13*s},{13*s} 0 0 0 0,{18*s}"/>
    <path class="wave" d="M{cx+12*s},{top-9*s} a{13*s},{13*s} 0 0 1 0,{18*s}"/>
    <path class="wave" d="M{cx-21*s},{top-16*s} a{22*s},{22*s} 0 0 0 0,{32*s}"/>
    <path class="wave" d="M{cx+21*s},{top-16*s} a{22*s},{22*s} 0 0 1 0,{32*s}"/>
  </g>'''
    return o

def rack(x, y, w=120, u=22, n=3):
    o = "<g>"
    for i in range(n):
        yy = y + i*(u+4)
        o += f'''
    <rect class="ic" x="{x}" y="{yy}" width="{w}" height="{u}" rx="4"/>
    <rect class="ic-hole" x="{x+10}" y="{yy+u/2-2}" width="{w*0.45:.0f}" height="4" rx="2"/>
    <circle class="t1-fill" cx="{x+w-14}" cy="{yy+u/2}" r="3"/><circle class="t2-fill" cx="{x+w-26}" cy="{yy+u/2}" r="3"/>'''
    return o + "\n  </g>"

def sprout(x, y):
    return (f'<path class="stem" d="M{x},{y} v-9"/>'
            f'<ellipse class="leaf" cx="{x-4}" cy="{y-9}" rx="4" ry="2.2" transform="rotate(-30 {x-4} {y-9})"/>'
            f'<ellipse class="leaf" cx="{x+4}" cy="{y-10}" rx="4" ry="2.2" transform="rotate(30 {x+4} {y-10})"/>')

def wheels(cx, g, dx=20, r=8):
    return "".join(f'<circle class="ic" cx="{cx+d}" cy="{g-5}" r="{r}"/><circle class="ic-hole" cx="{cx+d}" cy="{g-5}" r="3"/>' for d in (-dx, dx))

def picker(cx, g):
    return f'''<g>
    <rect class="ic" x="{cx-32}" y="{g-30}" width="64" height="22" rx="5"/>{wheels(cx, g)}
    <polyline class="ic-line" points="{cx+18},{g-30} {cx+30},{g-56} {cx+52},{g-48}" style="stroke-width:4"/>
    <circle class="ic" cx="{cx+30}" cy="{g-56}" r="4"/>
    <path class="ic-line" d="M{cx+52},{g-48} l6,-6 M{cx+52},{g-48} l7,3" style="stroke-width:2.5"/>
    <path class="berry" d="M{cx+62},{g-52} c6,0 8,5 5,10 c-2,4 -5,6 -6,6 c-1,0 -4,-2 -6,-6 c-3,-5 0,-10 7,-10 z"/>
    <path class="leaf" d="M{cx+56},{g-53} l5,-4 l3,4 l3,-4 l4,4 z"/>
  </g>'''

def rover(cx, g):
    return f'''<g>
    <rect class="ic" x="{cx-32}" y="{g-30}" width="64" height="22" rx="5"/>{wheels(cx, g)}
    <line class="ic-line" x1="{cx+14}" y1="{g-30}" x2="{cx+14}" y2="{g-52}"/>
    <rect class="ic" x="{cx+4}" y="{g-64}" width="22" height="13" rx="3"/>
    <circle class="ic-hole" cx="{cx+19}" cy="{g-57.5}" r="3.5"/>
  </g>'''

def drone(cx, cy):
    return f'''<g>
    <line class="ic-line" x1="{cx-30}" y1="{cy-4}" x2="{cx+30}" y2="{cy-4}"/>
    <line class="ic-line" x1="{cx-30}" y1="{cy-4}" x2="{cx-30}" y2="{cy-10}"/><line class="ic-line" x1="{cx+30}" y1="{cy-4}" x2="{cx+30}" y2="{cy-10}"/>
    <ellipse class="ic" cx="{cx-30}" cy="{cy-12}" rx="15" ry="3"/><ellipse class="ic" cx="{cx+30}" cy="{cy-12}" rx="15" ry="3"/>
    <rect class="ic" x="{cx-14}" y="{cy-10}" width="28" height="16" rx="6"/>
    <circle class="ic-hole" cx="{cx}" cy="{cy-2}" r="3.5"/>
    <path class="ic-thin" d="M{cx-10},{cy+6} l-5,7 M{cx+10},{cy+6} l5,7"/>
  </g>'''

def farmer(cx, cy):
    return f'''<g>
    <circle class="t3-fill" cx="{cx}" cy="{cy}" r="10"/>
    <ellipse class="t3-fill" cx="{cx}" cy="{cy-8}" rx="17" ry="3.5"/>
    <rect class="t3-fill" x="{cx-9}" y="{cy-18}" width="18" height="10" rx="4"/>
    <path class="t3-fill" d="M{cx-19},{cy+36} a19,22 0 0 1 38,0 z"/>
  </g>'''

def icon_bg(x, y, n):
    return f'<rect class="t{n}-fill" x="{x-20}" y="{y-20}" width="40" height="40" rx="9"/>'
SOFT = lambda n, w: f'fill:none;stroke:var(--t{n}-soft);stroke-width:{w};stroke-linecap:round;stroke-linejoin:round'
def code_icon(x, y):
    return f'<g>{icon_bg(x,y,1)}<polyline points="{x-5},{y-8} {x-13},{y} {x-5},{y+8}" style="{SOFT(1,3)}"/><polyline points="{x+5},{y-8} {x+13},{y} {x+5},{y+8}" style="{SOFT(1,3)}"/></g>'
def gear_icon(x, y):
    return (f'<g>{icon_bg(x,y,2)}<circle cx="{x}" cy="{y}" r="10.5" style="fill:none;stroke:var(--t2-soft);stroke-width:5;stroke-dasharray:4.12 4.12"/>'
            f'<circle cx="{x}" cy="{y}" r="8" style="fill:var(--t2-soft)"/><circle class="t2-fill" cx="{x}" cy="{y}" r="3.2"/></g>')
def diag_icon(x, y):
    return (f'<g>{icon_bg(x,y,3)}<circle cx="{x-3}" cy="{y-3}" r="9" style="{SOFT(3,2.8)}"/>'
            f'<line x1="{x+4}" y1="{y+4}" x2="{x+11}" y2="{y+11}" style="{SOFT(3,3.2)}"/>'
            f'<polyline points="{x-10},{y-3} {x-6},{y-3} {x-4},{y-8} {x-1},{y+2} {x+1},{y-3} {x+4},{y-3}" style="{SOFT(3,1.8)}"/></g>')

BW = 220  # thrust box width
def tbox(x, y, n, title, sub, icon):
    return f'''
  <rect class="t{n}-box" x="{x}" y="{y}" width="{BW}" height="80" rx="12"/>
  {icon(x+34, y+40)}
  <text class="t-title" x="{x+64}" y="{y+38}">{title}</text>
  <text class="t-body" x="{x+64}" y="{y+58}">{sub}</text>
  <text class="t-small" x="{x+BW-12}" y="{y+18}" text-anchor="end" style="font-size:11px;font-weight:700;letter-spacing:0.04em;fill:var(--t{n})">THRUST {n}</text>'''

def label(x, y, text, n):
    return f'<text class="t-edge" x="{x}" y="{y}" style="fill:var(--t{n})">{text}</text>'

# ---------------------------------------------------------------- architecture
BW = 262
def tbox(x, y, n, title, sub, icon):
    return f'''
  <rect class="t{n}-box" x="{x}" y="{y}" width="{BW}" height="92" rx="12"/>
  {icon(x+36, y+50)}
  <text class="t-title" x="{x+68}" y="{y+50}">{title}</text>
  <text class="t-body" x="{x+68}" y="{y+72}">{sub}</text>
  <text class="t-small" x="{x+BW-12}" y="{y+20}" text-anchor="end" style="font-size:12.5px;font-weight:700;letter-spacing:0.05em;fill:var(--t{n})">THRUST {n}</text>'''

C = 490                     # center x of the physical system
W = 980
L, R = 12, W - 12 - BW
sprouts = "".join(sprout(x + C - 470, y) for x, y in
    [(300,382),(326,390),(352,394),(380,396),(410,394),(438,390),(500,394),(528,396),(556,394),(590,396),(620,390),(646,384)])
arch = f'''<svg class="dg dg-arch" viewBox="0 0 {W} 446" role="img" aria-labelledby="dg-arch-t">
  <title id="dg-arch-t">FarmBrain architecture. Thrust 1, FarmLang, is the programming model. Thrust 2, the compiler and runtime, deploys programs across an on-farm edge server and farm robots connected by a farm-wide private 5G network. Thrust 3, AI-assisted management, collects telemetry from all of them, diagnoses problems, and guides the farm operator.</title>
  <defs>{marker("dg-ar-a1","t1-fill")}{marker("dg-ar-a2","t2-fill")}{marker("dg-ar-a3","t3-fill")}</defs>

  <!-- Thrusts 1 and 2 -->{tbox(L, 40, 1, "FarmLang", "Programming model", code_icon)}
  <line class="t1-line" x1="{L+BW/2}" y1="134" x2="{L+BW/2}" y2="166" marker-end="url(#dg-ar-a1)"/>
  {tbox(L, 170, 2, "Compiler &amp; runtime", "Partition, schedule", gear_icon)}
  {label(L+BW+30, 232, "deploy", 2)}

  <!-- Physical system -->
  <text class="t-strong" x="{C}" y="30" text-anchor="middle">On-farm edge server</text>
  {rack(C-60, 44)}
  <line class="line" x1="{C}" y1="120" x2="{C}" y2="150" style="stroke-width:2.5"/>
  {tower(C, 160, 92)}
  <text class="t-strong" x="{C+44}" y="214">Farm-wide private</text>
  <text class="t-strong" x="{C+44}" y="235">5G network</text>
  <ellipse class="field" cx="{C}" cy="372" rx="206" ry="40"/>
  {sprouts}
  {picker(C-118, 368)}
  {drone(C, 300)}
  {rover(C+116, 368)}
  <text class="t-strong" x="{C}" y="436" text-anchor="middle">Farm robots</text>

  <!-- Thrust 3 -->
  <path class="t3-line dashed" d="M{C+64},84 C{C+120},84 {R-60},84 {R-6},84" marker-end="url(#dg-ar-a3)"/>
  <path class="t3-line dashed" d="M{C+42},168 C{C+120},168 {R-50},112 {R-6},112" marker-end="url(#dg-ar-a3)"/>
  <path class="t3-line dashed" d="M{C+166},336 C{C+230},300 {R+30},200 {R+50},138" marker-end="url(#dg-ar-a3)"/>
  {label(C+82, 68, "telemetry", 3)}
  {tbox(R, 40, 3, "Management", "Diagnose, recover", diag_icon)}
  <line class="t3-line" x1="{R+BW/2}" y1="134" x2="{R+BW/2}" y2="196" marker-end="url(#dg-ar-a3)"/>
  {label(R+BW/2+14, 174, "guidance", 3)}
  {farmer(R+BW/2, 224)}
  <text class="t-strong" x="{R+BW/2}" y="286" text-anchor="middle">Farm operator</text>

  <!-- deploy arrows drawn last so they sit above the scene -->
  <path class="t2-line" d="M{L+BW},204 C{L+BW+60},204 {C-120},92 {C-72},92" marker-end="url(#dg-ar-a2)"/>
  <path class="t2-line" d="M{L+BW-50},262 C{L+BW-50},346 {L+BW-30},352 {C-160},350" marker-end="url(#dg-ar-a2)"/>
</svg>
'''

# ---------------------------------------------------------------- split: today
today = f'''<svg class="dg" viewBox="0 0 440 300" role="img" aria-labelledby="dg-today-t">
  <title id="dg-today-t">Today: a robot carries a high-performance on-board computer that runs both the reactive and the deliberative control loop, making it heavy, expensive, and power-hungry.</title>
  <defs>{marker("dg-today-a2","t2-fill",6,5)}{marker("dg-today-a3","t3-fill",6,5)}</defs>
  <rect class="warn-box" x="40" y="14" width="360" height="184" rx="10"/>
  <text class="t-title" x="58" y="42">High-performance on-board computer</text>
  <text class="t-body" x="58" y="61">GPU-class · big battery · cooling</text>
  <rect class="t2-box" x="54" y="76" width="332" height="50" rx="25"/>
  {loop(84, 101, 11, "t2-line", "dg-today-a2")}
  <text class="t-strong" x="108" y="97">Reactive loop</text>
  <text class="t-small" x="108" y="115">100–1000 Hz · motion, safety</text>
  <rect class="t3-box" x="54" y="136" width="332" height="50" rx="25"/>
  {loop(84, 161, 11, "t3-line", "dg-today-a3")}
  <text class="t-strong" x="108" y="157">Deliberative loop</text>
  <text class="t-small" x="108" y="175">3D scene, VLMs, motion planning</text>
  <rect class="chassis" x="30" y="206" width="380" height="36" rx="8"/>
  <text class="t-on-chassis" x="220" y="229" text-anchor="middle">Strawberry-picking robot</text>
  {"".join(f'<circle class="wheel" cx="{x}" cy="250" r="13"/>' for x in (80,170,270,360))}
  <text class="t-warn" x="220" y="290" text-anchor="middle">Heavy · expensive · power-hungry</text>
</svg>
'''

# ---------------------------------------------------------------- split: FarmBrain
minis = ""
for x in (268, 322, 376):
    minis += (f'<line class="line dashed" x1="{x+22}" y1="198" x2="{x+22}" y2="214"/>'
              f'<rect class="chassis" x="{x}" y="214" width="44" height="14" rx="4"/>'
              f'<circle class="wheel" cx="{x+11}" cy="232" r="5"/><circle class="wheel" cx="{x+33}" cy="232" r="5"/>')
fb = f'''<svg class="dg" viewBox="0 0 440 300" role="img" aria-labelledby="dg-fb-t">
  <title id="dg-fb-t">FarmBrain: the robot keeps only the reactive loop on a low-power embedded processor; the deliberative loop runs on a 5G edge server shared by many robots. Plans flow down to the robot and sensor data flows up over a farm-wide private 5G network.</title>
  <defs>{marker("dg-fb-a2","t2-fill",6,5)}{marker("dg-fb-a3","t3-fill",6,5)}{marker("dg-fb-af","fg-fill")}</defs>
  <rect class="t1-box" x="10" y="100" width="170" height="98" rx="10"/>
  <text class="t-strong" x="24" y="126">Embedded processor</text>
  <rect class="t2-box" x="20" y="140" width="150" height="48" rx="24"/>
  {loop(46, 164, 10, "t2-line", "dg-fb-a2")}
  <text class="t-strong" x="66" y="160">Reactive loop</text>
  <text class="t-small" x="66" y="178">100–1000 Hz</text>
  {tower(218, 30, 44, 0.7)}
  <text class="t-good" x="190" y="44" text-anchor="end" style="font-size:14px">Farm-wide</text>
  <text class="t-good" x="190" y="62" text-anchor="end" style="font-size:14px">private 5G</text>
  <text class="t-good" x="190" y="80" text-anchor="end" style="font-size:14px">network</text>
  <line class="line" x1="254" y1="124" x2="186" y2="124" marker-end="url(#dg-fb-af)"/>
  <text class="t-small" x="220" y="116" text-anchor="middle">plans</text>
  <line class="line" x1="184" y1="164" x2="252" y2="164" marker-end="url(#dg-fb-af)"/>
  <text class="t-small" x="220" y="182" text-anchor="middle">sensors</text>
  <rect class="box" x="258" y="14" width="176" height="184" rx="10"/>
  <text class="t-title" x="272" y="40">5G edge server</text>
  <text class="t-body" x="272" y="58">shared GPUs</text>
  <rect class="t3-box" x="266" y="68" width="160" height="66" rx="14"/>
  {loop(286, 90, 10, "t3-line", "dg-fb-a3")}
  <text class="t-strong" x="302" y="94">Deliberative</text>
  <text class="t-strong" x="302" y="111">loop</text>
  <text class="t-small" x="302" y="127">AI perception</text>
  {"".join(f'<rect class="plain" x="266" y="{y}" width="160" height="10" rx="3"/><circle class="t1-fill" cx="414" cy="{y+5}" r="2.5"/>' for y in (146,162,178))}
  <rect class="chassis" x="6" y="206" width="190" height="36" rx="8"/>
  <text class="t-on-chassis" x="101" y="229" text-anchor="middle">Lightweight robot</text>
  {"".join(f'<circle class="wheel" cx="{x}" cy="250" r="12"/>' for x in (46,101,156))}
  {minis}
  <text class="t-small" x="346" y="258" text-anchor="middle">fleet shares one edge</text>
  <text class="t-good" x="220" y="290" text-anchor="middle">Lightweight · inexpensive · low-power</text>
</svg>
'''
for name, svg in (("architecture.svg", arch), ("split-today.svg", today), ("split-farmbrain.svg", fb)):
    open(os.path.join(OUT, name), "w").write(svg)
print("ok")
