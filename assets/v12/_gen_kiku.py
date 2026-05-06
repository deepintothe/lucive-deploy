"""v15 · 국화 사진 3장 개별 생성 · 톤앤매너 맞추기 위해 Fast 모델 + 동일 BASE 사용.
Each image is generated independently with a very short, simple prompt so the
model can focus on ONE thing: drawing the correct flower count.
Usage: GEMINI_API_KEY="..." python _gen_kiku.py
"""
import os, json, base64, urllib.request, urllib.error, sys
from concurrent.futures import ThreadPoolExecutor
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['GEMINI_API_KEY']
URL = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={KEY}"

BASE = (
  "2D anime visual novel cinematic illustration, korean manhwa webtoon pixiv "
  "high quality art style, cel shading, dramatic cinematic lighting. Scene: "
)

JOBS = {
  # Square aspect, simple, concrete count instruction per image.
  'kiku_1': BASE + (
    "a single photograph print showing exactly ONE large white chrysanthemum flower "
    "centered on a dark ink background. Just one flower alone, no other plants, no "
    "people. White petals rendered in delicate cel-shaded ink illustration. Square "
    "composition. Funeral / memorial mood."
  ),
  'kiku_3': BASE + (
    "a photograph print showing exactly THREE white chrysanthemum flowers grouped "
    "together as a small bouquet, stems tied with string, arranged in a triangular "
    "cluster on a dark ink background. Three flower heads total, no more no less, no "
    "other plants, no people. White petals in delicate cel-shaded ink illustration. "
    "Square composition. Funeral bouquet mood."
  ),
  'kiku_6': BASE + (
    "a photograph print showing exactly SIX white chrysanthemum flowers grouped "
    "together as a dense funeral bouquet, stems bound with a black ribbon, arranged "
    "in a full spray fanning outward on a dark ink background. Six flower heads total, "
    "no more no less, no other plants, no people. White petals in delicate cel-shaded "
    "ink illustration. Square composition. Heavy funeral bouquet mood."
  ),
}

def gen(name, prompt):
    body = json.dumps({
        "instances":[{"prompt": prompt}],
        "parameters":{"sampleCount":1, "aspectRatio":"1:1"},
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
                    open(f'{name}.png','wb').write(base64.b64decode(img))
                    print(f'[ok] {name}.png')
                    return
        print(f'[err] {name}: empty predictions')
    except urllib.error.HTTPError as e:
        print(f'[err] {name}: HTTP {e.code} {e.read().decode()[:300]}')
    except Exception as e:
        print(f'[err] {name}: {e}')

with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(lambda kv: gen(*kv), JOBS.items()))
print('[done]')
