# Bank AI Chat Assistant

## Introduction
This project implements a conversational AI Chat Assistant designed for Silicon Valley Bank to provide customer support and insights into transaction details. The assistant uses state-of-the-art NLP models and is integrated with AWS Bedrock to offer a seamless, context-aware user experience. This README provides an overview of the codebase, architecture, and functionality.

---

## Features

1. **Conversational Interaction**:
   - Builds on ongoing conversations.
   - Retains context for seamless, personalized responses.
2. **Transaction Queries**:
   - Handles customer transaction details such as date, description, deposit, withdrawal, and balance.
3. **Bank Services Information**:
   - Fetches accurate information from Silicon Valley Bank’s resources.
4. **Error Handling**:
   - Detects ambiguous queries and prompts for clarification.
   - Corrects grammatical and syntax errors.

---

## Code Overview

### 1. Dependencies
- **boto3**: For AWS session management.
- **LangChain**: For building conversational workflows.
- **Datetime**: For managing timestamps.

Install dependencies using:
```bash
pip install boto3 langchain
```

### 2. Core Classes and Methods

#### `ChatBot`
- **Initialization**:
  - Sets up an AWS Bedrock session with Claude 3.5 model integration.
- **Method**: `SearchAssistantAgent`
  - Processes user queries.
  - Maintains a memory buffer for contextual conversation.
  - Generates responses using LangChain prompts tailored to banking scenarios.

---

## Architecture

### Multi-Agent System
1. **Research Agent**: Gathers industry trends and identifies use cases.
2. **Use Case Agent**: Generates AI applications relevant to banking.
3. **Resource Agent**: Identifies datasets and tools for training models.
4. **Implementation Agent**: Integrates the AI assistant with APIs and deploys the solution.



## How to Run

1. **Set Up AWS Credentials**:
   - Configure AWS credentials using `aws configure` or specify a profile.
   - Update the `profile_name` in the code with your AWS profile.

2. **Run the Script**:
   ```bash
   python chatbot.py
   ```

3. **Input Details**:
   - Provide transaction details and user queries.

4. **Output**:
   - The chatbot responds with contextually relevant answers.

---

## Example Input/Output

### Input:
```plaintext
Date: 2025-01-10
Description: Grocery purchase
Deposit: 0.00
Withdraw: 150.00
Balance: 1850.00
Question: What is my current balance?
```

### Output:
```plaintext
Your current balance is $1850.00. Let me know if you need further assistance!
```

---

## Datasets and Tools
- **Datasets**:
  - Kaggle: [Bank Customer Data](https://www.kaggle.com/).
  - HuggingFace: Pre-trained models for financial NLP.
- **Libraries**:
  - HuggingFace Transformers.
  - TensorFlow or PyTorch for ML model fine-tuning.

---

## Future Enhancements
1. **Fraud Detection**: Implement ML algorithms for anomaly detection.
2. **Budgeting Assistance**: Provide automated expense categorization and savings tips.
3. **Internal Knowledge Base**: Develop a system for employee support and compliance.
