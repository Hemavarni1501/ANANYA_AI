Frontend Design & Accessibility Guidelines

Project: ANANYA-AI
Audience: Frontend developers, designers
Goal: Bias-conscious, inclusive, accessible UI
Scope: MVP (P0 features)

1. Design Philosophy
ANANYA-AI’s UI must never reinforce inequality.

Core principles:

Accessibility-first

Non-competitive

Bias-neutral visuals

Calm, confidence-building experience

Adaptive without being intrusive

❗ UI must support learning, not evaluate learners.

2. Bias-Conscious UI Rules (Mandatory)
2.1 What UI MUST NOT Include
Rankings, leaderboards

Percentile scores

“Top performer” indicators

Competitive color coding

Stereotypical imagery (culture, gender, ability)

2.2 What UI MUST Include
Personal progress indicators only

Neutral language (“You explored”, not “You lag behind”)

Multiple representation options (text, visuals)

Easy access to accessibility tools

3. Color System (Accessible & Inclusive)
3.1 Core Palette
Purpose	Color	Reason
Primary	#2563EB	Trust, focus
Secondary	#10B981	Growth
Neutral	#64748B	Balance
Warning	#F59E0B	Attention
Error	#EF4444	Clarity
Background (Light)	#F8FAFC	Low strain
Background (Dark)	#0F172A	Night accessibility
✔ Contrast ratio ≥ WCAG 2.1 AA

4. Typography System
4.1 Fonts
Use	Font
Primary UI	Inter
Accessibility Option	OpenDyslexic
Code	JetBrains Mono
4.2 Rules
Minimum base size: 16px

Line height ≥ 1.6

User-adjustable font size

No condensed fonts

5. Layout & Spacing
5.1 Grid System
8px spacing grid

Max content width: 1200px

Generous white space

5.2 Responsiveness
Breakpoints:

Mobile: 640px

Tablet: 768px

Desktop: 1024px

Large: 1280px

Mobile-first design is mandatory.

6. Core UI Components (P0)
6.1 Student Components
Dashboard Cards

AI Tutor Chat Window

Learning Content Viewer

Progress Timeline

Accessibility Control Panel

6.2 Faculty Components
Analytics Charts (aggregated only)

Bias Alert Cards

Content Review Panel

6.3 Admin Components
System Health Metrics

Bias Detection Logs

Privacy Compliance Status

7. Accessibility Requirements (WCAG 2.1 AA)
Mandatory features:

Keyboard navigation

Screen-reader compatibility

Focus states visible

Text-to-speech toggle

Color contrast controls

Language switcher

8. Motion & Animation
8.1 Rules
Subtle only (200–300ms)

No motion essential to understanding

Disable animations option required

9. UI State Guidelines
State	Requirement
Loading	Calm skeleton loaders
Error	Clear, non-blaming messages
Empty	Encouraging guidance
Success	Minimal, affirming
10. Frontend Validation Checklist
 No competitive UI

 Accessible colors & fonts

 Language neutral & supportive

 Accessibility controls visible

 Mobile usable