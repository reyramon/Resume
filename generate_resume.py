from pathlib import Path
from openai import OpenAI
from datetime import datetime
import re
import shutil
import subprocess

client = OpenAI()

BASE_DIR = Path(__file__).parent

# Prefer updated files if they exist, otherwise fall back to original names
ORCHESTRATOR_FILE = (
    BASE_DIR / "resume-agent-orchestrator-updated.md"
    if (BASE_DIR / "resume-agent-orchestrator-updated.md").exists()
    else BASE_DIR / "resume-agent-orchestrator.md"
)

CAREER_PROFILE_FILE = (
    BASE_DIR / "career-profile-updated.md"
    if (BASE_DIR / "career-profile-updated.md").exists()
    else BASE_DIR / "career-profile.md"
    if (BASE_DIR / "career-profile.md").exists()
    else BASE_DIR / "rey-career-profile-updated.md"
    if (BASE_DIR / "rey-career-profile-updated.md").exists()
    else BASE_DIR / "rey-career-profile.md"
)

SOURCE_DATA_FILE = BASE_DIR / "resume-source-data.md"

JOB_ANALYZER_FILE = (
    BASE_DIR / "job-description-analyzer.md"
    if (BASE_DIR / "job-description-analyzer.md").exists()
    else None
)

MODEL_NAME = "gpt-5.4"

JOB_FILE = BASE_DIR / "job_description.txt"
ANALYSIS_FILE = BASE_DIR / "job_analysis.md"
STRATEGY_FILE = BASE_DIR / "resume_strategy.md"
OUTPUT_FILE = BASE_DIR / "generated_resume.md"
FINAL_RESUME_FILE = BASE_DIR / "final_resume.md"
FINAL_DOCX_FILE = BASE_DIR / "final_resume.docx"
REFERENCE_DOC_FILE = BASE_DIR / "resume-template.docx"
ARCHIVE_DIR = BASE_DIR / "Resumes"

EXAMPLE_FILE_HINTS = {
    str(SOURCE_DATA_FILE): "Copy resume-source-data.example.md to resume-source-data.md and replace it with your verified experience data.",
    str(CAREER_PROFILE_FILE): "Copy career-profile.example.md to career-profile.md and replace it with your own positioning/profile notes.",
    str(JOB_FILE): "Copy job_description.example.txt to job_description.txt and paste in the target job description.",
}


def load_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_required_file(path: Path, label: str) -> str:
    if path is None or not path.exists():
        hint = EXAMPLE_FILE_HINTS.get(str(path))
        message = f"Missing required file for {label}: {path}"
        if hint:
            message = f"{message}\n{hint}"
        raise FileNotFoundError(message)
    return load_file(path)


def sanitize_resume_markdown(text: str) -> str:
    """
    Normalize common encoding artifacts and keep markdown consistently readable
    for Pandoc -> Word conversion.
    """
    replacements = {
        "â€¢": "-",
        "â€”": "-",
        "â€“": "-",
        "â†’": "to",
        "â€˜": "'",
        "â€™": "'",
        "â€œ": '"',
        "â€\x9d": '"',
        "Â": "",
        "\u00a0": " ",
    }

    cleaned = text
    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)

    # Normalize all line endings and remove trailing whitespace.
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = "\n".join(line.rstrip() for line in cleaned.split("\n"))

    # Keep spacing tidy between markdown sections for Word conversion.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip() + "\n"
    return cleaned


def add_section_dividers(text: str) -> str:
    """
    Insert markdown horizontal rules before each top-level resume section so
    Pandoc renders a visible divider line in the final docx.
    """
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    result = []
    seen_first_section = False

    for line in lines:
        if line.startswith("## "):
            if seen_first_section:
                if result and result[-1] != "":
                    result.append("")
                result.append("---")
                result.append("")
            else:
                if result and result[-1] != "":
                    result.append("")
                result.append("---")
                result.append("")
                seen_first_section = True
        result.append(line)

    return "\n".join(result)


def add_experience_role_spacing(text: str) -> str:
    """
    In the Professional Experience section, add a blank line between the
    company line and the job title line when both are bold markdown lines.
    """
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    result = []
    in_experience = False

    for index, line in enumerate(lines):
        if line.startswith("## "):
            in_experience = line == "## Professional Experience"

        result.append(line)

        if not in_experience:
            continue

        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        current_looks_like_company = (
            line.startswith("**") and "|" not in line and next_line.startswith("**")
        )
        next_looks_like_title = "|" in next_line

        if current_looks_like_company and next_looks_like_title:
            result.append("")

    return "\n".join(result)


def convert_markdown_to_docx(markdown_path: Path, docx_path: Path) -> bool:
    """
    Convert markdown to docx using Pandoc if available.
    Uses resume-template.docx as reference style document when present.
    """
    if shutil.which("pandoc") is None:
        print("Pandoc not found on PATH. Skipping .docx conversion.")
        return False

    if docx_path.exists():
        ARCHIVE_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archived_file = ARCHIVE_DIR / f"{docx_path.stem}_{timestamp}{docx_path.suffix}"
        docx_path.rename(archived_file)
        print(f"Archived previous docx to: {archived_file}")

    cmd = ["pandoc", str(markdown_path), "-f", "gfm", "-t", "docx", "-o", str(docx_path)]
    if REFERENCE_DOC_FILE.exists():
        cmd.extend(["--reference-doc", str(REFERENCE_DOC_FILE)])

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as exc:
        print("Pandoc conversion failed. Skipping .docx output.")
        if exc.stderr:
            print(exc.stderr.strip())
        return False


def analyze_job(
    job_description: str,
    orchestrator: str,
    career_profile: str,
    source_data: str,
    job_analyzer: str,
) -> str:
    """
    Step 1:
    Use the job analyzer to classify the role, assess fit, select modes,
    and map JD signals to verified source data.
    """
    prompt = f"""
You are a job description analysis system for resume tailoring.

Your task is to analyze the target job description before resume generation.

Use the analyzer rules exactly.

===== JOB ANALYZER =====
{job_analyzer}

===== RESUME ORCHESTRATOR =====
{orchestrator}

===== CAREER POSITIONING PROFILE =====
{career_profile}

===== VERIFIED SOURCE DATA =====
{source_data}

===== TARGET JOB DESCRIPTION =====
{job_description}

INSTRUCTIONS:

1. Follow the Job Description Analyzer exactly.
2. Stay fully grounded in verified source data.
3. Do not invent experience, metrics, ownership, or management scope.
4. Choose the strongest truthful alignment possible.
5. Allow stretch alignment when reasonable.
6. Do not reject the role just because exact prior titles differ.

OUTPUT:
Return the internal analysis using this structure exactly:

Role Classification:
Seniority Assessment:
Primary Mode:
Secondary Mode:
Critical Signals:
Evidence Map:
Resume Emphasis Plan:
Keyword Alignment Plan:
Risks and Gaps:
Fit Score:
""".strip()

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()


def generate_strategy(
    job_description: str,
    orchestrator: str,
    career_profile: str,
    source_data: str,
    job_analyzer: str,
    analysis_result: str,
) -> str:
    """
    Step 2:
    Build a resume strategy plan before writing the resume.
    """
    prompt = f"""
You are a resume strategy planner.

Create a strategy plan that will guide resume generation.

Use:
- the orchestrator
- the career profile
- the verified source data
- the job analyzer
- the completed job analysis
- the target job description

===== RESUME ORCHESTRATOR =====
{orchestrator}

===== CAREER POSITIONING PROFILE =====
{career_profile}

===== VERIFIED SOURCE DATA =====
{source_data}

===== JOB ANALYZER =====
{job_analyzer}

===== TARGET JOB DESCRIPTION =====
{job_description}

===== COMPLETED JOB ANALYSIS =====
{analysis_result}

INSTRUCTIONS:

1. Stay fully grounded in verified source data.
2. Do not invent experience, metrics, titles, or management scope.
3. Determine the strongest truthful narrative for this role.
4. Prioritize the most relevant roles and achievements.
5. Keep the strategy practical for a one-page resume.
6. Prefer the strongest evidence over complete coverage.

OUTPUT:
Return the strategy using this structure exactly:

Summary Angle:
Role Ordering:
Top Achievements:
Skills to Emphasize:
Skills to De-emphasize:
Bullet Themes:
Keyword Strategy:
Project Inclusion Decision:
""".strip()

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()


def generate_resume_review_packet(
    job_description: str,
    orchestrator: str,
    career_profile: str,
    source_data: str,
    job_analyzer: str,
    analysis_result: str,
    strategy_result: str,
) -> str:
    """
    Step 3:
    Generate the review packet containing the draft resume and supporting
    improvement analysis.
    """
    prompt = f"""
You are a resume review packet generation system.

Generate a tailored review packet using the orchestrator, the career profile,
the verified source data, the job analyzer rules, the completed job analysis,
and the resume strategy plan.

===== RESUME ORCHESTRATOR =====
{orchestrator}

===== CAREER POSITIONING PROFILE =====
{career_profile}

===== VERIFIED SOURCE DATA =====
{source_data}

===== JOB ANALYZER =====
{job_analyzer}

===== TARGET JOB DESCRIPTION =====
{job_description}

===== COMPLETED JOB ANALYSIS =====
{analysis_result}

===== RESUME STRATEGY PLAN =====
{strategy_result}

INSTRUCTIONS:

1. Follow the orchestration rules exactly.
2. Use the completed job analysis and the resume strategy plan to guide emphasis and positioning.
3. Remain fully truthful to the source data.
4. Do not invent metrics, technologies, scope, or management responsibility.
5. Position at Staff level by default, but align to Senior if the job clearly targets Senior.
6. Avoid pure DBA framing.
7. Avoid pure DevOps framing.
8. Emphasize backend, data systems, product systems, or hybrid positioning based on the analysis.
9. Use only supported ATS keywords.
10. Prioritize the strongest and most relevant bullets rather than trying to mention everything.
11. Keep the draft resume readable for one page.
12. Prefer removing weaker bullets over over-compressing strong bullets.

OUTPUT IN THIS EXACT ORDER:

1. One-page tailored resume
2. Three improved impact metric variants for weak bullets
3. ATS keyword coverage analysis vs job description
4. Final compression pass improving language
""".strip()

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()


def generate_final_resume(
    job_description: str,
    orchestrator: str,
    career_profile: str,
    source_data: str,
    job_analyzer: str,
    analysis_result: str,
    strategy_result: str,
    review_packet: str,
) -> str:
    """
    Step 4:
    Generate the final polished one-page resume by applying the best truthful
    improvements from the review packet.
    """
    prompt = f"""
You are a final resume assembly system.

Your task is to produce the final polished one-page resume only.

Use:
- the orchestrator
- the career profile
- the verified source data
- the job analyzer
- the completed job analysis
- the resume strategy plan
- the review packet containing:
  * draft resume
  * weak bullet rewrite options
  * ATS keyword analysis
  * compression suggestions

===== RESUME ORCHESTRATOR =====
{orchestrator}

===== CAREER POSITIONING PROFILE =====
{career_profile}

===== VERIFIED SOURCE DATA =====
{source_data}

===== JOB ANALYZER =====
{job_analyzer}

===== TARGET JOB DESCRIPTION =====
{job_description}

===== COMPLETED JOB ANALYSIS =====
{analysis_result}

===== RESUME STRATEGY PLAN =====
{strategy_result}

===== REVIEW PACKET =====
{review_packet}

INSTRUCTIONS:

1. Produce only the final polished one-page resume.
2. Apply the strongest truthful improvements from the review packet.
3. Use stronger bullet rewrites when supported by source data.
4. Apply compression edits directly into the resume.
5. Preserve one-page readability.
6. Remove all commentary, analysis, notes, and alternative options.
7. Do not invent metrics, technologies, scope, ownership, or management responsibility.
8. Keep the result ATS-friendly, direct, and concise.
9. Return only resume content. Do not include headings like:
   - "Final Resume"
   - "ATS Analysis"
   - "Compression Pass"
   - "Recommendations"

OUTPUT:
Return only the final polished resume in markdown.
""".strip()

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return response.output_text.strip()

def archive_existing_resume():
    """
    Move the existing generated_resume.md to the resumes archive folder
    with a timestamp so it is not overwritten.
    """
    if not OUTPUT_FILE.exists():
        return

    ARCHIVE_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    archived_file = ARCHIVE_DIR / f"generated_resume_{timestamp}.md"

    OUTPUT_FILE.rename(archived_file)

    print(f"Archived previous resume to: {archived_file}")
    
def archive_existing_final_resume():
    """
    Move the existing generated_final_resume.md to the resumes archive folder
    with a timestamp so it is not overwritten.
    """
    if not FINAL_RESUME_FILE.exists():
        return

    ARCHIVE_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    archived_file = ARCHIVE_DIR / f"generated_final_resume_{timestamp}.md"

    FINAL_RESUME_FILE.rename(archived_file)

    print(f"Archived previous resume to: {archived_file}")

def main():
    job_file = JOB_FILE

    if not job_file.exists():
        print(
            "Missing job_description.txt.\n"
            "Copy job_description.example.txt to job_description.txt and paste in the target job description."
        )
        return

    try:
        orchestrator = read_required_file(ORCHESTRATOR_FILE, "orchestrator")
        career_profile = read_required_file(CAREER_PROFILE_FILE, "career profile")
        source_data = read_required_file(SOURCE_DATA_FILE, "source data")
        job_analyzer = read_required_file(JOB_ANALYZER_FILE, "job analyzer")
        job_description = load_file(job_file)
    except FileNotFoundError as exc:
        print(str(exc))
        return

    analysis_result = analyze_job(
        job_description=job_description,
        orchestrator=orchestrator,
        career_profile=career_profile,
        source_data=source_data,
        job_analyzer=job_analyzer,
    )

    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        f.write(analysis_result)

    strategy_result = generate_strategy(
        job_description=job_description,
        orchestrator=orchestrator,
        career_profile=career_profile,
        source_data=source_data,
        job_analyzer=job_analyzer,
        analysis_result=analysis_result,
    )

    with open(STRATEGY_FILE, "w", encoding="utf-8") as f:
        f.write(strategy_result)
        
    archive_existing_resume()

    review_packet = generate_resume_review_packet(
        job_description=job_description,
        orchestrator=orchestrator,
        career_profile=career_profile,
        source_data=source_data,
        job_analyzer=job_analyzer,
        analysis_result=analysis_result,
        strategy_result=strategy_result,
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(review_packet)

    archive_existing_final_resume()

    final_resume = generate_final_resume(
        job_description=job_description,
        orchestrator=orchestrator,
        career_profile=career_profile,
        source_data=source_data,
        job_analyzer=job_analyzer,
        analysis_result=analysis_result,
        strategy_result=strategy_result,
        review_packet=review_packet,
    )
    final_resume = sanitize_resume_markdown(final_resume)
    final_resume = add_section_dividers(final_resume)
    final_resume = add_experience_role_spacing(final_resume)
    final_resume = sanitize_resume_markdown(final_resume)

    with open(FINAL_RESUME_FILE, "w", encoding="utf-8") as f:
        f.write(final_resume)

    docx_created = convert_markdown_to_docx(FINAL_RESUME_FILE, FINAL_DOCX_FILE)

    print(f"Job analysis generated: {ANALYSIS_FILE}")
    print(f"Resume strategy generated: {STRATEGY_FILE}")
    print(f"Review packet generated: {OUTPUT_FILE}")
    print(f"Final resume generated: {FINAL_RESUME_FILE}")
    if docx_created:
        print(f"Final resume docx generated: {FINAL_DOCX_FILE}")


if __name__ == "__main__":
    main()
