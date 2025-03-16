# chagos-pdf-extractor

---

## ** Features**

✔ **Extract structured data** from technical PDFs (e.g., product names, specs, dates).
✔ **AI-powered LLM processing** (using OpenAI GPT-4o-mini).
✔ **Extracts & saves images** from PDFs.
✔ **Handles bulk PDF extraction** with parallel processing.
✔ **Configurable via CLI** (supports custom ZIP files & output paths).
✔ **Built for production** using `Poetry`, `pytest`, and `GitHub Actions`.

---

## **📂 Project Structure**

```
pdf_extractor/
├── extractor
│   ├── __init__.py
│   ├── pdf_text_extractor.py
│   ├── pdf_image_extractor.py
│   └── utils.py
├── config.py
├── main.py
├── sample_pdf
│   └── sample_brand
│       └── TM_MineraDeck.pdf
├── tests
│   └── test_extractor.py
├── pyproject.toml
└── README.md

```

---

## **🛠 Installation**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/bhydemi/pdf-extraction-parser.git
cd pdf-extraction-parser
```

### **2️⃣ Install Dependencies**
> 🚀 **Using Poetry for Dependency Management**
```bash
poetry install
```

---

## **🚀 Running the Extractor**

### **🔹 Run with Default Settings**
```bash
poetry run python main.py
```

### **🔹 Run with Custom Inputs**
```bash
poetry run python main.py --zip my_pdfs.zip --output extracted_data/output.json
```

---

## **📊 Example Output (`all_extracted_data.json`)**

```json
[
    {
        "file_name": "TechnicalDataSheet_Sto.pdf",
        "brand": "Sto",
        "product_name": "Sto-Übergangsprofil Keramik P",
        "product_code": "PROD3193",
        "revision_number": "Not Available",
        "document_date": "Date Not Provided",
        "properties": ["verschweißtes Kunststoffprofil", "integriertes Glasfasergewebe"],
        "application_area": "Übergang von Putz- zu Keramikflächen",
        "material_composition": "Kunststoff, Glasfaser",
        "storage_conditions": "Trocken lagern",
        "shelf_life": "No Expiration Specified",
        "manufacturer_contact": {
            "phone": "07744 57-0",
            "website": "www.sto.de"
        },
        "product_image": []
    }
]
```

---

## **🧪 Running Tests**

```bash
poetry run pytest tests/
```

---

## **📜 Environment Variables (`.env`)**

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
🚀 **Do not commit this file!** (It is already added to `.gitignore`.)

---

## **📌 Key Technologies Used**

- **LangChain** → AI-powered document parsing
- **OpenAI** → Extracts structured information
- **PyMuPDF4LLM** → PDF text & image extraction
- **Poet