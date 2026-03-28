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
        Contenu audio en bytes (MP3)
    """
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name=voice_name
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    return response.audio_content


def concatenate_mp3_files(mp3_files: list, output_path: str):
    """
    Concatène plusieurs fichiers MP3.
    
    Args:
        mp3_files: Liste de chemins vers les fichiers MP3
        output_path: Chemin du fichier de sortie
    """
    with open(output_path, "wb") as outfile:
        for i, mp3_file in enumerate(mp3_files):
            with open(mp3_file, "rb") as infile:
                outfile.write(infile.read())
            # Ajouter un petit silence entre les paragraphes
            # (les fichiers MP3 contiennent déjà leur propre silence naturel)


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
    mp3_files = []

    try:
        for i, paragraph in enumerate(paragraphs):
            logger.info(f"Traitement du paragraphe {i+1}/{len(paragraphs)}...")
            
            temp_mp3 = os.path.join(temp_dir, f"paragraph_{i:04d}.mp3")
            
            try:
                # Générer l'audio avec Google TTS
                audio_content = synthesize_text(
                    client, paragraph, voice_name, speaking_rate, pitch
                )
                
                with open(temp_mp3, "wb") as f:
                    f.write(audio_content)
                mp3_files.append(temp_mp3)
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement du paragraphe {i+1} : {e}")

        if not mp3_files:
            logger.warning(f"Aucun audio généré pour {docx_path}.")
            return

        logger.info("Concaténation des extraits audio...")
        concatenate_mp3_files(mp3_files, mp3_path)
        logger.info(f"Fichier sauvegardé: {mp3_path}")

    finally:
        # Nettoyer les fichiers temporaires
        for f in mp3_files:
            if os.path.exists(f):
                os.remove(f)
        try:
            os.rmdir(temp_dir)
        except OSError as e:
            logger.warning(f"Impossible de supprimer {temp_dir}: {e}")


def main():
    """Fonction principale."""
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
