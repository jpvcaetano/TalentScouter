# TalentScouter

TalentScouter is an AI-powered tool that automates the process of analyzing and ranking CVs (resumes) for job positions using OpenAI's GPT models.

## Features

- PDF CV processing and analysis
- Automated comparison against job criteria
- AI-powered candidate ranking
- Detailed candidate assessment reports
- CSV output for easy review

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/talentscouter.git
cd talentscouter
```

2. Install dependencies:

``` bash
poetry install
```

3. Create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key
```

## Configuration

The application can be configured through `config/config.yaml`. Key settings include:

- CV folder path
- Job criteria file path
- Output folder path
- OpenAI model settings
- Number of top candidates to select

## Usage

1. Place CV files (PDF format) in the configured CV folder
2. Create a criteria.txt file with the job requirements
3. Run the tool:

```bash
poetry run talentscouter
```

## Output

The tool generates two CSV files in the output folder:
- `candidates_summary.csv`: Initial analysis of all candidates
- `ranked_candidates.csv`: Final ranking and detailed assessment of top candidates

## Project Structure

talentscouter/
├── config/
│ └── config.yaml
├── src/
│ ├── main.py
│ ├── file_handler.py
│ ├── cv_processor.py
│ └── gpt_analyzer.py
├── tests/
├── poetry.lock
├── pyproject.toml
└── README.md

## Development

To contribute to the project:

1. Install development dependencies:

```bash
poetry install --with dev
```

2. Run tests:

```bash
poetry run pytest
```

3. Format code:

```bash
poetry run black .
```

4. Lint code:

```bash
poetry run isort .
```

4. Run linter:

```bash
poetry run flake8 
```


## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
