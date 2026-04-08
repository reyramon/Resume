# Resume Agent Orchestrator - Rey

## Purpose

This file defines the rules, structure, constraints, and coordination logic for generating Rey's resume using specialized section agents.

All resume output must align with the career positioning profile defined in:
`rey-career-profile.md`

This document is not the resume.
This document governs how the resume is created.

The system must be flexible enough to adapt to a wide range of software engineering job descriptions while remaining truthful to the source data.

---

# Global Positioning Rules

## Level Positioning

* Default position: Staff level engineer
* Allow Senior positioning if the job description clearly targets Senior level
* Never fabricate management responsibility
* Emphasize architecture ownership and system impact

Avoid framing as:

* Pure DBA
* Pure DevOps engineer
* Engineering manager

Allow hybrid positioning when supported by source data:

* Backend engineer
* Data systems engineer
* Platform engineer
* Full stack product engineer

---

# Strategic Modes

The orchestrator must determine which positioning mode best aligns with the target job description.

If multiple modes apply, blend them while maintaining resume clarity.

## Mode A - Backend / Systems Engineer

Use when targeting:

* Backend heavy roles
* Infrastructure platforms
* Core services teams
* System reliability teams

Emphasize:

* Architecture ownership
* Performance improvements
* Production reliability
* Backend APIs
* System modernization
* Scalability

De emphasize:

* UI implementation details

## Mode B - Product Systems Engineer

Use when targeting:

* Product engineering roles
* Full stack positions
* Founding engineer roles
* Internal platform teams

Emphasize:

* End to end product ownership
* Building internal tools
* Rapid prototyping
* Developer productivity improvements
* Business impact

De emphasize:

* Deep infrastructure detail

## Mode C - Data Systems / Performance Engineer

Use when targeting:

* Data platform teams
* Analytics infrastructure
* Data heavy backend roles

Emphasize:

* Query performance optimization
* ETL pipelines
* Data processing systems
* Data warehouse workloads
* Large dataset handling
* Data system architecture

De emphasize:

* UI work

## Mode D - Balanced Hybrid

If the job description is broad or ambiguous:

Blend signals from multiple modes while maintaining coherence.

Default emphasis order:

1. Backend systems
2. Data systems
3. Product engineering

---

# Resume Architecture

The resume will be assembled from the following agents.

1. Header Agent
2. Executive Summary Agent
3. Core Competencies Agent
3.5 Resume Strategy Agent
4. Professional Experience Agent
5. Impact Metrics Agent
6. Technical Skills Agent
7. Education Agent
8. Optional Projects Agent
9. Optimization Agent
10. Final Resume Assembly Agent

Each agent operates independently but must follow global rules.

---

# Section Agent Specifications

## 1. Header Agent

Output:

* Name
* Location (San Antonio or Remote)
* LinkedIn
* GitHub if relevant

Constraints:

* Clean
* No adjectives
* No marketing language

## 2. Executive Summary Agent

Length:

3 to 5 lines maximum

Structure the summary using this pattern:

Line 1:
Role identity aligned to the job description

Line 2:
Primary technical strengths

Line 3:
Types of systems built and environments

Line 4 (optional):
Scale or impact indicators

Must:

* Reflect the selected strategic mode
* Position the candidate at Staff or Senior level depending on job description
* Highlight system ownership and engineering impact

Avoid:

* Buzzword stacking
* Motivational language

## 3. Core Competencies Agent

Group into logical clusters based on job description.

Example clusters:

* System Architecture
* Backend Engineering
* Data Systems
* Infrastructure and CI/CD
* Product Development

Keep concise.
No sentences.

## 3.5 Resume Strategy Agent

Before generating resume content, produce a strategy plan.

The strategy plan determines:

- Summary positioning angle
- Role ordering priority
- Top achievements to highlight
- Technologies to emphasize
- Technologies to de-emphasize
- Bullet themes aligned with the job description
- Keywords that should appear naturally

Output format:

Summary Angle:
Role Ordering:
Top Achievements:
Skills to Emphasize:
Skills to De-emphasize:
Bullet Themes:
Keyword Strategy:

This strategy plan guides all subsequent section agents.

## 4. Professional Experience Agent

Highest priority section.

For each role include:

Company
Location
Title
Dates

Then select the top 6 to 8 bullets based on:

1. Relevance to the target job description
2. Demonstrated system ownership
3. Measurable impact
4. Architecture or technical complexity

Lower priority bullets should be removed before removing high-signal bullets.

Professional Experience must be in reverse chronological order (most recent to oldest).

### Bullet Construction Rules

Each bullet must:

* Start with a strong action verb
* Describe ownership
* Include measurable impact when available
* Show technical context

Bad example:

Used C# and SQL to build applications.

Strong example:

Architected backend services supporting financial reporting systems used by thousands of enterprise users.

### Emphasis Strategy

Defense Health Agency

Highlight:

* enterprise financial systems
* performance optimization
* compliance and reliability
* modernization work

WellMed

Highlight:

* healthcare data systems
* large scale rule engine
* cloud architecture research
* developer tooling

Earlier roles

Highlight:

* increasing ownership
* product creation
* internal system development

## 5. Impact Metrics Agent

Extract measurable achievements such as:

* performance improvements
* data scale
* user base size
* migration scope

If metrics are unavailable:

Use qualitative impact without inventing numbers.

## 6. Technical Skills Agent

Organize into tiers.

Core Strength

Strong

Working Knowledge

Avoid listing every technology used.

Select technologies relevant to the job description using this priority order:

1. Technologies appearing in the job description
2. Technologies used repeatedly across multiple roles
3. Technologies tied to measurable impact

Avoid listing technologies used only once unless they directly match the job description.

## 7. Education Agent

Minimal section.

List:

* Degree
* Institution

Avoid unnecessary detail.

## 8. Optional Projects Agent

Include only if:

* Reinforces technical credibility
* Demonstrates system ownership
* Is relevant to the job

## 9. Optimization Agent

Final pass must:

* Remove redundancy
* Compress language
* Ensure strong verbs
* Ensure each bullet demonstrates ownership

After generating optimization suggestions, the system must prepare the resume for final assembly.

The optimization pass is not the final deliverable by itself.
Its recommendations must be applied by the Final Resume Assembly Agent.

If multiple rewrite options exist, choose the version that:
1. Is best supported by source data
2. Improves clarity and impact
3. Strengthens alignment with the job description
4. Preserves concise one or two page readability

## 10. Final Resume Assembly Agent

Purpose:

Take the draft resume, impact metric improvements, ATS keyword analysis, and compression recommendations, then produce the final polished one or two page resume.

Must:

* Apply only truthful improvements supported by source data
* Replace weaker bullets when stronger rewrites are available
* Apply compression edits directly into the resume
* Preserve one or two page readability
* Preserve the strongest achievements
* Keep language direct and concise

Must not:

* Repeat analysis sections
* Output recommendation notes
* Output alternative bullet options
* Output ATS commentary
* Invent metrics or technologies

Final output:

* Return only the final polished resume

---

# Tone Requirements

* Direct
* Clear
* Professional
* Concise

Avoid:

* marketing language
* exaggerated claims

---

# Anti Patterns to Avoid

Do not use:

* Responsible for
* Worked on
* Helped with

Avoid:

* tool stacking without context
* listing obsolete technologies

---

# Assembly Protocol

1. Analyze job description.
2. Determine strategic mode.
3. Generate draft resume.
4. Extract impact metric improvements for weak bullets.
5. Perform ATS keyword alignment check.
6. Generate compression and wording improvements.
7. Apply truthful improvements to the draft resume.
8. Produce final polished one or two page resume only.

---

# Execution Protocol

For each job application provide the AI with four inputs.

1. resume-agent-orchestrator.md
2. rey-career-profile.md
3. resume-source-data.md
4. target job description

The system should execute in two phases.

## Phase 1: Review Packet

Return output in this order:

1. Draft one or two page tailored resume
2. Three improved impact metric variants for weak bullets
3. ATS keyword alignment check
4. Final compression pass improving language

## Phase 2: Final Resume

Using the draft resume and all improvement outputs above, generate:

5. Final polished one or two page resume

Rules for the final polished resume:

* Apply the strongest truthful improvements
* Prefer stronger rewrites for weak bullets when supported
* Apply compression edits directly
* Preserve one or two page readability
* Remove all recommendation notes and analysis commentary
* Return only the final resume text

---

# Metric Recovery Logic

If metrics are missing:

* prefer qualitative impact
* never fabricate
* suggest measurable alternatives when possible

---

# Flexibility Rule

This system must adapt to a wide range of engineering roles while remaining truthful to the source data.

The orchestrator should adjust emphasis rather than forcing the resume into a single predefined career narrative.

The goal is truthful alignment with the job description while highlighting the strongest relevant experience.

---

# Final Output Rules

The system must distinguish between:

* Review output for analysis
* Final output for actual resume use

If producing a review packet:
* include draft resume
* include weak bullet rewrites
* include ATS analysis
* include compression suggestions

If producing the final resume:
* output only the final polished one or two page resume
* apply the best truthful recommendations from prior stages
* remove all commentary, notes, and alternatives
* ensure the result reads as a finished resume, not a working draft

---

# Pandoc / Word Compatibility Rules

To keep generated `.docx` exports highly readable:

* Use standard Markdown bullets with `-`
* Prefer ASCII punctuation in final resume output
* Avoid smart quotes and special separators
* Avoid arrow symbols; use words like `to` instead
* Keep role bullets concise and scannable
* Do not include decorative unicode characters in headers
