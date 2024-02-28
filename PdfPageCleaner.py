import os
import fitz  # PyMuPDF

def delete_blank_pages(pdf_document):
    non_blank_pages = []
    for page_num in range(len(pdf_document)):
        page_text = pdf_document[page_num].get_text().strip()
        if page_text:
            non_blank_pages.append(page_num)
    return non_blank_pages

def delete_pages_with_few_words(pdf_document, threshold):
    pages_to_keep = []
    for page_num in range(len(pdf_document)):
        page_text = pdf_document[page_num].get_text().strip()
        word_count = len(page_text.split())
        if word_count >= threshold:
            pages_to_keep.append(page_num)
    return pages_to_keep

def main():
    # Input PDF file path
    pdf_path = input("Enter the path to the PDF file: ")

    # Create a directory for the modified PDF
    output_folder = os.path.splitext(os.path.basename(pdf_path))[0] + "_modified"
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Delete blank pages
    non_blank_pages = delete_blank_pages(pdf_document)

    # Ask user for word count thresholds
    threshold_20 = int(input("Enter the word count threshold (for deletion) for pages (default: 20): ") or "20")
    threshold_10 = int(input("Enter the word count threshold (for deletion) for pages (default: 10): ") or "10")
    threshold_5 = int(input("Enter the word count threshold (for deletion) for pages (default: 5): ") or "5")

    # Delete pages with fewer words than the specified thresholds
    pages_to_keep = delete_pages_with_few_words(pdf_document, threshold_20)
    pages_to_keep = delete_pages_with_few_words(pdf_document, threshold_10)
    pages_to_keep = delete_pages_with_few_words(pdf_document, threshold_5)

    # Combine page lists and remove duplicates
    pages_to_keep = list(set(pages_to_keep + non_blank_pages))

    # Write modified PDF to a new file
    output_pdf_path = os.path.join(output_folder, "modified.pdf")
    pdf_document.select(pages_to_keep)
    pdf_document.save(output_pdf_path)

    print("Modified PDF created in:", output_folder)

if __name__ == "__main__":
    main()
