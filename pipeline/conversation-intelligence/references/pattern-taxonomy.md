# Pattern Taxonomy — Conversation Intelligence

## 5 Pattern Classes

### 1. Competitor Mention
- **Detection:** Named competitor (from competitor-analysis taxonomy) in transcript/reply
- **Variants:** Positive-for-us ("we considered X and rejected them") vs Negative-for-us ("we're going with X instead")
- **Routing:** → competitive-intelligence (function-1)
- **Threshold:** 3 mentions/30d → alert

### 2. Pricing Pushback
- **Detection:** "expensive" / "out of budget" / "negotiate" / specific dollar pushback
- **Routing:** → revenue-forecasting ACV reality-check + objection-handling-library for response prep
- **Threshold:** 4/30d → alert

### 3. Feature Request
- **Detection:** "I wish" / "do you have" / specific named missing feature
- **Routing:** → customer-feedback-analysis (function-6) + product team channel
- **Threshold:** 5/30d → alert

### 4. Champion Language
- **Detection:** Strong-affirmation phrases ("we definitely need this" / "this would solve our X problem")
- **Routing:** → discovery-call-prep (champion-confirm) + kpi-reporting (champion-rate KPI)
- **Threshold:** 2 per deal → flag

### 5. Blocker Signal
- **Detection:** "IT/security/legal/procurement" gating language
- **Routing:** → discovery-call-prep (blocker-prep mode) + pipeline-stages (extends Discovery cycle estimate)
- **Threshold:** 1 per deal → flag

## Source Priority

Transcript (Gong/Chorus/Grain/Fathom) > meeting note > reply text > inferred from context
