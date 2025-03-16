import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_community.document_loaders.parsers.pdf import PyPDFParser
from langchain_core.documents.base import Blob


def extract_brand_from_path(pdf_path, base_folder):
    """Extracts the intermediate folder name as the brand name."""
    relative_path = os.path.relpath(pdf_path, base_folder)
    path_parts = relative_path.split(os.sep)
    return (
        path_parts[-2].capitalize() if len(path_parts) > 1 else "Unknown Manufacturer"
    )


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyPDFParser."""
    try:
        blob = Blob.from_path(pdf_path)
        parser = PyPDFParser(extraction_mode="plain")
        docs_lazy = parser.lazy_parse(blob)
        extracted_text = "\n".join([doc.page_content for doc in docs_lazy])
        return extracted_text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


def get_response_schema_and_parser(response_schemas):
    """Defines response schemas and returns format instructions and an output parser."""
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    return format_instructions, output_parser


def process_pdf_text(
    pdf_path, extraction_folder, openai_api_key, format_instructions, output_parser
):
    """Extracts text from a PDF and processes it using an LLM to return structured data."""
    filename = os.path.basename(pdf_path)
    brand_name = extract_brand_from_path(pdf_path, extraction_folder)

    try:
        extracted_text = extract_text_from_pdf(pdf_path)
        if not extracted_text:
            print(f"Skipping empty file: {filename}")
            return None

        llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="You are an expert in extracting structured data from technical PDFs."
                ),
                HumanMessage(
                    content="Extract the following information:\n"
                    + extracted_text
                    + "\n\n"
                    + format_instructions
                ),
            ]
        )

        response = llm.invoke(prompt.format_messages())
        response_text = (
            response.content if hasattr(response, "content") else str(response)
        )
        structured_output = output_parser.parse(response_text)
        structured_output["file_name"] = filename
        structured_output["brand"] = brand_name

        return structured_output

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        # Log the failure to a file in the current working directory
        with open(os.path.join(os.getcwd(), "failed_pdfs.txt"), "a") as f:
            f.write(f"{filename}\n")
        return None
