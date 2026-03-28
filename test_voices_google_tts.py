#!/usr/bin/env python3
"""
Script pour tester les voix françaises disponibles dans Google Cloud TTS.
Génère des échantillons audio pour chaque voix.

Usage:
    python test_voices_google_tts.py

Prérequis:
    1. Installer: pip install google-cloud-texttospeech
    2. Configurer les credentials: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
    
Les fichiers audio seront sauvegardés dans le dossier test_voices_google_output/
"""

import logging
from pathlib import Path

from utils import check_google_credentials

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


# Voix françaises disponibles dans Google Cloud TTS
FRENCH_VOICES = [
    # Chirp3-HD - Meilleure qualité (HD)
    ("fr-FR-Chirp3-HD-Algenib", "MALE"),
    ("fr-FR-Chirp3-HD-Aoede", "FEMALE"),
    # Neural2 - Très bonne qualité
    ("fr-FR-Neural2-A", "FEMALE"),
    ("fr-FR-Neural2-B", "MALE"),
    ("fr-FR-Neural2-C", "FEMALE"),
    ("fr-FR-Neural2-D", "MALE"),
    # Standard - Moins cher
    ("fr-FR-Standard-A", "FEMALE"),
    ("fr-FR-Standard-B", "MALE"),
    ("fr-FR-Standard-C", "FEMALE"),
    ("fr-FR-Standard-D", "MALE"),
]

# Texte de test
TEST_TEXT = "Bonjour, ceci est un test de synthèse vocale avec Google Cloud TTS. J'espère que vous apprécierez la qualité de cette voix française."


def test_voices():
    """Teste toutes les voix françaises et génère des échantillons audio."""
    
    # Vérifier les credentials
    if not check_google_credentials():
        return
    
    # Créer le dossier de sortie
    output_dir = Path("test_voices_google_output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialiser le client
    logger.info("Initialisation du client Google Cloud TTS...")
    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        return
    
    logger.info("=" * 60)
    logger.info("Test des voix françaises Google Cloud TTS")
    logger.info("=" * 60)
    logger.info(f'Texte de test: "{TEST_TEXT[:50]}..."')
    
    for voice_name, gender in FRENCH_VOICES:
        logger.info(f"Test de la voix: {voice_name} ({gender})")
        
        try:
            # Configurer la synthèse
            synthesis_input = texttospeech.SynthesisInput(text=TEST_TEXT)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code="fr-FR",
                name=voice_name
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            # Générer l'audio
            logger.info("Génération de l'audio...")
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Sauvegarder le fichier
            output_file = output_dir / f"{voice_name}.mp3"
            with open(output_file, "wb") as f:
                f.write(response.audio_content)
            
            logger.info(f"Fichier sauvegardé: {output_file}")
            
        except Exception as e:
            logger.error(f"Erreur avec {voice_name}: {e}")
    
    logger.info("=" * 60)
    logger.info("Tests terminés !")
    logger.info(f"Écoutez les fichiers dans: {output_dir.absolute()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    test_voices()
