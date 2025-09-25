# 🌙 Mnemosyne – The Goddess of Memory  

Mnemosyne, goddess of memory and mother of the Muses, preserves ideas for eternity.  
This app is inspired by her: **turn messy screenshots into clean, searchable notes in Notion.**  

Built for **GirlHack 2025**.  

---

## ✨ Features  
- 📸 **Screenshot to Notes** – Upload any screenshot (slides, whiteboards, notes).  
- 🔎 **OCR Extraction** – AI reads text from images.  
- 🧠 **Smart Summarization** – Summarizes ideas into concise bullet points.  
- 🗂 **Notion Integration** – Saves results directly into a Notion database.  
- 🎭 **Greek Goddess Theme** – Adds a touch of mythology to your workflow.  

---

## 🛠 Tech Stack  
- **Frontend**: Streamlit (Python)  
- **OCR**: Tesseract / GPT-4o Vision  
- **AI Summarization**: OpenAI API  
- **Database**: Notion API  
- **Deployment**: Local (hackathon demo)  

---

## 🚀 Getting Started  

### 1. Clone the repo  
```bash
git clone https://github.com/Livia-1212/mnemosyne.git
cd mnemosyne
2. Create & activate a virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure environment variables
Create a .env file in the project root:

ini
Copy code
OPENAI_API_KEY=your_openai_key_here
NOTION_API_KEY=your_notion_key_here
NOTION_DATABASE_ID=your_database_id_here
5. Run the app
bash
Copy code
streamlit run app/main.py
📂 Project Structure
bash
Copy code
mnemosyne/
│── app/
│   ├── main.py           # Streamlit app entry point
│   ├── ocr.py            # OCR logic
│   ├── summarizer.py     # Summarization logic
│   ├── notion_client.py  # Notion API client
│   └── utils.py          # Helper functions
│
├── data/
│   └── sample_screenshots/
│
├── tests/
│   └── test_app.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore


🎯 Roadmap
 Enhance OCR with GPT Vision for messy handwriting

 Add auto-tagging (topics, priority, deadlines)

 Browser extension for 1-click save to Notion

 Slack/Discord integration for team workflows

🏛 Inspiration
This project is named after Mnemosyne, the Greek goddess of memory.
Just as she ensured nothing was forgotten, this app makes sure your ideas never get lost in messy screenshots.

👩‍💻 Contributors
Livia-1212 (Lead Dev / Hackathon Participant)

📜 License
This project is licensed under the MIT License.

---

👉 Next step: save this content into your local `README.md`, then run:  

```bash
git add README.md
git commit -m "Add complete README"
git push ```
