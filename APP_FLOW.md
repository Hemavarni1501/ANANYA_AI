Application Flow Document

Project: ANANYA-AI
Focus: User journeys & system behavior
Aligned With: PRD.md (P0 scope only)

1. Global Design Principles (Applies to All Flows)
No comparative metrics (no ranks, no peer scores)

No demographic assumptions at any stage

Adaptive behavior is implicit, not announced to users

Privacy-preserving by default

Accessibility tools always available

2. Student Application Flow
2.1 Student Onboarding Flow
Goal: Allow access without collecting sensitive data

Flow:

Student visits platform

Login via campus credentials

System creates:

Anonymous internal learner ID

Empty learning interaction profile

No learning labels assigned

Redirect to Student Dashboard

Key Rule:
❌ No surveys about background, language, or ability

2.2 Student Dashboard Flow
Goal: Provide orientation and confidence without comparison

Flow:

Welcome message (neutral, supportive)

Display:

Current subjects

Recent learning activity

Personal progress indicators

Bias-awareness indicator (system-level, not personal)

Quick access to learning sessions

Excluded:

Leaderboards

Class averages

Percentile indicators

2.3 Learning Session Flow (Core Flow)
Goal: Deliver bias-aware adaptive learning

Flow:

Student selects subject/topic

Initial content rendered at default complexity

Student interacts:

Reads

Asks questions to ANANYA

Requests clarification

System monitors:

Response latency

Repeated errors

Clarification frequency

Bias detection layer evaluates:

Language complexity mismatch

Pace mismatch

Example comprehension issues

Adaptive response triggered:

Simplify language

Change explanation style

Add contextual examples

Learning continues seamlessly

Important:
Adaptation happens without alerting the student.

2.4 Student Progress Flow
Goal: Reinforce growth, not performance anxiety

Flow:

Student opens Progress page

System displays:

Learning journey timeline

Strength areas

Suggested focus topics

Metrics are:

Absolute (personal)

Trend-based

No grades, no ranking

3. Faculty Application Flow
3.1 Faculty Login & Dashboard
Goal: Insight without surveillance

Flow:

Faculty logs in

System verifies role

Dashboard shows:

Aggregated learning trends

Bias detection alerts

Content effectiveness overview

Key Constraint:
Faculty never see individual student data.

3.2 Faculty Analytics Flow
Goal: Identify systemic bias patterns

Flow:

Faculty selects subject/course

System displays:

Common misunderstanding zones

Bias indicators (language, pace)

Confidence drop-off regions

Visualizations are:

Aggregated

Time-based

System suggests:

Content adjustments

Inclusive teaching practices

3.3 Content Creation Flow (Faculty)
Goal: Prevent bias at content creation stage

Flow:

Faculty uploads content

Bias-check tool runs:

Language complexity analysis

Representation diversity check

System flags:

Overly complex phrasing

Culturally narrow examples

Faculty edits content

Approved content published

4. Admin Application Flow
4.1 Admin Dashboard
Goal: Ethical and technical oversight

Flow:

Admin logs in

Dashboard displays:

Bias detection system health

Privacy compliance status

AI decision transparency logs

No access to raw student data

4.2 Compliance & Monitoring Flow
Goal: Maintain ethical AI standards

Flow:

Admin reviews:

Bias detection logs

Adaptation frequency

System provides:

Audit summaries

Risk flags

Admin configures:

Privacy thresholds

Data retention policies

5. Error & Edge Case Flows
5.1 AI Service Unavailable
Fallback to static content

Log incident

Notify admin

5.2 Low Interaction Data
System avoids assumptions

Continues with default explanations

6. Flow Validation Checklist
 No demographic input anywhere

 No comparative metrics

 Privacy preserved at all points

 Adaptation is implicit

 Faculty insights are anonymized