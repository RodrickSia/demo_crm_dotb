---
name: followup-action-recommender
description: Recommend the most appropriate next follow-up action for a lead based on their profile and engagement history. Provide a specific action from a predefined list along with a professional explanation.
---

# Follow-up Action Recommender

**🚨 MANDATORY OUTPUT FORMAT 🚨**
**Your response MUST be ONLY this format with NO other text:**
`{"followup_action": "<Exact Action Name>", "followup_action_explanation": "<2-3 sentence explanation>"}`

**DO NOT include ANY of the following:**
- Preambles or closing remarks
- Markdown code blocks (```)
- ANY text before `{` or after `}`

## Valid Actions
You MUST choose ONLY from this list:
1. Send Welcome Email
2. Schedule Discovery Call
3. Share Program Information
4. Invite to Open House/Campus Tour
5. Send Personalized Enrollment Proposal
6. Follow Up on Pending Application
7. Schedule Assessment/Placement Test
8. Offer Trial Class/Demo Session
9. Send Re-Engagement Campaign
10. Request Referral/Testimonial

## Task Description
Analyze the student profile data (UserState) to determine:
- Current engagement level and responsiveness
- Recent activity and interaction history
- Stage in the customer journey
- Outstanding needs or gaps

**Output:**
- `followup_action`: The most appropriate action from the list above.
- `followup_action_explanation`: A concise 2-3 sentence explanation for why this action is the best next step, citing specific factors from the user data.

## Output Format
Example:
```
{"followup_action": "Schedule Discovery Call", "followup_action_explanation": "The lead has attended multiple workshops and expressed interest in specialized programs. A discovery call will help clarify their specific goals and recommend the most suitable enrollment track."}
```
