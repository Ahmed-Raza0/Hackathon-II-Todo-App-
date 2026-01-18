# SP-BACKEND-HF-BUILD – Hugging Face Backend Build & Runtime Specification

This **SP-SPECIFY** defines the **authoritative requirements** for running the **FastAPI backend on Hugging Face Spaces** when **no Dockerfile is provided** and the build is failing.

This spec is binding and exists to ensure the backend **builds, starts, and serves traffic correctly** on Hugging Face infrastructure.

---

## SP-HF-01: Problem Statement

Observed issue:

• Backend uploaded to Hugging Face
• No Dockerfile present
• Hugging Face build does not start or fails silently

**Root cause:** Hugging Face Spaces requires a **declared runtime entrypoint**. Without Docker, this must follow Hugging Face's **Python Space contract**.

---

## SP-HF-02: Approved Runtime Mode (Non‑Negotiable)

✅ **Python Space (Gradio-less FastAPI)**

❌ Docker Space (FORBIDDEN in this spec)
❌ Missing runtime declaration

---

## SP-HF-03: Required Root-Level Files

The backend repository **MUST contain** the following files at root level:

```
main.py          ← ENTRYPOINT (MANDATORY)
requirements.txt ← DEPENDENCIES (MANDATORY)
README.md        ← OPTIONAL
```

❌ Backend nested inside folders is FORBIDDEN

---

## SP-HF-04: main.py Runtime Contract (CRITICAL)

### Required Properties

• File name MUST be `main.py`
• MUST expose variable `app`
• MUST NOT rely on `if __name__ == '__main__'`
• MUST NOT call `uvicorn.run()` directly

### Canonical Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}
```

Hugging Face automatically runs the ASGI app.

---

## SP-HF-05: requirements.txt Contract

### MUST include (minimum):

```
fastapi
uvicorn
pydantic
sqlmodel
python-dotenv
```

❌ Version pinning is OPTIONAL but recommended
❌ Missing uvicorn → runtime FAIL

---

## SP-HF-06: Hugging Face Space Configuration

### Space Settings

| Setting        | Value     |
| -------------- | --------- |
| SDK            | Python    |
| Python Version | 3.10      |
| App File       | `main.py` |

If App File is not `main.py` → build FAIL

---

## SP-HF-07: Port Binding Rule

Hugging Face exposes the app automatically.

❌ Hardcoded ports are FORBIDDEN
❌ `--port` flags are FORBIDDEN

FastAPI MUST listen via ASGI only.

---

## SP-HF-08: Environment Variables

All secrets MUST be read via environment variables:

```
DATABASE_URL
BETTER_AUTH_SECRET
OPENAI_API_KEY
```

❌ Hardcoded secrets → REJECTED by HF

---

## SP-HF-09: Common Build Failure Causes & Fixes

| Failure            | Cause              | Resolution   |
| ------------------ | ------------------ | ------------ |
| Build never starts | Missing main.py    | Move to root |
| App crash          | uvicorn.run() used | Remove it    |
| Module not found   | Wrong imports      | Fix paths    |
| Port error         | Hardcoded port     | Remove port  |

---

## SP-HF-10: Validation Checklist

✔ Space set to Python SDK
✔ `main.py` at root
✔ `app` exposed
✔ `requirements.txt` present
✔ No Dockerfile
✔ No hardcoded ports

---

## SP-HF-11: Supremacy Clause

Hierarchy:

**Constitution > Backend Spec > SP-BACKEND-HF-BUILD > Code**

If Hugging Face build fails, this spec must be checked before any code changes.

---

**End of SP-BACKEND-HF-BUILD Specification**

## User Scenarios & Testing

### Scenario 1: Hugging Face Space Creation
**Given**: Developer uploads backend to Hugging Face without Dockerfile
**When**: Space is created with Python SDK and main.py exists at root
**Then**: Build starts and app runs successfully
**Validation**: Space shows running status and responds to HTTP requests

### Scenario 2: App Startup on Hugging Face Infrastructure
**Given**: Backend code is in repository with correct main.py structure
**When**: Hugging Face runtime loads the app
**Then**: FastAPI app is automatically instantiated and served
**Validation**: ASGI interface is properly exposed as 'app' variable

### Scenario 3: Environment Variable Access
**Given**: Secrets are configured in Hugging Face Space settings
**When**: App reads environment variables
**Then**: Secrets are accessible via os.environ
**Validation**: No hardcoded credentials in source code

### Scenario 4: Dependency Installation
**Given**: requirements.txt exists with proper dependencies
**When**: Hugging Face build process runs
**Then**: All dependencies are installed successfully
**Validation**: No "module not found" errors during startup

## Functional Requirements

### FR-01: Runtime Entry Point Declaration
**Requirement**: The system must declare a proper runtime entry point for Hugging Face Spaces.
**Acceptance Criteria**:
- File named main.py exists at repository root
- File exposes a FastAPI app instance as variable named 'app'
- No __name__ == '__main__' guards that prevent ASGI loading
- No direct uvicorn.run() calls that conflict with Hugging Face hosting

### FR-02: Dependency Management
**Requirement**: The system must properly declare dependencies for Hugging Face build process.
**Acceptance Criteria**:
- requirements.txt file exists at repository root
- File includes all necessary packages (fastapi, uvicorn, pydantic, etc.)
- Dependencies are compatible with Hugging Face's Python environment
- No version conflicts that prevent installation

### FR-03: Configuration via Environment Variables
**Requirement**: The system must read all configuration values from environment variables.
**Acceptance Criteria**:
- All secrets are accessed via environment variables, not hardcoded
- Configuration values like database URLs come from environment
- No sensitive data stored in source code
- App functions properly with Hugging Face's environment variable system

### FR-04: Port Binding Compliance
**Requirement**: The system must not bind to specific ports that conflict with Hugging Face's reverse proxy.
**Acceptance Criteria**:
- No hardcoded port numbers in application code
- No --port command line arguments
- App listens on whatever port Hugging Face assigns
- FastAPI uses ASGI interface without manual server startup

### FR-05: File Structure Compliance
**Requirement**: The system must follow Hugging Face's expected repository structure.
**Acceptance Criteria**:
- All required files exist at repository root level
- No nested directory structure that hides entry point
- README.md provides proper documentation for Hugging Face users
- No conflicting configuration files that interfere with build process

## Success Criteria

### Quantitative Measures
- 100% of builds start successfully when main.py is properly configured
- 0% of hardcoded secrets present in source code
- 100% of required dependencies successfully installed during build
- 0% of port binding conflicts during deployment
- Build completion time under 5 minutes

### Qualitative Measures
- Users can successfully deploy backend to Hugging Face Spaces
- Application responds correctly to HTTP requests
- Environment variables are properly utilized for configuration
- Error messages are clear when configuration requirements aren't met
- Deployment process follows Hugging Face's recommended practices

## Key Entities

### Runtime Entry Point (main.py)
- **Location**: Repository root directory
- **Purpose**: Entry point for Hugging Face's Python Space runtime
- **Interface**: Must expose FastAPI app instance as 'app' variable
- **Constraints**: Must use ASGI interface, no direct server startup

### Dependencies Manifest (requirements.txt)
- **Location**: Repository root directory
- **Purpose**: Declare Python dependencies for build process
- **Content**: List of required packages with optional version constraints
- **Constraints**: Must be compatible with Hugging Face's Python 3.10 environment

### Environment Configuration
- **Mechanism**: OS environment variables via Hugging Face Space settings
- **Purpose**: Secure configuration without hardcoded values
- **Access Method**: os.environ.get() pattern
- **Constraints**: No hardcoded secrets in source code

## Assumptions

- Hugging Face Spaces supports the Python SDK with ASGI applications
- FastAPI applications can run without explicit uvicorn startup in Hugging Face environment
- Python 3.10 is available in the Hugging Face build environment
- Standard Python packages (fastapi, uvicorn, etc.) are compatible with Hugging Face's environment
- Environment variables are the only secure way to provide secrets to Hugging Face Spaces

## Constraints

- Only one runtime entry point file (main.py) allowed at root
- No Dockerfile or container-based deployment (per specification)
- No hardcoded ports or server startup commands
- All secrets must come from environment variables
- Dependencies must be compatible with Hugging Face's Python 3.10 environment

## Dependencies

- Hugging Face Spaces Python SDK
- FastAPI framework for the web application
- Uvicorn ASGI server for Hugging Face's runtime environment
- Pydantic for data validation
- SQLModel for database operations
- Python-dotenv for environment variable management