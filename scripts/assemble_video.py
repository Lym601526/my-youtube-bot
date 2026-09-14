    final_output = "output/final_video.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "output/clips/list.txt",
        "-c", "copy",
        final_output
    ], check=True, cwd="output/clips")

    # ننقل الناتج النهائي بره مجلد clips لمكانه الصح
    os.replace("output/clips/final_video.mp4", final_output)
    print(f"\n✅ الفيديو النهائي جاهز: {final_output}")
