# Spectrum-Webmail-Assistant

Automate email management and spam filtering for Spectrum Webmail using Python, machine learning, and browser automation.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Machine Learning Details](#machine-learning-details)
- [Docker Support](#docker-support)
- [Customization](#customization)
- [Contributing](#contributing)

---

## Project Overview

Spectrum Webmail's interface is slow and cumbersome for bulk email management. This project automates mass deletion, spam filtering, and personal data collection for training custom spam filters. Originally built to help my gradma clear out thousands of emails to avoid running out of storage, it now includes a machine learning pipeline for spam detection and a modular Python codebase.

## Features

- **Automated Email Deletion:** Uses Selenium to mass-delete emails in Spectrum Webmail.
- **Spam Filtering:** Classifies and moves spam emails using an ensemble of ML models.
- **Custom Data Collection:** Interactive tool for labeling personal emails to improve spam detection.
- **IMAP Utilities:** Securely connects to mailboxes, fetches, and processes emails.
- **Text Preprocessing:** Cleans and transforms email text for analysis.
- **Model Training & Evaluation:** Jupyter notebook for training, evaluating, and saving ML models.
- **Dockerized Deployment:** Run the app in a container for easy setup.
- **Configurable Whitelist:** Avoids false positives by skipping whitelisted keywords.

## Architecture

```
app/
	main.py           # Entry point, runs spam filter
	emailDelete.py    # Selenium-based email deletion
	customData.py     # Collects and labels personal emails
	imapUtils.py      # IMAP connection and email processing
	spamFilter.py     # Spam classification and mailbox management
	model/
		Main.ipynb      # ML training and evaluation notebook
		data/           # Datasets for training
		trained/        # Saved models and vectorizer
		utils/
			classifySpam.py   # Loads models, classifies emails
			transformText.py  # Text preprocessing
			config.json       # Config file for state and whitelist
requirements.txt    # Python dependencies
Dockerfile          # Container setup
README.md           # Project documentation
```

## Setup & Installation

1. **Clone the repository:**
	 ```sh
	 git clone https://github.com/thayerh/Spectrum-Webmail-Assistant.git
	 cd Spectrum-Webmail-Assistant
	 ```

2. **Setup Virtual Environment**
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Install dependencies:**
	 ```sh
	 pip install -r requirements.txt
	 ```

3. **Set environment variables:**
	 - Create a `.env` file with:
		 ```
		 IMAP_SERVER=your.imap.server
		 EMAIL_ACCOUNT=your@email.com
		 EMAIL_PASSWORD=yourpassword
		 ```

4. **(Optional) Build Docker image:**
	 ```sh
	 docker build -t spectrum-webmail-assistant .
	 docker run --env-file .env spectrum-webmail-assistant
	 ```

## Usage

- **Spam Filtering:**  
	Run the main script to classify and move spam emails:
	```sh
	python app/main.py
	```

- **Bulk Email Deletion:**  
	Use Selenium automation:
	```sh
	python app/emailDelete.py
	```
	Follow the prompts in your browser.

- **Custom Data Collection:**  
	Label personal emails for improved spam detection:
	```sh
	python app/customData.py
	```

## Machine Learning Details

- **Models Used:** SVC, KNN, Naive Bayes, Logistic Regression, Random Forest, AdaBoost, Bagging, Extra Trees, Gradient Boosting.
- **Ensemble Voting:** Spam score is aggregated across models for robust classification.
- **Training Pipeline:** See `model/Main.ipynb` for data cleaning, feature extraction, model training, and evaluation (accuracy, precision).
- **Text Preprocessing:** Tokenization, stopword removal, stemming via NLTK.

## Docker Support

- The included `Dockerfile` allows for containerized deployment.
- All dependencies are installed, and the app runs with a single command.

## Customization

- **Whitelist:** Add keywords to `config.json` to prevent important emails from being marked as spam.
- **State Tracking:** The app tracks the last processed email to avoid duplicates.

## Contributing

Pull requests and suggestions are welcome! Please open an issue for major changes.
