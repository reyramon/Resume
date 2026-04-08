# Job Description Analyzer

## Purpose

This file defines how to analyze a target job description before generating a resume.

Its job is to classify the role, determine strategic fit, extract important language, and guide resume tailoring using the source data.

This analyzer does not rewrite history.
It only adjusts emphasis based on verified experience.

---

## Inputs

Required inputs:

1. resume-agent-orchestrator.md
2. rey-career-profile.md
3. resume-source-data.md
4. target job description

---

## Core Rules

* Remain truthful to source data
* Do not invent experience
* Do not force exact title matching when capability alignment is strong
* Tailor emphasis, vocabulary, and sequencing based on the job description
* Identify fit based on actual work performed, not only prior job titles

---

## Analyzer Output

Before generating a resume, produce the following internal analysis.

### 1. Role Classification

Classify the role into one or more categories:

* Backend / Systems Engineer
* Product Systems Engineer
* Data Systems / Performance Engineer
* Platform Engineer
* Full Stack Engineer
* Internal Tools Engineer
* Enterprise Applications Engineer
* Founding Engineer

### 2. Seniority Assessment

Determine expected seniority:

* Senior
* Staff
* Principal

Then answer:

* Is Rey directly aligned?
* Is Rey stretch aligned?
* Is the role poorly aligned?

### 3. Strategic Mode Selection

Select one primary mode and optional secondary mode.

Available modes:

* Mode A: Backend / Systems Engineer
* Mode B: Product Systems Engineer
* Mode C: Data Systems / Performance Engineer
* Mode D: Balanced Hybrid

### 4. Skill Signal Extraction

Extract the most important signals from the job description.

Examples:

* backend APIs
* distributed systems
* query performance
* CI/CD
* ETL
* product ownership
* cloud migration
* internal platforms
* reliability
* security and compliance

Rank them as:

* critical
* important
* optional

### 5. Evidence Mapping

For each critical signal, map it to verified source data.

Example format:

* Query performance -> DHA query optimization 120s to 2s
* Internal tools -> WellMed QA tooling and rule extraction tool
* Enterprise systems -> DHA financial systems used by 7,500 users

If a signal is not supported, mark it clearly as:

* unsupported
* weakly supported
* adjacent

### 6. Resume Emphasis Plan

Determine:

* which roles should carry the most weight
* which achievements should move to the top
* which technologies should appear in skills
* whether summary should lean backend, product, platform, or data systems

### 7. Keyword Alignment Plan

Extract likely ATS and recruiter keywords from the job description.

Group them into:

* titles
* technical keywords
* business / impact language
* architectural language

Only include keywords that can be supported honestly.

### 8. Risk and Gap Analysis

Identify:

* missing direct experience
* overstretch risk
* title mismatch risk
* culture risk if visible in the job description

For each risk, state whether it can be mitigated through truthful reframing.

### 9. Fit Score

Provide a practical fit score:

* High Fit
* Good Fit
* Stretch Fit
* Low Fit

This is not a rejection mechanism.
It is a calibration tool.

Even when fit is Stretch Fit, the resume should still be generated if the role is within plausible range.

---

## Decision Logic

### Use Mode A when the job emphasizes:

* backend systems
* service development
* reliability
* APIs
* modernization
* production engineering

### Use Mode B when the job emphasizes:

* product ownership
* full stack work
* user facing systems
* internal product tooling
* rapid iteration

### Use Mode C when the job emphasizes:

* data systems
* query performance
* ETL
* analytics infrastructure
* pipelines
* warehousing
* reporting systems

### Use Mode D when:

* the role is broad
* the signals are mixed
* the title is generic
* the company wants versatile engineers

---

## Tailoring Rules

### Summary Tailoring

The summary must reflect the selected mode and the top two or three strengths most relevant to the role.

### Experience Tailoring

* Move the most relevant bullets higher
* Remove low value bullets before removing high signal bullets
* Keep each role focused on evidence that matches the job

### Skills Tailoring

* Include only relevant skills supported by source data
* Do not flood the skills section
* Prefer strong and repeated technologies over one off tools

---

## Stretch Role Policy

The system may generate a resume for a stretch role if:

* the role remains within software engineering, platform, backend, product, or data systems scope
* the gap is about environment, scale, or terminology rather than core capability
* the resume can remain truthful while emphasizing adjacent experience

The system should not reject a role simply because the exact title does not match previous titles.

The system should attempt the best truthful alignment possible.

---

## Hard Limits

Do not:

* invent distributed systems experience that does not exist
* invent team size or management scope
* invent cloud production ownership beyond source data
* invent AI or ML engineering depth
* invent metrics

Do:

* reframe SQL performance work as performance engineering when appropriate
* reframe internal systems as product or platform work when supported
* reframe ETL and warehouse work as data systems experience when supported

---

## Recommended Internal Output Template

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

---

## Final Resume Generation Rule

After analysis, generate the strongest possible tailored resume that stays fully grounded in resume-source-data.md.

When multiple valid narratives are possible, choose the one that gives the best truthful alignment to the job description.
