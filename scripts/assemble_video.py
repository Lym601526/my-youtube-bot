import os
import json
import subprocess

def get_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def main():
    with open("output/idea.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/clips", exist_ok=True)
    clip_list = []

    for i in range(len(data["scenes"])):
        idx = f"{i+1:02d}"
        video_in = f"output/footage/scene_{idx}.mp4"
        audio_in = f"output/audio/scene_{idx}.mp3"
        caption_in = f"output/captions/scene_{idx}.ass"
        clip_out = f"output/clips/clip_{idx}.mp4"

        if not os.path.exists(video_in) or not os.path.exists(audio_in):
            print(f"تخطي المشهد {idx} - ملف ناقص")
            continue

        audio_duration = get_duration(audio_in)

        vf_filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        if os.path.exists(caption_in):
            vf_filter += f",subtitles={caption_in}"

        subprocess.run([
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", video_in,
            "-i", audio_in,
            "-t", str(audio_duration),
            "-vf", vf_filter,
            "-c:v", "libx264", "-c:a", "aac",
            "-map", "0:v:0", "-map", "1:a:0",
            clip_out
        ], check=True)

        clip_list.append(clip_out)
        print(f"تم تجميع: {clip_out}")

    with open("output/clips/list.txt", "w") as f:
        for clip in clip_list:
            f.write(f"file '{os.path.basename(clip)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "list.txt",
        "-c", "copy",
        "final_video.mp4"
    ], check=True, cwd="output/clips")

    final_output = "output/final_video.mp4"
    os.replace("output/clips/final_video.mp4", final_output)
    print(f"\n✅ الفيديو النهائي جاهز: {final_output}")

if __name__ == "__main__":
    main()
