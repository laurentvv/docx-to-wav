#!/usr/bin/env python3
"""
Génère un échantillon audio pour chaque voix masculine Google Cloud TTS.
"""

import os
import logging
from google.cloud import texttospeech
from utils import check_google_credentials

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MALE_VOICES = [
    "fr-FR-Chirp-HD-D",
    "fr-FR-Chirp3-HD-Achird",
    "fr-FR-Chirp3-HD-Algenib",
    "fr-FR-Chirp3-HD-Algieba",
    "fr-FR-Chirp3-HD-Alnilam",
    "fr-FR-Chirp3-HD-Charon",
    "fr-FR-Chirp3-HD-Enceladus",
    "fr-FR-Chirp3-HD-Fenrir",
    "fr-FR-Chirp3-HD-Iapetus",
    "fr-FR-Chirp3-HD-Orus",
    "fr-FR-Chirp3-HD-Puck",
    "fr-FR-Chirp3-HD-Rasalgethi",
    "fr-FR-Chirp3-HD-Sadachbia",
    "fr-FR-Chirp3-HD-Sadaltager",
    "fr-FR-Chirp3-HD-Schedar",
    "fr-FR-Chirp3-HD-Umbriel",
    "fr-FR-Chirp3-HD-Zubenelgenubi",
    "fr-FR-Neural2-G",
    "fr-FR-Polyglot-1",
    "fr-FR-Standard-G",
    "fr-FR-Studio-D",
    "fr-FR-Wavenet-G"
]

TEXT_TO_SYNTHESIZE = """
<speak>
    <prosody rate="0.9"><emphasis level="strong">L’HÉRITIER DU VIDE</emphasis></prosody>
    <break time="1s"/>
    Il s'assit dans une anfractuosité de la roche, à l'abri des embruns. 
    Il sortit l'objet de sa cachette avec des gestes de dévotion. 
    L'artefact pulsait d'une lueur azurée. 
    Ce n'était pas l'automne.
</speak>
"""

def main():
    if not check_google_credentials():
        return

    output_dir = "output_audio/male_voices_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    client = texttospeech.TextToSpeechClient()
    total = len(MALE_VOICES)

    logger.info(f"Démarrage de la génération pour {total} voix masculines...")

    for i, voice_name in enumerate(MALE_VOICES, 1):
        filename = f"sample_{voice_name.replace('fr-FR-', '')}.mp3"
        output_path = os.path.join(output_dir, filename)
        
        logger.info(f"[{i}/{total}] Synthèse avec {voice_name}...")
        
        try:
            synthesis_input = texttospeech.SynthesisInput(ssml=TEXT_TO_SYNTHESIZE)
            voice = texttospeech.VoiceSelectionParams(language_code="fr-FR", name=voice_name)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            response = client.synthesize_speech(
                input=synthesis_input, 
                voice=voice, 
                audio_config=audio_config
            )

            with open(output_path, "wb") as out:
                out.write(response.audio_content)
                
        except Exception as e:
            logger.error(f"Erreur pour la voix {voice_name} : {e}")

    logger.info(f"Terminé ! Échantillons disponibles dans {output_dir}/")

if __name__ == "__main__":
    main()
