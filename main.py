import re
import os
import requests
import time
from urllib.parse import quote

API_KEY = "Bitx-Jithula2356"
API_BASE = "https://bit-x-apis.vercel.app/talkai"

# Available models in order of preference
MODELS = ["writify", "claude", "dolphin", "overchat"]

def clean_translation(text):
    """
    Cleans the translated text by fixing extra spaces and specific Sinhala character spacing issues.
    """
    # 1. Fix extra spaces between words
    text = re.sub(r' +', ' ', text)           # multiple spaces → single space
    text = re.sub(r' \n', '\n', text)          # space before newline → remove
    text = re.sub(r'\n ', '\n', text)          # space after newline → remove
    text = re.sub(r'\n+', '\n', text)          # multiple newlines → single newline
    
    # 2. Fix specific Sinhala character spacing issues (e.g., spaces between characters and modifiers)
    sinhala_modifiers = r'[\u0DCA\u0DCF\u0DD0\u0DD1\u0DD2\u0DD3\u0DD4\u0DD6\u0DD8\u0DD9\u0DDA\u0DDB\u0DDC\u0DDD\u0DDE\u0DDF\u0DF2\u0DF3]'
    text = re.sub(f' ({sinhala_modifiers})', r'\1', text)
    
    return text.strip()

def translate_text(text, target_lang="Sinhala", retries=2, delay=3):
    clean_text = text.strip()
    if not clean_text or re.match(r'^--==.*==--$', clean_text) or "moviesnipipay" in clean_text.lower():
        return text

    # Try each model in the list until one works
    for model in MODELS:
        prompt = f"Translate the following movie subtitle text into natural and accurate {target_lang}. Ensure there are no extra spaces between characters or within words. Only return the translated text: {clean_text}"
        encoded_prompt = quote(prompt)
        # Assuming the API uses 'model' parameter to switch models
        api_url = f"{API_BASE}?apikey={API_KEY}&model={model}&q={encoded_prompt}"

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(api_url, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") is True:
                        translated = data.get("response", "").strip()
                        if translated:
                            return clean_translation(translated)
                    
                    print(f"[!] Model '{model}' returned unexpected structure. Trying next model...")
                    break # Break inner loop to try next model

                elif response.status_code == 429:
                    wait = delay * attempt
                    print(f"[!] Rate limited on '{model}'. Waiting {wait}s...")
                    time.sleep(wait)
                
                elif response.status_code == 401:
                    print("[!] Invalid API key. Stopping.")
                    return text

                else:
                    print(f"[!] HTTP {response.status_code} on model '{model}'. Trying next...")
                    break # Try next model

            except Exception as e:
                print(f"[!] Error with model '{model}': {e}")
                break # Try next model

    print(f"[!] All models failed for this block. Keeping original text.")
    return text


def process_srt(input_path, output_path, target_lang="Sinhala"):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\s*\n', content.strip())
    total = len(blocks)
    print(f"Total blocks to process: {total}")
    print(f"Using models: {', '.join(MODELS)} (Main: {MODELS[0]})")

    translated_blocks = []

    for i, block in enumerate(blocks):
        lines = block.split('\n')
        if len(lines) >= 3:
            header = lines[:2]
            text_to_translate = '\n'.join(lines[2:])
            translated_text = translate_text(text_to_translate, target_lang)
            translated_blocks.append('\n'.join(header + [translated_text]))
        else:
            translated_blocks.append(block)

        if (i + 1) % 5 == 0:
            print(f"Processed {i + 1}/{total} blocks...")

        time.sleep(0.2) # Reduced delay as we have multiple models

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))
    print(f"\nSuccess! Translated file saved to: {output_path}")


if __name__ == "__main__":
    # --- CONFIGURATION ---
    input_file = "Subtitles/Scissor.Seven.S05E05.1080p.NF.WEB-DL.DUAL.AAC2.0.H.srt"
    output_file = "Scissor.Seven.S05E05.1080p.NF.WEB-DL.DUAL.AAC2.0.H_sinhala.srt"
    target_language = "Sinhala"

    if os.path.exists(input_file):
        process_srt(input_file, output_file, target_language)
    else:
        print(f"Error: Could not find the input file at {input_file}")
