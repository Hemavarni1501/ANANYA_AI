Technical Stack & System Responsibility Document

Project: ANANYA-AI
Purpose: Define technologies, boundaries, and responsibilities
Scope: MVP (P0 features only)
Architecture Style: MERN + Python AI Microservices

1. High-Level Architecture Overview
ANANYA-AI follows a clear separation of concerns:

Web Layer (MERN): User experience, access control, data orchestration

AI Layer (Python): Intelligence, bias detection, adaptation, analytics

Data Layer: Secure, anonymized, privacy-preserving storage

This separation ensures:

Ethical AI enforcement

Scalability

Maintainability

Auditability (important for judges & institutions)

2. Frontend Stack (React – MERN)
2.1 Core Technologies
Technology	Purpose
React 18	Component-based UI
TypeScript	Type safety & clarity
Vite	Fast builds
TailwindCSS	Accessible design system
Shadcn UI	Prebuilt accessible components
Framer Motion	Smooth, subtle animations
Recharts	Faculty analytics visualizations
Zustand	Client-side state
React Query	Server-state & caching
Socket.io-client	Real-time AI responses
KaTeX / MathJax	Math rendering
react-markdown	Explanation rendering
2.2 Frontend Responsibilities
Frontend is NOT intelligent. It only:

Renders UI

Collects user interactions

Displays AI responses

Applies accessibility preferences

Sends events to backend

❌ Frontend must never:

Detect bias

Decide adaptations

Store learning intelligence

2.3 Frontend Folder Responsibility
src/
├── components/        # UI-only components
├── pages/             # Route-level views
├── hooks/             # UI behavior hooks
├── stores/            # Zustand stores
├── services/          # API calls
├── utils/             # Formatting, helpers
└── styles/            # Design tokens
3. Backend Stack (Node.js + Express)
3.1 Core Technologies
Technology	Purpose
Node.js	Runtime
Express.js	REST API
Socket.io	Real-time channel
MongoDB	Primary datastore
Mongoose	ODM
JWT	Authentication
Zod	Input validation
Helmet	Security headers
Redis	Caching & session memory
3.2 Backend Responsibilities
Backend acts as orchestrator:

Authentication & role control

Session management

API gateway to AI services

Data anonymization

Aggregation for faculty analytics

❌ Backend does not:

Generate explanations

Detect bias directly

Make pedagogical decisions

3.3 Backend API Domains
/api/auth          → Login, roles
/api/learning      → Session lifecycle
/api/ai            → Proxy to Python AI
/api/analytics     → Aggregated insights
/api/content       → Faculty materials
/api/admin         → System oversight
4. Database Stack (MongoDB)
4.1 Why MongoDB
Flexible schema for evolving AI data

Handles unstructured interaction logs

Easy anonymization

Horizontal scalability

4.2 Data Responsibility Rules
Data Type	Stored Where	Notes
Identity	users	Encrypted
Learning interactions	learning_sessions	Pseudonymized
Analytics	anonymized_analytics	No PII
Bias logs	bias_detection_logs	Auditable
❗ Rule:
No AI model ever accesses raw user identity.

5. AI / ML Stack (Python)
5.1 Core Technologies
Technology	Purpose
Python 3.10+	AI runtime
FastAPI	High-performance API
PyTorch	Deep learning
HuggingFace Transformers	LLMs
LangChain	Prompt orchestration
Sentence-Transformers	Embeddings
FAISS	Vector search
5.2 Bias & Fairness Stack (Core Innovation)
Tool	Purpose
Fairlearn	Fairness metrics
AIF360	Bias detection
SHAP	Explainability
textstat	Readability metrics
spaCy	NLP analysis
5.3 AI Service Boundaries
Each AI function is an independent microservice:

AI SERVICES
├── adaptive_tutor        (8001)
├── bias_detection        (8002)
├── content_analyzer      (8003)
├── learning_analytics    (8004)
Services communicate only through APIs.

6. AI Responsibilities (Very Important)
6.1 What AI CAN Do
Detect language complexity mismatch

Detect pacing issues

Detect representation effectiveness

Adapt explanations

Generate anonymized insights

6.2 What AI MUST NOT Do
❌ Infer demographics
❌ Label students
❌ Compare students
❌ Predict intelligence
❌ Store personal identifiers

7. Privacy & Ethics Enforcement (Stack-Level)
7.1 Privacy Techniques Used
Pseudonymization

Differential privacy (aggregates only)

No demographic fields

Session-based learning memory

Data minimization

8. Deployment Stack (MVP)
Layer	Platform
Frontend	Vercel
Backend	Railway / EC2
Database	MongoDB Atlas
Cache	Redis
AI Services	Docker + GPU VM
9. Why This Stack Is Judge-Proof
Industry-standard

Clear boundaries

Ethical AI alignment

Scalable

Auditable

No black-box behavior

10. Stack Validation Checklist
 MERN for web logic

 Python isolated for AI

 Bias detection isolated

 Privacy enforced structurally

 No intelligence leakage to frontend