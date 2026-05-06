"""v12 배경 아트 17장 · Imagen 4 Fast 병렬 생성.
Usage: GEMINI_API_KEY="..." python _generate.py
"""
import os, json, base64, urllib.request, urllib.error, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['GEMINI_API_KEY']
URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={KEY}"

BASE = ("2D anime visual novel cinematic illustration, korean manhwa webtoon pixiv "
        "high quality art style, cel shading, dramatic cinematic lighting, wide 16:9 "
        "composition. Background-focused — characters shown only as silhouettes or "
        "partial view (hands, uniform hem, backpack). Scene:")

JOBS = {
  # Act 1 · 死
  'bg_01_accident': BASE + " rain-slick night asphalt road intersection, neon sign red glow bleeding into puddles, overturned car silhouette in background, scattered broken glass shards in foreground, blue siren light pulsing in distance, no humans visible, cinematic slow-motion raindrop, melancholic noir palette",
  'bg_03_hospital': BASE + " empty hospital corridor at dawn, pale blue light through venetian blinds, single empty gurney in center with crumpled white sheets, flickering fluorescent tube overhead, sterile washed-out palette, long perspective, no people",
  'bg_04_watch': BASE + " extreme macro shot of cracked antique pocket watch on dark table, glass spider-web fractures, clock hands slowly reversing, blurred neon city lights reflected inside the glass like a ghost of previous scene, cinematic noir close-up",
  # Act 2 · 歸
  'bg_06_desk_afternoon': BASE + " first-person POV of wooden school desk in ASTIRIA Academy classroom, late afternoon golden west light, open notebook with pencil shavings, ginkgo tree leaf shadows dappled on paper, hands in school uniform sleeves resting on desk, no face visible, warm dust motes floating",
  'bg_07_doorway_seokhyun': BASE + " backlit classroom rear doorway, male student silhouette leaning against door frame, loosened school uniform tie, backpack strap on one shoulder, hand holding piece of bread, face obscured by bright hallway backlight, dust motes like golden powder floating, cinematic bokeh",
  'bg_08_notebook_macro': BASE + " extreme close-up on open school notebook page, handwritten Korean note 'June 14 · Leave early today - DO NOT', pencil shavings scattered, graphite highlight, open pencil case corner, warm classroom afternoon light",
  # Act 4-A · 숨김 (세하)
  'bg_A1_canteen_salt': BASE + " school canteen corner booth, vending machine emitting violet neon glow, cafeteria tray with chocolate milk carton and salt-dusted bread roll, macro shot of finger tip flicking salt crystals off bread surface, warm ambient light mixed with cool neon",
  'bg_A2_library_ticket': BASE + " library stack aisle in late afternoon, amber orange sunlight through tall arched windows, open book on oak table with dog-eared page, a bus ticket stub as bookmark showing '6월 14일' clearly visible, violet long-coat hem of a female figure glimpsed passing between bookshelves in background, quiet atmosphere",
  'bg_A3_gate_dusk': BASE + " school main gate at dusk, two students walking side by side away from camera into a forking road, one path leading toward distant traffic intersection, long shadows stretched by low setting sun, warm amber backlighting silhouettes, no faces visible",
  # Act 4-B · 재설계 (아리아)
  'bg_B1_sleeve_grab': BASE + " school corridor interior, back view of male student scratching neck with one hand, feminine hand entering frame from the right grabbing his blazer sleeve, warm indirect afternoon light, soft focus on both hands, no faces visible",
  'bg_B2_rose_collision': BASE + " marble hallway in golden sunset, two pairs of student shoes walking together, a third pair of shoes approaching in opposite direction carrying a white rose whose petals are tinged with crimson, the rose falling mid-air about to hit marble floor, shoulder-level partial silhouette contact, dramatic shaft of light through tall windows",
  'bg_B3_fork_petal': BASE + " residential alley at dusk, fork in road between two neighborhoods, male student standing unusually still at the split, one hand raised in a half-wave, single small rose petal clinging to his backpack strap catching the streetlight, warm sodium lamp glow, his shadow stretched long on pavement, no face visible",
  # Act 4-C · 폭로 (니아)
  'bg_C1_bread_down': BASE + " empty hallway beside classroom window, male student's hand placing a piece of bread down on windowsill, his sneakers turned slightly inward in defensive stance, dramatic chiaroscuro lighting shift from golden to overcast, tense stillness in air, no face visible, cinematic charged silence",
  'bg_C2_shutter_flash': BASE + " adjacent school corridor view, camera flash burst reflected in window glass, silhouette of a female student with camera strap and DSLR retreating quickly around a corner, motion blur, candid paparazzi framing, dusk hallway light, no face visible",
  'bg_C3_blurred_seokhyun': BASE + " cinematic close-up of male student face turning to look at viewer, but his face is intentionally out-of-focus with soft depth blur, eyes both focused on viewer and looking past them with an unsettling gravitas, warm window light behind, slight reality-glitch frame tremor at edges",
  # Act 5 · 수렴 (루나)
  'bg_20_four_photos': BASE + " nighttime bedroom desk from above, four developed photographs laid out in a row, photo 1 shows a hand flicking salt on bread, photo 2 shows a fallen white rose on marble, photo 3 shows a reflection in glass, photo 4 is an aerial observer-angle shot of a single figure in a classroom, handwritten pencil note on the back of the fourth photo, warm desk lamp amber glow, beyond the window in distance a tiny figure in white uniform standing on a stone balcony flipping a gold coin",
  'bg_21_desk_sunset': BASE + " same classroom wooden desk as afternoon scene but now at deep sunset, bright orange and crimson ginkgo tree framed through tall window, open notebook with three freshly handwritten Korean lines visible, pencil lying across the page, soft warm lens flare, final cinematic golden hour tone",
}

def gen(name, prompt):
    body = json.dumps({
        "instances":[{"prompt": prompt}],
        "parameters":{"sampleCount":1, "aspectRatio":"16:9"},
    }).encode()
    req = urllib.request.Request(URL, data=body,
        headers={"Content-Type":"application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.loads(r.read().decode())
            for p in d.get('predictions', []):
                img = p.get('bytesBase64Encoded')
                if img:
                    open(f'{name}.png','wb').write(base64.b64decode(img))
                    print(f'[ok] {name}')
                    return
        print(f'[err] {name}: empty predictions')
    except urllib.error.HTTPError as e:
        print(f'[err] {name}: HTTP {e.code} {e.read().decode()[:200]}')
    except Exception as e:
        print(f'[err] {name}: {e}')

# Parallel — 6 at a time
with ThreadPoolExecutor(max_workers=6) as ex:
    list(ex.map(lambda kv: gen(*kv), JOBS.items()))
print('[done]')
