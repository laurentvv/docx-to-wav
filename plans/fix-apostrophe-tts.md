# Plan de correction : Bug apostrophe dans Google TTS

## Problème identifié

La phrase venant du fichier "input_docs\Chapitre 1 - Le Vertige de la Chair.docx" : "Ce n'était pas la paralysie nette et propre..." est prononcée incorrectement comme "Ce 'N'...était pas..." par Google TTS.
Le moteur TTS interprète mal cette apostrophe courbe dans "n'était", traitant potentiellement le "n'" comme une entité séparée.

### Cause racine

Microsoft Word utilise l'**apostrophe courbe** (curly quote) `'` (Unicode U+2019 - RIGHT SINGLE QUOTATION MARK) au lieu de l'**apostrophe droite** `'` (ASCII 39 / U+0027).

Le moteur TTS interprète mal cette apostrophe courbe dans "n'était", traitant potentiellement le "n'" comme une entité séparée.

```mermaid
flowchart TD
    subgraph Problème
        A[Document Word .docx] --> B[Texte avec apostrophe courbe U+2019]
        B --> C["n'était" devient "n' + était"]
        C --> D[Audio: Ce N...était]
    end
    
    subgraph Solution
        E[Document Word .docx] --> F[Extraction texte]
        F --> G[Normalisation: U+2019 vers U+0027]
        G --> H["n'était" reste "n'était"]
        H --> I[Audio correct: Ce n'était]
    end
```

## Solution technique

### Fichier à modifier : `utils.py`

#### 1. Ajouter une fonction de normalisation

```python
def normalize_text(text: str) -> str:
    """
    Normalise le texte pour éviter les problèmes avec les moteurs TTS.
    
    Remplace les caractères typographiques spéciaux par leurs équivalents ASCII.
    
    Args:
        text: Texte à normaliser
        
    Returns:
        Texte normalisé
    """
    # Remplacer l'apostrophe courbe (U+2019) par l'apostrophe droite (U+0027)
    text = text.replace('\u2019', "'")  # Right single quotation mark
    
    # Autres apostrophes courbes possibles
    text = text.replace('\u2018', "'")  # Left single quotation mark
    text = text.replace('\u201b', "'")  # Single high-reversed-9 quotation mark
    
    # Guillemets courbes (optionnel, peut aider pour d'autres cas)
    text = text.replace('\u201c', '"')  # Left double quotation mark
    text = text.replace('\u201d', '"')  # Right double quotation mark
    
    return text
```

#### 2. Intégrer dans `extract_text_from_docx()`

Modifier la ligne 64 dans [`utils.py`](utils.py:64) :

```python
# Avant
paragraphs.append(text)

# Après
paragraphs.append(normalize_text(text))
```

## Code complet modifié

### utils.py (version corrigée)

```python
#!/usr/bin/env python3
"""
Module utilitaire commun pour les scripts de conversion docx vers audio.

Ce module contient les fonctions partagées entre les différents scripts du projet.
"""

import os
import logging
from pathlib import Path
from docx import Document

logger = logging.getLogger(__name__)


def check_google_credentials():
    """
    Vérifie que les credentials Google Cloud sont configurés.
    
    Returns:
        bool: True si les credentials sont configurés et valides, False sinon.
    """
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        logger.error("=" * 60)
        logger.error("Configuration des credentials requise !")
        logger.error("=" * 60)
        logger.info("1. Allez sur: https://console.cloud.google.com/apis/credentials")
        logger.info("2. Créez un compte de service")
        logger.info("3. Téléchargez le fichier JSON de la clé")
        logger.info("4. Définissez la variable d'environnement:")
        logger.info("   Windows (PowerShell):")
        logger.info('   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\key.json"')
        logger.info("   Windows (CMD):")
        logger.info('   set GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\key.json')
        logger.info("   Linux/macOS:")
        logger.info('   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"')
        logger.error("=" * 60)
        return False
    
    if not Path(creds_path).exists():
        logger.error(f"Fichier de credentials non trouvé: {creds_path}")
        return False
    
    logger.info(f"Credentials configurés: {creds_path}")
    return True


def normalize_text(text: str) -> str:
    """
    Normalise le texte pour éviter les problèmes avec les moteurs TTS.
    
    Remplace les caractères typographiques spéciaux par leurs équivalents ASCII.
    Cela résout notamment le problème où l'apostrophe courbe de Word (')
    est mal interprétée par Google TTS dans des mots comme "n'était".
    
    Args:
        text: Texte à normaliser
        
    Returns:
        Texte normalisé
    """
    # Apostrophes courbes vers apostrophe droite
    text = text.replace('\u2019', "'")  # Right single quotation mark (apostrophe française typique)
    text = text.replace('\u2018', "'")  # Left single quotation mark
    text = text.replace('\u201b', "'")  # Single high-reversed-9 quotation mark
    
    # Guillemets courbes vers guillemets droits (optionnel)
    text = text.replace('\u201c', '"')  # Left double quotation mark
    text = text.replace('\u201d', '"')  # Right double quotation mark
    
    return text


def extract_text_from_docx(docx_path):
    """
    Extrait le texte d'un document Word paragraphe par paragraphe.
    
    Args:
        docx_path: Chemin vers le fichier .docx
        
    Returns:
        list: Liste des paragraphes non vides, avec texte normalisé
    """
    logger.info(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append(normalize_text(text))
    return paragraphs
```

## Tests de validation

Après modification, tester avec :

1. La phrase problématique originale
2. Diverses phrases avec apostrophes (c'était, n'était, j'ai, l'homme, etc.)
3. Vérifier que l'audio produit est fluide

## Impact

- **Fichiers modifiés** : 1 fichier ([`utils.py`](utils.py))
- **Rétrocompatibilité** : Oui, la normalisation ne casse pas le texte existant
- **Performance** : Négligeable (simple remplacement de caractères)
