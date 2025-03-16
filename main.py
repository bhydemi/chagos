import os
import json
import concurrent.futures
from config import (
    ZIP_FILE_PATH,
    EXTRACTION_FOLDER,
    OUTPUT_JSON_PATH,
    IMAGE_OUTPUT_FOLDER,
    FAILED_PDFS_PATH,
    OPENAI_API_KEY,
    response_schemas,
    BATCH_SIZE,
    NUM_WORKERS,
)
from extractor.pdf_text_extractor import (
    process_pdf_text,
    get_response_schema_and_parser,
)
from extractor.pdf_image_extractor import save_images_from_pdf
from extractor.zip_extractor import extract_zip
from extractor.pdf_getter import get_pdf_files


def main():
    # Ensure necessary directories exist
    os.makedirs(EXTRACTION_FOLDER, exist_ok=True)
    os.makedirs(IMAGE_OUTPUT_FOLDER, exist_ok=True)

    # Step 1: Extract PDFs from ZIP
    extract_zip(ZIP_FILE_PATH, EXTRACTION_FOLDER)

    # Get response format instructions and parser (for LLM output)
    format_instructions, output_parser = get_response_schema_and_parser(
        response_schemas
    )

    # Step 2: Process PDFs for text extraction in parallel
    pdf_files = get_pdf_files(EXTRACTION_FOLDER)
    print(f"Found {len(pdf_files)} PDF files.")

    batch_size = BATCH_SIZE  # Process in batches of 10
    num_workers = NUM_WORKERS
    all_extracted_data = []

    for i in range(0, len(pdf_files), batch_size):
        batch = pdf_files[i : i + batch_size]
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(
                executor.map(
                    lambda p: process_pdf_text(
                        p,
                        EXTRACTION_FOLDER,
                        OPENAI_API_KEY,
                        format_instructions,
                        output_parser,
                    ),
                    batch,
                )
            )
        all_extracted_data.extend([data for data in results if data])

    # Step 3: Process images sequentially after text extraction
    for pdf_path in pdf_files:
        saved_images = save_images_from_pdf(pdf_path, IMAGE_OUTPUT_FOLDER)
        if saved_images:
            pdf_name = os.path.basename(pdf_path)
            for item in all_extracted_data:
                if item.get("file_name") == pdf_name:
                    item["product_image"] = [
                        os.path.relpath(p, start=IMAGE_OUTPUT_FOLDER)
                        for p in saved_images
                    ]

    # Step 4: Save the extracted data into a JSON file
    try:
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
            json.dump(all_extracted_data, json_file, indent=4, ensure_ascii=False)
        print(f"All extracted data saved in: '{OUTPUT_JSON_PATH}'")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

    print("Processing complete.")


if __name__ == "__main__":
    main()
