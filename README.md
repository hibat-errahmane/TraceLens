# TraceLens AI 🔍

**A local AI debugging assistant that investigates failing tests, proposes code fixes, and validates them before applying them.**

TraceLens helps Python developers investigate test failures using evidence and local AI. Instead of stopping at an error explanation, it can propose a repair and check whether the tests pass.

## ✨ Features

- 🔎 Discovers Python test files and source files.
- 🧪 Runs tests and captures output, failures, and timeouts.
- 🤖 Uses a local AI model through Ollama.
- 🛠️ Generates proposed code repairs.
- ✅ Validates proposed patches in a temporary project copy.
- 🔄 Supports applying patches and rolling back changes when validation fails.
- 🔒 Works without paid AI APIs.

## ⚙️ Requirements

- Python 3.14.7 (the version used during development).
- [Ollama](https://ollama.com/)
- The `llama3.2:3b` model.

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/hibat-errahmane/TraceLens.git
cd TraceLens
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies listed in the repository's requirements file, if provided:

```powershell
pip install -r requirements.txt
```

### 4. Download the AI model

Install Ollama from https://ollama.com/ and run:

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting TraceLens.

## ▶️ Run TraceLens

From the project root:

```powershell
python run_tracelens.py
```

TraceLens runs an investigation using the included demonstration project, which contains an intentionally incorrect `calculate_total` function.

## 🧪 Run the Unit Tests

In PowerShell, from the project root:

```powershell
$env:PYTHONPATH = ".\src"
python -m unittest discover -s tests -v
```

## 🧠 How It Works

1. **Discover:** Find Python tests and identify a supported test framework.
2. **Test:** Execute the tests and capture their results.
3. **Investigate:** Collect relevant source code and failure evidence.
4. **Diagnose:** Use the local AI model to analyze the evidence.
5. **Repair:** Generate a proposed code patch.
6. **Validate:** Run tests against the proposed patch in a temporary copy.
7. **Protect:** The patch application workflow supports rollback if validation fails.

**AI investigates. Tests decide.**

## 🔐 Privacy and Cost

TraceLens is designed to use a local AI model rather than a paid hosted AI API. Model downloads and local execution still require disk space and computing resources.

## ⚠️ Limitations

- The current implementation is primarily designed for Python projects.
- AI-generated patches can be incorrect and should be reviewed.
- Passing tests does not guarantee that every bug is fixed.
- Unusual project layouts or test configurations may require additional support.
- Local model speed and diagnosis quality depend on the available hardware and model.

## 🛣️ Future Improvements

- Broader test-framework support.
- Improved patch review and explanations.
- More integration tests across project layouts.
- Support for additional programming languages.

## 📄 License

See the repository for license information.
