import os
import json

def load_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    start, text_len = 0, len(text)
    chunks = []
    chunk_id = 1
    while start < text_len :
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            'chunk_id': chunk_id,
            'text': chunk.strip()
        })
        chunk_id+=1
        start = end - overlap
    
    return chunks

def save_chunks(chunks: list, output_path: str) -> None:
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(chunks, file, indent=4, ensure_ascii=False)
    print(f"File saved to {output_path}")


if __name__ == "__main__":
    input_file = os.path.join("..","data", "processed", "TN traffic rules.txt")
    output_file = os.path.join("..","data", "processed", "TN_traffic_rules_chunks.json")

    try:
        text = load_text(input_file)
        chunks = chunk_text(text)
        save_chunks(chunks, output_file)
    except Exception as e:
        print(f"Error: {e}")