import os
import json
import asyncio
import edge_tts

VOICE = "ar-EG-ShakirNeural"

async def synthesize(text, path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)

async def run_all():
    with open("output/idea.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/audio", exist_ok=True)

    for i, scene in enumerate(data["scenes"]):
        path = f"output/audio/scene_{i+1:02d}.mp3"
        await synthesize(scene["voice_text"], path)
        print(f"تم إنشاء: {path}")

    cta_path = "output/audio/cta.mp3"
    await synthesize(data["cta_text"], cta_path)
    print(f"تم إنشاء: {cta_path}")

if __name__ == "__main__":
    asyncio.run(run_all())
