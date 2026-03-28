import os

filepath = 'tts_project/test_voices.py'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the list of voices with the actual French voices (ff_ and fm_)
new_voices = "[ 'ff_siwis', 'fm_siwis' ] # Example of native French voices. Check Kokoro documentation for more."
content = content.replace(
    "['af_alloy', 'af_aoede', 'af_bella', 'af_jessica', 'af_kore', 'af_nicole', 'af_nova', 'af_river', 'af_sarah', 'af_sky', 'am_adam', 'am_echo', 'am_eric', 'am_fenrir', 'am_liam', 'am_michael', 'am_onyx', 'am_puck', 'am_santa']",
    new_voices
)

with open(filepath, 'w') as f:
    f.write(content)
