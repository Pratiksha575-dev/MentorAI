import fitz
import os

pdf_path = r'C:\Users\Pratiksha\.gemini\antigravity\brain\5d001b22-8283-4272-9555-de07468e5b96\.user_uploaded\media_1791020005296.pdf'
doc = fitz.open(pdf_path)

os.makedirs('extracted_images', exist_ok=True)

img_count = 0
for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_filename = f"extracted_images/image_{page_num + 1}_{img_index + 1}.{image_ext}"
        with open(image_filename, "wb") as image_file:
            image_file.write(image_bytes)
        print(f"Extracted {image_filename}")
        img_count += 1

print(f"Total images extracted: {img_count}")
