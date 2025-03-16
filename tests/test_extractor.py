import os
import json
from pathlib import Path

import pytest

from config import response_schemas

from extractor.pdf_text_extractor import (
    process_pdf_text,
    get_response_schema_and_parser,
    extract_brand_from_path,
    extract_text_from_pdf,
)
from extractor.pdf_image_extractor import save_images_from_pdf
from extractor.zip_extractor import extract_zip
from extractor.pdf_getter import get_pdf_files
from extractor.pdf_image_extractor import save_images_from_pdf

from langchain_openai import ChatOpenAI


def test_extract_brand_from_nested_path(tmp_path):
    """
    Test whether extract_brand_from_path() correctly extracts the folder name
    from a nested structure like:

        tmp_path / "sample_pdf" / "sample_brand" / "TM_MineraDeck.pdf"
    """
    # Create a nested folder structure in a temporary directory
    sample_pdf_folder = tmp_path / "sample_pdf"
    sample_pdf_folder.mkdir()

    sample_brand_folder = sample_pdf_folder / "sample_brand"
    sample_brand_folder.mkdir()

    pdf_file = sample_brand_folder / "TM_MineraDeck.pdf"
    pdf_file.touch()  # Create an empty file

    # The base_folder is the top-level from which we want to extract the brand
    base_folder = str(tmp_path / "sample_pdf")
    brand_name = extract_brand_from_path(str(pdf_file), base_folder)

    # Because the code calls `.capitalize()`, "sample_brand" becomes "Sample_brand"
    assert brand_name == "Sample_brand"


def test_extract_text_from_pdf_invalid(tmp_path):
    """
    Test that extract_text_from_pdf() gracefully returns None
    when the PDF does not exist.
    """
    invalid_pdf = tmp_path / "nonexistent.pdf"
    text = extract_text_from_pdf(str(invalid_pdf))
    assert text is None


def test_process_pdf_text_with_nested_structure(monkeypatch, tmp_path):
    """
    Test process_pdf_text() end-to-end with a nested folder structure.
    We monkeypatch PDF text extraction and LLM calls to avoid external dependencies.
    """
    # 2. Monkeypatch extract_text_from_pdf to return dummy text
    from extractor import pdf_text_extractor

    def dummy_extract_text(pdf_path):
        return "Dummy PDF text for testing brand extraction and structured data."

    monkeypatch.setattr(pdf_text_extractor, "extract_text_from_pdf", dummy_extract_text)

    # 3. Monkeypatch the LLM call (ChatOpenAI.invoke) to return a valid JSON string
    class DummyResponse:
        def __init__(self, content):
            self.content = content

    def dummy_invoke(messages):
        # Simulate a minimal JSON matching the required schema
        dummy_json = {
            "file_name": "TM_MineraDeck.pdf",
            "brand": "Sample_brand",
            "product_name": "Test Product",
            "product_code": "12345",
            "revision_number": "1.0",
            "document_date": "2023-01-01",
            "properties": [],
            "application_area": "General Use",
            "material_composition": "Some Material",
            "physical_properties": {},
            "available_sizes": [],
            "color_options": "Standard Color",
            "coating_finish": "No Special Coating",
            "storage_conditions": "Standard Storage Conditions",
            "shelf_life": "No Expiration Specified",
            "environmental_impact": "Environmental Impact Not Provided",
            "disposal_information": "Follow Local Regulations",
            "safety_warnings": "No Known Safety Risks",
            "mixing_instructions": "Ready-to-Use",
            "application_method": "General Application Methods",
            "substrate_requirements": "Standard Substrate Conditions",
            "standards_met": "No Standards Specified",
            "certifications": [],
            "manufacturer_contact": "No Contact Information Provided",
            "documentation_url": "No Document URL Available",
            "product_image": [],
        }
        return DummyResponse(json.dumps(dummy_json))

    monkeypatch.setattr(
        ChatOpenAI, "invoke", lambda self, messages: dummy_invoke(messages)
    )

    # 4. Get format_instructions and output_parser
    format_instructions, output_parser = get_response_schema_and_parser(
        response_schemas
    )

    # 5. Run process_pdf_text
    structured_output = process_pdf_text(
        pdf_path="sample_pdf/sample_brand/TM_MineraDeck.pdf",
        extraction_folder="sample_pdf",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        format_instructions=format_instructions,
        output_parser=output_parser,
    )

    # 6. Verify the brand name was extracted properly from the nested folder
    assert structured_output is not None
    assert structured_output["file_name"] == "TM_MineraDeck.pdf"
    assert structured_output["brand"] == "Sample_brand"


def test_save_images_from_pdf(monkeypatch, tmp_path):
    """
    Test save_images_from_pdf() by mocking out the pymupdf4llm.to_markdown call
    and simulating the creation of an image file.
    """
    from extractor import pdf_image_extractor

    # 1. Create a dummy PDF
    pdf_file = tmp_path / "dummy.pdf"
    pdf_file.touch()

    # 2. Create an output folder for images
    image_output_folder = tmp_path / "images"
    image_output_folder.mkdir()

    # 3. Mock out pymupdf4llm.to_markdown to simulate image extraction
    def dummy_to_markdown(doc, write_images, image_path):
        dummy_image = os.path.join(image_path, "dummy.jpg")
        with open(dummy_image, "w") as f:
            f.write("fake image bytes")

    monkeypatch.setattr(
        pdf_image_extractor,
        "pymupdf4llm",
        type("MockModule", (), {"to_markdown": dummy_to_markdown}),
    )

    # 4. Call save_images_from_pdf
    extracted_images = save_images_from_pdf(str(pdf_file), str(image_output_folder))

    # 5. Verify that the mocked image file was "extracted"
    assert len(extracted_images) == 1
    assert "dummy.jpg" in extracted_images[0]
