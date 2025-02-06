import requests
from bs4 import BeautifulSoup
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import time

# Initialize the database
def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        company TEXT,
                        location TEXT,
                        summary TEXT,
                        link TEXT UNIQUE)''')
    conn.commit()
    conn.close()

# Function to scrape Indeed jobs
def scrape_indeed_jobs():
    query = job_entry.get().strip().replace(" ", "+")
    location = location_entry.get().strip().replace(" ", "+")
    
    if not query or not location:
        messagebox.showerror("Error", "Please enter a job title and location")
        return
    
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to fetch job listings")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="job_seen_beacon")
    
    results_list.delete(0, tk.END)  # Clear previous results

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    for job in jobs[:10]:  # Limit to 10 results
        title = job.find("h2", class_="jobTitle")
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        link = job.find("a", class_="jcs-JobTitle")

        if title and link:
            job_title = title.text.strip()
            job_company = company.text.strip() if company else "Unknown"
            job_location = location.text.strip() if location else "Unknown"
            job_link = "https://www.indeed.com" + link["href"]

            # Insert into database
            try:
                cursor.execute("INSERT INTO jobs (title, company, location, summary, link) VALUES (?, ?, ?, ?, ?)",
                               (job_title, job_company, job_location, "No summary available", job_link))
            except sqlite3.IntegrityError:
                pass  # Skip duplicates

            # Display in GUI
            results_list.insert(tk.END, f"{job_title} - {job_company} ({job_location})")
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Job search completed!")

# Initialize the GUI
root = tk.Tk()
root.title("Indeed Job Scraper")

# Job Title Input
tk.Label(root, text="Job Title:").grid(row=0, column=0, padx=5, pady=5)
job_entry = tk.Entry(root, width=30)
job_entry.grid(row=0, column=1, padx=5, pady=5)

# Location Input
tk.Label(root, text="Location:").grid(row=1, column=0, padx=5, pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.grid(row=1, column=1, padx=5, pady=5)

# Search Button
search_button = tk.Button(root, text="Search Jobs", command=scrape_indeed_jobs)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

# Results List
results_list = tk.Listbox(root, width=60, height=10)
results_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Start GUI Loop
root.mainloop()
