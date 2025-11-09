# Project Anna

**HackUTD 2025**

## 🚀 Overview  
Project Anna is an AI-powered web application that performs sentiment analysis on JSON data. It uses the **twitter-roberta-base-sentiment** model from Transformers and exposes a Flask server for real-time analysis.  
Key features:  
- Accepts flat or nested JSON files for processing.  
- Provides a REST-ful endpoint served via Flask.  
- Ideal for bulk sentiment tagging of posts, reviews, social data, etc.

## 🏗 Architecture  
1. **Model Loading**  
   - Uses model: `cardiffnlp/twitter-roberta-base-sentiment`  
   - Automatically detects & handles JSON structures (flat / nested)  
2. **Server**  
   - Built with Flask (Python)  
   - Runs on host 0.0.0.0, port 5000 by default  
3. **Data Pipeline**  
   - JSON files placed into `Data/` directory  
   - Model processes text fields and returns sentiments  
   - Results can be saved or returned via HTTP response  
4. **Frontend (Optional)**  
   - UI assets under `static/` and `templates/` if applicable  
   - Enables uploading files + viewing results via browser (if implemented)  

## 🧑‍💻 Getting Started  

### Prerequisites  
- Python 3.x  
- pip (or poetry)  
- (Optional) Virtual environment  

### Installation  
```bash
git clone https://github.com/karthikbhag/ProjectAnna.git  
cd ProjectAnna  
# checkout the branch  
git checkout Tanish_branch  
# (optional) create a venv  
python -m venv venv  
source venv/bin/activate  # on Unix/macOS  
venv\Scripts\activate     # on Windows  
# install dependencies  
pip install -r requirements.txt
```

### Usage
1. Place JSON files you want to analyze into Data/.
2. Run the server:
   ```
   python Sentiment_Analysis_Server.py
   ```
   It will load the model and start serving at http://0.0.0.0:5000.
3. Send POST requests to the server with JSON payload or upload via UI (if present).
4. View returned sentiment scores or download output.


📝 Model Training / Fine-Tuning

For advanced users:
- Open ```Roberta training.ipynb``` to explore training/fine-tuning steps.
- Use your own labeled dataset to train the ```twitter-roberta-base-sentiment``` model.
- After training, update ```MODEL_NAME``` in server code to your custom model.
