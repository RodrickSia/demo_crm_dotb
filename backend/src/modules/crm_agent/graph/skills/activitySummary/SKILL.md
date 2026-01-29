---
name: lead-activity-summarizer
description: Analyze a lead's activity history and provide a concise summary of their engagement patterns along with actionable insights and recommendations. Use when receiving student profile data (UserState) to understand their journey and next steps.
---

# Lead Activity Summarizer

**🚨 MANDATORY OUTPUT FORMAT 🚨**
**Your response MUST be ONLY this format with NO other text:**
`{"activity_summary": "<3-4 sentences summarizing activities>", "activity_summary_explanation": "<2-3 sentences of insights and recommendations>"}`

**DO NOT include ANY of the following:**
- Preambles like "Based on the data..."
- Breakdowns or analysis sections
- Markdown code blocks (```)
- ANY text before `{` or after `}`

## Input Format

Expect prompts containing:
1. Student profile data (UserState JSON)

## Task Description

### 1. Activity Summary
Analyze the following from UserState:
- `calls`: Frequency, duration, and outcomes of phone interactions.
- `meetings`: Attendance at events, workshops, or consultations.
- `attendance`: Regularity of class or session participation.
- `tasks`: types of tasks assigned and their completion status.
- `notes`: Qualitative feedback from staff.

**Output:** A 3-4 sentence professional summary capturing the lead's overall engagement patterns and notable behaviors.

### 2. Insights & Recommendations
Based on the activity summary and data patterns, provide:
- 2-3 key insights about the lead's behavior/potential.
- Specific recommendations for next steps to advance the lead.

**Output:** 2-3 concise, actionable sentences.

## Output Format

**CRITICAL: Your entire response must be ONLY the dictionary string below. No preamble, no explanation, no markdown, no additional text.**

Return exactly this format:
```
{"activity_summary": "Lead has shown high engagement with 3 attended workshops and consistent responsiveness to follow-up calls. However, they have not yet scheduled a placement test despite several reminders in the notes.", "activity_summary_explanation": "The lead is highly interested but may have scheduling constraints. Recommend offering a flexible or online assessment option to move them toward enrollment."}
```
