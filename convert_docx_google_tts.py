#!/usr/bin/env python3
"""
Script de conversion de documents Word (.docx) en fichiers audio MP3
en utilisant Google Cloud Text-to-Speech.

Usage:
    python convert_docx_google_tts.py

Configuration:
    Modifiez le fichier config_google_tts.yaml pour changer la voix ou les dossiers.
    
Prérequis:
    1. Installer: pip install google-cloud-texttospeech
    2. Configurer les credentials: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
"""

import os
import sys
import glob
import logging
import yaml
import subprocess
import soundfile as sf
import numpy as np

from utils import check_google_credentials, extract_text_from_docx

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from google.cloud import texttospeech
except ImportError:
    logger.error("google-cloud-texttospeech n'est pas installé.")
    logger.info("Installez-le avec: pip install google-cloud-texttospeech")
    exit(1)


def load_config(config_path="config_google_tts.yaml"):
    """Charge la configuration depuis le fichier YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def synthesize_text(client, text, voice_name, speaking_rate=1.0, pitch=0.0):
    """
    Synthétise un texte en audio avec Google Cloud TTS.
    
    Args:
        client: Client Google Cloud TTS
        text: Texte à synthétiser
        voice_name: Nom de la voix (ex: fr-FR-Neural2-A)
        speaking_rate: Vitesse de parole (0.25 à 4.0)
        pitch: Ton (-20.0 à 20.0)
        
    Returns:
        Contenu audio en bytes (LINEAR16/WAV)
    """
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name=voice_name
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response.audio_content



def check_ffmpeg():
    """Vérifie que ffmpeg est installé et accessible dans le PATH."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("ffmpeg n'est pas installé ou non trouvé dans PATH")

def concatenate_wav_files(wav_files: list, output_wav_path: str, output_mp3_path: str):
    """
    Concatène plusieurs fichiers WAV en ajoutant un silence,
    puis convertit le résultat en MP3 avec ffmpeg.
    
    Args:
        wav_files: Liste de chemins vers les fichiers WAV
        output_wav_path: Chemin du fichier de sortie WAV temporaire
        output_mp3_path: Chemin du fichier de sortie MP3 final
    """
    all_audio_chunks = []
    sample_rate = 24000 # Google Cloud TTS LINEAR16 default is 24kHz

    # Pause courte entre les paragraphes (0.5 seconde de silence)
    pause_duration = 0.5

    for i, wav_file in enumerate(wav_files):
        # Lire le fichier WAV
        data, sr = sf.read(wav_file)
        sample_rate = sr # Mettre à jour avec le vrai sample_rate
        all_audio_chunks.append(data)

        # Ajouter un silence après chaque paragraphe (sauf le dernier)
        if i < len(wav_files) - 1:
            silence = np.zeros(int(sample_rate * pause_duration), dtype=data.dtype)
            all_audio_chunks.append(silence)

    logger.info("Concaténation des extraits audio...")
    final_audio = np.concatenate(all_audio_chunks)

    logger.info("Sauvegarde du fichier temporaire WAV...")
    sf.write(output_wav_path, final_audio, sample_rate)

    logger.info(f"Conversion en MP3 : {output_mp3_path}...")
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', output_wav_path,
            '-codec:a', 'libmp3lame', '-qscale:a', '2',
            '-loglevel', 'error', output_mp3_path
        ], check=True)
        logger.info("Conversion MP3 réussie !")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Erreur lors de la conversion ffmpeg : {e}")


def process_document(client, docx_path, output_dir, voice_name, speaking_rate=1.0, pitch=0.0):
    """Traite un document Word et génère le fichier audio MP3."""
    import tempfile
    
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    mp3_path = os.path.join(output_dir, f"{base_name}.mp3")

    paragraphs = extract_text_from_docx(docx_path)
    if not paragraphs:
        logger.warning(f"Le document {docx_path} est vide ou ne contient pas de texte lisible. Ignoré.")
        return

    logger.info(f"{len(paragraphs)} paragraphes trouvés. Début de la synthèse vocale...")

    # Dossier temporaire pour les fichiers MP3 de chaque paragraphe
    temp_dir = tempfile.mkdtemp(prefix="google_tts_")
    wav_files = []
    wav_path = mp3_path.replace('.mp3', '.wav')

    try:
        for i, paragraph in enumerate(paragraphs):
            logger.info(f"Traitement du paragraphe {i+1}/{len(paragraphs)}...")
            
            temp_wav = os.path.join(temp_dir, f"paragraph_{i:04d}.wav")
            
            try:
                # Générer l'audio avec Google TTS
                audio_content = synthesize_text(
                    client, paragraph, voice_name, speaking_rate, pitch
                )
                
                with open(temp_wav, "wb") as f:
                    f.write(audio_content)
                wav_files.append(temp_wav)
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement du paragraphe {i+1} : {e}")

        if not wav_files:
            logger.warning(f"Aucun audio généré pour {docx_path}.")
            return

        logger.info("Concaténation des extraits audio...")
        concatenate_wav_files(wav_files, wav_path, mp3_path)
        logger.info(f"Fichier sauvegardé: {mp3_path}")

    finally:
        # Nettoyer les fichiers temporaires
        for f in wav_files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        try:
            os.rmdir(temp_dir)
        except OSError as e:
            logger.warning(f"Impossible de supprimer {temp_dir}: {e}")



def main():
    """Fonction principale."""
    # Vérifier que ffmpeg est disponible
    try:
        check_ffmpeg()
    except RuntimeError as e:
        logger.error(f"{e}")
        logger.info("Installez ffmpeg: https://ffmpeg.org/download.html")
        return
    # Vérifier les credentials
    if not check_google_credentials():
        return
    
    config = load_config()
    input_dir = config.get("input_dir", "input_docs")
    output_dir = config.get("output_dir", "output_audio")
    voice_name = config.get("voice_name", "fr-FR-Neural2-A")
    speaking_rate = config.get("speaking_rate", 1.0)
    pitch = config.get("pitch", 0.0)

    # Création des dossiers si nécessaires
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Récupérer tous les fichiers .docx
    search_pattern = os.path.join(input_dir, "*.docx")
    docx_files = glob.glob(search_pattern)

    if not docx_files:
        logger.warning(f"Aucun fichier .docx trouvé dans le dossier '{input_dir}'.")
        return

    logger.info(f"Initialisation de Google Cloud TTS avec la voix : {voice_name}")
    
    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation du client Google Cloud TTS : {e}")
        return

    logger.info(f"{len(docx_files)} fichier(s) à traiter.")

    for docx_file in docx_files:
        logger.info(f"--- Traitement de : {docx_file} ---")
        process_document(
            client=client,
            docx_path=docx_file,
            output_dir=output_dir,
            voice_name=voice_name,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

    logger.info("Terminé ! Tous les fichiers ont été traités.")


if __name__ == "__main__":
    main()
