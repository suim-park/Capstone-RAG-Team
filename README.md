# Capstone-RAG-Team

## Table of Contents

1.	[Abstract](#abstract)
2.	[Introduction](#introduction)
3.	[Methods](#methods)

  	3.1 [Dataset](#dataset)
  	
3.2 Knowledge Distillation
3.3 Anchor Method
3.4 Novel Method 
5.	Experiments
4.1. Experiments: Existing Methods
4.1.1. Experiment setup
4.1.2. Metrics
4.1.3. Models
4.1.4. Results
4.2. Experiments: Novel Method
4.2.1. Experiment setup 
6.	Conclusion
7.	Package
8.	Resources
9.	[Contributors](#contributors)

## Abstract

Our team is developing a chatbot powered by GraphRAG (Graph Retrieval-Augmented Generation) technology, utilizing data from Wiki Journal Club—a free, open-source dataset that includes papers from reputable medical journals. For example, under the topic of sepsis, Wiki Journal Club features five relevant papers. Of these, two suggest that corticosteroids may improve patient outcomes, while the other three present different perspectives without explicitly supporting or opposing this intervention. Physicians seeking guidance on treating sepsis and adrenal insufficiency must often review these documents individually, a time-consuming process that our chatbot aims to streamline.

Leveraging GraphRAG, our chatbot constructs a high-level knowledge graph that summarizes key findings across multiple research papers, synthesizing information to provide concise and reliable insights in response to specific queries. While summarizing complex medical data risks oversimplification, we mitigate this by collaborating closely with clinical experts to ensure that summaries are clinically relevant and contextually appropriate. This tool is not intended to replace a physician’s decision-making but rather to expedite information retrieval, enabling clinicians to make informed decisions more efficiently and confidently. By surfacing relevant, up-to-date research on demand, the chatbot aims to significantly reduce the time physicians spend on manual research, ultimately enhancing patient care.

## Introduction

The Hippocratic oath, "do no harm," stands as the ethical cornerstone of the medical profession. Physicians strive to uphold this oath in all aspects of their work, whether in the clinic, emergency room, or operating theater. Medicine is not practiced in isolation; rather, teams of physicians from various disciplines often collaborate to devise treatment plans for individual patients. These decisions are frequently informed by current research and clinical guidelines.

However, physicians face significant challenges in staying up-to-date with the latest clinical guidelines and research, particularly for critical conditions. Reading through extensive texts to understand study populations, methods, clinical presentations, and outcomes is a necessary but time-intensive task. In the modern age of artificial intelligence, vast amounts of data have been utilized to train models, though most medical research is not open-access due to the sensitive nature of patient data.

This project aims to build an AI chatbot powered by GraphRAG, using a knowledge graph to deliver accurate summaries. When queried by a physician, the chatbot will provide detailed responses regarding research methodologies, the alignment of methods to conclusions, and the relevance of the research to the patient being treated. An example question is; Among patients with septic shock and relative adrenal insufficiency, do corticosteroids reduce 28-day mortality?

<img width="1108" alt="Screenshot 2024-11-08 at 1 32 33 PM" src="https://github.com/user-attachments/assets/f7203589-b6f3-42e0-b7d6-a49f80aae050">


Some research papers tend to agree with the question being asked whiles some disagree, but ultimately depends on the patient being treated by the physician and which of the study closely aligns to the patient. Ultimately, when physicians consult research guidelines, they seek to understand how closely the study populations align with their current patients and how the research methods could benefit their patients. Our chatbot aims to deliver quick, reliable insights, saving physicians significant time and providing accurate answers to aid in patient treatment and ongoing research.

## Methods

## Dataset

<img width="538" alt="Screenshot 2024-11-08 at 1 47 23 PM" src="https://github.com/user-attachments/assets/5bb925fa-1fa3-49c5-8215-0b3dd8a1894b">



## Experiment

Two medical questions regarding Sepsis and ARDS (Acute respiratory distress syndrome, one question for each medical condition) were chosen for the experiment. Each question was based on one *source document* (research question of a scientific paper). The GraphRAG model was tested under two conditions (*aligned* and *conflicting*, detail below) and the **resulted answers were evaluated** using Human Rating, **GPT-4 Rating**, BLEU score and ROUGE-L score.

1. In the **aligned condition**, documents pointing to **aligned conclusions** were used to construct knowledge graph. Specifically, we used 1 (source), 3 (source + 1 document with **aligned** conclusion + 1 document with equivocal conclusion regarding the treatment), and 5 (source + 1 document with **aligned** conclusion + 3 documents with equivocal conclusion regarding the treatment) to build the knowledge graph. 

2. In the **conflicting condition**, documents pointing to **conflicting conclusions** were used to construct knowledge graph. Specifically, we used 1 (source), 3 (source + 1 document with **conflicting** conclusion + 1 document related to ARDS but irrelevant to the treatment), and 5 (source + 1 document with **conflicting** conclusion + 3 documents related to ARDS but irrelevant to the treatment) to build the knowledge graph. 

## Results
![Sepsis Visualization](2__Visualization/Visualization_Sepsis.png)
![ARDS Visualization](2__Visualization/Visualization_ARDS.png)

The visualizations illustrate the effects of adding aligned or conflicting research papers on the quality of answers generated by the GraphRAG model for Sepsis and ARDS-related questions. In the **aligned condition** (first graph), even when inconclusive documents are added, the answer quality increases with the number of documents. Conversely, in the **conflicting condition** (second graph), despite starting with a conflicting document and subsequently adding one aligned document plus three equivocal ones, the answer quality continues to decline, highlighting the negative impact of conflicting information on model performance.

## Detailed Map of the Repo
### 0__Documents
- **Documents**: Contains the documents for constructing GraphRAG. We extracted full text of research papers from the Critical Care section of Wiki Journal Club ([Link](https://www.wikijournalclub.org/wiki/WikiJournalClub:Usable_articles#Critical_Care)). To simplify the the code, extracted texts were saved them as .txt files named in the format `doc_*.txt`. 
- **Mapping Document**: The mapping document matches each document’s file name with its original paper title, providing an easy reference for all critical care documents.

### 1__Codes
The Codes section encompasses all scripts necessary for the end-to-end workflow, from GraphRAG processing to deployment on Azure. This includes data preprocessing, query handling, and indexing for GraphRAG, as well as configuration and automation for deploying the final model on Azure. Each script is structured to streamline and optimize the setup, allowing for efficient handling of critical care documents, interactive query responses, and scalable deployment.

### 2__Visualization
The Visualizations section includes comprehensive visual aids for understanding the project workflow, from data ingestion to query processing and deployment. It features images illustrating the main interface and interaction flow of the deployed chatbot, highlighting the process and results generated through GraphRAG. Additionally, this section will showcase outcome visuals, such as document summaries and insights derived from the critical care dataset, providing a clear and interactive view of how the chatbot functions and the insights it offers.

### 3__Output
The Output section presents detailed responses generated in answer to question queries, along with evaluation scores based on various rating methods. Each answer is accompanied by metrics that assess its quality, relevance, and accuracy. These evaluation scores are generated through pre-defined rating methods to provide insight into the chatbot’s performance, the reliability of responses, and areas for improvement. This section enables users to gauge the effectiveness of the model’s answers, ensuring that the system meets quality standards for critical care information delivery.

### 4_Reports_Presentations
Documentation and presentation materials from the capstone project, including interim and final reports as well as presentations, are uploaded here to chronicle the project’s development and key milestones.

## Contributors
Capstone Github Repository for RAG Team with Duke University School of Medicine

* **Team Name**: RAG Team
* **Executive Sponsor**: Dr. Ian Wong (a.ian.wong@duke.edu)
* **Mentor Instructor**: Dr. Yue Jiang (yue.jiang@duke.edu)
* **Team Member**: Yun-chung (Murphy) Liu, Keon Nartey, Suim Park, Bob Zhang
