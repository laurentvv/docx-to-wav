# DOCX to MP3 Converter with Kokoro & Google Cloud TTS (Français)

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un outil puissant pour convertir vos documents Word (`.docx`) en fichiers audio (`.mp3`) de haute qualité. Ce projet supporte deux moteurs de synthèse vocale :

1. **[Kokoro (82M)](https://huggingface.co/hexgrad/Kokoro-82M)** : Extrêmement léger et rapide, idéal pour le CPU.
2. **[Google Cloud TTS](https://cloud.google.com/text-to-speech)** : Qualité professionnelle avec Chirp3-HD, free tier généreux (1M caractères/mois).

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
- [🔄 Comparaison des moteurs](#-comparaison-des-moteurs)
- [💰 Tarification](#-tarification)

---

## ✨ Fonctionnalités

- **Choix du Moteur** : Utilisez Kokoro pour le local ou Google Cloud TTS pour la meilleure qualité.
- **Support du Français** : Génération audio naturelle en français.
- **Traitement Intelligent** : Découpage automatique des documents `.docx` paragraphe par paragraphe.
- **Export direct en MP3** : Conversion automatique du WAV brut en MP3 compressé via `ffmpeg`.
- **Gestion de la mémoire** : Parfait pour les documents longs (romans, cours, rapports) sans saturer la RAM.
- **Scripts de test des voix** : Des outils inclus pour pré-écouter et choisir la voix qui vous convient le mieux.

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

1. **Python 3.12+**
2. **[uv](https://github.com/astral-sh/uv)** - Le gestionnaire de paquets Python ultra-rapide écrit en Rust :
   ```bash
   pip install uv
   ```
3. **FFmpeg** - Outil système requis pour la conversion `.wav` vers `.mp3` :
   - **Ubuntu/Debian** : `sudo apt update && sudo apt install ffmpeg`
   - **macOS** : `brew install ffmpeg`
   - **Windows** : Téléchargez depuis [le site officiel](https://ffmpeg.org/download.html) ou utilisez Winget : `winget install ffmpeg`

### Pour Google Cloud TTS

4. **Compte Google Cloud** avec l'API Text-to-Speech activée
5. **Clé JSON de compte de service** (voir [Configuration Google Cloud](#configuration-google-cloud-tts))

---

## 🚀 Installation

1. Clonez ce dépôt ou téléchargez les fichiers.
2. Déplacez-vous dans le répertoire du projet :
   ```bash
   cd docx-to-wav
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

### Kokoro TTS

Kokoro propose plusieurs modèles vocaux. Pour la langue française, nous utilisons généralement les modèles préfixés par `ff_` (French Female) ou `fm_` (French Male), par exemple `ff_siwis`.

```bash
python test_voices.py
```

Les fichiers audio de test seront générés dans le dossier `test_voices_output/`.

### Google Cloud TTS

Google Cloud TTS propose plusieurs types de voix françaises :
- **Chirp3-HD** : Meilleure qualité (HD), free tier 1M caractères/mois
- **Neural2** : Très bonne qualité, free tier 1M caractères/mois
- **Standard** : Qualité basique, free tier 4M caractères/mois

```bash
python test_voices_google_tts.py
```

Les fichiers audio de test seront générés dans le dossier `test_voices_google_output/`.

---

## 📖 Utilisation

### Avec Kokoro TTS (Local)

1. **Configuration** : Ouvrez le fichier `config.yaml` et modifiez la valeur `voice` avec la voix choisie.
2. **Préparation** : Placez tous vos fichiers Word (`.docx`) dans le dossier `input_docs/`.
3. **Conversion** : Lancez le script principal :
   ```bash
   python convert_docx.py
   ```
4. **Résultat** : Vos fichiers audio `.mp3` se trouveront dans le dossier `output_audio/`.

### Avec Google Cloud TTS (Cloud)

1. **Configuration Google Cloud** : Voir la section [Configuration Google Cloud TTS](#configuration-google-cloud-tts)
2. **Configuration** : Ouvrez le fichier `config_google_tts.yaml` et modifiez la voix si nécessaire.
3. **Préparation** : Placez tous vos fichiers Word (`.docx`) dans le dossier `input_docs/`.
4. **Conversion** : Lancez le script principal :
   ```bash
   python convert_docx_google_tts.py
   ```
5. **Résultat** : Vos fichiers audio `.mp3` se trouveront dans le dossier `output_audio/`.

---

## 📁 Structure du projet

```text
./
├── .venv/                      # Environnement virtuel (créé par uv)
├── input_docs/                 # Placez vos fichiers .docx ici
├── output_audio/               # Fichiers .mp3 générés
├── test_voices_output/         # Échantillons vocaux Kokoro
├── test_voices_google_output/  # Échantillons vocaux Google Cloud TTS
├── pyproject.toml              # Configuration du projet et dépendances
├── uv.lock                     # Lockfile pour des installations reproductibles
├── config.yaml                 # Fichier de configuration Kokoro
├── config_google_tts.yaml      # Fichier de configuration Google Cloud TTS
├── test_voices.py              # Script de test des voix Kokoro
├── test_voices_google_tts.py   # Script de test des voix Google Cloud TTS
├── convert_docx.py             # Script principal Kokoro
├── convert_docx_google_tts.py  # Script principal Google Cloud TTS
└── README.md                   # Ce fichier
```

---

## 🛠️ Configuration

### config.yaml (Kokoro)

```yaml
# Dossier contenant vos fichiers Word (.docx)
input_dir: "input_docs"

# Dossier où seront sauvegardés les fichiers finaux (.mp3)
output_dir: "output_audio"

# Voix française utilisée pour la synthèse vocale (ex: ff_siwis)
voice: "ff_siwis"

# Vitesse de diction (1.0 = normale)
speed: 1.0
```

### config_google_tts.yaml (Google Cloud TTS)

```yaml
# Dossier contenant vos fichiers Word (.docx)
input_dir: "input_docs"

# Dossier où seront sauvegardés les fichiers finaux (.mp3)
output_dir: "output_audio"

# Voix française Google TTS
# Options Chirp3-HD (meilleure qualité, free tier 1M chars/mois):
#   fr-FR-Chirp3-HD-Algenib (MALE), fr-FR-Chirp3-HD-Aoede (FEMALE)
# Options Neural2 (très bonne qualité):
#   fr-FR-Neural2-A (FEMALE), fr-FR-Neural2-B (MALE), etc.
voice_name: "fr-FR-Chirp3-HD-Algenib"

# Genre: MALE, FEMALE, NEUTRAL
voice_gender: "MALE"

# Langue
language_code: "fr-FR"

# Vitesse de parole (0.25 à 4.0, 1.0 = normal)
speaking_rate: 1.0

# Pitch (-20.0 à 20.0, 0.0 = normal)
pitch: 0.0

# Format de sortie
audio_encoding: "MP3"
```

### Configuration Google Cloud TTS

1. **Créer un projet Google Cloud** : https://console.cloud.google.com/
2. **Activer l'API Text-to-Speech** : https://console.cloud.google.com/apis/library/texttospeech.googleapis.com
3. **Créer un compte de service** :
   - Allez sur https://console.cloud.google.com/apis/credentials
   - Cliquez sur "Créer des identifiants" → "Compte de service"
   - Nom : `tts-service`
   - Rôle : **"Cloud Text-to-Speech User"**
4. **Télécharger la clé JSON** :
   - Cliquez sur le compte de service créé
   - Onglet "Clés" → "Ajouter une clé" → "Créer une clé" → JSON
5. **Configurer la variable d'environnement** :
   ```powershell
   # Windows PowerShell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\chemin\vers\votre-cle.json"
   
   # Linux/macOS
   export GOOGLE_APPLICATION_CREDENTIALS="/chemin/vers/votre-cle.json"
   ```

---

## 🔄 Comparaison des moteurs

| Caractéristique | Kokoro | Google Cloud TTS |
|-----------------|--------|------------------|
| **Taille du modèle** | 82M | Cloud (pas de modèle local) |
| **Vitesse** | Rapide | Dépend de la connexion |
| **GPU requis** | Non (CPU) | Non (Cloud) |
| **AMD Windows** | ✅ | ✅ |
| **NVIDIA CUDA** | ✅ | ✅ |
| **Qualité audio** | Excellente | Exceptionnelle (Chirp3-HD) |
| **Voix françaises** | Plusieurs | 10+ |
| **Installation** | Simple | Compte GCP requis |
| **Coût** | Gratuit | Free tier 1M chars/mois |

### Recommandation

- **Usage local / hors ligne** : Utilisez **Kokoro**
- **Meilleure qualité** : Utilisez **Google Cloud TTS** avec Chirp3-HD
- **Grands volumes** : **Google Cloud TTS** (free tier généreux)

---

## 💰 Tarification

### Google Cloud TTS

| Type de voix | Free tier | Prix après free tier |
|--------------|-----------|---------------------|
| Standard | 4M caractères/mois | $4/million |
| Neural2 | 1M caractères/mois | $16/million |
| Chirp3-HD | 1M caractères/mois | $30/million |

**Exemple** : Pour 23 fichiers DOCX (~284 000 caractères), vous restez dans le free tier = **GRATUIT**.

### Kokoro

**100% gratuit** - Fonctionne entièrement en local.

---

## 📝 Notes

- Pour les documents très longs, le traitement par paragraphe permet de ne pas saturer la mémoire
- Les credentials Google Cloud sont stockés localement et ne sont jamais partagés

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
