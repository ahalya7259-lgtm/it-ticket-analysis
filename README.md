# IT Service Desk Ticket Analysis

Analysis of 5,000 IT support tickets (Jan-Dec 2025) to find why tickets take long to close, where SLAs are missed, and how the service desk can improve.

> **Note:** The dataset is **synthetic (dummy) data** created with `generate_data.py` for learning and portfolio purposes. It is not from a real company.

## Problem Statement
A service desk team wants to know:
1. Which issues create the most tickets?
2. Which issues take the longest to fix?
3. Where are SLA targets being missed?
4. Does missing SLA hurt customer satisfaction?
5. How can workload and agent performance be improved?

## Tools Used
Python (Pandas, NumPy, Matplotlib, Seaborn), MySQL, Power BI, Jupyter/VS Code, GitHub

## Project Structure
```
it-ticket-analysis/
├── data/          tickets_raw.csv, tickets_clean.csv
├── sql/           queries.sql (15 queries)
├── images/        charts from the analysis
├── dashboard/     Power BI guide, file and screenshot
├── generate_data.py   creates the dummy dataset
├── analysis.py        cleans data, finds insights, saves charts
└── requirements.txt
```

## Steps I Followed
1. **Created the data** - 5,050 raw rows with deliberate problems (duplicates, mixed upper/lower case, missing values).
2. **Cleaned the data** - removed 50 duplicates, fixed text case, filled missing agents as "Unassigned".
3. **Feature engineering** - added resolution hours, month, weekday, SLA target and SLA breached flag.
4. **SQL analysis** - 15 queries including GROUP BY, subquery, CTE and window functions (RANK, LAG).
5. **Visualization** - charts in Python and a one-page Power BI dashboard.

SLA targets used: Critical 4 hrs, High 8 hrs, Medium 24 hrs, Low 48 hrs.

## Key Numbers
| Metric | Value |
|--------|-------|
| Total tickets | 5,000 |
| Average resolution time | 9.1 hours |
| Overall SLA breach rate | 12.6% |
| Average customer rating | 4.14 / 5 |

## Key Insights
1. **Password resets are about 30% of all tickets** but take only 1.3 hours each. A self-service password reset tool could cut ticket volume by almost one-third.
2. **Hardware (23.6 hrs) and Network (16.0 hrs) issues are the slowest.** Better spare-parts stock and clearer network escalation steps can help.
3. **Critical (38.4%) and High (30.1%) priority tickets breach SLA the most.** Urgent tickets are being missed, so the priority queue needs fixing first.
4. **Mondays get 1,276 tickets, about 57% more than an average weekday.** Adding staff on Mondays can reduce waiting time.
5. **One agent (Suresh) takes 14.5 hrs on average against a team average near 9 hrs.** Coaching or training would help. The fastest agent (Priya, 6.2 hrs) can share best practices.
6. **Breaching SLA drops customer rating from 4.29 to 3.12.** Faster closing directly improves satisfaction.

## Recommendations
- Launch a self-service password reset portal.
- Review the Critical/High escalation process.
- Add extra staff on Mondays.
- Train slower agents using the top performer's method.
- Keep spare hardware ready to reduce repair time.

## Charts
![Tickets by category](images/01_tickets_by_category.png)
![Resolution by category](images/02_resolution_by_category.png)
![SLA by priority](images/04_sla_by_priority.png)
![Agent performance](images/05_agent_performance.png)

## Power BI Dashboard
Add your screenshot here: `![Dashboard](dashboard/dashboard.png)`

## How to Run
```bash
git clone https://github.com/ahalya7259-lgtm/it-ticket-analysis.git
cd it-ticket-analysis
pip install -r requirements.txt
python generate_data.py
python analysis.py
```
Then run `sql/queries.sql` in MySQL Workbench and build the dashboard using `dashboard/powerbi_guide.md`.

## Author
**Ahalya** - BCA Graduate | Aspiring Data Analyst
LinkedIn: linkedin.com/in/ahalya-k-096a6a30a | GitHub: github.com/ahalya7259-lgtm
