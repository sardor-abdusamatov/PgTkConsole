
# 🔥 PgTkConsole 

A lightning-fast, lightweight PostgreSQL SQL client built with Python and CustomTkinter. 
Forget about heavy, slow Java/Electron-based database managers. PgTkConsole boots in under a second and gives you exactly what you need: a clean UI to write queries, view results, and export data.

## ✨ Features
* **Zero Bloat:** Launches instantly. 
* **Dark Mode Native:** Beautiful, hacker-friendly UI powered by `customtkinter`.
* **Smart Output:** Handles raw SQL execution, limits UI rendering to 100 rows to prevent freezing, while keeping all data in memory.
* **1-Click CSV Export:** Dump your SELECT query results straight into a CSV file.
* **Safe Encodings:** Automatically handles common Windows/PostgreSQL UTF-8 decoding crashes under the hood.
* **Keyboard Shortcuts:** Press `F5` to execute your query instantly.

## 🚀 Installation

1. Clone the repository:
git clone [https://github.com/YOUR_USERNAME/PgTkConsole.git](https://github.com/sardor-abdusamatov/PgTkConsole.git)

cd PgTkConsole

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
python pgtkconsole.py
