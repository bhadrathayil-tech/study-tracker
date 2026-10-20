# 📚 Study & Streak Tracker

A lightweight, full-stack Python web application designed to help students track daily study sessions, maintain consecutive study streaks, and monitor weekly subject totals.

## 🚀 Features
* **Session Logging:** Log study sessions with subject names, durations (in minutes), and custom dates[cite: 2].
* **Streak Tracking:** Automatically calculates your **Current Streak** and records your **Longest Streak**[cite: 2].
* **Weekly Subject Totals:** Displays total study time aggregated per subject for the current week[cite: 2].
* **Persistent Storage:** Uses a local SQLite database (`study_tracker.db`) to ensure your history is saved between sessions[cite: 3].
* **Session Management:** View and delete past entries seamlessly through a clean web dashboard[cite: 2].

## 🛠️ Tech Stack
* **Backend & Server:** Python, Flask[cite: 12]
* **Database:** SQLite[cite: 3]
* **Frontend:** HTML5, CSS3, Jinja2 Templates[cite: 12, 17]

## ⚙️ Setup & Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bhadrathayil-tech/study-tracker.git](https://github.com/bhadrathayil-tech/study-tracker.git)
   cd study-tracker