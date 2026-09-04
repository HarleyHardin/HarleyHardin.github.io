# 100 Days of Python

Projects completed as part of Harley Hardin's 100 Days of Python challenge.

- Day 01 — Number Guessing Game
- Day 02 — Simple Quiz Game
- Day 03 — Rock, Paper, Scissors
- Day 04 — Password Audit Tool
- Bonus Day 04 — Security Log Analyzer
- Bonus Day 04 — File Integrity Checker (work in progress)
- Bonus Day 04 — VirusTotal URL Analyzer
- Day 05 — Static File Analyzer (learning log / scope lesson)
- Day 06 — Suspicious Process Checker (one-hour Tkinter GUI practice)

Challenge progress: **06 / 100 days**  
Total projects shipped: **9**

## Day 05 — Static File Analyzer

I got way too ambitious with this one.

My original goal was to build a simple file scanner and spend some time designing my own GUI. Instead, I kept adding features until I ended up working with PE files, entropy analysis, hashes, certificates, macros, metadata, and disassembly—most of which were far beyond my current Python knowledge.

I had to research almost every function, and some of the search results gave me much more direct help than I actually wanted. Because of that, I don't consider every part of this program something I could independently recreate yet.

I'm still uploading it because this is what I worked on for Day 5, and the point of this challenge is to document the learning process—not pretend every day went perfectly.

The biggest thing I learned today wasn't Python: it was that I need to keep my projects small enough that I can actually solve the problems myself.

Tomorrow I'm scaling things back.


## Day 06 — Suspicious Process Checker

After deliberately scaling the challenge back down, Day 6 was limited to one hour and focused on completing a small GUI project I could understand end to end. The Tkinter interface is intentionally simple, but the program handles process-name checks, case-insensitive matching, blank input, a running check counter, an editable suspicious-process list, a history window, and result clearing.

The goal was not to build a production process-detection engine. It was to practice GUI event handling, state, lists, and finishing a project within a realistic scope.
