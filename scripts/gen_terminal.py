#!/usr/bin/env python3
"""生成 neofetch + top 风格的动画终端 SVG：python3 scripts/gen_terminal.py"""
import os
from html import escape

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "terminal.svg")

# Catppuccin Mocha
CRUST, BG, MANTLE, SURFACE, SURFACE2, OVERLAY = "#11111b", "#1e1e2e", "#181825", "#313244", "#45475a", "#6c7086"
TEXT, SUB = "#cdd6f4", "#a6adc8"
PINK, MAUVE, RED, PEACH = "#f5c2e7", "#cba6f7", "#f38ba8", "#fab387"
YELLOW, GREEN, TEAL, BLUE = "#f9e2af", "#a6e3a1", "#94e2d5", "#89b4fa"

FONT = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
FS, CW = 14, 8.4  # 字号、估算字宽

# ---------- 栅格 ----------
W = 900
M = 32            # 窗口内边距
PAD = 24          # 面板内边距
PL, PR = M, W - M  # 面板左右边界
LH = 22           # 信息行高
GAP = 10          # 分组间距

# ---------- neofetch：右侧信息（按组） ----------
INFO = [
    [
        ("OS",        "Linux 6.8.9-custom-soc x86_64", BLUE, TEXT),
        ("Role",      "Software Engineer · Architect", TEXT, SUB),
        ("Primary",   "Java 21 · Virtual Threads · JVM", PEACH, PEACH),
        ("Backend",   "Spring · PostgreSQL · Redis · MongoDB", YELLOW, TEXT),
    ],
    [
        ("Minecraft", "Spigot · Paper · Folia · Velocity", GREEN, TEXT),
        ("Systems",   "Rust · Concurrency · Performance", RED, TEXT),
        ("Cluster",   "Distributed Systems · System Design", TEAL, TEXT),
        ("Lambda",    "Elixir · Scala · Functional Prog.", MAUVE, TEXT),
        ("Infra",     "Docker · Kubernetes · Cryptography", BLUE, TEXT),
    ],
    [
        ("Swap",      "\"Song of Saya\" cache", OVERLAY, SUB),
        ("Hidden",    "./dg-lab-client --shock=auto", RED, RED),
    ],
]
KEY_W = 11  # key 列宽（字符）

# 像素画下方的小状态
STATS = [("uptime", "19y 172d"), ("load", "8.05 7.80 7.50"), ("uid", "2000000")]

# ---------- top：技能进程表 ----------
TOP = [
    # (pid, command, %cpu, 技能, 颜色)
    (2000, "java -jar legacy-lands.jar", 100.0, "Java · Fairy · Paper/Folia", PEACH),
    (3050, "java -jar spring-backend.jar", 98.5, "Java · Spring · Backend", YELLOW),
    (1337, "cargo run --release", 92.0, "Rust · Concurrency · Perf", RED),
    (4022, "beam.smp --distributed", 85.0, "Elixir · Distributed", MAUVE),
    (5120, "kubectl apply -f k8s/", 72.0, "Docker · Kubernetes", BLUE),
    (5432, "postgres / redis / mongod", 65.0, "PostgreSQL · Redis · Mongo", TEAL),
    (8086, "claude --assist", 40.0, "AI-Assisted Tooling", PINK),
]
ROW_H = 30

# ---------- git log：经历时间线 ----------
CAREER = [
    # (年份, 名称, 角色, 备注, 进行中, 颜色)
    ("2026 — now",  "Pillage.net",        "Minecraft Server Dev", "anarchy server", True, RED),
    ("2026 — now",  "PvPCN.net",          "Practice Server Dev",  "practice server", True, PEACH),
    ("2024 — now",  "Legacy Lands",       "Core Developer",       "★ 700+ · 90+ forks", True, MAUVE),
    ("2024 — now",  "HZ / Cloud Habitat", "Admin & Tech Support", "wiki · l10n", True, YELLOW),
    ("2024 — now",  "Open Source",        "Contributor",          "CMI · Slimefun zh-CN", True, TEAL),
    ("2020 — 2023", "Atorant / HolyKits", "Founder & Lead Dev",   "PvP network", False, BLUE),
    ("2018 — 2020", "MC Networks",        "Server Staff",         "where it began", False, OVERLAY),
]
HIGHLIGHT = "Legacy Lands"

# ---------- 像素画：QwQ ----------
Q = [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"]
w = [".....", ".....", "#...#", "#...#", "#.#.#", "#.#.#", ".#.#."]
ART = [Q[r] + "." + w[r] + "." + Q[r] for r in range(7)]
PX = 13
ART_COL_W = 268   # 左栏宽度

# ---------- 时间轴 ----------
T_CMD1, T_INFO, STEP = 0.35, 1.6, 0.07
N_INFO = sum(len(g) for g in INFO)
T_CMD2 = T_INFO + (N_INFO + 4) * STEP + 0.3
T_TOP = T_CMD2 + 1.2
T_CMD3 = T_TOP + (len(TOP) + 1) * 0.11 + 0.5
T_GIT = T_CMD3 + 1.2
T_END = T_GIT + (len(CAREER) + 1) * 0.11 + 0.6

keyframes = []
body = []


def t(x, y, s, fill=TEXT, extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}"{extra}>{escape(s)}</text>'


def fade(delay, inner):
    return f'<g class="l" style="animation-delay:{delay:.2f}s">{inner}</g>'


PROMPT = (f'<tspan fill="{GREEN}">qwqdev@soc</tspan><tspan fill="{OVERLAY}">:</tspan>'
          f'<tspan fill="{BLUE}">~</tspan><tspan fill="{OVERLAY}">$ </tspan>')
PROMPT_W = len("qwqdev@soc:~$ ") * CW


def typed(idx, y, cmd, delay):
    """提示符 + 逐字出现的命令。"""
    n = len(cmd)
    keyframes.append(f"@keyframes type{idx}{{to{{transform:translateX({n * CW:.1f}px)}}}}")
    return (f'<text x="{M}" y="{y}">{PROMPT}<tspan fill="{TEXT}">{escape(cmd)}</tspan></text>'
            f'<rect x="{M + PROMPT_W:.1f}" y="{y - 16}" width="{(n + 2) * CW:.1f}" height="22" fill="{BG}" '
            f'style="animation:type{idx} {max(.5, n * .045):.2f}s steps({n}) {delay:.2f}s forwards"/>')


def panel(y1, y2, title, color, delay, right=None):
    """btop 风格面板：圆角边框 + 嵌在上边框的标题。"""
    s = f'<rect x="{PL}" y="{y1}" width="{PR - PL}" height="{y2 - y1}" rx="10" fill="{MANTLE}" stroke="{SURFACE}"/>'
    tw = 20 + len(title) * 7.4 + 12  # 左：圆点区，右：留白
    s += (f'<rect x="{PL + 18}" y="{y1 - 10}" width="{tw:.1f}" height="20" rx="10" fill="{BG}" stroke="{SURFACE}"/>'
          f'<circle cx="{PL + 30}" cy="{y1}" r="3" fill="{color}"/>'
          + t(PL + 38, y1 + 4, title, color, ' font-size="12" font-weight="bold"'))
    if right:
        rw = len(right) * 7.4 + 28
        s += (f'<rect x="{PR - 18 - rw:.1f}" y="{y1 - 10}" width="{rw:.1f}" height="20" rx="10" fill="{BG}" stroke="{SURFACE}"/>'
              + t(PR - 18 - rw / 2, y1 + 4, right, OVERLAY, ' font-size="12" text-anchor="middle"'))
    return fade(delay, s)


# ============ 第一段：neofetch ============
y = 72
body.append(typed(1, y, "neofetch --full-stack", T_CMD1))

P1_TOP = y + 30
info_x = PL + ART_COL_W + 28
y = P1_TOP + PAD + 18
info = [f'<text x="{info_x}" y="{y}" font-weight="bold"><tspan fill="{MAUVE}">QwQ-dev</tspan>'
        f'<tspan fill="{OVERLAY}">@</tspan><tspan fill="{BLUE}">QWQ_LAB_SOC</tspan></text>'
        + t(PR - PAD, y, "Shaping the unseen.", OVERLAY, ' font-style="italic" font-size="12" text-anchor="end"')]
y += 12
info.append(f'<rect x="{info_x}" y="{y}" width="{len("QwQ-dev@QWQ_LAB_SOC") * CW:.1f}" height="2" rx="1" fill="url(#g)"/>')
y += 8
i = 0
for gi, group in enumerate(INFO):
    if gi:
        y += GAP
    for k, v, kc, vc in group:
        y += LH
        info.append((i, t(info_x, y, k, kc, ' font-weight="bold"') + t(info_x + KEY_W * CW, y, v, vc)))
        i += 1
y += LH + 10
blocks = "".join(f'<rect x="{info_x + j * 28}" y="{y - 12}" width="22" height="12" rx="3" fill="{c}"/>'
                 for j, c in enumerate((RED, PEACH, YELLOW, GREEN, TEAL, BLUE, MAUVE, PINK)))
P1_BOT = y + PAD

body.append(panel(P1_TOP, P1_BOT, "neofetch", MAUVE, T_INFO - 0.2, right=f"{N_INFO} modules"))
body.append(fade(T_INFO - 0.1, f'<rect x="{PL + ART_COL_W}" y="{P1_TOP + PAD}" width="1" height="{P1_BOT - P1_TOP - 2 * PAD}" fill="{SURFACE}"/>'))
body.append(fade(T_INFO, info[0] + info[1]))
for idx, s in info[2:]:
    body.append(fade(T_INFO + (idx + 1) * STEP, s))
body.append(fade(T_INFO + (N_INFO + 1) * STEP, blocks))

# 左栏：像素画 + 状态，整体垂直居中
art_w, art_h = 17 * PX, 7 * PX
stats_h = len(STATS) * 20
block_h = art_h + 34 + stats_h
art_x = PL + (ART_COL_W - art_w) / 2
art_y = (P1_TOP + P1_BOT) / 2 - block_h / 2
body.append('<g filter="url(#glow)">')
for r, row in enumerate(ART):
    for c, ch in enumerate(row):
        if ch == "#":
            d = T_INFO - 0.1 + c * 0.03 + r * 0.02
            body.append(f'<rect class="p" style="animation-delay:{d:.2f}s" x="{art_x + c * PX:.1f}" y="{art_y + r * PX:.1f}" '
                        f'width="{PX - 2}" height="{PX - 2}" rx="2" fill="url(#g)"/>')
body.append("</g>")
sy = art_y + art_h + 34
sk_x = art_x + 8
sv_x = art_x + art_w - 8
for j, (k, v) in enumerate(STATS):
    body.append(fade(T_INFO + (j + 2) * STEP,
                     t(sk_x, sy + j * 20, k, OVERLAY, ' font-size="12"')
                     + t(sv_x, sy + j * 20, v, SUB, ' font-size="12" text-anchor="end"')))
grad = (art_x, art_y, art_x + art_w, art_y + art_h)

# ============ 第二段：top ============
y = P1_BOT + 48
body.append(fade(T_CMD2 - 0.05, typed(2, y, "top -o %CPU -u qwqdev", T_CMD2)))

P2_TOP = y + 30
C_PID = PL + PAD + 4 * CW          # 右对齐
C_CMD = C_PID + 20
C_BAR, BAR_W = C_CMD + 29 * CW, 150
C_PCT = C_BAR + BAR_W + 58         # 右对齐
C_SKILL = C_PCT + 22

y = P2_TOP + PAD + 14
hdr = ' font-size="12" letter-spacing="1"'
rows = [t(C_PID, y, "PID", OVERLAY, hdr + ' text-anchor="end"') + t(C_CMD, y, "COMMAND", OVERLAY, hdr)
        + t(C_BAR, y, "LOAD", OVERLAY, hdr) + t(C_PCT, y, "%CPU", OVERLAY, hdr + ' text-anchor="end"')
        + t(C_SKILL, y, "SKILL", OVERLAY, hdr)
        + f'<rect x="{PL + PAD}" y="{y + 10}" width="{PR - PL - 2 * PAD}" height="1" fill="{SURFACE}"/>']
y += 10
for i, (pid, cmd, pct, skill, color) in enumerate(TOP):
    y += ROW_H
    d = T_TOP + (i + 1) * 0.11
    hl = i < 2  # Java 两行高亮
    row = ""
    if i == 0:
        row += f'<rect x="{PL + PAD - 10}" y="{y - 20}" width="{PR - PL - 2 * PAD + 20}" height="28" rx="6" fill="{SURFACE}" fill-opacity=".45"/>'
    row += (t(C_PID, y, str(pid), OVERLAY, ' text-anchor="end"')
            + t(C_CMD, y, cmd, TEXT if hl else SUB, ' font-weight="bold"' if i == 0 else "")
            + f'<rect x="{C_BAR}" y="{y - 8}" width="{BAR_W}" height="6" rx="3" fill="{SURFACE2 if i == 0 else SURFACE}"/>'
            + f'<rect class="bar" style="animation-delay:{d + .15:.2f}s" x="{C_BAR}" y="{y - 8}" '
              f'width="{BAR_W * pct / 100:.1f}" height="6" rx="3" fill="{color}"/>'
            + t(C_PCT, y, f"{pct:.1f}", color, ' font-weight="bold" text-anchor="end"')
            + t(C_SKILL, y, skill, TEXT if hl else SUB))
    rows.append((d, row))
P2_BOT = y + PAD

body.append(panel(P2_TOP, P2_BOT, "proc", PEACH, T_TOP - 0.1, right=f"{len(TOP)} running · sorted by %CPU"))
body.append(fade(T_TOP, rows[0]))
for d, row in rows[1:]:
    body.append(fade(d, row))

# ============ 第三段：git log ============
y = P2_BOT + 48
body.append(fade(T_CMD3 - 0.05, typed(3, y, "git log --graph ~/career", T_CMD3)))

P3_TOP = y + 30
G_X = PL + PAD + 8
C_YEAR = G_X + 20
C_NAME = C_YEAR + 13 * CW
C_ROLE = C_NAME + 21 * CW
C_NOTE = PR - PAD  # 右对齐
y = P3_TOP + PAD - 2
first_y = y + ROW_H - 4
rows = []
for i, (year, name, role, note, live, color) in enumerate(CAREER):
    y += ROW_H
    d = T_GIT + (i + 1) * 0.11
    cy = y - 4
    row = ""
    if name == HIGHLIGHT:
        row += f'<rect x="{PL + PAD - 10}" y="{y - 20}" width="{PR - PL - 2 * PAD + 20}" height="28" rx="6" fill="{SURFACE}" fill-opacity=".45"/>'
    if live:
        row += (f'<circle cx="{G_X}" cy="{cy}" r="8" fill="{color}" fill-opacity=".18"/>'
                f'<circle cx="{G_X}" cy="{cy}" r="4.5" fill="{color}"/>')
    else:
        row += f'<circle cx="{G_X}" cy="{cy}" r="4.5" fill="{MANTLE}" stroke="{color}" stroke-width="2"/>'
    row += (t(C_YEAR, y, year, OVERLAY, ' font-size="12"')
            + t(C_NAME, y, name, color if live else SUB, ' font-weight="bold"')
            + t(C_ROLE, y, role, TEXT if live else SUB)
            + t(C_NOTE, y, note, MAUVE if name == HIGHLIGHT else OVERLAY,
                ' font-size="12" text-anchor="end"' + (' font-weight="bold"' if name == HIGHLIGHT else "")))
    rows.append((d, row))
last_y = y - 4
P3_BOT = y + PAD

body.append(panel(P3_TOP, P3_BOT, "career", GREEN, T_GIT - 0.1, right="since 2018"))
body.append(fade(T_GIT, f'<rect x="{G_X - 1}" y="{first_y}" width="2" height="{last_y - first_y}" rx="1" fill="{SURFACE}"/>'))
for d, row in rows:
    body.append(fade(d, row))

# ============ 结尾 ============
y = P3_BOT + 44
body.append(fade(T_END, t(M, y, "# Passionate about hand-crafted code, augmented by AI.", OVERLAY, ' font-style="italic"')))
y += 30
body.append(fade(T_END + .15, f'<text x="{M}" y="{y}">{PROMPT}</text>'
                 f'<rect class="cur" x="{M + PROMPT_W:.1f}" y="{y - 14}" width="{CW:.1f}" height="18" fill="{PINK}"/>'))
H = int(y + 34)

# ============ 组装 ============
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
out.append(f"""<style>
text{{font-family:{FONT};font-size:{FS}px;white-space:pre}}
.l{{opacity:0;animation:in .35s ease-out forwards}}
.p{{opacity:0;animation:pop .4s cubic-bezier(.3,1.6,.6,1) forwards;transform-box:fill-box;transform-origin:center}}
.bar{{transform:scaleX(0);transform-box:fill-box;transform-origin:left;animation:grow .9s cubic-bezier(.2,.8,.2,1) forwards}}
.cur{{animation:blink 1s step-end infinite}}
@keyframes in{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes grow{{to{{transform:scaleX(1)}}}}
@keyframes blink{{50%{{opacity:0}}}}
{chr(10).join(keyframes)}
</style>""")
out.append(f"""<defs>
<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="{grad[0]:.1f}" y1="{grad[1]:.1f}" x2="{grad[2]:.1f}" y2="{grad[3]:.1f}">
<stop offset="0" stop-color="{PINK}"/><stop offset=".5" stop-color="{MAUVE}"/><stop offset="1" stop-color="{BLUE}"/>
</linearGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>""")
out.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{SURFACE}"/>')
out.append(f'<path d="M.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12V38H.5z" fill="{CRUST}"/>')
out.append(f'<rect x=".5" y="38" width="{W - 1}" height="1" fill="{SURFACE}"/>')
for i, c in enumerate((RED, YELLOW, GREEN)):
    out.append(f'<circle cx="{22 + i * 20}" cy="19" r="6" fill="{c}"/>')
out.append(t(W / 2, 24, "QwQ-dev@QWQ_LAB_SOC: ~", OVERLAY, ' text-anchor="middle" font-size="12"'))
out += body
out.append("</svg>")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(out))
print(OUT, f"{W}x{H}", f"anim≈{T_END + .5:.1f}s")
