# GraphRAG-Based Critical Care Question Answering

## Overview
This project leverages **GraphRAG**, an advanced Retrieval-Augmented Generation (RAG) framework, to answer critical care-related medical questions. The system builds and queries knowledge graphs using medical documents on **ARDS (Acute Respiratory Distress Syndrome)** and **Sepsis**, providing accurate responses supported by evidence from research papers. The results are evaluated through various metrics to ensure quality and reliability.

## Features
- **Knowledge Graph Generation:** Create and visualize graphs that map relationships between medical concepts.
- **Querying System:** Answer questions in two modes (Local and Global) for specific or comprehensive responses.
- **Evaluation Metrics:** Evaluate answers using Human Rating, GPT Rating, ROUGE, and BLEU.
- **State-of-the-Art GPT Models:** Incorporates the latest **GPT-4o** for superior performance.

## Folder Structure
```
|– input/
|   |– doc_0.txt
|   |– doc_1.txt
|   |– …
|   |– doc_23.txt
|– settings.yaml
|– output/
|– prompts/
```

### Explanation
1. **input/**: Stores research papers in `.txt` format organized into categories (e.g., ARDS, Sepsis).
2. **settings.yaml**: Configuration file for GraphRAG, including API keys and model settings.
3. **output/**: Contains query responses and generated graphs.

## Installation
1. Install the required library:
```bash
pip install graphrag
```

## Setup
1. Initialize GraphRAG
Run the following command to initialize GraphRAG:
```bash
python -m graphrag.index --root . --init
```
Ensure your settings.yaml file is configured with the correct API keys for OpenAI or Azure OpenAI. The project uses GPT-4o, the latest GPT model.

2. Prepare Input Data

	1. Create an input/ folder:
	    ```bash
	    mkdir input
	    ```
	2. Extract research papers from Wiki Journal Club related to ARDS and Sepsis.
	3. Save each paper as a .txt file in the respective subfolder (e.g., doc_*.txt).

3. Create Knowledge Graphs

	Run the following command to generate knowledge graphs from the input data:
	```bash
	python -m graphrag.index --root .
	```

4. Query the System
	Ask questions using Local or Global search modes:
	```bash
	python -m graphrag.query --root . --method local "Your_Question"
	python -m graphrag.query --root . --method global "Your_Question"
	```

5. Evaluate the Results

	The responses are evaluated using:
	- Human Rating
	- GPT Rating
	- ROUGE-L
	- BLEU
