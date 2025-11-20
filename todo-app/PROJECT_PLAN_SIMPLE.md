# ToDo Application Project Plan - Simplified Standalone Version

## Project Overview

A modern, educational web application for managing todos with a stunning UI. Built with Python, FastAPI, and HTMX, this **standalone version** eliminates external dependencies (no Supabase, no database) for maximum simplicity and learning focus. Demonstrates server-side rendering with SPA-like user experience, suitable for workshops on AI coding agents and as a reference for porting to other languages/frameworks.

**Key Difference**: This version uses **mock authentication** and **in-memory data storage** instead of Supabase, making it perfect for learning, workshops, and rapid prototyping without any external service dependencies.

## MVP Scope & Philosophy

**This is an MVP/Lab project** - the goal is educational clarity, not production completeness. We prioritize:
- **Simple over complex**: Clear patterns over extensive features
- **Working over perfect**: Functional examples over comprehensive edge case handling
- **Teachable over scalable**: Code that's easy to understand and modify
- **Zero setup friction**: No external services, no configuration, just run it

**MVP Feature Set**:
- Mock authentication (login, register, logout) - **no real security**
- Multiple todo lists per user
- Todo items with: title, notes, completion status, due dates, priority levels
- Basic search (text match on titles)
- Simple list reordering (up/down buttons, not drag-drop)

**Explicitly OUT of MVP Scope**:
- Tags/categories (can be added as workshop exercise)
- Advanced filtering/sorting
- Statistics dashboard
- Password reset/change (no real auth system)
- Email verification
- Rate limiting
- Drag-and-drop reordering
- Extensive monitoring/observability
- CI/CD pipeline
- Data persistence (resets on server restart)

**What Makes This "Simple"**:
- ❌ No Supabase or any external service
- ❌ No database (PostgreSQL, SQLite, etc.)
- ❌ No real authentication (plain text passwords, mock sessions)
- ❌ No JWT tokens or password hashing
- ❌ No RLS policies or security concerns
- ✅ Pure in-memory Python dictionaries
- ✅ Can run immediately with `uv run uvicorn`
- ✅ Perfect for learning and workshops

## Technology Stack

### Core Technologies
- **Backend Framework**: FastAPI 0.115+
- **Frontend Approach**: HTMX 2.0+ (via CDN)
- **Templating**: Jinja2
- **UI Components**: Shoelace 2.20+ (via CDN)
- **Data Storage**: In-memory Python dictionaries (no database!)
- **Auth**: Mock sessions with cookies (no JWT, no Supabase Auth)
- **Package Management**: uv 0.5+
- **Python Version**: 3.11 or 3.12

### Key Libraries (pinned in pyproject.toml)
- `fastapi>=0.115.0` - Web framework
- `uvicorn[standard]>=0.32.0` - ASGI server
- `jinja2>=3.1.0` - Templating engine
- `python-multipart>=0.0.9` - Form data parsing
- `pytest>=8.0.0` - Testing framework (dev)
- `httpx>=0.27.0` - Async HTTP client for tests (dev)

**That's it!** Only 4 core dependencies (2 dev dependencies). Compare to full version: no `supabase`, no `python-jose`, no database drivers.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────┐
│           Browser (Client)                  │
│  ┌──────────────┐  ┌──────────────────────┐│
│  │  HTML + CSS  │  │  Shoelace Components ││
│  │  + Vanilla JS│  │  HTMX (via CDN)      ││
│  └──────────────┘  └──────────────────────┘│
└─────────────────┬───────────────────────────┘
                  │ HTTP/HTTPS
                  │ (HTMX Requests)
┌─────────────────▼───────────────────────────┐
│         FastAPI Application                 │
│  ┌──────────────────────────────────────┐  │
│  │  Routes (endpoints)                   │  │
│  │  - Auth routes                        │  │
│  │  - Todo list routes                   │  │
│  │  - Todo item routes                   │  │
│  │  - Partial HTML responses for HTMX    │  │
│  └────────────┬─────────────────────────┘  │
│               │                              │
│  ┌────────────▼─────────────────────────┐  │
│  │  Services (Business Logic)            │  │
│  │  - Authentication service             │  │
│  │  - Todo list service                  │  │
│  │  - Todo item service                  │  │
│  └────────────┬─────────────────────────┘  │
│               │                              │
│  ┌────────────▼─────────────────────────┐  │
│  │  Models (Domain Model)                │  │
│  │  - User, TodoList, Todo               │  │
│  └────────────┬─────────────────────────┘  │
│               │                              │
│  ┌────────────▼─────────────────────────┐  │
│  │  Jinja2 Templates                     │  │
│  │  - base.html                          │  │
│  │  - login.html                         │  │
│  │  - app.html (main app)                │  │
│  │  - partials/* (HTMX responses)        │  │
│  └──────────────────────────────────────┘  │
│               │                              │
│  ┌────────────▼─────────────────────────┐  │
│  │  In-Memory Storage (Global Dicts)    │  │
│  │  - USERS = {}                         │  │
│  │  - TODO_LISTS = {}                    │  │
│  │  - TODOS = {}                         │  │
│  │  - SESSIONS = {}                      │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘

No Supabase! No Database! Just Python dictionaries!
```

### Authentication & Session Management (Mock)

**Token Strategy** (mock - intentionally simple):
- **NO JWT tokens** - just random UUID session IDs
- **NO password hashing** - plain text storage (for educational purposes only!)
- Store `session_id` in HTTP-only cookie
- Map session_id → user_id in memory (SESSIONS dict)
- Session lost on server restart (no persistence)

**Cookie Configuration**:
- Development: `secure=False` (HTTP allowed), `samesite="lax"`
- Production: `secure=True` (HTTPS only), `samesite="lax"` (if you deploy this simple version)
- Both: `httponly=True`, `max_age=3600` (1 hour)
- **IMPORTANT**: This is intentionally insecure - for learning only!

**Authentication Flow** (mock):
1. User visits `/` → check session_id cookie → redirects to `/login` if missing/invalid
2. Login form (HTMX) → POST `/auth/login` → check email/password in USERS dict (plain text!)
3. On success: create random session_id → store in SESSIONS dict → set cookie → return HX-Redirect to `/app`
4. On error: return error partial to display in form
5. Logout: DELETE `/auth/logout` → delete from SESSIONS dict → clear cookie → redirect to `/login`

**Session Validation** (mock):
- Every protected route uses `get_current_user_id` dependency
- Dependency extracts session_id cookie → looks up in SESSIONS dict
- Returns user_id or raises 401
- No JWT validation, no Supabase, just dict lookup!

**Security Note**: This is **intentionally insecure** for educational purposes. Never use in production!

### Application Flow

1. **HTMX Interaction Pattern**:
   - User actions trigger HTMX requests (hx-get, hx-post, hx-delete, hx-patch)
   - Server checks for `HX-Request` header
   - If HTMX request: return HTML partial
   - If regular request: return full page
   - HTMX swaps returned HTML into target element
   - Loading states: use `hx-indicator` for spinners

2. **Data Flow**:
   - Routes receive requests → authenticate user → validate with Pydantic
   - Call service layer with validated data + user_id
   - Services interact with in-memory dicts (USERS, TODO_LISTS, TODOS)
   - Return data to routes
   - Routes render Jinja2 templates/partials
   - Return HTML to browser

## Domain Model

### In-Memory Data Structures

```python
# Global storage (in main.py)
# WARNING: All data lost on server restart!

from typing import Dict
from uuid import UUID

# Storage dictionaries
USERS: Dict[str, dict] = {}          # user_id -> user data
TODO_LISTS: Dict[str, dict] = {}     # list_id -> list data
TODOS: Dict[str, dict] = {}          # todo_id -> todo data
SESSIONS: Dict[str, str] = {}        # session_id -> user_id

# User structure
user = {
    "id": "uuid-string",
    "email": "user@example.com",
    "password": "plaintext123",  # NO HASHING!
    "created_at": "2025-11-20T12:00:00"
}

# TodoList structure
todo_list = {
    "id": "uuid-string",
    "user_id": "uuid-string",
    "name": "Work Tasks",
    "description": "Things to do at work",
    "color": "#3b82f6",
    "position": 0,
    "created_at": "2025-11-20T12:00:00",
    "updated_at": "2025-11-20T12:00:00"
}

# Todo structure
todo = {
    "id": "uuid-string",
    "list_id": "uuid-string",
    "title": "Buy groceries",
    "note": "Milk, eggs, bread",
    "is_completed": False,
    "completed_at": None,
    "due_date": "2025-11-25",  # ISO date string or None
    "priority": "medium",  # 'low', 'medium', 'high'
    "position": 0,
    "created_at": "2025-11-20T12:00:00",
    "updated_at": "2025-11-20T12:00:00"
}
```

**Comparison to Full Version**:
- Full version: PostgreSQL tables with foreign keys, indexes, RLS policies
- Simple version: Python dictionaries with string keys, no constraints
- Full version: Persists to database
- Simple version: Lost on restart (can add JSON file persistence as exercise)

### Pydantic Models

```python
# Request/Response Models
# (Same as full version - validation still important!)

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID

# Authentication
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

# Todo Lists
class TodoListCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    color: Optional[str] = "#3b82f6"  # default blue

class TodoListUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = None
    position: Optional[int] = None

class TodoListResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    color: str
    position: int
    todo_count: int
    completed_count: int
    created_at: datetime

# Todos
class TodoCreate(BaseModel):
    title: str = Field(..., max_length=200)
    note: Optional[str] = None
    due_date: Optional[date] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    note: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    position: Optional[int] = None

class TodoResponse(BaseModel):
    id: UUID
    list_id: UUID
    title: str
    note: Optional[str]
    is_completed: bool
    completed_at: Optional[datetime]
    due_date: Optional[date]
    priority: str
    position: int
    is_overdue: bool  # computed property
    created_at: datetime
    updated_at: datetime
```

## Project Structure

```
todo-lab-python/
├── .gitignore
├── pyproject.toml                # uv project configuration
├── README.md                     # Project documentation
├── PROJECT_PLAN_SIMPLE.md       # This file
└── src/
    └── app/
        ├── __init__.py
        ├── main.py              # FastAPI app + in-memory storage
        ├── config.py            # Minimal config (SECRET_KEY optional)
        │
        ├── core/                # Core functionality
        │   ├── __init__.py
        │   ├── deps.py          # Dependencies (auth)
        │   └── storage.py       # In-memory storage helpers
        │
        ├── models/              # Pydantic models
        │   ├── __init__.py
        │   ├── auth.py          # Auth request/response models
        │   ├── todo_list.py     # TodoList models
        │   └── todo.py          # Todo models
        │
        ├── services/            # Business logic layer
        │   ├── __init__.py
        │   ├── auth.py          # Mock authentication service
        │   ├── todo_list.py     # TodoList operations
        │   └── todo.py          # Todo operations
        │
        ├── routes/              # API routes/endpoints
        │   ├── __init__.py
        │   ├── auth.py          # Login, logout, register
        │   ├── pages.py         # Full page routes (/, /app, /login)
        │   ├── todo_lists.py    # TodoList CRUD endpoints
        │   └── todos.py         # Todo CRUD endpoints
        │
        ├── templates/           # Jinja2 HTML templates
        │   ├── base.html        # Base template with Shoelace imports
        │   ├── login.html       # Login/register page
        │   ├── app.html         # Main application page
        │   │
        │   └── partials/        # HTMX response partials
        │       ├── todo_list_item.html      # Single list in sidebar
        │       ├── todo_list_grid.html      # All lists (for reloading)
        │       ├── todo_item.html           # Single todo item
        │       ├── todo_items.html          # List of todos
        │       ├── todo_form.html           # Add/edit todo form
        │       ├── search_form.html         # Search input
        │       └── error.html               # Error message partial
        │
        └── static/              # Static files
            ├── css/
            │   └── styles.css   # Custom CSS (minimal, mainly for layout)
            └── js/
                └── app.js       # Vanilla JS utilities (minimal)

tests/                           # Test directory
├── __init__.py
├── conftest.py                  # Pytest fixtures
├── test_auth.py                 # Auth tests (no mocking needed!)
├── test_todo_lists.py           # TodoList tests
├── test_todos.py                # Todo tests
└── test_models.py               # Pydantic model validation tests
```

**Differences from Full Version**:
- **Removed**: `core/security.py` (no JWT/password hashing), `core/supabase.py` (no Supabase)
- **Removed**: `scripts/` folder (no database setup/seed scripts)
- **Added**: `core/storage.py` (helpers for in-memory storage)
- **Simpler**: No `.env` file needed (can be fully optional)

## Features & Requirements

### Phase 1: Authentication & Basic Structure

#### 1.1 Authentication System (Mock)
- [ ] Login page with email/password form
- [ ] Registration (sign up) functionality
- [ ] Logout functionality
- [ ] Session cookie management (simple UUID sessions)
- [ ] Protected routes (require authentication)
- [ ] Mock auth service (plain text password check)
- [ ] Session persistence in memory (lost on restart)
- [ ] Error handling for auth failures

**Acceptance Criteria**:
- Login form validates email format, password min 6 chars
- On login success: create session, set cookie, redirect to /app
- On login failure: show error message in form (wrong credentials)
- Register validates email format, password min 6 chars, passwords match
- On register success: auto-login and redirect to /app
- Logout clears session from memory and cookie, redirects to /login
- Protected routes (/app, /api/*) redirect to /login if not authenticated
- User email shown in header when logged in

**Implementation Notes**:
- No JWT validation - just dict lookup: `SESSIONS.get(session_id)`
- No password hashing - direct comparison: `user["password"] == password`
- Session ID is random UUID: `str(uuid.uuid4())`

#### 1.2 Basic UI Layout
- [ ] Base HTML template with Shoelace imports (CDN)
- [ ] Responsive layout (mobile-first, works on 320px+)
- [ ] Navigation/header with user email and logout button
- [ ] Sidebar for todo lists (collapsible on mobile)
- [ ] Main content area for todos
- [ ] Basic styling and color scheme
- [ ] Loading states (Shoelace spinner)

### Phase 2: Todo Lists Management

#### 2.1 Todo List CRUD
- [ ] View all todo lists (sidebar)
- [ ] Create new todo list
- [ ] Edit todo list (name, description, color)
- [ ] Delete todo list (with confirmation)
- [ ] Reorder todo lists (up/down buttons only - simple)
- [ ] Select active list (highlight in sidebar)
- [ ] Display todo count per list

**Acceptance Criteria**:
- User can create list with name (required), description (optional), color (defaults to blue)
- Clicking a list in sidebar loads its todos in main area
- Delete requires confirmation, cascades to all todos in list (remove from TODOS dict)
- Up/down buttons move list position by 1, updating position field

**Implementation Notes**:
- Store in `TODO_LISTS` dict: `TODO_LISTS[list_id] = {...}`
- Filter by user: `[lst for lst in TODO_LISTS.values() if lst["user_id"] == current_user_id]`
- Sort by position: `.sort(key=lambda x: x["position"])`
- Delete cascade: `[tid for tid, t in TODOS.items() if t["list_id"] == list_id]`

#### 2.2 List UI Components
- [ ] List item component with color indicator
- [ ] Add list button/form
- [ ] Edit list modal/form (Shoelace dialog)
- [ ] Delete confirmation dialog (Shoelace dialog)
- [ ] Empty state when no lists exist

### Phase 3: Todo Items Management

#### 3.1 Todo CRUD
- [ ] View todos in selected list
- [ ] Create new todo with title
- [ ] Edit todo (modal form)
- [ ] Delete todo (with confirmation)
- [ ] Mark todo as complete/incomplete (checkbox)
- [ ] Reorder todos within list (up/down buttons)
- [ ] Add notes to todo (expandable section)
- [ ] Set due date (date picker)
- [ ] Set priority level (dropdown: low/medium/high)

**Acceptance Criteria**:
- User can quick-add todo with just title from top of list
- Checkbox toggles completion, updates completed_at timestamp
- Overdue = due_date < today AND not completed (server-side logic)
- Edit form shows all fields, validates title required, max 200 chars
- Delete requires confirmation
- Up/down buttons move todo position by 1 within same list

**Implementation Notes**:
- Store in `TODOS` dict: `TODOS[todo_id] = {...}`
- Filter by list: `[t for t in TODOS.values() if t["list_id"] == list_id]`
- Sort by position: `.sort(key=lambda x: x["position"])`
- Overdue check: `from datetime import date; todo["due_date"] and date.fromisoformat(todo["due_date"]) < date.today() and not todo["is_completed"]`

#### 3.2 Todo UI Components
- [ ] Todo item component (compact view)
- [ ] Checkbox for completion
- [ ] Priority indicator (colored icon: 🔴 high, 🟡 medium, 🟢 low)
- [ ] Due date display (with overdue warning in red)
- [ ] Expandable notes section (click to expand)
- [ ] Quick add form (at top of list)
- [ ] Detailed edit form (Shoelace dialog)
- [ ] Empty state when no todos exist

#### 3.3 Visual Indicators
- [ ] Overdue todos highlighted in red
- [ ] Priority colors (high=red, medium=yellow, low=green)
- [ ] Completed todos with strikethrough
- [ ] Due today indicator (blue highlight)

### Phase 4: Search (MVP Minimal)

#### 4.1 Basic Search
- [ ] Search todos by title text match (case-insensitive)
- [ ] Search input with HTMX live search (300ms debounce)
- [ ] Clear search button
- [ ] Show "X results" or "No results" message

**Acceptance Criteria**:
- Search filters todos in currently selected list only
- Partial text match on title field
- Empty search shows all todos

**Implementation Notes**:
- Filter: `[t for t in list_todos if query.lower() in t["title"].lower()]`

### Phase 5: Polish & Testing

#### 5.1 User Experience
- [ ] Smooth HTMX transitions
- [ ] Loading indicators
- [ ] Success/error notifications (Shoelace alerts)
- [ ] Keyboard shortcuts (optional)
- [ ] Form validation with helpful messages
- [ ] Confirmation dialogs for destructive actions
- [ ] Mobile-responsive design

#### 5.2 Testing
- [ ] Model validation tests
- [ ] Service layer unit tests (no mocking needed - just test dict operations!)
- [ ] Route tests (test with in-memory storage)
- [ ] End-to-end test examples
- [ ] Test documentation

## Implementation Strategy

### Development Phases (MVP - Simplified)

**Total Estimated Time: 3-4 days** (faster than full version due to no external dependencies!)

#### Phase 1: Foundation & Auth (Day 1)
1. Project setup with uv and dependencies
2. FastAPI app structure (main.py, config, core modules)
3. In-memory storage setup (global dicts in main.py)
4. Mock authentication service (plain text passwords)
5. Auth routes with HTMX
6. Base HTML template with Shoelace
7. Login/register page
8. Seed demo data on startup

**Deliverable**: Users can register, login, logout (mock auth)

#### Phase 2: Todo Lists (Day 2)
1. TodoList service layer (dict operations)
2. TodoList CRUD routes
3. App layout template (header, sidebar, main)
4. List display and selection in sidebar
5. Create/edit/delete list with forms
6. Up/down reorder buttons

**Deliverable**: Users can manage multiple todo lists

#### Phase 3: Todo Items (Day 3)
1. Todo service layer (dict operations)
2. Todo CRUD routes
3. Todo item display template
4. Quick-add form
5. Edit form with all fields (title, note, due_date, priority)
6. Complete/uncomplete toggle
7. Delete with confirmation
8. Up/down reorder within list

**Deliverable**: Users can manage todos with all MVP features

#### Phase 4: Search & Polish (Day 4)
1. Basic search functionality (title match)
2. Loading indicators and error messages
3. Empty states
4. Visual indicators (overdue, priorities, completion)
5. Mobile responsiveness check
6. Write basic tests
7. README with quick start

**Deliverable**: Fully functional MVP, tested and documented

### Technical Implementation Details

#### HTMX Patterns to Use

**Same patterns as full version!** HTMX code doesn't change.

1. **List Management**:
```html
<!-- Add new list -->
<form hx-post="/api/lists" hx-target="#lists-container" hx-swap="afterbegin">
  <input name="name" type="text" required>
  <button type="submit">Add List</button>
</form>

<!-- Delete list -->
<button hx-delete="/api/lists/{id}"
        hx-confirm="Delete this list and all its todos?"
        hx-target="closest .list-item"
        hx-swap="outerHTML swap:1s">
  Delete
</button>
```

2. **Todo Items**:
```html
<!-- Toggle completion -->
<input type="checkbox"
       hx-patch="/api/todos/{id}/toggle"
       hx-target="closest .todo-item"
       hx-swap="outerHTML">

<!-- Inline edit -->
<div hx-get="/api/todos/{id}/edit"
     hx-trigger="click"
     hx-target="this"
     hx-swap="outerHTML">
  {todo.title}
</div>
```

3. **Search/Filter**:
```html
<!-- Live search -->
<input type="search"
       name="q"
       hx-get="/api/todos/search"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#todos-list"
       placeholder="Search todos...">
```

#### In-Memory Storage Setup

1. **Global Storage** (main.py):
```python
from typing import Dict
from uuid import uuid4
from datetime import datetime

# Global storage - WARNING: Lost on server restart!
USERS: Dict[str, dict] = {}
TODO_LISTS: Dict[str, dict] = {}
TODOS: Dict[str, dict] = {}
SESSIONS: Dict[str, str] = {}

# Helper to generate IDs
def new_id() -> str:
    return str(uuid4())

# Helper to get current timestamp
def now_iso() -> str:
    return datetime.now().isoformat()
```

2. **Seed Demo Data** (main.py startup):
```python
@app.on_event("startup")
async def seed_demo_data():
    """Create demo user and sample data."""

    # Create demo user
    demo_user_id = new_id()
    USERS[demo_user_id] = {
        "id": demo_user_id,
        "email": "demo@example.com",
        "password": "demo123",  # Plain text!
        "created_at": now_iso()
    }

    # Create sample list
    list_id = new_id()
    TODO_LISTS[list_id] = {
        "id": list_id,
        "user_id": demo_user_id,
        "name": "Getting Started",
        "description": "Sample todos to get you started",
        "color": "#3b82f6",
        "position": 0,
        "created_at": now_iso(),
        "updated_at": now_iso()
    }

    # Create sample todos
    sample_todos = [
        {"title": "Click to complete me!", "priority": "high"},
        {"title": "Edit me by clicking the edit icon", "priority": "medium"},
        {"title": "Create your own lists and todos", "priority": "low"},
    ]

    for idx, todo_data in enumerate(sample_todos):
        todo_id = new_id()
        TODOS[todo_id] = {
            "id": todo_id,
            "list_id": list_id,
            "title": todo_data["title"],
            "note": "",
            "is_completed": False,
            "completed_at": None,
            "due_date": None,
            "priority": todo_data["priority"],
            "position": idx,
            "created_at": now_iso(),
            "updated_at": now_iso()
        }

    print("✅ Seeded demo user: demo@example.com / demo123")
```

3. **Storage Helpers** (core/storage.py):
```python
from typing import Dict, List, Optional
from app.main import USERS, TODO_LISTS, TODOS, SESSIONS

def get_user_lists(user_id: str) -> List[dict]:
    """Get all lists for a user, sorted by position."""
    user_lists = [
        lst for lst in TODO_LISTS.values()
        if lst["user_id"] == user_id
    ]
    user_lists.sort(key=lambda x: x["position"])
    return user_lists

def get_list_todos(list_id: str) -> List[dict]:
    """Get all todos in a list, sorted by position."""
    list_todos = [
        todo for todo in TODOS.values()
        if todo["list_id"] == list_id
    ]
    list_todos.sort(key=lambda x: x["position"])
    return list_todos

def delete_list_cascade(list_id: str):
    """Delete a list and all its todos."""
    # Delete all todos in this list
    todos_to_delete = [
        tid for tid, todo in TODOS.items()
        if todo["list_id"] == list_id
    ]
    for tid in todos_to_delete:
        del TODOS[tid]

    # Delete list
    del TODO_LISTS[list_id]

def get_user_by_email(email: str) -> Optional[dict]:
    """Find user by email."""
    return next((u for u in USERS.values() if u["email"] == email), None)
```

#### Authentication Implementation (Mock)

1. **Session Management** (core/deps.py):
```python
from typing import Optional
from uuid import uuid4
from fastapi import Cookie, HTTPException, status
from app.main import SESSIONS, USERS

def create_session(user_id: str) -> str:
    """Create a new session and return session ID."""
    session_id = str(uuid4())
    SESSIONS[session_id] = user_id
    return session_id

def get_session_user_id(session_id: Optional[str]) -> Optional[str]:
    """Get user ID from session ID."""
    if not session_id:
        return None
    return SESSIONS.get(session_id)

def delete_session(session_id: str):
    """Delete a session."""
    if session_id in SESSIONS:
        del SESSIONS[session_id]

# Dependency for protected routes
async def get_current_user_id(session_id: Optional[str] = Cookie(None)) -> str:
    """Dependency to get current user from session cookie."""
    user_id = get_session_user_id(session_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user_id

def get_user(user_id: str) -> Optional[dict]:
    """Get user by ID from in-memory storage."""
    return USERS.get(user_id)
```

2. **Auth Routes** (routes/auth.py):
```python
from fastapi import APIRouter, Form, Response, Request, Cookie
from fastapi.responses import HTMLResponse
from app.main import USERS, templates
from app.core.deps import create_session, delete_session
from app.core.storage import get_user_by_email, new_id, now_iso

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Register a new user (mock - no validation)."""
    if password != confirm_password:
        # Return error partial for HTMX
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Passwords don't match"}
        )

    # Check if email exists
    if get_user_by_email(email):
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Email already registered"}
        )

    # Create user (plain text password!)
    user_id = new_id()
    USERS[user_id] = {
        "id": user_id,
        "email": email,
        "password": password,  # NO HASHING!
        "created_at": now_iso()
    }

    # Auto-login
    session_id = create_session(user_id)
    response = Response()
    response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
    response.headers["HX-Redirect"] = "/app"
    return response

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Login (mock - plain text password check)."""
    user = get_user_by_email(email)

    # Check password (plain text comparison!)
    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Invalid email or password"}
        )

    # Create session
    session_id = create_session(user["id"])
    response = Response()
    response.set_cookie("session_id", session_id, httponly=True, max_age=3600)
    response.headers["HX-Redirect"] = "/app"
    return response

@router.post("/logout")
async def logout(session_id: Optional[str] = Cookie(None)):
    """Logout and clear session."""
    if session_id:
        delete_session(session_id)

    response = Response()
    response.delete_cookie("session_id")
    response.headers["HX-Redirect"] = "/login"
    return response
```

3. **Service Layer Example** (services/todo_list.py):
```python
from typing import List, Optional
from app.main import TODO_LISTS, TODOS
from app.core.storage import new_id, now_iso, get_user_lists, delete_list_cascade

class TodoListService:
    """Service for todo list operations."""

    def get_user_lists(self, user_id: str) -> List[dict]:
        """Get all lists for a user with todo counts."""
        lists = get_user_lists(user_id)

        # Add todo counts
        for lst in lists:
            list_todos = [t for t in TODOS.values() if t["list_id"] == lst["id"]]
            lst["todo_count"] = len(list_todos)
            lst["completed_count"] = sum(1 for t in list_todos if t["is_completed"])

        return lists

    def create_list(self, user_id: str, name: str, description: Optional[str] = None, color: str = "#3b82f6") -> dict:
        """Create a new todo list."""
        list_id = new_id()

        # Calculate next position
        user_lists = get_user_lists(user_id)
        next_position = max([l["position"] for l in user_lists], default=-1) + 1

        new_list = {
            "id": list_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "color": color,
            "position": next_position,
            "created_at": now_iso(),
            "updated_at": now_iso()
        }

        TODO_LISTS[list_id] = new_list
        return new_list

    def update_list(self, list_id: str, user_id: str, **updates) -> Optional[dict]:
        """Update a todo list."""
        if list_id not in TODO_LISTS:
            return None

        lst = TODO_LISTS[list_id]

        # Check ownership
        if lst["user_id"] != user_id:
            return None

        # Update fields
        for key, value in updates.items():
            if value is not None and key in ["name", "description", "color", "position"]:
                lst[key] = value

        lst["updated_at"] = now_iso()
        return lst

    def delete_list(self, list_id: str, user_id: str) -> bool:
        """Delete a todo list and all its todos."""
        if list_id not in TODO_LISTS:
            return False

        lst = TODO_LISTS[list_id]

        # Check ownership
        if lst["user_id"] != user_id:
            return False

        delete_list_cascade(list_id)
        return True
```

## Testing Strategy

### Unit Tests (tests/test_models.py)

**Same as full version!** Pydantic validation tests don't change.

```python
import pytest
from app.models.todo import TodoCreate, TodoUpdate

def test_todo_create_validation():
    """Test TodoCreate model validation."""
    # Valid todo
    todo = TodoCreate(
        title="Buy groceries",
        priority="high"
    )
    assert todo.title == "Buy groceries"
    assert todo.priority == "high"

    # Invalid priority
    with pytest.raises(ValueError):
        TodoCreate(title="Test", priority="urgent")

    # Title too long
    with pytest.raises(ValueError):
        TodoCreate(title="x" * 201)
```

### Service Tests (tests/test_todo_lists.py)

**Much simpler!** No mocking needed - just test dict operations.

```python
import pytest
from app.main import TODO_LISTS, TODOS, USERS
from app.services.todo_list import TodoListService
from app.core.storage import new_id

@pytest.fixture(autouse=True)
def clear_storage():
    """Clear in-memory storage before each test."""
    USERS.clear()
    TODO_LISTS.clear()
    TODOS.clear()
    yield
    # Cleanup after test
    USERS.clear()
    TODO_LISTS.clear()
    TODOS.clear()

def test_create_todo_list():
    """Test creating a todo list."""
    service = TodoListService()
    user_id = new_id()

    result = service.create_list(
        user_id=user_id,
        name="Work",
        description="Work tasks"
    )

    assert result["name"] == "Work"
    assert result["user_id"] == user_id
    assert result["position"] == 0
    assert len(TODO_LISTS) == 1

def test_get_user_lists():
    """Test getting user's lists."""
    service = TodoListService()
    user_id = new_id()

    # Create multiple lists
    list1 = service.create_list(user_id, "Work")
    list2 = service.create_list(user_id, "Personal")

    lists = service.get_user_lists(user_id)

    assert len(lists) == 2
    assert lists[0]["name"] == "Work"
    assert lists[1]["name"] == "Personal"

def test_delete_list_cascade():
    """Test deleting list deletes all todos."""
    service = TodoListService()
    user_id = new_id()

    # Create list
    lst = service.create_list(user_id, "Work")

    # Add todos to list
    TODOS[new_id()] = {"list_id": lst["id"], "title": "Todo 1"}
    TODOS[new_id()] = {"list_id": lst["id"], "title": "Todo 2"}

    assert len(TODOS) == 2

    # Delete list
    service.delete_list(lst["id"], user_id)

    assert len(TODO_LISTS) == 0
    assert len(TODOS) == 0
```

### Route Tests (tests/test_auth.py)

**Easier!** Test with actual in-memory storage.

```python
from fastapi.testclient import TestClient
from app.main import app, USERS, SESSIONS

client = TestClient(app)

def test_login_page_loads():
    """Test that login page loads."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

def test_register_and_login():
    """Test user registration and login flow."""
    # Clear storage
    USERS.clear()
    SESSIONS.clear()

    # Register
    response = client.post("/auth/register", data={
        "email": "test@example.com",
        "password": "test123",
        "confirm_password": "test123"
    })

    assert response.status_code == 200
    assert len(USERS) == 1
    user = list(USERS.values())[0]
    assert user["email"] == "test@example.com"
    assert user["password"] == "test123"  # Plain text!

    # Login
    response = client.post("/auth/login", data={
        "email": "test@example.com",
        "password": "test123"
    })

    assert response.status_code == 200
    assert "session_id" in response.cookies

def test_unauthorized_access_redirects():
    """Test that accessing protected routes redirects to login."""
    response = client.get("/app", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert "/login" in response.headers["location"]
```

## Development Setup

### Initial Setup Steps

1. **Clone and navigate to project**:
```bash
cd todo-lab-python/todo-cc
```

2. **Install uv** (if not installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Initialize Python project**:
```bash
uv init
uv add fastapi uvicorn[standard] jinja2 python-multipart
uv add --dev pytest httpx
```

4. **Run development server** (that's it!):
```bash
uv run uvicorn app.main:app --reload
```

5. **Access the app**:
- Open browser to `http://localhost:8000`
- Login with demo user: `demo@example.com` / `demo123`

**No configuration needed!** No .env file, no database setup, no API keys. Just run it.

### Development Workflow

1. Start development server: `uv run uvicorn app.main:app --reload --port 8000`
2. Access app at `http://localhost:8000`
3. API docs at `http://localhost:8000/docs`
4. Run tests: `uv run pytest`
5. Run tests with coverage: `uv run pytest --cov=app`

### Optional: JSON File Persistence

Add persistence as a workshop exercise:

```python
# Add to main.py
import json
from pathlib import Path

DATA_FILE = Path("data/db.json")

def load_data():
    """Load data from JSON file."""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            USERS.update(data.get("users", {}))
            TODO_LISTS.update(data.get("todo_lists", {}))
            TODOS.update(data.get("todos", {}))
            SESSIONS.update(data.get("sessions", {}))

def save_data():
    """Save data to JSON file."""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({
            "users": USERS,
            "todo_lists": TODO_LISTS,
            "todos": TODOS,
            "sessions": SESSIONS
        }, f, indent=2)

# Load on startup
@app.on_event("startup")
async def startup():
    load_data()
    seed_demo_data()  # Only if empty

# Save periodically or on changes
# (Can be added as exercise)
```

## Deployment Considerations

### Environment Setup
- No environment variables required!
- Optional: Add `SECRET_KEY` if you want to add session encryption later

### Production Settings (if deploying this simple version)
- Set `secure=True` for cookies (HTTPS)
- Consider adding password hashing (workshop exercise)
- Add JSON file persistence or upgrade to SQLite
- Still not truly production-ready - but better than pure in-memory

### Hosting Options (Examples)
- **Render.com**: Easy Python app deployment
- **Railway.app**: Simple deployment with free tier
- **Fly.io**: Global deployment with free tier
- **Google Cloud Run**: Serverless container deployment

**Note**: This simple version is mainly for learning/workshops. For production, use the full version with Supabase.


## Next Steps

After planning approval:

1. Review and adjust plan based on feedback
2. Set up project structure with uv (5 minutes!)
3. Begin Phase 1 implementation (no external setup needed)
4. Iterate through phases with regular check-ins
5. Consider upgrades: JSON persistence → SQLite → Supabase


## Notes

- **Priority**: Focus on educational value and clarity over complex features
- **Keep It Simple**: Better to have a polished basic app than incomplete advanced features
- **Document As You Go**: Add comments and docstrings for workshop participants
- **Test What Matters**: Focus tests on business logic (dict operations are easy to test!)
- **HTMX First**: Always consider if HTMX can handle it before adding JavaScript
- **No Security Theater**: This is intentionally insecure for learning - be explicit about it!
- **Upgrade Path**: Clear path from simple → SQLite → Supabase for progressive learning

---

## Revision History

### Version 3.0 (2025-11-20) - Simplified Standalone
**Status**: Ready for Implementation

**Major Simplifications**:
- ✅ Removed Supabase (no external services)
- ✅ Removed database (in-memory dicts only)
- ✅ Mock authentication (no JWT, no password hashing)
- ✅ Simple session cookies (UUID-based)
- ✅ Seed demo data on startup
- ✅ No configuration required
- ✅ Single command to run
- ✅ 3-4 day implementation (vs 5-7 for full)

**What Stayed the Same**:
- Same MVP features (lists, todos, search)
- Same UI/UX (Shoelace + HTMX)
- Same architecture (layered, services)
- Same HTMX patterns
- Same Pydantic models
- Same testing approach (but simpler!)
- Same project structure (mostly)
- Same detailed planning

**Perfect For**:
- Learning FastAPI and HTMX
- Workshops without internet
- Rapid prototyping
- Understanding architecture before adding complexity
- Porting exercises (easier to port something simple first)

**Not For**:
- Production applications
- Multi-user scenarios requiring security
- Applications requiring data persistence
- Anything that needs real authentication

**Migration Path**: JSON file → SQLite → Supabase (PROJECT_PLAN.md)

---

**Document Version**: 3.0 - Simplified Standalone
**Based On**: PROJECT_PLAN_SUPABASE.md v2.0
**Last Updated**: 2025-11-20
**Status**: Ready for Implementation
