import os
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key is missing. Set the OPENAI_API_KEY environment variable."
    )

# Define paths
ZIP_FILE_PATH = "pdf_files.zip"
EXTRACTION_FOLDER = "extracted_pdfs"
OUTPUT_JSON_PATH = "all_extracted_data.json"
IMAGE_OUTPUT_FOLDER = "extracted_images"
FAILED_PDFS_PATH = "failed_pdfs.txt"

response_schemas = [
    ResponseSchema(
        name="file_name",
        description="Original PDF name; if unavailable, return 'Unknown'.",
    ),
    ResponseSchema(
        name="brand",
        description="Brand from intermediate folder; if unavailable, return 'Unknown Manufacturer'.",
    ),
    ResponseSchema(
        name="product_name",
        description="Official product name; if not found, return 'Not Specified'.",
    ),
    ResponseSchema(
        name="product_code",
        description="Unique product identifier; if unavailable, return 'N/A'.",
    ),
    ResponseSchema(
        name="revision_number",
        description="Document revision/version; if missing, return 'Not Available'.",
    ),
    ResponseSchema(
        name="document_date",
        description="Publication or update date (YYYY-MM-DD); if missing, return 'Date Not Provided'.",
    ),
    ResponseSchema(
        name="properties",
        description="List of technical specifications; if unspecified, return [].",
    ),
    ResponseSchema(
        name="application_area",
        description="Intended industry use; if not mentioned, return 'General Use'.",
    ),
    ResponseSchema(
        name="material_composition",
        description="Primary materials used; if unknown, return 'Composition Not Specified'.",
    ),
    ResponseSchema(
        name="physical_properties",
        description="Physical characteristics; if not provided, return {}.",
    ),
    ResponseSchema(
        name="available_sizes",
        description="List of available sizes; if none, return [].",
    ),
    ResponseSchema(
        name="color_options",
        description="Available color options; if unspecified, return 'Standard Color'.",
    ),
    ResponseSchema(
        name="coating_finish",
        description="Surface coating/finishing; if missing, return 'No Special Coating'.",
    ),
    ResponseSchema(
        name="storage_conditions",
        description="Storage guidelines; if not specified, return 'Standard Storage Conditions'.",
    ),
    ResponseSchema(
        name="shelf_life",
        description="Expected shelf life; if not available, return 'No Expiration Specified'.",
    ),
    ResponseSchema(
        name="environmental_impact",
        description="VOC emissions/sustainability; if missing, return 'Environmental Impact Not Provided'.",
    ),
    ResponseSchema(
        name="disposal_information",
        description="Waste/disposal guidelines; if unspecified, return 'Follow Local Regulations'.",
    ),
    ResponseSchema(
        name="safety_warnings",
        description="Hazard warnings; if none, return 'No Known Safety Risks'.",
    ),
    ResponseSchema(
        name="mixing_instructions",
        description="Mixing/preparation instructions; if not applicable, return 'Ready-to-Use'.",
    ),
    ResponseSchema(
        name="application_method",
        description="Application techniques; if unspecified, return 'General Application Methods'.",
    ),
    ResponseSchema(
        name="substrate_requirements",
        description="Surface preparation details; if not provided, return 'Standard Substrate Conditions'.",
    ),
    ResponseSchema(
        name="standards_met",
        description="Industry compliance details; if unknown, return 'No Standards Specified'.",
    ),
    ResponseSchema(
        name="certifications",
        description="Regulatory certifications; if not found, return [].",
    ),
    ResponseSchema(
        name="manufacturer_contact",
        description="Contact details; if unavailable, return 'No Contact Information Provided'.",
    ),
    ResponseSchema(
        name="documentation_url",
        description="Link to technical document; if missing, return 'No Document URL Available'.",
    ),
    ResponseSchema(
        name="product_image",
        description="Paths to extracted product images; if none, return [].",
    ),
]

BATCH_SIZE = 10
NUM_WORKERS = min(8, os.cpu_count() or 1)
