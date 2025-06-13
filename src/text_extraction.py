import os
import PyPDF2

def extract_text_from_pdf(pdf_path: str) -> str:
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File Not Found: {pdf_path}")
    
    extracted_text = []

    with open(pdf_path , 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            # print(f"text: {text}")
            if text:
                extracted_text.append(text)
            else:
                print(f"Warning: Page {page_number} has no extractable text")
            
    return "\n".join(text.replace('\n', '') for text in extracted_text)



if __name__ == "__main__":
    pdf_file_path = os.path.join("..","data","TN traffic rules.pdf")

    try:
        text = extract_text_from_pdf(pdf_file_path)
        output_dir = os.path.join("..","data", "processed")
        os.makedirs(output_dir, exist_ok=True)

        output_file_path = os.path.join(output_dir, "TN_traffic_rules.txt")
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Extraction complete. Text saved to {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")
    