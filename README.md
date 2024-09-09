# Multimodal LLM Testing Instruction Generator

This repository contains a **Streamlit** web application that generates detailed, step-by-step testing instructions for digital product features. It uses **LangChain**, **Google Gemini-1.5-pro**, and **LLMChain** to process uploaded screenshots and optional context, creating comprehensive test guides.

## Features

- **Screenshot Upload**: Upload multiple screenshots representing product features.
- **Context Input**: Optionally provide additional context to improve instruction accuracy.
- **Automatic Test Guide Generation**: Generates testing instructions using the LLM based on the context and screenshots.
- **Downloadable Instructions**: Download generated instructions as a text file.

## Prompting Strategy

The application prompts the LLM with structured templates for generating testing instructions. The prompt includes:

- **Example Test Cases**: To guide the format and structure of the generated output.
- **Contextual Information**: Screenshots and optional context are integrated into the prompt.
- **Test Case Structure**: Clear instructions to the LLM on how to format the output, including pre-conditions, steps, and expected results for each test case.

## Screenshots

1. Upload screenshots and provide optional context.
   Sample optional context:The app allows users to book intercity travel by selecting their journey details (source, destination, date), browsing buses, picking seats, and reviewing offers. The goal is to create a set of test cases based on screenshots to verify the correct functionality of the features.
  
3. **Generated Instructions**: 
   - View the detailed testing instructions generated based on uploaded screenshots.
   

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/rashibatra78/multimodal-llm-testing-instruction-generator.git
    ```

2. Navigate to the project directory:
    ```bash
    cd multimodal-llm-testing-instruction-generator
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add your Google API Key to the `.env` file:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

5. Run the application:
    ```bash
    streamlit run app.py
    ```

6. Open your browser and go to:
    ```
    http://localhost:8501
    ```
