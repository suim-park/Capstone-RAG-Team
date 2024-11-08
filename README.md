# Capstone-RAG-Team
Capstone Github Repository for RAG Team with Duke University School of Medicine
* **Team Name**: RAG Team
* **Executive Sponsor**: Dr. Ian Wong (a.ian.wong@duke.edu)
* **Mentor Instructor**: Dr. Yue Jiang (yue.jiang@duke.edu)
* **Team Member**: Yun-chung (Murphy) Liu, Keon Narty, Suim Park, Bob Zhang

## Project Overview
This project aims to develop and deploy a chatbot for critical care using a GraphRAG-based approach. By storing and indexing published journal articles on critical care, the chatbot will provide responses based on verified sources, ensuring that medical teams access current, reliable information. Leveraging GraphRAG will address many limitations of standard large language models (LLMs) by grounding responses in specific articles, helping to reduce hallucinations, minimize reliance on potentially outdated guidelines, and improve transparency. Furthermore, by sourcing responses directly from the most recent medical literature, the chatbot can offer accurate, up-to-date information while respecting patient privacy and ensuring that all answers are easily verifiable.

## Background

As the number of research papers and guidelines increase, it becomes a tremendous burden for physicians to stay up-to-date to make informed decisions faced with various clinical conditions. The main object for this project is the development of an evidence-based medical question answering model for clinical use.

## Example Question 

Among patients with septic shock and relative adrenal insufficiency, do corticosteroids reduce 28-day mortality?


<img width="1108" alt="Screenshot 2024-11-08 at 1 32 33 PM" src="https://github.com/user-attachments/assets/f7203589-b6f3-42e0-b7d6-a49f80aae050">

Some research papers tend to agree with the question being asked whiles some disagree, but ultimately depends on the patient being treated by the physician and which of the study closely aligns to the patient.

## Outline

>- [Dataset](https://www.wikijournalclub.org/wiki/WikiJournalClub:Usable_articles#Critical_Care)
>- The GraphRAG Model
>- Evaluation Metrics
>- A Small GraphRAG Experiment
>- Results
>- Next Steps

## The GraphRag Model


<img width="538" alt="Screenshot 2024-11-08 at 1 47 23 PM" src="https://github.com/user-attachments/assets/5bb925fa-1fa3-49c5-8215-0b3dd8a1894b">

## Experiment

talk about experiment

## Results

Insert Visualisation here

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

### 4_Reports_Presentations
Documentation and presentation materials from the capstone project, including interim and final reports as well as presentations, are uploaded here to chronicle the project’s development and key milestones.
