# DOCX to MP3 Converter with Kokoro & Google Cloud TTS (Français)

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Un outil puissant pour convertir vos documents Word (`.docx`) en fichiers audio (`.mp3`) de haute qualité. Ce projet supporte deux moteurs de synthèse vocale :

1. **[Kokoro (82M)](https://huggingface.co/hexgrad/Kokoro-82M)** : Extrêmement léger et rapide, idéal pour le CPU.
2. **[Google Cloud TTS](https://cloud.google.com/text-to-speech)** : Qualité professionnelle avec Chirp3-HD, voix Studio et Neural2.

---

## ✨ Fonctionnalités (Version 2.0)

- **Optimisation Google Cloud TTS** : 
    - Génération MP3 directe (plus besoin de `ffmpeg` pour le moteur Google).
    - Support complet du **SSML** pour une prosodie naturelle.
- **Correction Chirp3-HD** : 
    - "Correcteur d'élisions" automatique pour forcer la prononciation correcte des apostrophes (`n'`, `l'`, `qu'`, etc.) sur le modèle Chirp3-HD.
- **Mise en valeur des Titres** : 
    - Détection automatique des titres (`Heading 1`, texte en gras, MAJUSCULES).
    - Intonation spécifique pour les titres : plus lente (`rate="0.9"`), plus d'emphase, et pause de 1.5s après la lecture.
- **Traitement Intelligent** : 
    - Découpage par phrases au lieu de paragraphes pour éviter les erreurs de prosodie.
    - Normalisation automatique de la typographie Word (apostrophes courbes, guillemets, etc.).
- **Gestion de la mémoire** : Parfait pour les documents longs (romans, cours, rapports) sans saturer la RAM.

---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

1. **Python 3.12+**
2. **[uv](https://github.com/astral-sh/uv)** :
   ```bash
   pip install uv
   ```
3. **FFmpeg** (Requis uniquement pour le moteur **Kokoro**)

### Pour Google Cloud TTS

4. **Compte Google Cloud** avec l'API Text-to-Speech activée.
5. **Clé JSON de compte de service**.

---

## 🚀 Installation

1. Clonez ce dépôt.
2. Installez les dépendances :
   ```bash
   uv sync
   ```

---

## 📖 Utilisation

### Avec Google Cloud TTS (Recommandé)

1. **Configuration** : Modifiez `config_google_tts.yaml`. 
   - Voix par défaut : `fr-FR-Chirp3-HD-Algenib` (grain de voix humain).
2. **Préparation** : Placez vos `.docx` dans `input_docs/`.
3. **Conversion** :
   ```bash
   uv run python convert_docx_google_tts.py
   ```
4. **Validation** : Vous pouvez tester le nettoyage du texte sans consommer de crédit API :
   ```bash
   uv run python test_ssml_cleanup.py
   ```

### Avec Kokoro TTS (Local)

```bash
uv run python convert_docx.py
```

---

## 📁 Structure du projet

```text
./
├── input_docs/                 # Fichiers source .docx
├── output_audio/               # Fichiers .mp3 générés
├── config_google_tts.yaml      # Configuration Google Cloud
├── convert_docx_google_tts.py  # Script principal Google (SSML + Direct MP3)
├── convert_docx.py             # Script principal Kokoro (Local)
├── utils.py                    # Utilities (Extraction, Normalisation, SSML cleanup)
├── test_ssml_cleanup.py        # Outil de test pour vérifier le nettoyage SSML
└── README.md                   # Ce fichier
```

---

## 🛠️ Configuration Google Cloud

Le fichier `config_google_tts.yaml` permet de régler :
- `voice_name` : `fr-FR-Chirp3-HD-Algenib` (Recommandé avec notre correcteur), `fr-FR-Studio-D` (Narration pure), ou `fr-FR-Neural2-G`.
- `speaking_rate` : Vitesse de lecture globale.

---

## 📄 Licence

Ce projet est sous licence MIT.
