"""v23 · TTS for Story 1 PROLOGUE · ElevenLabs v3 · NEW VOICE IDs.

User feedback in v22:
  - Raon's voice sounded like "a young middle-school girl" → switch voice ID
  - Need DEEP MASCULINE Korean voices for Raon (호위 14년차) and Dex (히트맨)

NEW voices selected from ElevenLabs shared library:
  - Raon: CW8sR0DtVIQaeLyAjGAf · "Premium Korean Baritone"
          young Seoul male · deep, resonant, calm · pro 3-hour clone
  - Dex:  V6IXmZ3a4ixL7ixYPupu · "Steve - Mysterious Horror"
          middle-aged Seoul male · deep, calm, mysterious narrator

Test files written by `_test_voices.py` (raon_test_*.mp3) for A/B compare.
Alternative Raon candidates if Baritone doesn't fit:
  - 7ZVPKvVmVZZERLd1Q6BS  Min-jun (young · deep resonant)
  - mK6Q1HRYYwUJwQGwMPYw  Luca (young · calm serious)
  - ibCGc01503OQd2R6i1n1  Marcus - Baritone Stoic (middle-aged · husky)
  - aQzFKIjVemqRAhfd9est  Midnight Cave (middle-aged · resonant)

Usage:
  ELEVENLABS_API_KEY="..." python _gen_voices.py
"""
import os, json, urllib.request, urllib.error, sys, re
sys.stdout.reconfigure(encoding='utf-8')

KEY = os.environ['ELEVENLABS_API_KEY']
MODEL = "eleven_v3"

# Voice IDs · v23/v26
VOICE_RAON  = "CW8sR0DtVIQaeLyAjGAf"  # Premium Korean Baritone (young · deep · Seoul)
VOICE_DEX   = "V6IXmZ3a4ixL7ixYPupu"  # Steve · Mysterious Horror (deep · calm · narrator)
VOICE_KARLO = "aQzFKIjVemqRAhfd9est"  # Midnight Cave · deep middle-aged baritone (patriarch)

# Settings · low stability + max style forces v3 to honor emotion tags hard
SETTINGS_PEAK = {
  "stability": 0.18, "similarity_boost": 0.92, "style": 1.0, "use_speaker_boost": True,
}
SETTINGS_DEX = {
  "stability": 0.28, "similarity_boost": 0.85, "style": 0.95, "use_speaker_boost": True,
}
SETTINGS_KARLO = {
  "stability": 0.32, "similarity_boost": 0.85, "style": 0.92, "use_speaker_boost": True,
}
SETTINGS_RAON = {
  "stability": 0.40, "similarity_boost": 0.88, "style": 0.78, "use_speaker_boost": True,
}

# Lines · (name, voice_id, settings, text)
LINES = [
  # === v23 PROLOGUE CORE · max dramatic ===
  ("raon_05_run", VOICE_RAON, SETTINGS_PEAK,
    "[BREATHLESS][LUNGS BURNING][adrenaline][hissed shouting through teeth]"
    "뛰어요!! [PANICKED HARSH WHISPER]지금!! [GASPING]지금!!"),
  ("dex_01_surrender", VOICE_DEX, SETTINGS_DEX,
    "[ice cold][slow controlled][low voice][menacing]"
    "…라온. 투항해."),
  ("raon_c2_yeonwoo", VOICE_RAON, SETTINGS_PEAK,
    "[BROKEN VOICE][shaking gasping sob][devastated whisper][trembling]"
    "…연우……… [BARELY AUDIBLE BREATH]연우……"),

  # === v23 REGRESSION FRAME · new lines for the "again" structure ===
  ("raon_00_regret", VOICE_RAON, SETTINGS_PEAK,
    "[BARELY BREATHING][dying whisper][choked][devastated]"
    "…만약 그 때, [GASPING]그 한 마디를 했더라면."),
  ("raon_99_again", VOICE_RAON, SETTINGS_PEAK,
    "[broken whisper][trembling][raw determination]"
    "…또. [HARSH BREATH]또 다시."),

  # === v26 KARLO (the boss / handler) · cold patriarch ===
  ("karlo_01_recognize", VOICE_KARLO, SETTINGS_KARLO,
    "[ICE COLD][slow controlled menace][deep low voice][taunting]"
    "…라온의 그 여자가, [PAUSE][almost amused] 너구나."),

  # === LEGACY · v17–v22 backward compat ===
  ("raon_01_check", VOICE_RAON, SETTINGS_RAON,
    "[low voice][controlled tension][quiet] 연우 씨, [softer] 자리 확인 부탁드려요."),
  ("raon_02_intro", VOICE_RAON, SETTINGS_RAON,
    "[low voice][quiet][professional but tense] 호위 맡은 라온입니다. [firmer][quietly urgent] 지금 일어나지 마세요."),
  ("raon_03_warn", VOICE_RAON, SETTINGS_RAON,
    "[low voice][tense whisper][cautious] 우측 출구 근처에. [pause][harder whisper] 모르는 얼굴 셋."),
  ("raon_04_cmd", VOICE_RAON, SETTINGS_RAON,
    "[low voice][URGENT][hissed][controlled panic] 3초 뒤. [harder] 왼쪽 화장실 방향으로!"),
  ("raon_a1_ok", VOICE_RAON, SETTINGS_RAON,
    "[breathless][concerned][quiet][voice rough] 괜찮아?"),
  ("raon_a2_behind", VOICE_RAON, SETTINGS_RAON,
    "[low voice][protective][gentle but firm] 내 등 뒤에 있어."),
  ("raon_b1_name", VOICE_RAON, SETTINGS_PEAK,
    "[low voice][relieved][quietly broken][choked] 연우…"),
  ("raon_b2_alive", VOICE_RAON, SETTINGS_PEAK,
    "[low voice][soft][broken][almost a sigh][relieved] 죽지 않았네. [quietly][trembling] 그거면 됐어."),
]

def strip_tags(text):
  return re.sub(r"\[[^\]]+\]", "", text).replace("  ", " ").strip()

def gen(name, voice_id, settings, text):
  url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
  body = {
    "text": text if MODEL == "eleven_v3" else strip_tags(text),
    "model_id": MODEL,
    "voice_settings": settings,
  }
  data = json.dumps(body, ensure_ascii=False).encode("utf-8")
  req = urllib.request.Request(url, data=data, method="POST",
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

print(f"[info] model={MODEL} · raon={VOICE_RAON} · dex={VOICE_DEX}")
for name, voice_id, settings, text in LINES:
  gen(name, voice_id, settings, text)
print("[done]")
