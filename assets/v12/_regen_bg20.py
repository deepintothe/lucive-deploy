"""v15 · bg_20 재생성 · 책상 위 4장의 사진 (중 3장이 흰 국화 1·3·6송이 그려짐).
Usage: GEMINI_API_KEY="..." python _regen_bg20.py
"""
import os, json, base64, urllib.request, urllib.error, sys
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['GEMINI_API_KEY']
# Back to FAST model for style consistency with the other 17 story images.
# Chrysanthemum count accuracy is handled via separate CSS overlays, not by this image.
URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={KEY}"

BASE = (
  "2D anime visual novel cinematic illustration, korean manhwa webtoon pixiv "
  "high quality art style, cel shading, dramatic cinematic lighting, wide 16:9 "
  "composition. Background-focused — character shown only as silhouette or "
  "partial view (back of head, shoulders, arms). Scene: "
)

PROMPT = BASE + (
  "overhead top-down bird's-eye view straight down at a dark wooden desk at night, warm "
  "amber desk lamp glow from one corner. A teenage boy in school uniform stands in front "
  "of the desk (at the bottom edge of the frame) leaning forward with both hands planted "
  "flat on the desk — we see only the top of his back-of-head, shoulders, and arms "
  "reaching forward onto the desk, hands spread naturally. No face, no chair, no legs. "

  "Scattered all over the desk surface are about 25 small illustrated photograph prints, "
  "rotated at random angles, overlapping loosely. The photos are a MIX of different "
  "genres — NOT just portraits. Include a wide variety of cinematic scene types from "
  "a korean teen mystery webtoon: "
  " • atmospheric LOCATION shots (a rainy city intersection with neon bleeding into "
  "   puddles, an empty hospital corridor at dawn, a school gate at dusk with long "
  "   shadows, a dark residential alley with a fork in the road, a library aisle with "
  "   amber light through tall windows, a rooftop at golden hour, a bus stop under a "
  "   streetlamp, a classroom window with ginkgo tree shadow); "
  " • extreme MACRO / detail shots (a cracked antique pocket watch with hands turning "
  "   backward, a single rose petal falling onto marble floor, a camera flash reflected "
  "   in a window pane, a piece of bread placed on a windowsill, salt crystals on a "
  "   cafeteria table); "
  " • partial-view CHARACTER shots (a silhouette at a backlit doorway, a hand grabbing "
  "   a school blazer sleeve, two students walking down a corridor from behind, a "
  "   half-blurred male face turning toward viewer, two pairs of student shoes on "
  "   marble, a hand placing something on a desk); "
  " • a few ambient CONVERSATION shots (two students at a cafeteria booth, figures in "
  "   a classroom at sunset). "
  "Mix these freely — roughly one third locations, one third detail/macro shots, one "
  "third partial character shots. AVOID filling the desk with only portraits. "

  "All photos in cel-shaded korean manhwa webtoon panel style. The desk contains ONLY "
  "photos — no phones, no notebooks sitting on the desk, no flowers, no clutter. "
  "Melancholic quiet mood, unified korean manhwa webtoon cel-shaded illustration style."
)

def gen():
    body = json.dumps({
        "instances":[{"prompt": PROMPT}],
        "parameters":{"sampleCount":1, "aspectRatio":"16:9"},
    }).encode()
    req = urllib.request.Request(URL, data=body,
        headers={"Content-Type":"application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode())
            for p in d.get('predictions', []):
                img = p.get('bytesBase64Encoded')
                if img:
                    open('bg_20_four_photos.png','wb').write(base64.b64decode(img))
                    print('[ok] bg_20_four_photos.png regenerated')
                    return
        print('[err] empty predictions')
    except urllib.error.HTTPError as e:
        print(f'[err] HTTP {e.code} {e.read().decode()[:400]}')
    except Exception as e:
        print(f'[err] {e}')

gen()
