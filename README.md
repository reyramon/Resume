# Resume Generator

This repo contains the reusable code, prompts, and templates for generating tailored resumes with the OpenAI API.

It is set up so personal data, target job descriptions, and generated outputs stay local and do not need to be committed to GitHub.

## What should go to GitHub

- `generate_resume.py`
- `create_global_resume.py`
- prompt and workflow docs such as `resume-agent-orchestrator.md` and `job-description-analyzer.md`
- reusable formatting assets such as `resume-template.docx`
- example/template input files
- `.gitignore`
- this `README.md`

## What should stay local

- your real source data file: `resume-source-data.md`
- your real career profile: `career-profile.md`
- your real screening answers: `global_resume_screening_answers.md`
- the active target job description: `job_description.txt`
- generated outputs and archives:
  - `job_analysis.md`
  - `resume_strategy.md`
  - `generated_resume.md`
  - `final_resume.md`
  - `final_resume.docx`
  - `Global Resume/`
  - `Resumes/`

## First-time setup

1. Copy `resume-source-data.example.md` to `resume-source-data.md`.
2. Copy `career-profile.example.md` to `career-profile.md`.
3. Optionally copy `global_resume_screening_answers.example.md` to `global_resume_screening_answers.md`.
4. Copy `job_description.example.txt` to `job_description.txt`.
5. Add your `OPENAI_API_KEY` to your local environment.
6. Install dependencies:

```powershell
pip install openai
```

## Shareable workflow

The repo is now structured so a friend can clone it, fill in their own private files from the examples, and generate output locally without exposing your personal resume data or job targets.
