# Resume Generator

This project helps you generate resumes with the OpenAI API.

You do not need to be a developer to use it, but you do need to follow the setup steps carefully the first time.

There are 2 main things this project can do:

1. Create a custom resume for one specific job posting
2. Create a broader "global resume package" that can be reused for many applications

## What This Project Does

You give the project:

- your work history and facts
- a short career profile
- optionally your saved answers for common application questions
- a job description

The project then uses that information to generate:

- a job analysis
- a resume strategy
- a tailored resume in Markdown
- a Word version of the final resume if Pandoc is installed

## Who This Is For

This repo is meant for someone who:

- wants help tailoring resumes faster
- is comfortable editing simple text files
- can follow copy/paste instructions in PowerShell
- has an OpenAI API key

## Before You Start

You will need:

- Windows
- Python installed
- an OpenAI API key
- internet access
- this project downloaded to your computer

Optional but helpful:

- Pandoc, if you want the project to also create `.docx` Word files automatically

## Easiest Way To Get The Project

If you are not familiar with Git, do this:

1. Open the GitHub repo page.
2. Click `Code`.
3. Click `Download ZIP`.
4. Extract the ZIP somewhere easy, like `Documents\Resume`.

If you already use Git, you can clone the repo normally.

## Project Files In Plain English

These are the most important files:

- `generate_resume.py`
  This creates a resume for one specific job description.

- `create_global_resume.py`
  This creates a broader resume package for general job applications.

- `resume-source-data.example.md`
  A template where you put your real background, work history, projects, and facts.

- `career-profile.example.md`
  A template where you describe how you want to be positioned professionally.

- `global_resume_screening_answers.example.md`
  A template for common application questions like work authorization, salary range, relocation, and start date.

- `job_description.example.txt`
  A template for the job posting you want to target.

- `resume-template.docx`
  A Word formatting template used when exporting the final resume to `.docx`.

## Step 1: Install Python

If Python is not already installed:

1. Go to [python.org](https://www.python.org/downloads/).
2. Download Python 3.
3. During installation, make sure you check the box that says `Add Python to PATH`.

To verify Python is installed:

1. Open PowerShell.
2. Run:

```powershell
python --version
```

If you see a version number, you are good.

## Step 2: Install The OpenAI Python Package

Open PowerShell in the project folder and run:

```powershell
pip install openai
```

If `pip` does not work, try:

```powershell
python -m pip install openai
```

## Step 3: Create Your OpenAI API Key

You need your own OpenAI API key for this project to work.

1. Sign in to your OpenAI account.
2. Create an API key.
3. Keep it private.

Then set it in PowerShell before running the scripts:

```powershell
$env:OPENAI_API_KEY="paste-your-key-here"
```

Important:

- You must do this in the same PowerShell window where you run the scripts.
- If you close that window, you may need to set the key again next time.

## Step 4: Create Your Real Input Files

The example files are just templates. You need to copy them and fill in your own information.

In PowerShell, run these commands from the project folder:

```powershell
Copy-Item .\resume-source-data.example.md .\resume-source-data.md
Copy-Item .\career-profile.example.md .\career-profile.md
Copy-Item .\global_resume_screening_answers.example.md .\global_resume_screening_answers.md
Copy-Item .\job_description.example.txt .\job_description.txt
```

Now open those new files and replace the placeholder text with your real information.

You can use:

- Notepad
- VS Code
- any text editor you like

## What To Put In Each File

### `resume-source-data.md`

Put facts here, such as:

- your real name
- contact information
- work history
- project details
- technologies you actually used
- education
- certifications
- specific achievements you can stand behind

Be truthful and specific. This file is the factual source material.

### `career-profile.md`

Put positioning information here, such as:

- what roles you want
- what strengths should be emphasized
- what kinds of jobs fit you best
- what should not be misrepresented

This file helps the system decide how to frame your experience.

### `global_resume_screening_answers.md`

Put standard application answers here, such as:

- work authorization
- sponsorship needs
- relocation
- security clearance
- salary target
- availability to start

If you do not want to use this yet, you can leave it simple or skip the global resume workflow.

### `job_description.txt`

Paste the full text of the job posting here when you want a tailored resume for one job.

## Step 5: Generate A Resume For One Job

This is the main script for tailoring your resume to a specific job posting.

In PowerShell, run:

```powershell
python .\generate_resume.py
```

If everything is set up correctly, the project will generate:

- `job_analysis.md`
- `resume_strategy.md`
- `generated_resume.md`
- `final_resume.md`
- `final_resume.docx` if Pandoc is installed

## Step 6: Generate A Global Resume Package

If you want a broader package for general job applications, run:

```powershell
python .\create_global_resume.py
```

This creates a folder called `Global Resume` with files such as:

- `global_resume.md`
- `candidate_profile.md`
- `application_agent_instructions.md`
- `screening_answers.md`
- `verified_source_data.md`
- `global_resume.docx` if Pandoc is installed

## Where The Output Goes

When you run the scripts, new files are created in the project folder.

For a targeted resume run:

- `job_analysis.md`
- `resume_strategy.md`
- `generated_resume.md`
- `final_resume.md`
- `final_resume.docx`

Older generated resumes may also be archived into the `Resumes` folder.

For the global package run:

- the `Global Resume` folder is created or updated

## Optional: Install Pandoc For Word Output

If you want automatic `.docx` files, install Pandoc:

1. Go to [pandoc.org](https://pandoc.org/installing.html)
2. Install it
3. Restart PowerShell

Then check that it works:

```powershell
pandoc --version
```

If Pandoc is not installed, the scripts can still generate the Markdown files.

## Common Problems

### "Missing required file"

This usually means you forgot to copy one of the example files and rename it.

Make sure these exist:

- `resume-source-data.md`
- `career-profile.md`
- `job_description.txt`

### "OPENAI_API_KEY" problems

Make sure you ran:

```powershell
$env:OPENAI_API_KEY="your-key"
```

in the same PowerShell window before running the script.

### "python is not recognized"

Python is either not installed or was not added to PATH during installation.

### No `.docx` file was created

That usually means Pandoc is not installed. The Markdown output should still be created.

## Privacy And GitHub

This repo is set up so private information stays local.

These files should stay on your computer and should not be committed:

- `resume-source-data.md`
- `career-profile.md`
- `global_resume_screening_answers.md`
- `job_description.txt`
- `job_description.md`
- `job_analysis.md`
- `resume_strategy.md`
- `generated_resume.md`
- `final_resume.md`
- `final_resume.docx`
- `Global Resume/`
- `Resumes/`

That is why the repo includes a `.gitignore` file.

## Recommended First Run

If this is your first time using the project, follow this order:

1. Download the repo
2. Install Python
3. Run `pip install openai`
4. Set your `OPENAI_API_KEY`
5. Copy the example files to their real file names
6. Fill in `resume-source-data.md`
7. Fill in `career-profile.md`
8. Paste a job posting into `job_description.txt`
9. Run `python .\generate_resume.py`
10. Open `final_resume.md`

## Quick Start Commands

If you already have Python installed, these are the main commands:

```powershell
python -m pip install openai
$env:OPENAI_API_KEY="paste-your-key-here"
Copy-Item .\resume-source-data.example.md .\resume-source-data.md
Copy-Item .\career-profile.example.md .\career-profile.md
Copy-Item .\global_resume_screening_answers.example.md .\global_resume_screening_answers.md
Copy-Item .\job_description.example.txt .\job_description.txt
python .\generate_resume.py
```

## If You Are Helping A Friend Use This

Tell them:

- start with the example files
- do not edit the Python scripts
- be honest in the source data
- paste the full job description
- expect the first setup to take a little time

Once setup is done, using it is much easier.
