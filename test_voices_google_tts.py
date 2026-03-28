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

import os
from pathlib import Path

try:
    from google.cloud import texttospeech
except ImportError:
    print("Erreur: google-cloud-texttospeech n'est pas installé.")
    print("Installez-le avec: pip install google-cloud-texttospeech")
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


def check_credentials():
    """Vérifie que les credentials Google Cloud sont configurés."""
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        print("=" * 60)
        print("⚠️  Configuration des credentials requise !")
        print("=" * 60)
        print("\n1. Allez sur: https://console.cloud.google.com/apis/credentials")
        print("2. Créez un compte de service")
        print("3. Téléchargez le fichier JSON de la clé")
        print("4. Définissez la variable d'environnement:")
        print("\n   Windows (PowerShell):")
        print('   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\key.json"')
        print("\n   Windows (CMD):")
        print('   set GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\key.json')
        print("\n   Linux/macOS:")
        print('   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"')
        print("\n" + "=" * 60)
        return False
    
    if not Path(creds_path).exists():
        print(f"✗ Fichier de credentials non trouvé: {creds_path}")
        return False
    
    print(f"✓ Credentials configurés: {creds_path}")
    return True


def test_voices():
    """Teste toutes les voix françaises et génère des échantillons audio."""
    
    # Vérifier les credentials
    if not check_credentials():
        return
    
    # Créer le dossier de sortie
    output_dir = Path("test_voices_google_output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialiser le client
    print("\nInitialisation du client Google Cloud TTS...")
    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print(f"✗ Erreur lors de l'initialisation: {e}")
        return
    
    print("=" * 60)
    print("Test des voix françaises Google Cloud TTS")
    print("=" * 60)
    print(f"\nTexte de test: \"{TEST_TEXT[:50]}...\"\n")
    
    for voice_name, gender in FRENCH_VOICES:
        print(f"\n--- Test de la voix: {voice_name} ({gender}) ---")
        
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
            print(f"  Génération de l'audio...")
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Sauvegarder le fichier
            output_file = output_dir / f"{voice_name}.mp3"
            with open(output_file, "wb") as f:
                f.write(response.audio_content)
            
            print(f"  ✓ Fichier sauvegardé: {output_file}")
            
        except Exception as e:
            print(f"  ✗ Erreur avec {voice_name}: {e}")
    
    print("\n" + "=" * 60)
    print("Tests terminés !")
    print(f"Écoutez les fichiers dans: {output_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    test_voices()
