# Library Management

Library management app for frappe-bench.  
Designed for managing recruitment workflows including job applications, interviews, and more.

---

##  Installation

Follow the steps below to install the `library_management` app in your Frappe/ERPNext environment.

###  Prerequisites
- Python environment activated
- Frappe version: v14+ or v15+
- Install erpnext
- Install Hrms 
- A site already created (or use `bench new-site`)

### 1. get the App

```bash
cd ~/frappe-bench
bench get-app https://github.com/Dnyaneshwari311/Recrutement-process.git

### 2. Install the App on Your Site

cd ~/frappe-bench
bench --site your-site-name install-app library_management

### 3. Apply Migrations

bench --site your-site-name migrate

### 4.Start bench
bench start


### 5.Email Account Configuration
add email
authentication generted password

######### Recruitment Workflow ############

The recruitment process in the `library_management` app follows these key steps:

### 1. Job Opening Creation
- HR/Admin creates a **Job Opening** with:
  - Job Title
  - Number of openings
  - Department, Employment Type, and Job Description
- Add **Interview Rounds** in the child table for the Job Opening (e.g., HR Round, Technical Round, Final Round).

### 2. Define Interview Rounds (Reusable)
- Define available **Interview Rounds** globally under the **Interview Rounds** DocType (if not already created).
- Each round can include expected skills or responsibilities.
- These rounds will be linked in each Job Opening to structure the interview process.


### 4. Job Application
- Candidates apply via the **Job Application Web Form** or are manually added by HR.
- Fields include applicant name, email, resume, and job title etc.
- Trigger mail to candidate

### 5. Job Applicant Review
- HR reviews the application and can **shortlist** or **reject** candidates.
- Trigger mail to candidate

### 6. Interview Scheduling
- For shortlisted candidates, interviews are scheduled using the **Interview** DocType.
- Interview rounds and skills,skill type are selected based on the linked **Job Opening**.
- Interviewers are assigned.
- If Google Meet is configured, a meeting link is auto-generated.
- For generation of link we have to set Google meet oauth doc all fields from google cloud(ex-client id,refresh token ......etc)
- Trigger mail to candidate and interviewer

### 7. Skill Evaluation
- During or after interviews, evaluators rate the candidate using **Interview Skill Rating**.
- HR collects feedback for final decision-making.

### 8. Rescheduling (if needed)
- Interviews can be rescheduled.
- Reschedule triggers email notification if configured.

### 9. Final Decision
- Based on feedback, candidates can be **Accepted** or **Rejected**.

### 10. Job Offer
- Job offer creted for candidate status ia Awaiting Response 
- Trigger mail to candidate
- If accepted job offer from candidate, automatically the status of job offer is changed from Awaiting Response to Accepted or Aating Response to Rejected.


### License

mit
# Recrutement-process

