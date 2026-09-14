import os
import json
import requests

API_KEY = os.environ["PEXELS_API_KEY"]
HEADERS = {"Authorization": API_KEY}

def search_video(keyword):
    url = "https://api.pexels.com/videos/search"
    params = {"query": keyword, "per_page": 1, "orientation": "portrait"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    results = r.json().get("videos", [])
    if not results:
        return None
    video_files = results[0]["video_files"]
    # اختار أقرب جودة لـ 720p عشان الحجم يفضل معقول
    video_files = sorted(video_files, key=lambda v: abs((v.get("height") or 0) - 1280))
    return video_files[0]["link"]

def download(url, path):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def main():
    with open("output/idea.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/footage", exist_ok=True)

    for i, scene in enumerate(data["scenes"]):
        keyword = scene["visual_keyword"]
        path = f"output/footage/scene_{i+1:02d}.mp4"
        video_url = search_video(keyword)
        if video_url:
            download(video_url, path)
            print(f"تم تحميل: {path} ({keyword})")
        else:
            print(f"تحذير: ما لقيتش فيديو لـ '{keyword}' - هستخدم بديل")
            fallback_url = search_video("abstract background")
            if fallback_url:
                download(fallback_url, path)

if __name__ == "__main__":
    main()
