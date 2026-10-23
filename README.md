# PPT Language Translation

A Python-based web application that extracts text from a PowerPoint presentation and translates it from English to Hindi using Deep Translator and Google Translator.

## Problem Statement

Users may receive PowerPoint presentation files in English, but they may need the content in Hindi for better understanding or presentation purposes. In many cases, students, teachers, and professionals have to manually translate the text of each slide. This process becomes difficult when the presentation contains a large number of slides. Therefore, there is a need for an automatic system that can extract text from PPT slides and translate it from English to Hindi quickly and accurately.

## Project Description

This project allows users to upload a PowerPoint presentation and automatically translates the text present in the slides from English to Hindi. The application extracts text from each slide using the python-pptx library. The extracted English text is then translated into Hindi using Deep Translator and Google Translator.

The project was first developed and tested in Google Colab. Later, the same logic was used to create a Streamlit web application. The application was connected to GitHub for deployment.

## Features

- Upload PowerPoint presentation file
- Extract text from each slide
- Translate English text into Hindi
- Display translated text slide by slide
- Simple and user-friendly web interface
- Developed using Python and Streamlit

## Technologies Used

- Python
- python-pptx
- Deep Translator
- Google Translator
- Streamlit
- Google Colab
- GitHub

## Workflow

1. User opens the PPT Language Translation application.
2. User uploads a PowerPoint presentation file.
3. The application reads the PPT file using python-pptx.
4. Text is extracted from each slide.
5. Extracted English text is translated into Hindi.
6. Translated Hindi text is displayed to the user.

## How to Run

1. Clone this repository:
   ```bash
   git clone <your-repository-link>
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Requirements

```text
streamlit
python-pptx
deep-translator
googletrans
```

## Output

- PowerPoint presentation is uploaded successfully.
- Text is extracted from all slides.
- English text is translated into Hindi.
- Translated Hindi text is displayed slide by slide.

## Live Application

[https://pragyanaipythonprojectpptlanguagetranslation-o7ju9gj9hw7tn6dvu.streamlit.app/]

## Future Scope

- Add support for more languages
- Add option to download the translated PPT file
- Add translation of tables, charts, and images
- Improve translation accuracy
- Add support for
