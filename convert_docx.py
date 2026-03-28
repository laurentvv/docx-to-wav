import os
import glob
import subprocess
import logging
import yaml
import soundfile as sf
import numpy as np
from docx import Document
from kokoro import KPipeline

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_ffmpeg():
    """Vérifie que ffmpeg est installé et accessible dans le PATH."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("ffmpeg n'est pas installé ou non trouvé dans PATH")


def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_text_from_docx(docx_path):
    logger.info(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        # Ignorer les paragraphes vides
        if text:
            paragraphs.append(text)
    return paragraphs

def process_document(docx_path, output_dir, pipeline, voice, speed=1.0, sample_rate=24000):
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    wav_path = os.path.join(output_dir, f"{base_name}.wav")
    mp3_path = os.path.join(output_dir, f"{base_name}.mp3")

    paragraphs = extract_text_from_docx(docx_path)
    if not paragraphs:
        logger.warning(f"Le document {docx_path} est vide ou ne contient pas de texte lisible. Ignoré.")
        return

    logger.info(f"{len(paragraphs)} paragraphes trouvés. Début de la synthèse vocale...")

    all_audio_chunks = []

    # Pause courte entre les paragraphes (0.5 seconde de silence)
    pause_duration = 0.5
    silence = np.zeros(int(sample_rate * pause_duration), dtype=np.float32)

    for i, paragraph in enumerate(paragraphs):
        logger.info(f"Traitement du paragraphe {i+1}/{len(paragraphs)}...")

        try:
            # Kokoro generator
            generator = pipeline(
                paragraph, voice=voice,
                speed=speed, split_pattern=r'\n+'
            )

            for _, _, audio in generator:
                if audio is not None:
                    # Ajouter l'audio généré
                    all_audio_chunks.append(audio)

            # Ajouter une pause après chaque paragraphe (sauf le dernier)
            if i < len(paragraphs) - 1:
                all_audio_chunks.append(silence)

        except Exception as e:
            logger.error(f"Erreur lors du traitement du paragraphe {i+1} : {e}")

    if not all_audio_chunks:
        logger.warning(f"Aucun audio généré pour {docx_path}.")
        return

    logger.info("Concaténation des extraits audio...")
    final_audio = np.concatenate(all_audio_chunks)

    logger.info("Sauvegarde du fichier temporaire WAV...")
    sf.write(wav_path, final_audio, sample_rate)

    logger.info(f"Conversion en MP3 : {mp3_path}...")
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', wav_path,
            '-codec:a', 'libmp3lame', '-qscale:a', '2',
            '-loglevel', 'error', mp3_path
        ], check=True)
        logger.info("Conversion MP3 réussie !")

        # Supprimer le fichier WAV temporaire
        if os.path.exists(wav_path):
            os.remove(wav_path)
            logger.info("Fichier WAV temporaire supprimé.")

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Erreur lors de la conversion ffmpeg : {e}")

def main():
    # Vérifier que ffmpeg est disponible
    try:
        check_ffmpeg()
    except RuntimeError as e:
        logger.error(f"{e}")
        logger.info("Installez ffmpeg: https://ffmpeg.org/download.html")
        return

    config = load_config()
    input_dir = config.get("input_dir", "input_docs")
    output_dir = config.get("output_dir", "output_audio")
    voice = config.get("voice", "ff_siwis")
    speed = config.get("speed", 1.0)
    sample_rate = config.get("sample_rate", 24000)

    # Création des dossiers si nécessaires
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Récupérer tous les fichiers .docx
    search_pattern = os.path.join(input_dir, "*.docx")
    docx_files = glob.glob(search_pattern)

    if not docx_files:
        logger.warning(f"Aucun fichier .docx trouvé dans le dossier '{input_dir}'.")
        return

    logger.info(f"Initialisation de Kokoro avec la voix : {voice}")
    try:
        pipeline = KPipeline(lang_code='f')
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du pipeline Kokoro : {e}")
        return

    logger.info(f"{len(docx_files)} fichier(s) à traiter.")

    for docx_file in docx_files:
        logger.info(f"--- Traitement de : {docx_file} ---")
        process_document(
            docx_path=docx_file,
            output_dir=output_dir,
            pipeline=pipeline,
            voice=voice,
            speed=speed,
            sample_rate=sample_rate
        )

    logger.info("Terminé ! Tous les fichiers ont été traités.")

if __name__ == "__main__":
    main()
