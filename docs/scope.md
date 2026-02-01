# Product Scope & MVP Definition

## Target Audience
* **Primary:** Technical Recruiters & Hiring Managers.
* **Goal:** Increase consistency in evaluation and reduce the administrative burden of writing scorecards.

## 2. In-Scope (MVP + V1)

### Phase 1: Interview Preparation
- [ ] **Ingestion:** Parse Job Descriptions (JD) and Candidate Resumes (PDF/Text).
- [ ] **Generation:** Create a structured interview guide with specific technical questions based on the JD-Resume gap.
- [ ] **Rubric:** Auto-generate specific "Look for" signals for every question.

### Phase 2: Live Copilot (The Core)
- [ ] **Audio:** Real-time ingestion via browser microphone or system audio loopback.
- [ ] **Transcription:** Low-latency speech-to-text.
- [ ] **Copilot UI:**
    - Non-intrusive side panel.
    - Real-time checklist of "covered topics."
    - Suggested follow-up questions based on the last 30 seconds of context.

### Phase 3: Post-Interview Intelligence
- [ ] **Summarization:** Structured summary (Strengths, Weaknesses, Flags).
- [ ] **Scoring:** 0-5 rating per competency, **strictly backed by quoted evidence**.
- [ ] **Recruiter Feedback:** Private tips for the interviewer (e.g., "You spoke 60% of the time").

## 3. Integrations (MVP)
* **Video:** Agnostic (System Audio / "Listen Only" Bot). We will not build deep API integrations with Zoom/Meet in V1.
* **ATS:** Export results as Copy-Paste Markdown or PDF.

---

## 5. Success Criteria
* **Latency:** Real-time prompts appear < 3 seconds after the candidate pauses.
* **Utility:** Users click/use at least 1 AI-generated follow-up question per interview.
* **Trust:** Users accept >80% of the generated scorecard summaries with minor or no edits.
