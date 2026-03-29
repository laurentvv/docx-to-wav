# GEMINI.md - Project Context (v2.0)

This file provides foundational context and technical mandates for the `docx-to-wav` project.

## Project Mandates

1.  **Direct Audio Output**: Prefer direct MP3 generation for Google Cloud TTS to avoid `ffmpeg` dependencies in the cloud workflow.
2.  **SSML-First Architecture**: Always use SSML for text synthesis to ensure precise control over prosody, pauses, and pronunciation.
3.  **Elision Safety**: All French text sent to the TTS must pass through `fix_french_elisions_ssml` to prevent "letter-by-letter" pronunciation of elisions (`n'`, `l'`, `qu'`) on the Chirp3-HD model.
4.  **Content Separation**: Distinguish between narrative text and structural elements (Titles). Titles must have distinct audio characteristics.

## Architecture & Conventions

### Text Processing Flow
1.  **Extraction** (`utils.py`): Extract paragraphs from `.docx` and detect titles based on Word styles, Bold runs, or uppercase content.
2.  **Normalization** (`utils.py`): Convert Microsoft Word typography (curly quotes, ellipsis, guillemets) to standardized ASCII.
3.  **Splitting** (`utils.py`): Break long segments into sentences (max 1500 chars) to prevent prosody degradation.
4.  **SSML Enrichment** (`convert_docx_google_tts.py`): 
    *   Inject `<break time="500ms"/>` between standard segments.
    *   Apply `<prosody rate="0.9">` and `<emphasis level="strong">` to Titles, followed by a `<break time="1.5s"/>`.
    *   Wrap elisions in `<sub alias="...">` tags using the `fix_french_elisions_ssml` utility.

### Key Files
- `utils.py`: The single source of truth for text manipulation and SSML cleanup.
- `convert_docx_google_tts.py`: Orchestrates direct MP3 synthesis via Google Cloud.
- `config_google_tts.yaml`: Primary configuration for the Google engine (Voice selection, global speed).
- `test_ssml_cleanup.py`: Mandatory tool for validating SSML output without API calls.

## Development Conventions
- **Language**: Optimization is focused on **French (fr-FR)**.
- **Dependencies**: Use `uv` for all environment and script executions.
- **Validation**: Before deploying changes to `utils.py`, always run `test_ssml_cleanup.py` to verify that elisions and titles are correctly formatted.

## Known Model Behaviors
- **Chirp3-HD-Algenib**: High-quality "human" grain but sensitive to elisions. Requires `<sub alias>` tagging for `n'`, `l'`, `d'`, `qu'`, etc.
- **Studio-D**: Best for pure, stable narration but less "textured" than Chirp models.
- **Neural2-G**: Extremely stable, middle ground between Studio and Chirp.

## TODOs
- **Python Version**: Correct `pyproject.toml` to specify `python = ">=3.12"` (currently incorrectly set to 3.14).
- **Batching**: Monitor the 5000-character SSML limit during heavy batching in `convert_docx_google_tts.py`.
