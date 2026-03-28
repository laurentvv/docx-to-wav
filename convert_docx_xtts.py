import os

import glob
import subprocess
import yaml
import soundfile as sf
import numpy as np
from docx import Document
import torch

# Fix for weight_only PyTorch 2.6 issue
try:
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig
    torch.serialization.add_safe_globals([XttsConfig, XttsArgs, XttsAudioConfig])
except ImportError:
    pass

import warnings
warnings.filterwarnings('ignore')
# Monkey patch torch.load to ignore weights_only=True errors temporarily
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# Auto-accept Coqui's license by mocking input, or by setting the environment variable
os.environ["COQUI_TOS_AGREED"] = "1"

from TTS.api import TTS

def load_config(config_path="config_xtts.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_text_from_docx(docx_path):
    print(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        # Ignorer les paragraphes vides
        if text:
            paragraphs.append(text)
    return paragraphs

def process_document(docx_path, output_dir, tts, voice, language="fr"):
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    wav_path = os.path.join(output_dir, f"{base_name}.wav")
    mp3_path = os.path.join(output_dir, f"{base_name}.mp3")

    paragraphs = extract_text_from_docx(docx_path)
    if not paragraphs:
        print(f"  -> Le document {docx_path} est vide ou ne contient pas de texte lisible. Ignoré.")
        return

    print(f"  -> {len(paragraphs)} paragraphes trouvés. Début de la synthèse vocale XTTS v2...")

    all_audio_chunks = []

    # XTTS v2 generates audio at 24kHz
    sample_rate = 24000
    # Pause courte entre les paragraphes (par exemple, 0.5 seconde de silence à 24kHz)
    pause_duration = 0.5
    silence = np.zeros(int(sample_rate * pause_duration), dtype=np.float32)

    for i, paragraph in enumerate(paragraphs):
        print(f"     Traitement du paragraphe {i+1}/{len(paragraphs)}...")

        try:
            # XTTS api generation
            wav = tts.tts(text=paragraph, speaker=voice, language=language)

            if wav is not None:
                # Add generated audio
                all_audio_chunks.append(np.array(wav, dtype=np.float32))

                # Ajouter une pause après chaque paragraphe (sauf le dernier)
                if i < len(paragraphs) - 1:
                    all_audio_chunks.append(silence)

        except Exception as e:
            print(f"     Erreur lors du traitement du paragraphe {i+1} : {e}")

    if not all_audio_chunks:
        print(f"  -> Aucun audio généré pour {docx_path}.")
        return

    print("  -> Concaténation des extraits audio...")
    final_audio = np.concatenate(all_audio_chunks)

    print("  -> Sauvegarde du fichier temporaire WAV...")
    sf.write(wav_path, final_audio, sample_rate)

    print(f"  -> Conversion en MP3 : {mp3_path}...")
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', wav_path,
            '-codec:a', 'libmp3lame', '-qscale:a', '2',
            '-loglevel', 'error', mp3_path
        ], check=True)
        print("  -> Conversion MP3 réussie !")

        # Supprimer le fichier WAV temporaire
        if os.path.exists(wav_path):
            os.remove(wav_path)
            print("  -> Fichier WAV temporaire supprimé.")

    except subprocess.CalledProcessError as e:
        print(f"  -> Erreur lors de la conversion ffmpeg : {e}")
    except Exception as e:
        print(f"  -> Erreur générale lors de la conversion ffmpeg : {e}")


def main():
    config_file = "config_xtts.yaml"
    if not os.path.exists(config_file):
        print(f"Fichier {config_file} introuvable, utilisation des paramètres par défaut.")
        config = {}
    else:
        config = load_config(config_file)

    input_dir = config.get("input_dir", "input_docs")
    output_dir = config.get("output_dir", "output_audio")
    voice = config.get("voice", "Claribel Dervla") # Use one of the voices tested
    language = config.get("language", "fr")

    # Création des dossiers si nécessaires
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Récupérer tous les fichiers .docx
    search_pattern = os.path.join(input_dir, "*.docx")
    docx_files = glob.glob(search_pattern)

    if not docx_files:
        print(f"Aucun fichier .docx trouvé dans le dossier '{input_dir}'.")
        return

    print(f"Initialisation de XTTS v2 avec la voix : {voice}")
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    except Exception as e:
        print(f"Erreur lors de l'initialisation du pipeline XTTS v2 : {e}")
        return

    print(f"{len(docx_files)} fichier(s) à traiter.")

    for docx_file in docx_files:
        print(f"\n--- Traitement de : {docx_file} ---")
        process_document(
            docx_path=docx_file,
            output_dir=output_dir,
            tts=tts,
            voice=voice,
            language=language
        )

    print("\nTerminé ! Tous les fichiers ont été traités.")

if __name__ == "__main__":
    main()
