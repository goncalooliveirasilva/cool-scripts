# Cool Scripts

Cool Scripts is a growing collection of small, handy automation tools written in **Python**, for speeding up repetitive or boring tasks.

## What's Inside

| Script                                       | Description                                                                                                                      |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [extract_pdf.py](./scripts/extract_pdf.py)   | Extracts specific pages from a PDF and saves them as a new file.                                                                 |
| [extract_text.py](./scripts/extract_text.py) | Extracts all text content from a PDF file with optional metadata.                                                                |
| [llm.py](./scripts/llm.py)                   | Interact with local LLMs via [Ollama](https://ollama.com/): send a prompt, view Markdown output, and optionally keep the result. |

## Installation

1. Clone this repo

```bash
git clone git@github.com:goncalooliveirasilva/cool-scripts.git
cd cool-scripts/
```

2. Install dependencies

```bash
uv sync
```

3. Run a script

```bash
uv run scripts/<script-name>.py [options]
```

## License

This project is licensed under the MIT License — feel free to use, modify, and share.
