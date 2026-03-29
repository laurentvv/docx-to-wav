import os
import html
import logging
from utils import extract_text_from_docx, fix_french_elisions_ssml

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_docx_cleanup():
    docx_path = r"input_docs\Chapitre 1 - Le Vertige de la Chair.docx"
    if not os.path.exists(docx_path): return

    chunks = extract_text_from_docx(docx_path)
    
    for i, (text, is_title) in enumerate(chunks):
        # On reproduit la nouvelle logique de convert_docx_google_tts.py
        safe_text = html.escape(text).replace("&#x27;", "'").replace("&quot;", '"')
        processed_text = fix_french_elisions_ssml(safe_text)
        
        if is_title:
            final_ssml = f'<prosody rate="0.8"><emphasis level="strong">{processed_text}</emphasis></prosody> <break time="1.5s"/>'
        else:
            final_ssml = processed_text
            
        if "'" in text or "sub alias=" in final_ssml:
            logger.info(f"Segment #{i+1} :")
            logger.info(f"  Original    : {text}")
            logger.info(f"  SSML Final  : {final_ssml}")
            logger.info("-" * 60)

if __name__ == "__main__":
    test_docx_cleanup()
