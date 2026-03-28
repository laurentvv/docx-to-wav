# Convertisseur DOCX en MP3 avec Kokoro (Français)

Ce projet permet de convertir vos documents Word (.docx) en fichiers audio (.mp3) en utilisant le modèle de synthèse vocale (TTS) Kokoro (82M) via son API Python. La conversion se fait paragraphe par paragraphe pour plus d'efficacité, et supporte les voix françaises.

## Prérequis

1. Installez `uv` si ce n'est pas déjà fait :
   ```bash
   pip install uv
   ```
2. Installez le logiciel système `ffmpeg` (requis pour convertir le fichier `.wav` en `.mp3`).
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Téléchargez-le depuis le site officiel ou via winget : `winget install ffmpeg`

## Installation

1. Allez dans le dossier du projet.
2. Initialisez l'environnement et installez les dépendances :
   ```bash
   uv sync
   ```
3. Activez l'environnement virtuel :
   - Linux/macOS : `source .venv/bin/activate`
   - Windows : `.venv\Scripts\activate`

## Tester les voix françaises

Kokoro propose plusieurs voix (hommes et femmes). Pour tester et choisir celle qui vous convient le mieux :

```bash
python test_voices.py
```

Cela génèrera une phrase test pour toutes les voix françaises disponibles dans le dossier `test_voices_output`.

## Utilisation

1. Modifiez le fichier `config.yaml` pour sélectionner votre voix préférée (ex: `ff_siwis`, `am_adam`, etc.).
2. Placez vos fichiers `.docx` dans le dossier `input_docs` (ou celui défini dans votre config).
3. Lancez le script de conversion :
   ```bash
   python convert_docx.py
   ```
4. Retrouvez vos fichiers audios `.mp3` dans le dossier `output_audio`.

> Note: Le fichier temporaire `.wav` est automatiquement supprimé après la conversion.
