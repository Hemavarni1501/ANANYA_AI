Backend Architecture & API Specification

Project: ANANYA-AI
Stack: Node.js + Express + MongoDB + Redis
Role: Secure orchestration & privacy enforcement
Scope: MVP (P0 features only)

1. Backend Design Philosophy
The backend is the ethical gatekeeper of ANANYA-AI.

Its responsibilities are to:

Protect user identity

Orchestrate AI services

Enforce anonymization

Prevent misuse of AI outputs

Serve only role-appropriate data

❗ Backend logic must always prefer privacy over convenience.

2. High-Level Backend Responsibilities
Responsibility	Description
Authentication	Secure login & role validation
Session Control	Learning session lifecycle
AI Orchestration	Proxy requests to Python AI
Data Anonymization	Strip identifiers before analytics
Aggregation	Class-level insights only
Audit Logging	Bias & adaptation traceability
3. API Layer Structure
/api
├── auth
├── learning
├── ai
├── analytics
├── content
├── admin
└── health
4. Authentication & Authorization
4.1 Auth Method
JWT-based authentication

Role-based access control (RBAC)

4.2 Roles
Role	Access
Student	Learning, progress
Faculty	Aggregated analytics
Admin	System oversight
❌ No cross-role data leakage allowed.

5. Core API Endpoints (P0)
5.1 Auth APIs
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
Rules:

No demographic fields

Minimal identity storage

Secure cookie or header tokens

5.2 Learning Session APIs
POST   /api/learning/session/start
POST   /api/learning/session/interact
POST   /api/learning/session/end
Behavior:

Assigns anonymized session ID

Streams interactions via WebSocket

Logs only interaction patterns

5.3 AI Gateway APIs
POST   /api/ai/respond
POST   /api/ai/analyze
Gateway Rules:

Backend never modifies AI output

All requests sanitized

Identity stripped before AI call

5.4 Faculty Analytics APIs
GET    /api/analytics/overview
GET    /api/analytics/bias-alerts
Constraints:

Aggregated data only

Minimum group size enforced

Differential noise applied

5.5 Content Management APIs
POST   /api/content/upload
GET    /api/content/review
PUT    /api/content/update
Pipeline:
Upload → Bias Scan → Review → Publish

5.6 Admin APIs
GET    /api/admin/system-health
GET    /api/admin/bias-logs
PUT    /api/admin/policies
6. Data Models (MongoDB)
6.1 Users Collection
{
  _id: ObjectId,
  email: String,
  passwordHash: String,
  role: "student" | "faculty" | "admin",
  createdAt: Date
}
6.2 Learning Sessions
{
  _id: ObjectId,
  sessionHash: String,
  subject: String,
  interactions: [{
    timestamp: Date,
    actionType: String,
    responseTime: Number,
    adaptationApplied: Boolean
  }]
}
6.3 Anonymized Analytics
{
  _id: ObjectId,
  courseId: ObjectId,
  timeWindow: Date,
  metrics: {
    difficultyZones: Object,
    biasIndicators: Object
  }
}
6.4 Bias Detection Logs (Audit)
{
  _id: ObjectId,
  timestamp: Date,
  biasType: String,
  severity: String,
  actionTaken: String
}
7. Anonymization Pipeline (Mandatory)
function anonymize(session) {
  return {
    sessionHash: hash(session._id + SALT),
    patterns: extractPatterns(session),
    timestampBucket: roundTime(session.createdAt)
  };
}
❗ No student ID passes beyond this layer.

8. Caching Strategy (Redis)
Cache	Purpose
Session state	Real-time learning
AI responses	Reduce cost
Analytics	Faster dashboards
9. Error Handling Rules
No stack traces to client

Generic error messages

Full error logs internally

AI failure → fallback content

10. Backend Validation Checklist
 Role-based isolation

 Anonymization enforced

 No demographic fields

 AI fully sandboxed

 Audit trail present