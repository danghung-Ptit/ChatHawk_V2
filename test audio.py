import whisper

model = whisper.load_model("medium")
result = model.transcribe("demo_wav_1.mp3")
print(result["text"])