"""v16 · Raon 보이스 · ElevenLabs v3 + 감정 태그.

라온 톤: 낮고 건조 · 과묵 · 긴박할 때도 차분 · 집착적 보호
Voice: 먼저 기본 Dogjoy(qSSLFjgzC2qvkt4Uba0s)로 시도 · 너무 어리면 adult male voice ID 교체 필요.
대안 voice IDs (ElevenLabs Library · Korean-capable, male, low):
  - qSSLFjgzC2qvkt4Uba0s  Dogjoy          (calm Korean male · maybe too young)
  - pFZP5JQG7iQjIQuC4Bku  Lily            (female, skip)
  - AZnzlk1XvdvUeBnXmlld  Domi            (female, skip)
  - cgSgspJ2msm6clMCkdW9  Jessica         (female, skip)
  - VR6AewLTigWG4xSOukaG  Arnold          (US adult male · English heavy · test)
Best option to try: Dogjoy with different settings — lower stability, raised style to get harsher delivery.

Usage: ELEVENLABS_API_KEY="..." python _gen_raon_voice.py
"""
import os, json, urllib.request, urllib.error, sys, re
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['ELEVENLABS_API_KEY']

# Try Dogjoy first with adult-harshened settings; if too young, we can swap voice ID.
VOICE_ID = "qSSLFjgzC2qvkt4Uba0s"
MODEL = "eleven_v3"

VOICE_SETTINGS = {
  "stability": 0.55,          # slightly unstable for edge
  "similarity_boost": 0.82,
  "style": 0.55,              # v3 will honor emotion tags more heavily
  "use_speaker_boost": True,
}

LINES = {
  "raon_follow": (
    "[urgent][low voice][controlled whisper] 움직여. "
    "[pause] 지금. "
    "[soft exhale] 내가 뒤에 있어."
  ),
  "raon_autonomy": (
    "[low voice][quiet][tender restraint] 답 없어도 돼. "
    "[pause] 아직 살아 있다는 거. "
    "[softly] 네가 응답 안 읽고 있는 게 증거야. "
    "[almost whispered] 지켜볼게. 잠들어도 돼."
  ),
  # Bonus line for header / loading moment
  "raon_greet": (
    "[low voice][flat] 왜 안 들어. "
    "[harder] 그 골목이었어. "
    "[tense] 지금 너 따라붙은 차."
  ),
}

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def strip_tags_if_v2(text):
  if MODEL == "eleven_multilingual_v2":
    return re.sub(r"\[[^\]]+\]", "", text).replace("  ", " ").strip()
  return text

def gen(name, text):
  body = {
    "text": strip_tags_if_v2(text),
    "model_id": MODEL,
    "voice_settings": VOICE_SETTINGS,
  }
  data = json.dumps(body, ensure_ascii=False).encode("utf-8")
  req = urllib.request.Request(URL, data=data, method="POST",
    headers={
      "xi-api-key": KEY,
      "Content-Type": "application/json; charset=utf-8",
      "Accept": "audio/mpeg",
    })
  try:
    with urllib.request.urlopen(req, timeout=120) as r:
      audio = r.read()
      with open(f"{name}.mp3", "wb") as f:
        f.write(audio)
      print(f"[ok] {name}.mp3 ({len(audio)//1024} KB)")
  except urllib.error.HTTPError as e:
    print(f"[err] {name}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
  except Exception as e:
    print(f"[err] {name}: {e}")

print(f"[info] model={MODEL}  voice={VOICE_ID}")
for name, text in LINES.items():
  gen(name, text)
print("[done]")
