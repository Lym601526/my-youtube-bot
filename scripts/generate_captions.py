import os
import json
from faster_whisper import WhisperModel

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,110,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,0,2,60,60,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def build_ass(words):
    lines = [ASS_HEADER]
    for w in words:
        start = format_ass_time(w["start"])
        end = format_ass_time(w["end"])
        text = w["word"].strip()
        if not text:
            continue
        lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
    return "\n".join(lines)

def main():
    print("جاري تحميل نموذج التفريغ الصوتي (مرة واحدة)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")

    with open("output/idea.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs("output/captions", exist_ok=True)

    for i in range(len(data["scenes"])):
        idx = f"{i+1:02d}"
        audio_path = f"output/audio/scene_{idx}.mp3"
        if not os.path.exists(audio_path):
            continue

        segments, _ = model.transcribe(audio_path, word_timestamps=True, language="ar")

        words = []
        for segment in segments:
            for word in segment.words:
                words.append({"word": word.word, "start": word.start, "end": word.end})

        ass_content = build_ass(words)
        ass_path = f"output/captions/scene_{idx}.ass"
        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_content)

        print(f"تم إنشاء ترجمة: {ass_path} ({len(words)} كلمة)")

if __name__ == "__main__":
    main()
