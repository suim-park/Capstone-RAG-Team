# Capstone-RAG-Team
Capstone Github Repository for RAG Team with Duke University School of Medicine
* **Team Name**: RAG Team
* **Executive Sponsor**: Dr. Ian Wong (a.ian.wong@duke.edu)
* **Mentor Instructor**: Dr. Yue Jiang (yue.jiang@duke.edu)
* **Team Member**: Yun-chung (Murphy) Liu, Keon Narty, Suim Park, Bob Zhang

## Project Overview
This project aims to develop and deploy a chatbot for critical care using a GraphRAG-based approach. By storing and indexing published journal articles on critical care, the chatbot will provide responses based on verified sources, ensuring that medical teams access current, reliable information. Leveraging GraphRAG will address many limitations of standard large language models (LLMs) by grounding responses in specific articles, helping to reduce hallucinations, minimize reliance on potentially outdated guidelines, and improve transparency. Furthermore, by sourcing responses directly from the most recent medical literature, the chatbot can offer accurate, up-to-date information while respecting patient privacy and ensuring that all answers are easily verifiable.

## Instruction
### 0__Documents
- This section contains all the documents for GraphRAG. Each document is extracted from the Critical Care section of Wiki Journal Club ([Link](https://www.wikijournalclub.org/wiki/WikiJournalClub:Usable_articles#Critical_Care)). While documents on the website are presented as abbreviations, we have extracted the full text of each and saved them as .txt files named in the format `doc_*.txt`. This unified document set simplifies the GraphRAG process.
- **Mapping Document**: The mapping document matches each document’s file name with its original paper title, providing an easy reference for all critical care documents.

### 1__Codes
The Codes section encompasses all scripts necessary for the end-to-end workflow, from GraphRAG processing to deployment on Azure. This includes data preprocessing, query handling, and indexing for GraphRAG, as well as configuration and automation for deploying the final model on Azure. Each script is structured to streamline and optimize the setup, allowing for efficient handling of critical care documents, interactive query responses, and scalable deployment.

### 2__Visualization
The Visualizations section includes comprehensive visual aids for understanding the project workflow, from data ingestion to query processing and deployment. It features images illustrating the main interface and interaction flow of the deployed chatbot, highlighting the process and results generated through GraphRAG. Additionally, this section will showcase outcome visuals, such as document summaries and insights derived from the critical care dataset, providing a clear and interactive view of how the chatbot functions and the insights it offers.

### 3__Output
The Output section presents detailed responses generated in answer to question queries, along with evaluation scores based on various rating methods. Each answer is accompanied by metrics that assess its quality, relevance, and accuracy. These evaluation scores are generated through pre-defined rating methods to provide insight into the chatbot’s performance, the reliability of responses, and areas for improvement. This section enables users to gauge the effectiveness of the model’s answers, ensuring that the system meets quality standards for critical care information delivery.

## Report and Presentation
Documentation and presentation materials from the capstone project, including interim and final reports as well as presentations, are uploaded here to chronicle the project’s development and key milestones.
