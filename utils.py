#!/usr/bin/env python3
"""
Module utilitaire commun pour les scripts de conversion docx vers audio.

Ce module contient les fonctions partagées entre les différents scripts du projet.
"""

import os
from pathlib import Path
from docx import Document


def check_google_credentials():
    """
    Vérifie que les credentials Google Cloud sont configurés.
    
    Returns:
        bool: True si les credentials sont configurés et valides, False sinon.
    """
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


def extract_text_from_docx(docx_path):
    """
    Extrait le texte d'un document Word paragraphe par paragraphe.
    
    Args:
        docx_path: Chemin vers le fichier .docx
        
    Returns:
        list: Liste des paragraphes non vides
    """
    print(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append(text)
    return paragraphs
