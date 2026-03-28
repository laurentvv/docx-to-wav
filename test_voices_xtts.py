import os

import torch

# Fix for weight_only PyTorch 2.6 issue
try:
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig
    torch.serialization.add_safe_globals([XttsConfig, XttsArgs, XttsAudioConfig])
except ImportError:
    pass

# Auto-accept Coqui's license by mocking input, or by setting the environment variable
os.environ["COQUI_TOS_AGREED"] = "1"


from TTS.api import TTS

def main():
    output_dir = "test_voices_xtts_output"
    os.makedirs(output_dir, exist_ok=True)

    print("Initialisation du modèle XTTS v2...")
    # Initialiser le modèle XTTS v2

    import warnings
    warnings.filterwarnings('ignore')
    # Monkey patch torch.load to ignore weights_only=True errors temporarily
    original_torch_load = torch.load
    def patched_torch_load(*args, **kwargs):
        kwargs['weights_only'] = False
        return original_torch_load(*args, **kwargs)
    torch.load = patched_torch_load

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

    # Texte de test en français
    test_text = "Bonjour, ceci est un test de ma voix. Comment trouvez-vous le résultat ?"

    # Récupérer la liste des locuteurs par défaut inclus dans XTTS
    if hasattr(tts, 'speakers') and tts.speakers:
        speakers = tts.speakers
    elif hasattr(tts, 'synthesizer') and hasattr(tts.synthesizer, 'tts_model') and hasattr(tts.synthesizer.tts_model, 'speaker_manager') and tts.synthesizer.tts_model.speaker_manager:
        speakers = list(tts.synthesizer.tts_model.speaker_manager.name_to_id)
    else:
        # Fallback list of some known XTTS default speakers
        speakers = ["Ana Florence", "Henriette Usha", "Gilles Beatrice", "Jude Damien", "Martin Célestin"]

    # Just test first 5 speakers to be quick in the test script, user can edit to test all
    speakers_to_test = speakers[:5]
    print(f"{len(speakers_to_test)} voix par défaut seront testées sur les {len(speakers)} disponibles.")

    for speaker in speakers_to_test:
        print(f"Génération du test pour la voix : {speaker}...")
        try:
            output_path = os.path.join(output_dir, f"{speaker.replace(' ', '_')}.wav")
            # Pour générer, on utilise tts_to_file
            tts.tts_to_file(text=test_text, speaker=speaker, language="fr", file_path=output_path)
            print(f" -> Enregistré : {output_path}")
        except Exception as e:
            print(f" -> Erreur avec {speaker} : {e}")

    print("\nTests terminés. Vous pouvez écouter les fichiers dans le dossier", output_dir)
    print("Ensuite, mettez à jour la valeur 'voice' dans config_xtts.yaml avec le nom de votre voix préférée.")

if __name__ == "__main__":
    main()
