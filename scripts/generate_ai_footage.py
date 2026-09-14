import os
import json
import time
from huggingface_hub import InferenceClient
import requests

HF_TOKEN = os.environ.get("HF_API_TOKEN")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

client = InferenceClient(token=HF_TOKEN)

MODELS = [
    "THUDM/CogVideoX-2b",
    "ali-vilab/text-to-video-ms-1.7b",
]

def generate_ai_video(prompt, path, max_retries=2):
    for model in MODELS:
        for attempt in range(max_retries):
            try:
                print(f"محاولة توليد فيديو AI: '{prompt}' بموديل {model}")
                video_bytes = client.text_to_video(prompt, model=model)
                with open(path, "wb") as f:
                    f.write(video_bytes)
                print(f"✅ نجح توليد AI: {path}")
                return True
            except Exception as e:
                print(f"فشلت المحاولة ({model}): {e}")
                time.sleep(5)
    return False

def fallback_pexels(keyword, path):
    headers = {"Authorization": PEXELS_API_KEY}
    url = "https://api.pexels.com/videos/search"
    params = {"query": keyword, "per_page": 1, "orientation": "portrait"}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    results = r.json().get("videos", [])
    if not results:
        return False
    video_files = sorted(results[0]["video_files"], key=lambda v: abs((v.get("height") or 0) - 1280))
    video_url = video_files[0]["link"]
    r = requests.get(video_url, stream=True)
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"↩️ تم استخدام بديل Pexels: {path}")
    return True

def main():
    with open("output/idea.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/footage", exist_ok=True)

    for i, scene in enumerate(data["scenes"]):
        keyword = scene["visual_keyword"]
        path = f"output/footage/scene_{i+1:02d}.mp4"

        success = generate_ai_video(keyword, path)
        if not success:
            print(f"⚠️ فشل التوليد بالذكاء الاصطناعي لـ '{keyword}' - هستخدم Pexels كبديل")
            fallback_pexels(keyword, path)

if __name__ == "__main__":
    main()
