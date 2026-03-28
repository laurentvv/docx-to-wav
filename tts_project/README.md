# DOCX to MP3 Converter with Kokoro TTS (Français)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un outil puissant et léger pour convertir vos documents Word (`.docx`) en fichiers audio (`.mp3`) de haute qualité en utilisant le modèle de synthèse vocale [Kokoro (82M)](https://huggingface.co/hexgrad/Kokoro-82M).

Le script est optimisé pour le français, traite les longs documents paragraphe par paragraphe pour économiser la mémoire RAM/VRAM, et insère des pauses naturelles entre les idées.

---

## 📑 Table des Matières

- [✨ Fonctionnalités](#-fonctionnalités)
- [⚙️ Prérequis](#️-prérequis)
- [🚀 Installation](#-installation)
- [🗣️ Tester les voix](#️-tester-les-voix)
- [📖 Utilisation](#-utilisation)
- [📁 Structure du projet](#-structure-du-projet)
- [🛠️ Configuration](#️-configuration)

---

## ✨ Fonctionnalités

- **Haute Qualité & Léger** : Utilise Kokoro (82M), un modèle TTS extrêmement performant qui tourne facilement sur CPU.
- **Support du Français** : Génération audio naturelle en français.
- **Traitement Intelligent** : Découpage automatique des documents `.docx` paragraphe par paragraphe.
- **Export direct en MP3** : Conversion automatique du WAV brut en MP3 compressé via `ffmpeg`.
- **Gestion de la mémoire** : Parfait pour les documents longs (romans, cours, rapports) sans saturer la RAM.
- **Script de test des voix** : Un outil inclus pour pré-écouter et choisir la voix qui vous convient le mieux.

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

1. **Python 3.10+**
2. **[uv](https://github.com/astral-sh/uv)** - Le gestionnaire de paquets Python ultra-rapide écrit en Rust :
   ```bash
   pip install uv
   ```
3. **FFmpeg** - Outil système requis pour la conversion `.wav` vers `.mp3` :
   - **Ubuntu/Debian** : `sudo apt update && sudo apt install ffmpeg`
   - **macOS** : `brew install ffmpeg`
   - **Windows** : Téléchargez depuis [le site officiel](https://ffmpeg.org/download.html) ou utilisez Winget : `winget install ffmpeg`

---

## 🚀 Installation

1. Clonez ce dépôt ou téléchargez les fichiers.
2. Déplacez-vous dans le répertoire du projet :
   ```bash
   cd tts_project
   ```
3. Installez les dépendances et créez l'environnement virtuel automatiquement via `uv` :
   ```bash
   uv sync
   ```
4. Activez l'environnement virtuel :
   - **Linux/macOS** : `source .venv/bin/activate`
   - **Windows** : `.venv\Scripts\activate`

---

## 🗣️ Tester les voix

Kokoro propose plusieurs modèles vocaux. Pour la langue française, nous utilisons généralement les modèles préfixés par `ff_` (French Female) ou `fm_` (French Male), par exemple `ff_siwis`.

Pour écouter le rendu de ces voix et faire votre choix, lancez le script de test :

```bash
python test_voices.py
```

Les fichiers audio de test seront générés dans le dossier `test_voices_output/`. Vous pourrez alors écouter chaque MP3 et noter le nom de votre voix préférée.

---

## 📖 Utilisation

1. **Configuration** : Ouvrez le fichier `config.yaml` et modifiez la valeur `voice` avec la voix choisie lors de l'étape précédente.
2. **Préparation** : Placez tous vos fichiers Word (`.docx`) dans le dossier `input_docs/`.
3. **Conversion** : Lancez le script principal :
   ```bash
   python convert_docx.py
   ```
4. **Résultat** : Patientez pendant la génération. Une fois terminé, vos fichiers audio `.mp3` se trouveront dans le dossier `output_audio/`.

---

## 📁 Structure du projet

```text
tts_project/
├── .venv/                   # Environnement virtuel (créé par uv)
├── input_docs/              # Placez vos fichiers .docx ici
├── output_audio/            # Fichiers .mp3 générés
├── test_voices_output/      # Echantillons vocaux générés par test_voices.py
├── pyproject.toml           # Configuration du projet et dépendances
├── uv.lock                  # Lockfile pour des installations reproductibles
├── config.yaml              # Fichier de configuration (dossiers, voix, vitesse)
├── test_voices.py           # Script pour générer des extraits de test des voix
├── convert_docx.py          # Script principal de conversion Docx -> MP3
└── README.md                # Ce fichier
```

---

## 🛠️ Configuration

Le fichier `config.yaml` vous permet d'ajuster le comportement du script principal sans toucher au code :

```yaml
# Dossier contenant vos fichiers Word (.docx)
input_dir: "input_docs"

# Dossier où seront sauvegardés les fichiers finaux (.mp3)
output_dir: "output_audio"

# Voix française utilisée pour la synthèse vocale (ex: ff_siwis)
voice: "ff_siwis"

# Vitesse de diction (1.0 = normale, >1.0 = plus rapide, <1.0 = plus lent)
speed: 1.0
```
