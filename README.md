\# TraceLens AI 🔍



\*\*A local AI debugging assistant that investigates failing tests, proposes code fixes, and validates them before applying them.\*\*



\## ✨ Features



\- 🔎 Automatically discovers Python tests and source files.

\- 🧪 Runs tests and collects failure evidence.

\- 🤖 Uses a locally running AI model through Ollama.

\- 🛠️ Generates a proposed code repair.

\- ✅ Validates patches by running tests in a temporary copy.

\- 🔄 Applies validated patches and rolls back changes if tests fail.

\- 🔒 Runs locally without paid AI APIs.



\## ⚙️ Requirements



\- Python

\- \[Ollama](https://ollama.com/)

\- The `llama3.2:3b` model



\## 🚀 Setup



Clone the repository:



```bash

git clone https://github.com/hibat-errahmane/TraceLens.git

cd TraceLens

