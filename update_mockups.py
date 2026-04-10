#!/usr/bin/env python3
"""Replace CSS-only mockups with photo-based mockup cards using Pexels images."""

import re

filepath = r'd:\Pragmatech\Works\Vaam\VAAM_BRAND_IDENTITY.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1) ADD NEW PHOTO-MOCKUP CSS BEFORE </style> ─────────────────────────
new_css = """
/* ═══ PHOTO MOCKUP SYSTEM ═══ */
.pm-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:16px 0}
.pm-grid--3{grid-template-columns:repeat(3,1fr)}
.pm-grid--1{grid-template-columns:1fr;max-width:480px}
.pm-item{text-align:center}
.pm-card{position:relative;overflow:hidden;border-radius:16px;
  box-shadow:0 4px 20px rgba(0,0,0,.08),0 12px 40px rgba(0,0,0,.06);
  transition:transform .5s cubic-bezier(.23,1,.32,1),box-shadow .5s ease}
.pm-card:hover{transform:translateY(-6px);box-shadow:0 12px 32px rgba(0,0,0,.12),0 24px 56px rgba(0,0,0,.08)}
.pm-bg{width:100%;display:block;object-fit:cover}
.pm-bg--4x3{aspect-ratio:4/3}.pm-bg--3x4{aspect-ratio:3/4}.pm-bg--16x9{aspect-ratio:16/9}.pm-bg--1x1{aspect-ratio:1}
.pm-brand{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}
.pm-brand--dark{background:linear-gradient(160deg,rgba(15,23,42,.6),rgba(15,23,42,.35) 50%,rgba(15,23,42,.55))}
.pm-brand--light{background:linear-gradient(160deg,rgba(255,255,255,.7),rgba(255,255,255,.4) 50%,rgba(255,255,255,.6))}
.pm-brand--vignette{background:radial-gradient(ellipse at center,rgba(15,23,42,.1) 30%,rgba(15,23,42,.55) 100%)}
.pm-brand--bottom{background:linear-gradient(to top,rgba(15,23,42,.75) 0%,rgba(15,23,42,.15) 50%,transparent 100%);justify-content:flex-end;padding-bottom:28px}
.pm-brand img{filter:drop-shadow(0 2px 8px rgba(0,0,0,.25))}
.pm-name{font-family:'Plus Jakarta Sans';font-weight:800;color:#fff;letter-spacing:4px;text-shadow:0 2px 8px rgba(0,0,0,.25)}
.pm-name--dark{color:var(--s9);text-shadow:none}
.pm-sub{font-size:9px;color:rgba(255,255,255,.5);letter-spacing:3px;text-transform:uppercase}
.pm-detail{font-size:9px;color:rgba(255,255,255,.45);line-height:1.6;text-align:center;margin-top:4px}
.pm-rule{width:36px;height:2px;background:var(--grad);border-radius:1px}
.pm-label{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--s4);font-weight:600;text-align:center;margin-top:14px}
"""

# Insert before the closing </style> (add to responsive section)
content = content.replace(
    '  .scene--row{flex-direction:column;align-items:center}\n}\n</style>',
    '  .scene--row{flex-direction:column;align-items:center}\n  .pm-grid,.pm-grid--3{grid-template-columns:1fr}\n}\n' + new_css + """
/* Photo mockup print */
@media print{
  .pm-card{box-shadow:0 1px 4px rgba(0,0,0,.08) !important;transform:none !important;border-radius:10px}
  .pm-card:hover{transform:none !important}
  .pm-grid{gap:12px;margin:8px 0}
  .pm-grid--3{gap:10px}
}
</style>"""
)

# ─── 2) REPLACE MOCKUP SECTIONS 08-12 WITH PHOTO-BASED 05-09 ─────────────

# Pexels base URL
P = "https://images.pexels.com/photos"

new_sections = f'''<!-- ═════════════════════════════════════════════ -->
<!--  05 — SƏNƏDLƏŞMƏ                           -->
<!-- ═════════════════════════════════════════════ -->
<div class="sec page-break" id="s5">
  <div class="sec-head"><span class="sec-num">05</span><h2 class="sec-title">Sənədləşmə</h2></div>

  <p class="sub-title">Kartvizit</p>
  <div class="pm-grid">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--4x3" src="{P}/4466104/pexels-photo-4466104.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Kartvizit">
        <div class="pm-brand pm-brand--dark">
          <img style="width:36px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:18px">VAAM</div>
          <div class="pm-rule"></div>
          <div class="pm-detail">Zeynal Nabiyev<br>İnkişaf Meneceri<br>+86 186 9014 9671<br>info@vaamglobal.com</div>
        </div>
      </div>
      <div class="pm-label">Ön tərəf</div>
    </div>
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--4x3" src="{P}/4465147/pexels-photo-4465147.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Kartvizit arxa">
        <div class="pm-brand pm-brand--vignette">
          <img style="width:48px;opacity:.8" src="static/images/logo/vaam-icon.svg" alt="">
        </div>
      </div>
      <div class="pm-label">Arxa tərəf</div>
    </div>
  </div>

  <p class="sub-title">Blanka &amp; Zərf</p>
  <div class="pm-grid">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/5706020/pexels-photo-5706020.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Blanka">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:28px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:13px">VAAM</div>
          <div class="pm-sub">vaamglobal.com · info@vaamglobal.com</div>
        </div>
      </div>
      <div class="pm-label">Blanka</div>
    </div>
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/5706002/pexels-photo-5706002.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Zərf">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:28px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:13px">VAAM</div>
          <div class="pm-sub">Otaq 688, Huanshi Qərb Yolu, Quançjou</div>
        </div>
      </div>
      <div class="pm-label">Zərf</div>
    </div>
  </div>

  <p class="sub-title">Möhür</p>
  <div class="pm-grid--1" style="margin:16px 0">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--4x3" src="{P}/9869077/pexels-photo-9869077.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Möhür">
        <div class="pm-brand pm-brand--vignette">
          <div style="width:120px;height:120px;border-radius:50%;border:3px solid rgba(16,185,129,.7);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;background:rgba(255,255,255,.15);backdrop-filter:blur(4px)">
            <img style="width:28px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.2))" src="static/images/logo/vaam-icon.svg" alt="">
            <span style="font-family:'Plus Jakarta Sans';font-weight:800;font-size:7px;color:#fff;letter-spacing:3px;text-shadow:0 1px 4px rgba(0,0,0,.3)">VAAM GLOBAL</span>
          </div>
        </div>
      </div>
      <div class="pm-label">Korporativ Möhür</div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═════════════════════════════════════════════ -->
<!--  06 — OFİS LƏVAZİMATLARI                    -->
<!-- ═════════════════════════════════════════════ -->
<div class="sec page-break" id="s6">
  <div class="sec-head"><span class="sec-num">06</span><h2 class="sec-title">Ofis Ləvazimatları</h2></div>

  <p class="sub-title">Qələmlər</p>
  <div class="pm-grid--1" style="margin:16px 0;max-width:600px">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--16x9" src="{P}/346553/pexels-photo-346553.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Qələm">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:20px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:10px;letter-spacing:3px">VAAM</div>
        </div>
      </div>
      <div class="pm-label">Korporativ Qələm</div>
    </div>
  </div>

  <p class="sub-title">USB Flash</p>
  <div class="pm-grid--1" style="margin:16px 0;max-width:600px">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--16x9" src="{P}/2608409/pexels-photo-2608409.jpeg?auto=compress&cs=tinysrgb&w=800" alt="USB">
        <div class="pm-brand pm-brand--dark">
          <img style="width:24px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:10px;letter-spacing:3px">VAAM</div>
          <div class="pm-sub">USB Flash Drive</div>
        </div>
      </div>
      <div class="pm-label">USB Flash</div>
    </div>
  </div>

  <p class="sub-title">Dəftər &amp; Qovluq</p>
  <div class="pm-grid">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/28536453/pexels-photo-28536453.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Dəftər">
        <div class="pm-brand pm-brand--vignette">
          <img style="width:36px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:12px">VAAM</div>
          <div class="pm-rule"></div>
        </div>
      </div>
      <div class="pm-label">Dəftər</div>
    </div>
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/8947463/pexels-photo-8947463.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Qovluq">
        <div class="pm-brand pm-brand--vignette">
          <img style="width:36px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:12px">VAAM</div>
          <div class="pm-rule"></div>
        </div>
      </div>
      <div class="pm-label">Qovluq</div>
    </div>
  </div>

  <p class="sub-title">Fincan</p>
  <div class="pm-grid--1" style="margin:16px 0">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--4x3" src="{P}/11075707/pexels-photo-11075707.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Fincan">
        <div class="pm-brand pm-brand--light">
          <img style="width:36px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name pm-name--dark" style="font-size:14px">VAAM</div>
        </div>
      </div>
      <div class="pm-label">Keramik Fincan</div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═════════════════════════════════════════════ -->
<!--  07 — GEYİM & AKSESUAR                      -->
<!-- ═════════════════════════════════════════════ -->
<div class="sec page-break" id="s7">
  <div class="sec-head"><span class="sec-num">07</span><h2 class="sec-title">Geyim &amp; Aksesuar</h2></div>

  <div class="pm-grid--3">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/3779445/pexels-photo-3779445.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Polo">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:28px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:10px">VAAM</div>
        </div>
      </div>
      <div class="pm-label">Polo Köynək</div>
    </div>
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/7530916/pexels-photo-7530916.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Papaq">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:28px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:10px">VAAM</div>
        </div>
      </div>
      <div class="pm-label">Papaq</div>
    </div>
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--3x4" src="{P}/6373948/pexels-photo-6373948.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Şəxsiyyət kartı">
        <div class="pm-brand pm-brand--bottom">
          <img style="width:28px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:10px">VAAM</div>
          <div class="pm-detail">Zeynal Nabiyev<br>Menecer</div>
        </div>
      </div>
      <div class="pm-label">Şəxsiyyət Kartı</div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═════════════════════════════════════════════ -->
<!--  08 — RƏQƏMSAL                              -->
<!-- ═════════════════════════════════════════════ -->
<div class="sec" id="s8">
  <div class="sec-head"><span class="sec-num">08</span><h2 class="sec-title">Rəqəmsal Materiallar</h2></div>

  <p class="sub-title">Sosial Media</p>
  <div class="pm-grid--1" style="margin:16px 0;max-width:400px">
    <div class="pm-item">
      <div class="pm-card">
        <div class="pm-bg pm-bg--1x1" style="background:linear-gradient(150deg,#020617,#0f172a 45%,#0c2822)"></div>
        <div class="pm-brand" style="background:none">
          <div style="position:absolute;width:200px;height:200px;border-radius:50%;top:-60px;left:-50px;background:radial-gradient(circle,rgba(16,185,129,.1),transparent 60%)"></div>
          <div style="position:absolute;width:160px;height:160px;border-radius:50%;bottom:-50px;right:-40px;background:radial-gradient(circle,rgba(251,191,36,.07),transparent 60%)"></div>
          <img style="width:56px;position:relative" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:22px;position:relative">VAAM</div>
          <div class="pm-rule" style="position:relative"></div>
          <div class="pm-sub" style="position:relative;margin-top:8px">Import · Export · Trading</div>
        </div>
      </div>
      <div class="pm-label">Profil əsası</div>
    </div>
  </div>

  <p class="sub-title">E-poçt İmzası</p>
  <div style="margin:16px 0;display:flex;justify-content:center">
    <div class="esig3d">
      <div class="es-icon"><img src="static/images/logo/vaam-icon.svg" alt=""></div>
      <div class="es-div"></div>
      <div class="es-info">
        <div class="es-name">Zeynal Nabiyev</div>
        <div class="es-title">İnkişaf Meneceri</div>
        <div class="es-contact">+86 186 9014 9671<br>info@vaamglobal.com<br><a href="#">vaamglobal.com</a></div>
      </div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═════════════════════════════════════════════ -->
<!--  09 — NƏQLİYYAT & QABLAŞDIRMA              -->
<!-- ═════════════════════════════════════════════ -->
<div class="sec page-break" id="s9">
  <div class="sec-head"><span class="sec-num">09</span><h2 class="sec-title">Nəqliyyat &amp; Qablaşdırma</h2></div>

  <p class="sub-title">Nəqliyyat</p>
  <div style="margin:16px 0">
    <div class="pm-card">
      <img class="pm-bg pm-bg--16x9" src="{P}/4391470/pexels-photo-4391470.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Nəqliyyat">
      <div class="pm-brand pm-brand--dark">
        <img style="width:44px" src="static/images/logo/vaam-icon.svg" alt="">
        <div class="pm-name" style="font-size:26px">VAAM</div>
        <div class="pm-sub">Import · Export · Trading</div>
        <div class="pm-rule"></div>
        <div class="pm-detail">vaamglobal.com</div>
      </div>
    </div>
    <div class="pm-label" style="text-align:center">Korporativ Nəqliyyat</div>
  </div>

  <p class="sub-title">Qutu</p>
  <div class="pm-grid--1" style="margin:16px 0;max-width:500px">
    <div class="pm-item">
      <div class="pm-card">
        <img class="pm-bg pm-bg--4x3" src="{P}/7956854/pexels-photo-7956854.jpeg?auto=compress&cs=tinysrgb&w=800" alt="Qutu">
        <div class="pm-brand pm-brand--vignette">
          <img style="width:36px" src="static/images/logo/vaam-icon.svg" alt="">
          <div class="pm-name" style="font-size:14px">VAAM</div>
          <div class="pm-rule"></div>
        </div>
      </div>
      <div class="pm-label">Karton Qutu</div>
    </div>
  </div>
</div>

<hr class="divider">

'''

# Find the section 08 block start
marker_08 = '<!--  08 — SƏNƏDLƏŞMƏ'
marker_13 = '<!--  13 — EDİLMƏLİ'

idx_08 = content.find(marker_08)
idx_13 = content.find(marker_13)

if idx_08 == -1 or idx_13 == -1:
    print("ERROR: Could not find section markers!")
    exit(1)

# Go back from idx_08 to find the fence line (<!-- ═══...═══ -->)
fence_08_start = content.rfind('<!-- ═', 0, idx_08)

# Go back from idx_13 to find the fence line before it
fence_13_start = content.rfind('<!-- ═', 0, idx_13)

# The block to replace is from fence_08_start to fence_13_start
old_block = content[fence_08_start:fence_13_start]
print(f"Old block length: {len(old_block)} chars")
print(f"Old block starts with: {old_block[:80]}...")
print(f"Old block ends with:   ...{old_block[-80:]}")

# Replace the block
content = content[:fence_08_start] + new_sections + content[fence_13_start:]

# ─── 3) RENUMBER SECTION 13 → 10 ─────────────────────────────────────────
content = content.replace('<!--  13 — EDİLMƏLİ / EDİLMƏMƏLİ                -->', '<!--  10 — EDİLMƏLİ / EDİLMƏMƏLİ                -->')
content = content.replace('id="s13"', 'id="s10"')
content = content.replace('<span class="sec-num">13</span><h2 class="sec-title">Edilməli', '<span class="sec-num">10</span><h2 class="sec-title">Edilməli')

# ─── 4) WRITE THE FILE ───────────────────────────────────────────────────
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! File updated successfully.")
print(f"New file size: {len(content)} chars")
