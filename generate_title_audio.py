#!/usr/bin/env python3
"""
Génère le fichier MP3 pour le titre "LE BILAN DE L'ÉTHER" 
avec 2 secondes de silence avant et après.
"""

import os
import logging
import html
import yaml
from google.cloud import texttospeech
from utils import check_google_credentials

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path="config_google_tts.yaml"):
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def main():
    # 1. Vérifications initiales
    if not check_google_credentials():
        return

    config = load_config()
    voice_name = config.get("voice_name", "fr-FR-Chirp3-HD-Algenib")
    output_dir = config.get("output_dir", "output_audio")
    os.makedirs(output_dir, exist_ok=True)

    # Passage en minuscules pour éviter que le TTS n'épèle les mots en majuscules
    title_text = "le bilan de laitere - Un roman de Dark Fantasy - Par Elias Thorne"
    output_path = os.path.join(output_dir, "titre_livre.mp3")

    # 2. Préparation du texte SSML
    # On échappe le texte mais on préserve l'apostrophe pour le correcteur d'élisions
    safe_text = html.escape(title_text).replace("&#x27;", "'").replace("&quot;", '"')

    # Construction du payload SSML selon les standards du projet (GEMINI.md)
    # + Demande utilisateur : 1s de silence avant et après
    ssml_payload = (
        f"<speak>"
        f"<break time='1s'/>"
        f"<prosody rate='0.9'><emphasis level='strong'>{safe_text}</emphasis></prosody>"
        f"<break time='1s'/>"
        f"</speak>"
    )

    logger.info(f"Synthèse du titre : {title_text}")
    logger.info(f"Utilisation de la voix : {voice_name}")

    # 3. Appel à l'API Google TTS
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_payload)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR", 
            name=voice_name
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9, # Un peu plus lent pour le titre
        )

        response = client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            
        logger.info(f"Succès ! Fichier généré : {output_path}")

    except Exception as e:
        logger.error(f"Erreur lors de la synthèse : {e}")

if __name__ == "__main__":
    main()
