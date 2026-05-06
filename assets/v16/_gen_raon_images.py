"""v16 · Raon (Moonlight Cartel) 이미지 · Imagen 4 Fast · manhwa/webtoon cel-shaded.
Usage: GEMINI_API_KEY="..." python _gen_raon_images.py
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
  # Profile portrait (avatar + header) — Raon as bodyguard assassin
  'raon_profile': BASE + (
    "close-up portrait of a korean teenage boy, late teens, bodyguard assassin for a "
    "mafia family heir. Black tailored suit jacket, simple black button shirt, skinny "
    "black tie loose at the neck. Short black hair, sharp cold eyes with quiet "
    "intensity, neutral pokerface expression hiding calculation. Small clear earpiece "
    "visible in one ear with a curl of cable disappearing behind collar. Subtle scar on "
    "one cheekbone. Moody noir low-key lighting from above, background out of focus dark "
    "alley or underground club ambient with faint amber neon bokeh. Looking slightly off "
    "camera as if scanning a threat. Head and shoulders composition, centered, square "
    "1:1 framing. Dangerous calm."
  ),
  # S4 attachment — blurred car in mirror
  'raon_mirror_shot': BASE + (
    "low-angle candid cellphone camera photo effect, looking into a streaked rainy "
    "side mirror of a car parked in a dark back alley at night. In the mirror reflection, "
    "two unmarked dark sedans are visible behind with their headlights off, parked too "
    "close, suggesting they are tailing. Neon signs in the distance bleed red and amber "
    "reflections on wet pavement. Raindrops on the mirror surface distort the image, "
    "slight motion blur. No people visible. Sense of quiet dread. Shot feels like a "
    "warning someone sent you. Wide 16:9."
  ),
  # S7 attachment — bloody gloved hand
  'raon_gloved_hand': BASE + (
    "extreme macro close-up of a man's black leather gloved hand resting on a dark "
    "concrete floor of an underground parking lot. Faint crimson blood smears on the "
    "knuckles and one fingertip, droplets beading on the leather. Cold bluish moonlight "
    "from off-frame blends with a single warm amber tungsten lamp, creating dramatic "
    "chiaroscuro. Hand is relaxed, palm down, as if the person is kneeling. No face, no "
    "body — just the hand and floor. Wide 16:9 composition. Noir atmosphere, melancholic "
    "aftermath mood, not gore — implied violence."
  ),
  # Optional: ambient BG for the chat UI (cartel underground vibe)
  'raon_bg_ambient': BASE + (
    "wide atmospheric background shot of an empty underground parking garage at night, "
    "warm amber sodium lamps overhead creating pools of light, concrete columns receding "
    "in perspective, one distant figure silhouetted walking away at the far end, puddles "
    "on the ground reflecting lights, subtle rain haze, cinematic shallow depth of field "
    "with heavy bokeh, 16:9. No characters in foreground. Melancholic quiet tension, "
    "korean noir manhwa aesthetic."
  ),
}

def gen(name, prompt):
    aspect = "1:1" if name == "raon_profile" else "16:9"
    body = json.dumps({
        "instances":[{"prompt": prompt}],
        "parameters":{"sampleCount":1, "aspectRatio":aspect},
    }).encode()
    req = urllib.request.Request(URL, data=body,
        headers={"Content-Type":"application/json"}, method="POST")
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

with ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(lambda kv: gen(*kv), JOBS.items()))
print('[done]')
