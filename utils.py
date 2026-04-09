#!/usr/bin/env python3
"""
Module utilitaire commun pour les scripts de conversion docx vers audio.
"""

import os
import logging
import re
from pathlib import Path
from docx import Document

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Normalise le texte pour éviter les problèmes avec les moteurs TTS."""
    if not text:
        return ""
    # On a supprimé le remplacement des apostrophes courbes
    text = text.replace('\u201c', '"').replace('\u201d', '"').replace('\u00ab', '"').replace('\u00bb', '"')
    text = text.replace('\u2026', '...').replace('\u2013', '-').replace('\u2014', '-')
    return text


def check_google_credentials():
    """Vérifie que les credentials Google Cloud sont configurés."""
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path or not Path(creds_path).exists():
        logger.error("Configuration des credentials Google Cloud requise !")
        return False
    return True


def split_into_sentences(text: str, max_chars: int = 1000) -> list:
    """Découpe un texte en morceaux plus petits."""
    if len(text) <= max_chars:
        return [text]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk = (current_chunk + " " + sentence) if current_chunk else sentence
        else:
            if current_chunk: chunks.append(current_chunk)
            if len(sentence) > max_chars:
                for i in range(0, len(sentence), max_chars): chunks.append(sentence[i:i+max_chars])
                current_chunk = ""
            else: current_chunk = sentence
    if current_chunk: chunks.append(current_chunk)
    return chunks


def extract_text_from_docx(docx_path, split_long_paragraphs: bool = True, max_chars: int = 1500):
    """
    Extrait le texte d'un document Word.
    Retourne une liste de tuples (texte, est_titre).
    """
    logger.info(f"Extraction du texte depuis {docx_path}...")
    doc = Document(docx_path)
    all_chunks = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        is_title = False
        if para.style.name.startswith(('Heading', 'Titre', 'Title')):
            is_title = True
        elif text.lower().startswith(('chapitre', 'acte')):
            is_title = True
        elif all(run.bold for run in para.runs if run.text.strip()):
            is_title = True
        elif text.isupper() and len(text) < 100:
            is_title = True
            
        normalized_text = normalize_text(text)
        
        if is_title:
            all_chunks.append((normalized_text, True))
        else:
            if split_long_paragraphs:
                sentences = split_into_sentences(normalized_text, max_chars=max_chars)
                for s in sentences:
                    all_chunks.append((s, False))
            else:
                all_chunks.append((normalized_text, False))
                
    return all_chunks
