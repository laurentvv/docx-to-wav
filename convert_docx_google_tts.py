#!/usr/bin/env python3
"""
Script de conversion de documents Word (.docx) en fichiers audio MP3
en utilisant Google Cloud Text-to-Speech.
"""

import os
import glob
import logging
import yaml
import html

from utils import check_google_credentials, extract_text_from_docx, fix_french_elisions_ssml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from google.cloud import texttospeech
except ImportError:
    logger.error("google-cloud-texttospeech n'est pas installé.")
    exit(1)


def load_config(config_path="config_google_tts.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def synthesize_ssml(client, ssml_text, voice_name, speaking_rate=1.0, pitch=0.0):
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    voice = texttospeech.VoiceSelectionParams(language_code="fr-FR", name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch
    )
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content


def process_document(client, docx_path, output_dir, voice_name, speaking_rate=1.0, pitch=0.0):
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    mp3_path = os.path.join(output_dir, f"{base_name}.mp3")

    chunks = extract_text_from_docx(docx_path)
    if not chunks:
        logger.warning(f"Le document {docx_path} est vide.")
        return

    logger.info(f"{len(chunks)} segments extraits. Préparation de la synthèse...")

    batches = []
    current_batch = []
    current_length = 0
    
    for text, is_title in chunks:
        # --- CORRECTION ICI : On applique le correcteur d'élisions AVANT l'échappement HTML ---
        # On utilise une version "safe" pour le SSML
        fixed_text = fix_french_elisions_ssml(text)
        
        # On n'échappe QUE si le texte n'a pas été transformé en SSML par fix_french_elisions_ssml
        # En fait, le plus simple est d'échapper les caractères dangereux (& < >) 
        # mais de GARDER l'apostrophe pour que le regex puisse travailler.
        
        safe_text = html.escape(text).replace("&#x27;", "'").replace("&quot;", '"')
        processed_text = fix_french_elisions_ssml(safe_text)
        
        if is_title:
            # Un peu plus lent que le récit (rate="0.9"), emphase forte, et pause après de 1.5s
            formatted_text = f'<prosody rate="0.9"><emphasis level="strong">{processed_text}</emphasis></prosody> <break time="1.5s"/>'
        else:
            formatted_text = processed_text
            
        if current_length + len(formatted_text) + 50 > 4500:
            batches.append(current_batch)
            current_batch = [formatted_text]
            current_length = len(formatted_text)
        else:
            current_batch.append(formatted_text)
            current_length += len(formatted_text) + 50
            
    if current_batch:
        batches.append(current_batch)

    try:
        with open(mp3_path, "wb") as out_file:
            for i, batch in enumerate(batches):
                logger.info(f"Synthèse du groupe {i+1}/{len(batches)}...")
                combined_text = ' <break time="500ms"/> '.join(batch)
                ssml_payload = f"<speak>{combined_text}</speak>"
                
                audio_content = synthesize_ssml(client, ssml_payload, voice_name, speaking_rate, pitch)
                out_file.write(audio_content)
                
        logger.info(f"Succès ! Fichier MP3 créé : {mp3_path}")
    except Exception as e:
        logger.error(f"Erreur lors de la création du MP3 : {e}")
        if os.path.exists(mp3_path): os.remove(mp3_path)


def main():
    if not check_google_credentials(): return
    config = load_config()
    input_dir = config.get("input_dir", "input_docs")
    output_dir = config.get("output_dir", "output_audio")
    voice_name = config.get("voice_name", "fr-FR-Chirp3-HD-Algenib")
    speaking_rate = config.get("speaking_rate", 1.0)
    pitch = config.get("pitch", 0.0)

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    docx_files = glob.glob(os.path.join(input_dir, "*.docx"))
    if not docx_files: return

    logger.info(f"Utilisation de la voix : {voice_name}")
    client = texttospeech.TextToSpeechClient()

    for docx_file in docx_files:
        logger.info(f"--- Fichier : {docx_file} ---")
        process_document(client, docx_file, output_dir, voice_name, speaking_rate, pitch)

    logger.info("Traitement terminé.")


if __name__ == "__main__":
    main()
