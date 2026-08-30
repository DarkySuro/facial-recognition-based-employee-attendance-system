# AI-Powered Face Recognition Employee Attendance Management System

An AI-powered employee attendance management system that uses **real-time face recognition** to identify employees and automatically record attendance.

The system combines **Computer Vision, Face Recognition, FastAPI, React, SQLAlchemy, MySQL, and REST APIs** to provide an end-to-end employee enrollment, recognition, and attendance workflow.

> **Current Status:** Working End-to-End Prototype
> **Next Phase:** Production hardening and industry-level enhancement

---

## 📌 Overview

Traditional attendance systems often require manual verification, ID cards, biometric devices, or employee interaction.

This project explores an automated alternative using facial recognition.

The system allows an administrator to:

* Register employees
* Enroll an employee using multiple face images
* Generate and store face embeddings
* Perform real-time face recognition
* Identify registered employees
* Reject unknown faces
* Automatically record employee attendance
* Prevent duplicate attendance for the same employee on the same date
* Monitor attendance and recognition activity through a web dashboard

The project is designed with a **modular architecture** so that the AI pipeline, business logic, database layer, API layer, and frontend can evolve independently.

---

# ✨ Key Features

## 👤 Employee Management

* Create and manage employee records
* Track employee status
* Display employee information through the dashboard
* Employee-specific attendance history

## 📸 Face Enrollment

Employees can be enrolled using multiple face images.

The current enrollment workflow requires a minimum of **5 images**.

Each image goes through:

1. Image validation
2. Image decoding
3. Face detection
4. Face quality validation
5. Face embedding extraction
6. Embedding consistency validation
7. Database persistence

The system rejects unsuitable samples instead of blindly storing every uploaded image.

---

## 🧠 Face Recognition

The recognition pipeline uses **InsightFace** for face detection and feature extraction.

The system:

1. Captures frames from the camera
2. Detects faces
3. Generates face embeddings
4. Normalizes embeddings
5. Compares them with enrolled embeddings
6. Calculates similarity
7. Applies the recognition threshold
8. Identifies the employee when the similarity requirement is satisfied

The system also supports handling unknown persons by rejecting faces that do not meet the recognition threshold.

---

## 📊 Automated Attendance

After successful recognition, the system automatically records attendance.

Attendance records contain information such as:

* Employee
* Attendance date
* Check-in time
* Check-out time
* Attendance status
* Recognition confidence

Duplicate attendance is prevented through database-level constraints and application-level attendance handling.

The intended behavior is:

```text
Face Recognized
      ↓
Recognition Validated
      ↓
Attendance Service
      ↓
Check Existing Attendance
      ↓
Already Present? ── Yes ──→ Do Not Create Duplicate
      │
      No
      ↓
Create Attendance Record
```

---

## 📈 Dashboard

The React dashboard provides an overview of the system, including:

* Total employees
* Active employees
* Today's attendance
* Recognition events
* Recent attendance records
* Recognition activity
* Recognition confidence
* Attendance status

The dashboard retrieves data from the FastAPI backend through REST APIs.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      React UI       │
                         │     Frontend        │
                         └──────────┬──────────┘
                                    │
                              REST API / Axios
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │     API Layer       │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ AI / Computer │     │   Services    │     │   Database    │
      │    Vision     │     │    Layer      │     │     Layer     │
      └───────┬───────┘     └───────┬───────┘     └───────┬───────┘
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │ InsightFace │       │  Attendance │       │    MySQL    │
       │ OpenCV      │       │  Enrollment │       │ SQLAlchemy  │
       │ NumPy       │       │ Recognition │       │   Alembic   │
       └─────────────┘       └─────────────┘       └─────────────┘
```

---

# 🔄 Application Workflow

## 1. Employee Registration

```text
Administrator
     ↓
Create Employee
     ↓
Employee ID Generated
```

## 2. Face Enrollment

```text
Upload 5+ Face Images
        ↓
Validate Image
        ↓
Decode with OpenCV
        ↓
Detect Face
        ↓
Check Face Quality
        ↓
Generate Embedding
        ↓
Validate Embedding Consistency
        ↓
Store Embeddings
```

## 3. Real-Time Recognition

```text
Camera Frame
     ↓
Face Detection
     ↓
Face Embedding
     ↓
Embedding Normalization
     ↓
Similarity Comparison
     ↓
Recognition Threshold
     ↓
Employee Identified
```

## 4. Attendance

```text
Employee Recognized
       ↓
Attendance Service
       ↓
Check Existing Attendance
       ↓
Create / Update Attendance
       ↓
MySQL
       ↓
Dashboard
```

---

# 🧠 AI / ML Pipeline

The project uses **InsightFace** with the `buffalo_l` model for face analysis and embedding generation.

### Embeddings

The system uses **512-dimensional face embeddings**.

Embeddings are normalized before similarity comparison.

### Similarity

Recognition uses cosine similarity between the live face embedding and enrolled embeddings.

Conceptually:

```text
similarity = normalized_embedding_1 · normalized_embedding_2
```

Higher similarity indicates greater facial feature similarity.

### Enrollment Consistency

Multiple enrollment samples are compared to ensure that the captured samples are sufficiently consistent before they are persisted.

This helps prevent poor-quality or inconsistent enrollment data from entering the recognition database.

---

# 🛡️ Recognition & Enrollment Validation

The system contains several validation stages.

### Enrollment

* Minimum number of samples
* Image MIME-type validation
* Image decoding validation
* Face detection validation
* Face detection confidence
* Face quality checks
* Embedding validation
* Embedding consistency validation

### Recognition

* Face detection
* Face quality validation
* Embedding generation
* Similarity calculation
* Recognition threshold
* Recognition stabilization
* Duplicate attendance prevention

---

# 🧰 Technology Stack

## Backend

| Technology   | Purpose                              |
| ------------ | ------------------------------------ |
| Python       | Core backend and AI development      |
| FastAPI      | REST API framework                   |
| Uvicorn      | ASGI server                          |
| SQLAlchemy   | ORM / database abstraction           |
| Alembic      | Database migrations                  |
| MySQL        | Relational database                  |
| NumPy        | Numerical computation                |
| OpenCV       | Image processing and camera handling |
| InsightFace  | Face detection and recognition       |
| ONNX Runtime | AI model inference                   |

## Frontend

| Technology   | Purpose              |
| ------------ | -------------------- |
| React        | Frontend application |
| Vite         | Frontend build tool  |
| Axios        | API communication    |
| Tailwind CSS | UI styling           |
| JavaScript   | Frontend logic       |

## Development

* Git
* GitHub
* VS Code
* MySQL Workbench
* `uv`

---

# 📁 Project Structure

```text
facial-recognition-based-employee-attendance-system/
│
├── backend/
│   └── app/
│       ├── ai/
│       │   ├── face_engine.py
│       │   └── quality.py
│       │
│       ├── api/
│       │
│       ├── db/
│       │
│       ├── models/
│       │
│       ├── schemas/
│       │
│       └── services/
│
├── frontend/
│   └── src/
│       ├── assets/
│       │
│       ├── components/
│       │   ├── EmployeeDetails.jsx
│       │   ├── EmployeeTable.jsx
│       │   ├── Sidebar.jsx
│       │   └── StatCard.jsx
│       │
│       ├── layouts/
│       │   └── DashboardLayout.jsx
│       │
│       ├── pages/
│       │   ├── AttendancePage.jsx
│       │   ├── DashboardPage.jsx
│       │   ├── EmployeesPage.jsx
│       │   ├── EnrollmentPage.jsx
│       │   └── RecognitionLogPage.jsx
│       │
│       └── services/
│           ├── api.js
│           ├── attendanceService.js
│           ├── employeeService.js
│           ├── faceEnrollmentService.js
│           └── recognitionLogService.js
│
├── alembic/
│
├── tests/
│
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

> The exact structure may evolve as the project moves from prototype to production architecture.

---

# ⚙️ Installation

## Prerequisites

Make sure the following are installed:

* Python 3.12+
* Node.js
* npm
* MySQL
* Git
* `uv`

---

# 🔧 Backend Setup

Clone the repository:

```bash
git clone https://github.com/DarkySuro/facial-recognition-based-employee-attendance-system.git

cd facial-recognition-based-employee-attendance-system
```

Create the Python environment using `uv`:

```bash
uv sync
```

Configure the database connection in your environment file.

Example:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/attendance_db
```

Run database migrations:

```bash
uv run alembic upgrade head
```

Start the FastAPI server:

```bash
uv run uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🗄️ Database

The application uses MySQL as its primary relational database.

Core entities include:

```text
Employees
    │
    ├── Face Embeddings
    │
    ├── Attendance
    │
    └── Recognition Logs
```

Database schema changes are managed through **Alembic migrations**.

Example migration workflow:

```bash
uv run alembic revision --autogenerate -m "describe schema change"

uv run alembic upgrade head
```

---

# 🔌 API Overview

The backend exposes REST APIs for major application operations.

Examples include:

```text
POST   /api/v1/employees
GET    /api/v1/employees
GET    /api/v1/employees/{employee_id}

POST   /api/v1/employees/{employee_id}/face-enrollment

POST   /api/v1/employees/{employee_id}/face-enrollment/images

GET    /api/v1/attendance
GET    /api/v1/attendance/employee/{employee_id}

GET    /api/v1/recognition-logs
```

Interactive API documentation is available through FastAPI Swagger UI.

---

# 🧪 Current Prototype Validation

The current implementation has been tested through the complete enrollment workflow.

Example enrollment result:

```json
{
  "employee_id": 1,
  "embeddings_saved": 5,
  "minimum_similarity": 0.7424,
  "maximum_similarity": 0.9220,
  "average_similarity": 0.8418
}
```

This demonstrates that five enrollment samples were successfully processed, validated, and persisted.

The live recognition workflow has also been tested with successful employee recognition and automatic attendance creation.

---

# 🚀 Current Development Status

### Completed

* [x] FastAPI backend
* [x] MySQL database integration
* [x] SQLAlchemy ORM
* [x] Alembic migrations
* [x] Employee management APIs
* [x] Face enrollment pipeline
* [x] Multiple image upload
* [x] Face quality validation
* [x] InsightFace integration
* [x] 512-dimensional face embeddings
* [x] Embedding normalization
* [x] Embedding consistency validation
* [x] Face embedding persistence
* [x] Real-time face recognition
* [x] Recognition similarity calculation
* [x] Recognition stabilization
* [x] Attendance creation
* [x] Duplicate attendance prevention
* [x] Recognition logs
* [x] React dashboard
* [x] Employee management frontend
* [x] Attendance frontend
* [x] Face enrollment frontend
* [x] Recognition activity dashboard
* [x] Frontend-to-backend multipart image upload

### 🚧 Planned — Production / Industry-Level Phase

* [ ] Authentication and authorization
* [ ] Role-based access control
* [ ] Production-grade frontend architecture
* [ ] Improved real-time recognition UI
* [ ] WebSocket/SSE-based real-time dashboard updates
* [ ] Better recognition tracking
* [ ] Improved camera lifecycle management
* [ ] Advanced face quality metrics
* [ ] Configurable recognition thresholds
* [ ] Comprehensive automated tests
* [ ] API integration tests
* [ ] Structured logging
* [ ] Centralized exception handling
* [ ] Configuration management
* [ ] Security hardening
* [ ] Rate limiting
* [ ] Dockerization
* [ ] CI/CD pipeline
* [ ] Production deployment
* [ ] Monitoring and health checks
* [ ] Performance optimization
* [ ] Database indexing optimization
* [ ] API documentation improvements

---

# 🔐 Security Considerations

Face recognition systems handle biometric information and therefore require careful security considerations.

Future production work will focus on:

* Secure authentication
* Authorization and RBAC
* Protected API endpoints
* Secure environment configuration
* Database access controls
* Input validation
* File upload restrictions
* API rate limiting
* Secure storage of face embeddings
* Audit logging
* Data retention policies
* Protection against unauthorized access

This prototype should **not be considered production-ready for handling sensitive biometric data** without additional security and privacy controls.

---

# 📊 Design Principles

The project is being developed with the following principles:

### Modularity

AI logic, services, APIs, database models, and frontend components should remain independently maintainable.

### Separation of Concerns

Business logic should not be tightly coupled to API routes or UI components.

### Maintainability

Code should be structured so that future developers can understand and modify individual components without unnecessarily affecting the entire system.

### Reliability

Recognition and attendance operations should be validated before modifying persistent data.

### Extensibility

The architecture should support future improvements such as authentication, real-time communication, better tracking, cloud deployment, and advanced recognition strategies.

---

# 🛣️ Development Roadmap

The project is being developed progressively.

```text
Phase 1
Backend Foundation
        ↓
Phase 2
Database & Migrations
        ↓
Phase 3
Face Enrollment Pipeline
        ↓
Phase 4
Face Recognition
        ↓
Phase 5
Attendance Management
        ↓
Phase 6
React Frontend Prototype
        ↓
Phase 7
End-to-End Integration
        ↓
Phase 8
Production Hardening
        ↓
Phase 9
Testing & Security
        ↓
Phase 10
Deployment & Monitoring
```

The current repository represents the **working end-to-end prototype baseline**. Future development will focus on transforming this prototype into a more robust, scalable, secure, and production-oriented system.

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

For significant changes:

1. Create a feature branch
2. Implement the change
3. Add or update tests
4. Verify the complete workflow
5. Commit with a descriptive message
6. Open a pull request

Example:

```bash
git checkout -b feature/improve-recognition-pipeline
```

---

# 📜 License

This project is currently intended for educational, research, and portfolio development purposes.

A formal open-source license can be added before public production distribution.

---

# 👨‍💻 Author

**Surojit Jana**

B.Tech — Computer Science & Engineering

GitHub: [DarkySuro](https://github.com/DarkySuro)

---

# ⭐ Project Vision

The long-term goal of this project is to evolve the current working prototype into a **production-oriented AI attendance platform** with:

* Reliable real-time face recognition
* Robust attendance processing
* Secure biometric data handling
* Scalable backend architecture
* Maintainable frontend architecture
* Automated testing
* Observability and monitoring
* Containerized deployment
* CI/CD
* Production-grade security

The prototype establishes the core AI, backend, database, and frontend workflow. The next stage focuses on engineering the system for **reliability, security, scalability, and maintainability**.
