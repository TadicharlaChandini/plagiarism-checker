# 📄 Plagiarism Checker 🔍

A full-stack web application that allows users to upload documents and checks for plagiarism using intelligent text comparison.

This system is built to assist students, teachers, and institutions in identifying duplicate content across multiple documents quickly and efficiently.

---

## 🚀 Features

- 🔐 User Registration & Login
- 📁 Upload `.txt`, `.pdf`,`.docx` and `.java`,`.py`documents
- 🔄 Compare uploaded documents with existing ones
- 📊 View similarity percentage and detailed results
- 🕓 Track document history by user
- 🧾 Clean and user-friendly interface

---

## 💻 Tech Stack

| Layer         | Technology                        |
|---------------|------------------------------------|
| Backend       | Python (Flask)                    |
| Frontend      | HTML5, CSS3,Bootstrap             |
| Styling       | Custom CSS                        |
| Database      | SQLite3                           |
| Templating    | Jinja2                            |
| File Handling | Python-docx, PyPDF2               |
| Deployment    | Render (Planned)                  |

---

## 🗂️ Folder Structure
plagiarism-checker/
│
├── static/  # Static assets (CSS)
├── stored_docs/  # Stored reference documents
├── templates/  # HTML templates
├── uploads/   # Temporarily uploaded files
│
├── app.py   # Main Flask app
├── models.py  # Database model
├── requirements.txt  # Project dependencies
├── *.db  # SQLite database files
└── README.md  # Project overview


---

## 🧠 How It Works

1. User registers and logs in
2. Uploads a file for plagiarism check
3. System compares it against all stored documents
4. Calculates similarity using cosine/text-based matching
5. Displays results and saves them for future reference

---

## 🧑‍💻 Developed By

**Tadicharla Chandini**  
B.Tech in AI & Data Science  
[LinkedIn 🔗](https://www.linkedin.com/in/chandini-tadicharla-5952022a6/)  
[GitHub 🔗](https://github.com/TadicharlaChandini)  

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/TadicharlaChandini/plagiarism-checker.git
cd plagiarism-checker
pip install -r requirements.txt
python app.py

🌐 Deployment
The app is planned to be deployed using Render for free public access. Stay tuned for the live link!

📜 License
This project is open-source and free to use for academic purposes.