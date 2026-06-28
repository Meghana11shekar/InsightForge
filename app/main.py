from app.pdf.parser import extract_text
import os

pdf_path = "data/uploads/sample.pdf"

text, pages = extract_text(pdf_path)

filename = os.path.basename(pdf_path)

print("=" * 50)
print("📄 InsightForge - PDF Analysis")
print("=" * 50)

print(f"File: {filename}")
print(f"Pages: {pages}")
print(f"Characters: {len(text)}")
print(f"Words: {len(text.split())}")

print("\n----- Preview -----\n")
print(text[:1000])
