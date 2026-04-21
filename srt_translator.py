import re
import os
import requests
import time
from urllib.parse import quote

API_KEY = "Bitx-Jithula2356"
API_BASE = "https://bit-x-apis.vercel.app/talkai"

def translate_text(text, target_lang="Sinhala", retries=3, delay=5):
    clean_text = text.strip()
    if not clean_text or re.match(r'^--==.*==--$', clean_text) or "moviesnipipay" in clean_text.lower():
        return text

    prompt = f"Translate the following movie subtitle text into natural and accurate {target_lang}. Only return the translated text: {clean_text}"
    encoded_prompt = quote(prompt)
    api_url = f"{API_BASE}?apikey={API_KEY}&q={encoded_prompt}"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(api_url, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get("status") is True:
                    translated = data.get("response", "").strip()
                    if translated:
                        return translated
                print(f"[!] Unexpected response structure: {data}")
                return text

            elif response.status_code == 429:
                wait = delay * attempt
                print(f"[!] Rate limited. Waiting {wait}s before retry {attempt}/{retries}...")
                time.sleep(wait)

            elif response.status_code == 401:
                print("[!] Invalid API key. Please check your credentials.")
                return text

            else:
                print(f"[!] HTTP {response.status_code} on attempt {attempt}/{retries}")
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"[!] Timeout on attempt {attempt}/{retries}. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"[!] Error on attempt {attempt}/{retries}: {e}")
            time.sleep(delay)

    print(f"[!] All {retries} attempts failed. Keeping original text.")
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

        time.sleep(0.5)  # polite delay between requests

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))
    print(f"\nSuccess! Translated file saved to: {output_path}")


if __name__ == "__main__":
    input_file = "Subtitles/Fast.X.2023.720p.WEBRip.x264.AAC-[YTS.MX].srt"
    output_file = "Fast.X.2023.720p.WEBRip.x264.AAC-[YTS.MX]_sinhala.srt"
    target_language = "Sinhala"

    process_srt(input_file, output_file, target_language)