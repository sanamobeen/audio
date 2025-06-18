import subprocess
import os


def apply_voice_effect(file_path, effect):
    effected_path = file_path.replace(".mp3", "_effected.mp3")

    if effect == "kids":
        command = [
            "ffmpeg",
            "-y",
            "-i",
            file_path,
            "-filter:a",
            "asetrate=44100*1.6,aresample=44100",
            effected_path,
        ]
    elif effect == "male":
        command = [
            "ffmpeg",
            "-y",
            "-i",
            file_path,
            "-filter:a",
            "asetrate=44100*0.8,aresample=44100",
            effected_path,
        ]
    elif effect == "female":
        command = [
            "ffmpeg",
            "-y",
            "-i",
            file_path,
            "-filter:a",
            "asetrate=44100*1.2,aresample=44100",
            effected_path,
        ]
    else:
        raise ValueError("Unsupported effect")

    subprocess.run(command, check=True)

    return effected_path
