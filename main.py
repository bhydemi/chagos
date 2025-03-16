import os
import json
import concurrent.futures
import argparse

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
from extractor.pdf_text_extractor import process_pdf_text, get_response_schema_and_parser
from extractor.pdf_image_extractor import save_images_from_pdf
from extractor.zip_extractor import extract_zip
from extractor.pdf_getter import get_pdf_files


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract text and images from PDF files in a ZIP archive."
    )
    parser.add_argument(
        "--zip-file",
        default=ZIP_FILE_PATH,
        help="Path to the ZIP file containing PDFs (default: %(default)s)",
    )
    parser.add_argument(
        "--extraction-folder",
        default=EXTRACTION_FOLDER,
        help="Folder to extract PDFs (default: %(default)s)",
    )
    parser.add_argument(
        "--output-json",
        default=OUTPUT_JSON_PATH,
        help="Output JSON file path (default: %(default)s)",
    )
    parser.add_argument(
        "--image-output-folder",
        default=IMAGE_OUTPUT_FOLDER,
        help="Folder to store extracted images (default: %(default)s)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help="Number of PDFs to process in one batch (default: %(default)s)",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=NUM_WORKERS,
        help="Number of threads for parallel processing (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Ensure necessary directories exist
    os.makedirs(args.extraction_folder, exist_ok=True)
    os.makedirs(args.image_output_folder, exist_ok=True)

    # Step 1: Extract PDFs from ZIP
    extract_zip(args.zip_file, args.extraction_folder)

    # Get response format instructions and parser (for LLM output)
    format_instructions, output_parser = get_response_schema_and_parser(response_schemas)

    # Step 2: Process PDFs for text extraction in parallel
    pdf_files = get_pdf_files(args.extraction_folder)
    print(f"Found {len(pdf_files)} PDF files.")

    all_extracted_data = []

    for i in range(0, len(pdf_files), args.batch_size):
        batch = pdf_files[i : i + args.batch_size]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.num_workers) as executor:
            results = list(
                executor.map(
                    lambda p: process_pdf_text(
                        p,
                        args.extraction_folder,
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
        saved_images = save_images_from_pdf(pdf_path, args.image_output_folder)
        if saved_images:
            pdf_name = os.path.basename(pdf_path)
            for item in all_extracted_data:
                if item.get("file_name") == pdf_name:
                    item["product_image"] = [
                        os.path.relpath(p, start=args.image_output_folder)
                        for p in saved_images
                    ]

    # Step 4: Save the extracted data into a JSON file
    try:
        with open(args.output_json, "w", encoding="utf-8") as json_file:
            json.dump(all_extracted_data, json_file, indent=4, ensure_ascii=False)
        print(f"All extracted data saved in: '{args.output_json}'")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

    print("Processing complete.")


if __name__ == "__main__":
    main()
