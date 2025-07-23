🔖 Section 0: Fellow Details
Fill out the table below:

Field	Your Entry
Name	
GitHub Username	
Preferred Feature Track	Data / Visual / Interactive / Smart
Team Interest	Yes / No — If Yes: Project Owner or Contributor
✍️ Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

Key Takeaways: 

What did you learn about capstone goals and expectations?
- I learned that it's broken up into accomplishable chunks
- I learned exactly what was required in order for me to have a successful Capstone


Concept Connections: 

Which Week 1–10 skills feel strongest? Which need more practice?
- I'm especially excited to brush up on my syntax and TKinter skills. 


Early Challenges: 

Any blockers (e.g., API keys, folder setup)?
- So far, I've had a pretty buggy TKinter experience: not code problems or even lack of understanding. Getting Tkinter to work successfully and consistently has been a challenge.

Support Strategies: 

Which office hours or resources can help you move forward?

- I attend Afsana's office hours regularly. I'm reviewing readings and documentation, as well as, being better regimented about my time. 
- I've reached out to classmates for assistance as well.

🧠 Section 2: Feature Selection Rationale
List three features + one enhancement you plan to build.

#	Feature Name	Difficulty (1–3)	Why You Chose It / Learning Goal
1			Weather History
2			Simple Statistics
3			City Comparison
Enhancement		–	Not quite sure yet. Most likely custom descriptions

🧩 Tip: Pick at least one “level 3” feature to stretch your skills!

🗂️ Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:

Core modules and folders
    - core folder houses api duties as well as data storage and processing

Feature modules
    - feature folder houses each of my three chosen features as well as a base file for shared dependencies

Data flow between components
    -main.py runs the entire application
    -most folders contain an __init__.py in order to allow them to be run as packages
    -

📊 Section 4: Data Model Plan
Fill in your planned data files or tables:

File/Table Name	Format (txt, json, csv, other)	Example Row
weather_history.txt	txt	2025-06-09,New Brunswick,78,Sunny
📆 Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

Week	Monday	Tuesday	Wednesday	Thursday	Key Milestone
12	API setup	Error handling	Tkinter shell	Buffer day	Basic working app
13	Feature 1			Integrate	Feature 1 complete
14	Feature 2 start		Review & test	Finish	Feature 2 complete
15	Feature 3	Polish UI	Error passing	Refactor	All features complete
16	Enhancement	Docs	Tests	Packaging	Ready-to-ship app
17	Rehearse	Buffer	Showcase	–	Demo Day
⚠️ Section 6: Risk Assessment
Identify at least 3 potential risks and how you’ll handle them.

Risk	Likelihood (High/Med/Low)	Impact (High/Med/Low)	Mitigation Plan
API Rate Limit	Medium	Medium	Add delays or cache recent results
🤝 Section 7: Support Requests
What specific help will you ask for in office hours or on Slack?

✅ Section 8: Before Monday (Start of Week 12)
Complete these setup steps before Monday:

Push main.py, config.py, and a /data/ folder to your repo

Add OpenWeatherMap key to .env (⚠️ Do not commit the key)

Create files for the chosen feature in /features/ 

like this:
# weather_journal.py
"""
Feature: Weather Journal
- Stores daily mood and notes alongside weather data
"""
def add_journal_entry(date, mood, notes):
    # your code goes here
    pass
Commit and push a first-draft README.md

Book office hours if you're still stuck on API setup

📤 Final Submission Checklist:
✅ Week11_Reflection.md completed
✅ File uploaded to GitHub repo /docs/
✅ Repo link submitted on Canvas