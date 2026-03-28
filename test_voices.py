import os
import logging
import soundfile as sf
import subprocess
from kokoro import KPipeline

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Définition de la phrase de test
TEST_TEXT = "Bonjour, ceci est un test de la qualité des voix françaises avec Kokoro. J'espère que le résultat sera à la hauteur de vos attentes."

# Dossier de sortie pour les tests
OUTPUT_DIR = "test_voices_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialisation du pipeline Kokoro pour le français
logger.info("Initialisation du pipeline Kokoro pour le français ('f')...")
try:
    pipeline = KPipeline(lang_code='f')
except Exception as e:
    logger.error(f"Erreur lors de l'initialisation du pipeline : {e}")
    exit(1)

# Liste des voix françaises (généralement préfixées par ff_ et fm_)
french_voices = ['ff_siwis'] # Ajoutez d'autres voix françaises ici si elles sont disponibles dans votre version

logger.info(f"Génération d'échantillons pour {len(french_voices)} voix...")

for voice_name in french_voices:
    logger.info(f"Test de la voix : {voice_name}")
    try:
        # Générer l'audio
        generator = pipeline(
            TEST_TEXT, voice=voice_name, # Voice name
            speed=1.0, split_pattern=r'\n+'
        )

        # Le générateur produit (graphemes, phonemes, audio)
        for i, (gs, ps, audio) in enumerate(generator):
            if audio is not None:
                wav_path = os.path.join(OUTPUT_DIR, f"{voice_name}.wav")
                mp3_path = os.path.join(OUTPUT_DIR, f"{voice_name}.mp3")

                # Sauvegarder en WAV d'abord (format brut attendu par sf)
                sf.write(wav_path, audio, 24000)

                # Convertir en MP3 avec ffmpeg
                # -y pour écraser si le fichier existe, -loglevel error pour cacher les infos non essentielles
                subprocess.run([
                    'ffmpeg', '-y', '-i', wav_path,
                    '-codec:a', 'libmp3lame', '-qscale:a', '2',
                    '-loglevel', 'error', mp3_path
                ], check=True)

                # Supprimer le WAV temporaire
                if os.path.exists(wav_path):
                    os.remove(wav_path)

                logger.info(f"Fichier généré avec succès : {mp3_path}")
            else:
                logger.warning(f"Aucun audio généré pour {voice_name}.")

            # Un seul bloc de texte ici, on peut faire un break (utile si le split découpe en plusieurs bouts)
            break

    except Exception as e:
        logger.error(f"Erreur avec la voix {voice_name} : {e}")

logger.info(f"Tests terminés ! Vous pouvez écouter les fichiers MP3 dans le dossier : {OUTPUT_DIR}")
