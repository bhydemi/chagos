import os
import pymupdf4llm


def save_images_from_pdf(pdf_path, image_output_folder):
    """Extracts and saves images from a PDF using pymupdf4llm.to_markdown()."""
    try:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_image_dir = os.path.join(image_output_folder, pdf_name)
        os.makedirs(pdf_image_dir, exist_ok=True)

        pymupdf4llm.to_markdown(
            doc=pdf_path, write_images=True, image_path=pdf_image_dir
        )

        image_paths = [
            os.path.join(pdf_image_dir, f)
            for f in os.listdir(pdf_image_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        return image_paths
    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")
        return []
