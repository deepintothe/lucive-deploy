"""v15 · 석현 보이스 재생성 · ElevenLabs v3 + 감정 태그.

ElevenLabs v3 (eleven_v3) supports inline audio tags in square brackets to express
emotion and delivery. We wrap each Seokhyun line with intent-specific tags:
  [friendly][curious] · [suspicious][quiet] · [surprised][bright] · [serious][low] · [dazed][hushed]

Usage:
  ELEVENLABS_API_KEY="..." python _regen_seokhyun_v3.py

If eleven_v3 is not yet available on your account, set MODEL = "eleven_multilingual_v2"
and tags will be dropped by the older engine. The text itself still reads naturally.
"""
import os, json, urllib.request, urllib.error, sys, re
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['ELEVENLABS_API_KEY']
VOICE_ID = "qSSLFjgzC2qvkt4Uba0s"  # Dogjoy — calm Korean male
MODEL = "eleven_v3"  # fallback: "eleven_multilingual_v2"

# Text prefixed with v3 emotion tags. v3 accepts both English and Korean cues.
LINES = {
  "seokhyun_01_what": (
    "[friendly][slight smile] 뭐야? "
    "[curious][softly] 어제 왜 일찍 나갔어?"
  ),
  "seokhyun_A_suspicious": (
    "[suspicious][quietly]… 너 요즘 뭐 있어? "
    "[narrowed eyes] 말 안 하는 척 하는 거 다 티나, "
    "[teasing] 그거 알지?"
  ),
  "seokhyun_B_surprised": (
    "[surprised][laughing] 오늘 왜 이래? "
    "[excited] 진짜 밥 사줄 거야? "
    "[warm smile] 좋아. "
    "[pouting playfully] 어제 너 먼저 가서 내가 얼마나 심심했는데."
  ),
  "seokhyun_C_serious": (
    "[serious][low voice]… 무섭다고? "
    "[confused][hurt] 나랑 있는 게? "
    "[pause][gentle]… 야, 말해봐. "
    "[worried] 무슨 꿈 꿨어?"
  ),
  "seokhyun_C_dream": (
    "[dazed][hushed]… 야. "
    "[reluctant][softly] 솔직히 나도, 요즘 자꾸 이상한 꿈 꿔. "
    "[trailing off]… 우리, 이 대화 나중에 다시 해."
  ),
}

# v3 generates voice settings slightly differently; these are safe defaults.
VOICE_SETTINGS = {
  "stability": 0.68,
  "similarity_boost": 0.85,
  "style": 0.35,          # v3 respects emotion tags more when style > 0
  "use_speaker_boost": True,
}

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def strip_tags_if_v2(text):
  # If falling back to v2, strip [tags] so they aren't read aloud.
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
  req = urllib.request.Request(
    URL, data=data, method="POST",
    headers={
      "xi-api-key": KEY,
      "Content-Type": "application/json; charset=utf-8",
      "Accept": "audio/mpeg",
    }
  )
  try:
    with urllib.request.urlopen(req, timeout=120) as r:
      audio = r.read()
      with open(f"{name}.mp3", "wb") as f:
        f.write(audio)
      print(f"[ok] {name}.mp3 ({len(audio)//1024} KB)")
  except urllib.error.HTTPError as e:
    msg = e.read().decode(errors="replace")[:400]
    print(f"[err] {name}: HTTP {e.code} {msg}")
    if 'eleven_v3' in msg and 'not found' in msg.lower():
      print("  \u21aa v3 not available \u2014 edit MODEL = 'eleven_multilingual_v2' and re-run.")
  except Exception as e:
    print(f"[err] {name}: {e}")

print(f"[info] model={MODEL}  voice=Dogjoy")
for name, text in LINES.items():
  gen(name, text)
print("[done]")
