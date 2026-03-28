# DOCX to MP3 Converter with Kokoro & XTTS v2 (Français)

[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un outil puissant et léger pour convertir vos documents Word (`.docx`) en fichiers audio (`.mp3`) de haute qualité. Ce projet supporte désormais deux modèles de synthèse vocale :
1. **[Kokoro (82M)](https://huggingface.co/hexgrad/Kokoro-82M)** : Extrêmement léger et rapide.
2. **[XTTS v2](https://github.com/coqui-ai/tts)** : Modèle très avancé de Coqui AI offrant un grand naturel et une fidélité émotionnelle supérieure.

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

- **Choix du Modèle** : Utilisez soit Kokoro pour la vitesse, soit XTTS v2 pour une qualité et un naturel premium.
- **Support du Français** : Génération audio naturelle en français sur les deux modèles.
- **Traitement Intelligent** : Découpage automatique des documents `.docx` paragraphe par paragraphe.
- **Export direct en MP3** : Conversion automatique du WAV brut en MP3 compressé via `ffmpeg`.
- **Gestion de la mémoire** : Parfait pour les documents longs (romans, cours, rapports) sans saturer la RAM.
- **Scripts de test des voix** : Des outils inclus pour pré-écouter et choisir la voix qui vous convient le mieux, pour Kokoro et XTTS v2.

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

1. **Python 3.11** (Requis pour la compatibilité avec Coqui TTS)
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
   cd .
   ```
3. Installez les dépendances et créez l'environnement virtuel automatiquement via `uv` :
   ```bash
   uv sync
   ```
   *Note : Le projet utilise des paquets PyTorch compilés pour CPU (via une URL d'index personnalisée dans le fichier `pyproject.toml`) pour faciliter l'installation.*

4. Activez l'environnement virtuel :
   - **Linux/macOS** : `source .venv/bin/activate`
   - **Windows** : `.venv\Scripts\activate`

---

## 🗣️ Tester les voix

Afin de choisir la voix parfaite, générez des échantillons audio :

**Pour Kokoro :**
```bash
python test_voices.py
```
*(Écoutez les fichiers dans le dossier `test_voices_output/`)*

**Pour XTTS v2 :**
```bash
python test_voices_xtts.py
```
*(Écoutez les fichiers dans le dossier `test_voices_xtts_output/`)*

Notez le nom de la voix que vous préférez.

---

## 📖 Utilisation

1. **Configuration** :
   - Ouvrez le fichier `config.yaml` (pour Kokoro) ou `config_xtts.yaml` (pour XTTS v2).
   - Modifiez la valeur `voice` avec la voix choisie lors de l'étape précédente.
2. **Préparation** : Placez tous vos fichiers Word (`.docx`) dans le dossier `input_docs/`.
3. **Conversion** :
   - Pour Kokoro :
     ```bash
     python convert_docx.py
     ```
   - Pour XTTS v2 :
     ```bash
     python convert_docx_xtts.py
     ```
4. **Résultat** : Patientez pendant la génération. Une fois terminé, vos fichiers audio `.mp3` se trouveront dans le dossier `output_audio/`.

---

## 📁 Structure du projet

```text
./
├── .venv/                   # Environnement virtuel (créé par uv)
├── input_docs/              # Placez vos fichiers .docx ici
├── output_audio/            # Fichiers .mp3 générés
├── test_voices_output/      # Echantillons vocaux (Kokoro)
├── test_voices_xtts_output/ # Echantillons vocaux (XTTS v2)
├── pyproject.toml           # Configuration du projet et dépendances
├── uv.lock                  # Lockfile pour des installations reproductibles
├── config.yaml              # Fichier de configuration (Kokoro)
├── config_xtts.yaml         # Fichier de configuration (XTTS v2)
├── test_voices.py           # Script pour tester les voix Kokoro
├── test_voices_xtts.py      # Script pour tester les voix XTTS v2
├── convert_docx.py          # Script principal de conversion Docx -> MP3 (Kokoro)
├── convert_docx_xtts.py     # Script principal de conversion Docx -> MP3 (XTTS v2)
└── README.md                # Ce fichier
```

---

## 🛠️ Configuration

Les fichiers de configuration `config.yaml` et `config_xtts.yaml` vous permettent d'ajuster le comportement des scripts principaux :

**config_xtts.yaml (Exemple)**
```yaml
# Dossier contenant vos fichiers Word (.docx)
input_dir: "input_docs"

# Dossier où seront sauvegardés les fichiers finaux (.mp3)
output_dir: "output_audio"

# Voix par défaut pour XTTS v2
voice: "Claribel Dervla"

# Langue
language: "fr"
```
