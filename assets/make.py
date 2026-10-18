# Builds the profile README's banner and project cards (light + dark SVGs).
#   python assets/make.py
# Same flat tile look as Claude Switch: thin borders, uppercase titles,
# ring gauges. Fonts are system stacks because GitHub blocks web fonts in SVGs.
import os, html

OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
THEMES = {
    'dark':  dict(bg='#0d1117', card='#161b22', inner='#1f2630', border='#30363d', text='#e6edf3', muted='#9da7b3',
                  accent='#4db0f2', track='#2d333b', good='#3fb950', warn='#f2c14e'),
    'light': dict(bg='#ffffff', card='#f6f8fa', inner='#eef1f5', border='#d0d7de', text='#1f2328', muted='#57606a',
                  accent='#0a62a0', track='#d8dee4', good='#1a7f37', warn='#9a6700'),
}
e = html.escape


def ring(cx, cy, r, pct, color, label, value, t, delay):
    c = 2 * 3.14159 * r
    off = c * (1 - pct / 100)
    return f'''
  <g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t['track']}" stroke-width="7"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"
            stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" transform="rotate(-90 {cx} {cy})">
      <animate attributeName="stroke-dashoffset" from="{c:.1f}" to="{off:.1f}" dur="1.6s" begin="{delay}s" fill="freeze"
               calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/>
    </circle>
    <text x="{cx}" y="{cy + 7}" text-anchor="middle" font-size="21" font-weight="700" fill="{color}">{e(value)}</text>
    <text x="{cx}" y="{cy + r + 26}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{t['muted']}" letter-spacing="1">{e(label)}</text>
  </g>'''


def banner(name):
    t = THEMES[name]
    chips = ['AI agents', 'MCP servers', 'LLM apps', 'Laravel', 'Python', 'React', '.NET', 'Cloudflare']
    x, chip_svg = 48, ''
    for c in chips:
        w = 18 + len(c) * 8.2
        chip_svg += (f'<rect x="{x}" y="196" width="{w:.0f}" height="28" rx="6" fill="{t["inner"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="215" text-anchor="middle" font-size="13.5" font-weight="600" fill="{t["text"]}">{e(c)}</text>')
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" font-family="{FONT}">
  <title>Ngonidzashe Maphosa, Lead Software Developer</title>
  <style>
    .fade {{ opacity: 0; animation: in .8s ease-out forwards; }}
    .d1 {{ animation-delay: .1s }} .d2 {{ animation-delay: .35s }} .d3 {{ animation-delay: .6s }} .d4 {{ animation-delay: .85s }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(8px) }} to {{ opacity: 1; transform: none }} }}
    @media (prefers-reduced-motion: reduce) {{ .fade {{ animation: none; opacity: 1 }} }}
  </style>
  <rect x="1" y="1" width="1198" height="298" rx="14" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.5"/>
  <rect x="48" y="38" width="64" height="5" rx="2.5" fill="#D97757"/>
  <rect x="116" y="38" width="64" height="5" rx="2.5" fill="#3B82F6"/>
  <rect x="184" y="38" width="64" height="5" rx="2.5" fill="#16A34A"/>
  <g class="fade d1"><text x="48" y="96" font-size="44" font-weight="800" fill="{t['text']}" letter-spacing=".5">NGONIDZASHE MAPHOSA</text></g>
  <g class="fade d2"><text x="48" y="134" font-size="21" font-weight="600" fill="{t['accent']}">Lead Software Developer at Elula</text>
     <text x="48" y="164" font-size="17" fill="{t['muted']}">Harare, Zimbabwe · I build products end to end: backends, AI features, apps and the cloud they run on</text></g>
  <g class="fade d3">{chip_svg}</g>
  <g class="fade d4"><text x="48" y="262" font-size="14" fill="{t['muted']}">BSc Hons Computer Science, NUST · UNICEF Generation Unlimited national winner · 1st place, BancABC fintech hackathon</text></g>
  <line x1="842" y1="40" x2="842" y2="260" stroke="{t['border']}"/>
  {ring(925, 128, 46, 100, t['accent'], 'PRODUCTS SHIPPED', '6+', t, 0.3)}
  {ring(1075, 128, 46, 86, '#D97757', 'AGENTS & MCP', 'AI', t, 0.6)}
</svg>'''


def wrap(text, limit):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > limit and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    lines.append(cur)
    return lines


CARDS = [
    ('claude-switch', 'Claude Switch', 'OPEN SOURCE', '#D97757',
     'Run several Claude Desktop accounts side by side, with usage rings, reset times and one-click hand-off between accounts.',
     ['C#', '.NET', 'Avalonia', 'Win · Mac · Linux']),
    ('vacancypal', 'VacancyPal', 'ON GOOGLE PLAY', '#16A34A',
     'AI job-search assistant for Zimbabwe, with OpenAI and Claude built in and Pesepay payments.',
     ['Next.js', 'Cloudflare Workers', 'Android']),
    ('moleads', 'MoLeads', 'LIVE', '#3B82F6',
     "Zimbabwe's local services marketplace: bidding, in-app calls and chat, verified providers and Pesepay top-ups.",
     ['Next.js', 'MySQL', 'WebRTC', 'Pesepay']),
    ('folio', 'Folio', 'LIVE', '#9333EA',
     'A tile-based e-book reader for free classics from Project Gutenberg, with reading progress and history.',
     ['TypeScript', 'Cloudflare Pages', 'OPDS']),
    ('platform-qa-kit', 'Platform QA Kit', 'OPEN SOURCE', '#0891B2',
     'A Claude skill that runs recorded end-to-end QA of a live web platform and writes a polished report with fixes.',
     ['Claude Code', 'Skills', 'Browser automation']),
    ('pocket-lab', 'My Pocket Lab', 'AWARD WINNER', '#CA8A04',
     '3D virtual chemistry lab for students without a physical lab. UNICEF Generation Unlimited national winner.',
     ['3D', 'WebGL', 'Education']),
]


def card(name, slug, title, badge, color, desc, chips):
    t = THEMES[name]
    lines = wrap(desc, 62)[:2]
    bw = 38 + len(badge) * 7.9
    chip_svg, x = '', 24
    for c in chips:
        w = 16 + len(c) * 7.2
        chip_svg += (f'<rect x="{x}" y="150" width="{w:.0f}" height="24" rx="5" fill="{t["inner"]}" stroke="{t["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="166.5" text-anchor="middle" font-size="12" font-weight="600" fill="{t["text"]}">{e(c)}</text>')
        x += w + 6
    desc_svg = ''.join(f'<text x="24" y="{98 + i * 22}" font-size="14.5" fill="{t["muted"]}">{e(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="196" viewBox="0 0 580 196" font-family="{FONT}">
  <title>{e(title)}</title>
  <rect x="1" y="1" width="578" height="194" rx="12" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.5"/>
  <rect x="24" y="22" width="532" height="4" rx="2" fill="{color}"/>
  <text x="24" y="64" font-size="22" font-weight="800" fill="{t['text']}" letter-spacing=".3">{e(title.upper())}</text>
  <rect x="{556 - bw:.0f}" y="44" width="{bw:.0f}" height="26" rx="13" fill="none" stroke="{color}" stroke-width="1.5"/>
  <circle cx="{556 - bw + 13:.0f}" cy="57" r="4" fill="{color}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
  <text x="{556 - bw / 2 + 8:.0f}" y="61.5" text-anchor="middle" font-size="11.5" font-weight="700" fill="{color}" letter-spacing=".4">{e(badge)}</text>
  {desc_svg}
  {chip_svg}
</svg>'''


for theme in THEMES:
    open(os.path.join(OUT, f'banner-{theme}.svg'), 'w', encoding='utf-8', newline='\n').write(banner(theme))
    for slug, title, badge, color, desc, chips in CARDS:
        open(os.path.join(OUT, f'card-{slug}-{theme}.svg'), 'w', encoding='utf-8', newline='\n').write(card(theme, slug, title, badge, color, desc, chips))
print('ok')
