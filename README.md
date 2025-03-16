
# chagos-pdf-extractor

A robust PDF extraction tool that leverages AI-powered LLM processing to extract structured data and images from technical PDFs.

---

## **Features**

- ✔ **Extract structured data** from technical PDFs (e.g., product names, specs, dates).
- ✔ **AI-powered LLM processing** (using OpenAI GPT-4o-mini) to parse and structure content.
- ✔ **Extracts & saves images** from PDFs.
- ✔ **Handles bulk PDF extraction** with parallel processing.
- ✔ **Configurable via CLI** (supports custom ZIP files & output paths).
- ✔ **Built for production** using `Poetry`, `pytest`, and `GitHub Actions`.

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

*Additional CLI options allow you to override the extraction folder, image output folder, batch size, and number of workers.*

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

Use the following command to run the automated test suite:
```bash
poetry run pytest tests/
```

---

## **📜 Environment Variables (`.env`)**

Create a `.env` file in the project root and add:
```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
🚀 **Do not commit this file!** (It is already added to `.gitignore`.)

---

## **📌 Key Technologies Used**

- **LangChain** → AI-powered document parsing
- **OpenAI** → Extracts structured information using GPT-4o-mini
- **PyMuPDF4LLM** → PDF text & image extraction
- **Poetry** → Dependency management and packaging
- **pytest** → Automated testing
- **GitHub Actions** → CI/CD pipeline for testing and deployment

---

## **⚙ CI/CD Pipeline**

The project uses GitHub Actions for continuous integration and deployment. The CI/CD pipeline:

- Runs tests on every push and pull request.
- Blocks pull requests from merging if tests are not passing (via branch protection rules).
- On release creation, it builds (and optionally publishes) the package.
- Loads sensitive credentials (like `OPENAI_API_KEY`) from repository secrets.

*Workflow file location: `.github/workflows/ci-cd.yml`*

---

## **🤝 Contributing**

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch** (`git checkout -b feature/my-new-feature`)
3. **Commit Your Changes** (`git commit -am 'Add new feature'`)
4. **Push to the Branch** (`git push origin feature/my-new-feature`)
5. **Create a Pull Request**

Make sure your code passes the tests by running `poetry run pytest`.


