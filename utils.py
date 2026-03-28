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


def extract_text_from_docx(docx_path):
    """
    Extrait le texte d'un document Word paragraphe par paragraphe.
    
    Args:
        docx_path: Chemin vers le fichier .docx
        
    Returns:
        list: Liste des paragraphes non vides
    """
    logger.info(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append(text)
    return paragraphs
