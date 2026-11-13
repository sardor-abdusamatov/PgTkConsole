import customtkinter as ctk
from tkinter import filedialog
import psycopg2
import csv


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PgTkConsole(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PgTkConsole - Lightweight PostgreSQL Client")
        self.geometry("1000x750")
        self.conn = None
        self.last_results = []
        self.last_columns = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self._build_ui()

    def _build_ui(self):
    
        self.conn_frame = ctk.CTkFrame(self, corner_radius=10)
        self.conn_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        self.db_entry = ctk.CTkEntry(self.conn_frame, placeholder_text="Database (e.g. postgres)")
        self.db_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.user_entry = ctk.CTkEntry(self.conn_frame, placeholder_text="User")
        self.user_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.pass_entry = ctk.CTkEntry(self.conn_frame, placeholder_text="Password", show="*")
        self.pass_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.connect_btn = ctk.CTkButton(self.conn_frame, text="Connect", command=self.connect_db, fg_color="#2FA572", hover_color="#1D7A50")
        self.connect_btn.pack(side="left", padx=10, pady=10)


        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.grid(row=1, column=0, padx=20, sticky="ew")

        self.query_label = ctk.CTkLabel(self.toolbar, text="SQL Query:", font=("Consolas", 14, "bold"))
        self.query_label.pack(side="left")

        self.export_btn = ctk.CTkButton(self.toolbar, text="💾 Export to CSV", command=self.export_csv, state="disabled", width=120)
        self.export_btn.pack(side="right", padx=(10, 0))

        self.clear_btn = ctk.CTkButton(self.toolbar, text="🗑 Clear Output", command=self.clear_console, width=120, fg_color="#555555", hover_color="#333333")
        self.clear_btn.pack(side="right")


        self.sql_input = ctk.CTkTextbox(self, height=180, font=("Consolas", 15))
        self.sql_input.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.sql_input.insert("1.0", "-- Write your SQL here\nSELECT version();")

        self.execute_btn = ctk.CTkButton(self, text="⚡ Execute Query (F5)", command=self.execute_query, font=("Arial", 14, "bold"), height=40)
        self.execute_btn.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.execute_btn.configure(state="disabled")


        self.output_console = ctk.CTkTextbox(self, height=250, font=("Consolas", 13), text_color="#00FF00", fg_color="#1E1E1E", wrap="none")
        self.output_console.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.output_console.insert("1.0", "Waiting for connection...\n")
        self.output_console.configure(state="disabled")


        self.bind("<F5>", lambda event: self.execute_query())

    def log(self, text, color="#00FF00"):
        self.output_console.configure(state="normal")
        self.output_console.configure(text_color=color)
        self.output_console.insert("end", text + "\n")
        self.output_console.see("end")
        self.output_console.configure(state="disabled")

    def clear_console(self):
        self.output_console.configure(state="normal")
        self.output_console.delete("1.0", "end")
        self.output_console.configure(state="disabled")

    def connect_db(self):
        dbname = self.db_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, 
                host="localhost", port="5432", client_encoding="UTF8"
            )
            self.conn.autocommit = True
            self.clear_console()
            self.log(f"✅ Connected successfully to: {dbname}")
            
            self.connect_btn.configure(text="Connected", fg_color="#2FA572", state="disabled")
            self.execute_btn.configure(state="normal")
        except Exception as e:
            err = str(e)
            if "codec can't decode" in err:
                err = "Auth failed: Check DB name, user, or password."
            self.log(f"❌ Connection Error:\n{err}", color="#FF4C4C")

    def execute_query(self):
        if not self.conn: return
        query = self.sql_input.get("1.0", "end-1c").strip()
        if not query:
            self.log("⚠️ Query is empty!", color="#FFA500")
            return

        self.last_results, self.last_columns = [], []
        self.export_btn.configure(state="disabled")

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                if cursor.description:
                    self.last_columns = [desc[0] for desc in cursor.description]
                    self.last_results = cursor.fetchall()
                    
                    self.log(f"\n--- Output ({len(self.last_results)} rows) ---", color="#00FFFF")
                    self.log(" | ".join(self.last_columns), color="#FFFFFF")
                    self.log("-" * 60, color="#FFFFFF")
                    
                    for row in self.last_results[:100]:
                        self.log(" | ".join(str(val) for val in row))
                    
                    if len(self.last_results) > 100:
                        self.log(f"...and {len(self.last_results) - 100} more rows. Use 'Export to CSV' to see all.", color="#FFA500")
                    
                    if self.last_results:
                        self.export_btn.configure(state="normal")
                else:
                    self.log(f"\n✅ Query executed successfully. No data returned.", color="#00FF00")
        except Exception as e:
            self.log(f"\n❌ SQL Error:\n{e}", color="#FF4C4C")

    def export_csv(self):
        if not self.last_results: return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Query Results"
        )
        if filepath:
            try:
                with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.last_columns)
                    writer.writerows(self.last_results)
                self.log(f"✅ Data exported to {filepath}", color="#00FFFF")
            except Exception as e:
                self.log(f"❌ Export error: {e}", color="#FF4C4C")
if __name__ == "__main__":
    app = PgTkConsole()
    app.mainloop()
