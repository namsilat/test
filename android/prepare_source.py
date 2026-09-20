import base64
import hashlib
import json
import math
import re
import struct
import wave
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS_DIR = Path(__file__).resolve().parent / "source_chunks"
EXPECTED_SHA256 = "3ca29d9d676c3c0761123da8dad16befddeb8c6e6e573aa00b3e87f7b64504fe"

chunk_files = sorted(CHUNKS_DIR.glob("*.txt"))
if not chunk_files:
    raise SystemExit(f"No source chunks found in {CHUNKS_DIR}")

payload = "".join(p.read_text(encoding="ascii").strip() for p in chunk_files)
source_bytes = zlib.decompress(base64.b64decode(payload))
actual_sha256 = hashlib.sha256(source_bytes).hexdigest()
if actual_sha256 != EXPECTED_SHA256:
    raise SystemExit(
        f"Reconstructed main.py checksum mismatch: {actual_sha256} != {EXPECTED_SHA256}"
    )

(ROOT / "main.py").write_bytes(source_bytes)

labels = {
    "mappings": [
        {"contains":"Playstation 3","label":"PlayStation 3","background":"#002AFF","text":"#FFFFFF"},
        {"contains":"Playstation 2","label":"PlayStation 2","background":"#2D5FBA","text":"#FFFFFF"},
        {"contains":"Playstation 4","label":"PlayStation 4","background":"#3C7CF0","text":"#FFFFFF"},
        {"contains":"PSP","label":"PSP","background":"#2D5FBA","text":"#FFFFFF"},
        {"contains":"Nintendo DS","label":"Nintendo DS","background":"#DA3F6B","text":"#171717"},
        {"contains":"Nintendo Wii","label":"Wii","background":"#FFFFFF","text":"#CB1010"},
        {"contains":"XBOX 360","label":"XBOX 360","background":"#55AF13","text":"#FFFFFF"},
        {"contains":"XBOX ONE","label":"XBOX ONE","background":"#79C541","text":"#FFFFFF"},
        {"contains":"ПК","label":"PC","background":"#F3EB8E","text":"#000000"},
        {"contains":"Blu-ray","label":"Blu-ray","background":"#00A2FF","text":"#000000"},
        {"contains":"DVD","label":"DVD","background":"#83D9C0","text":"#000000"},
        {"contains":"картки","label":"Картка","background":"#DE7BFF","text":"#FFFFFF"},
        {"contains":"фігурка","label":"Фігурка","background":"#DE7BFF","text":"#FFFFFF"},
        {"contains":"Стартовий набір","label":"Набір","background":"#eeeeee","text":"#000000"},
    ]
}
(ROOT / "Settings").mkdir(exist_ok=True)
(ROOT / "Settings" / "labels.json").write_text(
    json.dumps(labels, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

source = source_bytes.decode("utf-8")
sound_files = sorted(set(re.findall(r"Sounds/([A-Za-z0-9_\\-]+\\.wav)", source)))
sounds_dir = ROOT / "Sounds"
sounds_dir.mkdir(exist_ok=True)
sample_rate = 22050

for idx, name in enumerate(sound_files):
    path = sounds_dir / name
    duration = 0.32
    count = int(sample_rate * duration)
    frequency = 420 + (idx * 73) % 1100
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for i in range(count):
            t = i / sample_rate
            env = min(1.0, t / 0.015) * min(1.0, (duration - t) / 0.05)
            value = int(9000 * env * math.sin(2 * math.pi * frequency * t))
            wf.writeframesraw(struct.pack("<h", value))

print(f"prepared main.py ({len(source_bytes)} bytes), {len(sound_files)} sounds")
