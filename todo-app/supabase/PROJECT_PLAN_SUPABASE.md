# Supabase ToDo Application Project Plan

## Project Overview

A modern, educational web application for managing todos with a stunning UI. Built with Python, FastAPI, and HTMX, this project demonstrates server-side rendering with SPA-like user experience, suitable for workshops on AI coding agents and as a reference for porting to other languages/frameworks.

## MVP Scope & Philosophy

**This is an MVP/Lab project** - the goal is educational clarity, not production completeness. We prioritize:
- **Simple over complex**: Clear patterns over extensive features
- **Working over perfect**: Functional examples over comprehensive edge case handling
- **Teachable over scalable**: Code that's easy to understand and modify

**MVP Feature Set**:
- Email/password authentication (login, register, logout)
- Multiple todo lists per user
- Todo items with: title, notes, completion status, due dates, priority levels
- Basic search (text match on titles)
- Simple list reordering (up/down buttons, not drag-drop)

**Explicitly OUT of MVP Scope**:
- Tags/categories (can be added as workshop exercise)
- Advanced filtering/sorting
- Statistics dashboard
- Password reset/change
- Email verification
- Rate limiting
- Drag-and-drop reordering
- Extensive monitoring/observability
- CI/CD pipeline

## Technology Stack

### Core Technologies
- **Backend Framework**: FastAPI 0.115+
- **Frontend Approach**: HTMX 2.0+ (via CDN)
- **Templating**: Jinja2
- **UI Components**: Shoelace 2.20+ (via CDN)
- **Database & Auth**: Supabase (PostgreSQL + Auth)
- **Package Management**: uv 0.5+
- **Python Version**: 3.11 or 3.12

### Key Libraries (pinned in pyproject.toml)
- `fastapi>=0.115.0` - Web framework
- `uvicorn[standard]>=0.32.0` - ASGI server
- `jinja2>=3.1.0` - Templating engine
- `supabase>=2.9.0` - Supabase client for database and auth
- `pydantic>=2.0.0` - Data validation
- `python-multipart>=0.0.9` - Form data parsing
- `pytest>=8.0.0` - Testing framework (dev)
- `httpx>=0.27.0` - Async HTTP client for tests (dev)

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
└─────────────────┬───────────────────────────┘
                  │
                  │ Supabase Client
┌─────────────────▼───────────────────────────┐
│           Supabase Platform                 │
│  ┌──────────────────┐  ┌─────────────────┐ │
│  │  PostgreSQL DB   │  │  Auth Service   │ │
│  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────┘
```

### Authentication & Session Management

**Token Strategy** (using Supabase Auth tokens directly):
- Supabase Auth provides `access_token` (JWT, 1 hour expiry) and `refresh_token`
- Store `access_token` in HTTP-only, secure, SameSite=Lax cookie
- Store `refresh_token` in separate HTTP-only cookie (for MVP simplicity)
- Backend validates access token on each request using Supabase JWT secret
- On token expiry, use refresh token to get new access token (client-side JS handles this)

**Cookie Configuration**:
- Development: `secure=False` (HTTP allowed), `samesite="lax"`
- Production: `secure=True` (HTTPS only), `samesite="lax"`
- Both: `httponly=True`, `max_age=3600` (access token)
- **IMPORTANT**: Never expose `SUPABASE_SERVICE_KEY` to client; backend only

**Authentication Flow**:
1. User visits `/` → middleware checks cookie → redirects to `/login` if missing/invalid
2. Login form (HTMX) → POST `/auth/login` → Supabase Auth validates
3. On success: set cookies → return HX-Redirect header to `/app`
4. On error: return error partial to display in form
5. Logout: DELETE `/auth/logout` → clear cookies → redirect to `/login`

**Session Validation**:
- Every protected route uses `get_current_user` dependency
- Dependency extracts access_token cookie → validates JWT with Supabase
- Returns user info (id, email) or raises 401
- For MVP: no CSRF tokens (rely on SameSite cookies + HTTPS)

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
   - Services interact with Supabase client (uses RLS policies)
   - Return data to routes
   - Routes render Jinja2 templates/partials
   - Return HTML to browser

## Domain Model

### Database Schema

```python
# Core Entities

User (Supabase Auth - managed by Supabase)
├── id: UUID (primary key)
├── email: string
├── created_at: timestamp
└── metadata: jsonb (optional extra user data)

TodoList
├── id: UUID (primary key)
├── user_id: UUID (foreign key to User)
├── name: string (e.g., "Work", "Personal", "Shopping")
├── description: string (optional)
├── color: string (hex color for visual distinction)
├── position: integer (for custom ordering)
├── created_at: timestamp
└── updated_at: timestamp

Todo
├── id: UUID (primary key)
├── list_id: UUID (foreign key to TodoList)
├── title: string (max 200 chars)
├── note: text (optional, longer description)
├── is_completed: boolean (default false)
├── completed_at: timestamp (nullable)
├── due_date: date (nullable)
├── priority: enum ('low', 'medium', 'high')
├── position: integer (for custom ordering within list)
├── created_at: timestamp
└── updated_at: timestamp
```

### Pydantic Models

```python
# Request/Response Models

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
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Template for environment variables
├── .gitignore
├── pyproject.toml                # uv project configuration
├── README.md                     # Project documentation
├── PROJECT_PLAN.md              # This file
└── src/
    └── app/
        ├── __init__.py
        ├── main.py              # FastAPI application entry point
        ├── config.py            # Configuration management
        │
        ├── core/                # Core functionality
        │   ├── __init__.py
        │   ├── deps.py          # Dependencies (auth, db connections)
        │   ├── security.py      # Security utilities (JWT, password hashing)
        │   └── supabase.py      # Supabase client setup
        │
        ├── models/              # Pydantic models
        │   ├── __init__.py
        │   ├── auth.py          # Auth request/response models
        │   ├── todo_list.py     # TodoList models
        │   └── todo.py          # Todo models
        │
        ├── services/            # Business logic layer
        │   ├── __init__.py
        │   ├── auth.py          # Authentication service
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
├── test_auth.py                 # Auth tests (mocked)
├── test_todo_lists.py           # TodoList tests
├── test_todos.py                # Todo tests
└── test_models.py               # Pydantic model validation tests

scripts/                         # Utility scripts
├── setup_db.py                  # Database initialization script
└── seed_data.py                 # Optional: seed with sample data
```

## Features & Requirements

### Phase 1: Authentication & Basic Structure

#### 1.1 Authentication System
- [ ] Login page with email/password form
- [ ] Registration (sign up) functionality
- [ ] Logout functionality
- [ ] JWT token management (HTTP-only cookies)
- [ ] Protected routes (require authentication)
- [ ] Supabase Auth integration
- [ ] Session persistence
- [ ] Error handling for auth failures

**Acceptance Criteria**:
- Login form validates email format, password min 6 chars
- On login success: set cookies, redirect to /app
- On login failure: show error message in form (wrong credentials, network error)
- Register validates email format, password min 6 chars, passwords match
- On register success: auto-login and redirect to /app
- Logout clears cookies and redirects to /login
- Protected routes (/app, /api/*) redirect to /login if not authenticated
- User email shown in header when logged in

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
- Delete requires confirmation, cascades to all todos in list
- Up/down buttons move list position by 1, updating position field

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
- [ ] Service layer unit tests (mocked Supabase)
- [ ] Route tests (mocked auth)
- [ ] End-to-end test examples
- [ ] Test documentation

## Implementation Strategy

### Development Phases (MVP - Simplified)

**Total Estimated Time: 5-7 days** (flexible for workshop/learning pace)

#### Phase 1: Foundation & Auth (Days 1-2)
1. Project setup with uv and dependencies
2. FastAPI app structure (main.py, config, core modules)
3. Supabase connection setup
4. Database schema + RLS policies (run SQL migrations)
5. Authentication service (login, register, logout)
6. Auth routes with HTMX
7. Base HTML template with Shoelace
8. Login/register page

**Deliverable**: Users can register, login, logout

#### Phase 2: Todo Lists (Day 3)
1. TodoList service layer
2. TodoList CRUD routes
3. App layout template (header, sidebar, main)
4. List display and selection in sidebar
5. Create/edit/delete list with forms
6. Up/down reorder buttons

**Deliverable**: Users can manage multiple todo lists

#### Phase 3: Todo Items (Days 4-5)
1. Todo service layer
2. Todo CRUD routes
3. Todo item display template
4. Quick-add form
5. Edit form with all fields (title, note, due_date, priority)
6. Complete/uncomplete toggle
7. Delete with confirmation
8. Up/down reorder within list

**Deliverable**: Users can manage todos with all MVP features

#### Phase 4: Search & Polish (Day 6)
1. Basic search functionality (title match)
2. Loading indicators and error messages
3. Empty states
4. Visual indicators (overdue, priorities, completion)
5. Mobile responsiveness check

**Deliverable**: Fully functional MVP

#### Phase 5: Testing & Documentation (Day 7)
1. Write basic model validation tests
2. Write service layer tests (3-5 examples)
3. Write route tests (auth + CRUD examples)
4. README with setup instructions
5. Final bug fixes
6. Code cleanup and comments

**Deliverable**: Tested, documented MVP ready for workshop use

### Technical Implementation Details

#### HTMX Patterns to Use

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

#### Supabase Setup

1. **Environment Variables** (.env):
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
JWT_SECRET=your-jwt-secret
SECRET_KEY=your-app-secret-key
```

2. **Database Tables** (SQL migrations):
```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TodoLists table
CREATE TABLE todo_lists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#3b82f6',
    position INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    list_id UUID NOT NULL REFERENCES todo_lists(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    note TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    due_date DATE,
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    position INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_todo_lists_user_id ON todo_lists(user_id);
CREATE INDEX idx_todos_list_id ON todos(list_id);
CREATE INDEX idx_todos_due_date ON todos(due_date);
CREATE INDEX idx_todos_is_completed ON todos(is_completed);

-- Row Level Security (RLS) policies
ALTER TABLE todo_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

-- Todo Lists: Users can only access their own lists
CREATE POLICY "Users can view own todo lists" ON todo_lists
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own todo lists" ON todo_lists
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own todo lists" ON todo_lists
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own todo lists" ON todo_lists
    FOR DELETE USING (auth.uid() = user_id);

-- Todos: Users can only access todos in lists they own
CREATE POLICY "Users can view todos in their lists" ON todos
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM todo_lists
            WHERE todo_lists.id = todos.list_id
            AND todo_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert todos in their lists" ON todos
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM todo_lists
            WHERE todo_lists.id = todos.list_id
            AND todo_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update todos in their lists" ON todos
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM todo_lists
            WHERE todo_lists.id = todos.list_id
            AND todo_lists.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete todos in their lists" ON todos
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM todo_lists
            WHERE todo_lists.id = todos.list_id
            AND todo_lists.user_id = auth.uid()
        )
    );
```

3. **Supabase Client** (core/supabase.py):
```python
from supabase import create_client, Client
from app.config import settings

def get_supabase_client() -> Client:
    """Create and return Supabase client."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_ANON_KEY
    )

# Admin client for operations requiring elevated privileges
def get_supabase_admin_client() -> Client:
    """Create and return Supabase admin client."""
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )
```

#### Authentication Implementation

1. **JWT Dependency** (core/deps.py):
```python
from fastapi import Depends, HTTPException, status, Cookie
from jose import JWTError, jwt
from typing import Optional

async def get_current_user(
    access_token: Optional[str] = Cookie(None)
) -> dict:
    """Extract and validate user from JWT token in cookie."""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            access_token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

2. **Login Route** (routes/auth.py):
```python
from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    """Login with email and password."""
    try:
        # Authenticate with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # Set HTTP-only cookie with access token
        response = Response()
        response.set_cookie(
            key="access_token",
            value=auth_response.session.access_token,
            httponly=True,
            secure=True,  # HTTPS only in production
            samesite="lax",
            max_age=3600  # 1 hour
        )

        # Return redirect to app or success message
        if request.headers.get("HX-Request"):
            response.headers["HX-Redirect"] = "/app"
            return response
        else:
            return RedirectResponse(url="/app", status_code=303)

    except Exception as e:
        # Return error partial for HTMX or full page error
        if request.headers.get("HX-Request"):
            return templates.TemplateResponse(
                "partials/error.html",
                {"request": request, "error": str(e)}
            )
        # ... handle regular request error
```

## Testing Strategy

### Unit Tests (tests/test_models.py)
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
```python
import pytest
from unittest.mock import Mock, patch
from app.services.todo_list import TodoListService

@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    with patch('app.services.todo_list.get_supabase_client') as mock:
        yield mock.return_value

def test_create_todo_list(mock_supabase):
    """Test creating a todo list."""
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
        {"id": "123", "name": "Work", "user_id": "user1"}
    ]

    service = TodoListService()
    result = service.create_list(
        user_id="user1",
        name="Work",
        description="Work tasks"
    )

    assert result["name"] == "Work"
    mock_supabase.table.assert_called_with("todo_lists")
```

### Route Tests (tests/test_auth.py)
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_page_loads():
    """Test that login page loads."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "login" in response.text.lower()

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
uv add fastapi uvicorn jinja2 supabase python-jose[cryptography] python-multipart
uv add --dev pytest httpx pytest-asyncio
```

4. **Create environment file**:
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. **Set up Supabase**:
- Create project at supabase.com
- Copy URL and anon key to .env
- Run database migrations (SQL scripts)
- Configure auth settings

6. **Run development server**:
```bash
uv run uvicorn app.main:app --reload
```

### Development Workflow

1. Start development server: `uv run uvicorn app.main:app --reload --port 8000`
2. Access app at `http://localhost:8000`
3. API docs at `http://localhost:8000/docs`
4. Run tests: `uv run pytest`
5. Run tests with coverage: `uv run pytest --cov=app`

## Deployment Considerations

### Environment Setup
- Use environment variables for all secrets
- Never commit .env file
- Provide .env.example as template

### Production Settings
- Set `secure=True` for cookies (HTTPS)
- Configure CORS properly
- Use production Supabase instance
- Set appropriate JWT expiration
- Enable proper logging

### Hosting Options (Examples)
- **Render.com**: Easy Python app deployment
- **Railway.app**: Simple deployment with free tier
- **Fly.io**: Global deployment with free tier
- **Google Cloud Run**: Serverless container deployment

## Educational Lab Considerations

### Workshop-Friendly Aspects

1. **Clear Separation of Concerns**:
   - Routes → Services → Database
   - Easy to understand and modify
   - Each layer can be explained independently

2. **Modern Python Practices**:
   - Type hints throughout
   - Pydantic for validation
   - Async/await patterns
   - Modern tooling (uv)

3. **HTMX Learning**:
   - Clear examples of HTMX patterns
   - Progressive enhancement approach
   - Minimal JavaScript required

4. **Real-World Auth**:
   - Industry-standard JWT tokens
   - Proper security practices
   - Integration with popular service (Supabase)

5. **Testing Examples**:
   - Unit test examples
   - Mocking patterns
   - Test organization

### Lab Exercise Ideas

1. **Add a new feature**:
   - Add recurring todos
   - Add todo templates
   - Add collaboration (share lists)

2. **Modify UI**:
   - Change color scheme
   - Add animations
   - Implement dark mode

3. **Port to another tech stack**:
   - Flask + HTMX
   - Django + HTMX
   - Node.js + HTMX
   - Go + Templ

4. **Add integrations**:
   - Email notifications
   - Calendar sync
   - Export to CSV/PDF

## Future Portability Considerations

### Architecture Decisions for Easy Porting

1. **Layered Architecture**:
   - Clear separation makes it easy to port piece by piece
   - Service layer is framework-agnostic
   - Models can be easily translated

2. **Standard Patterns**:
   - REST-like API structure
   - CRUD operations
   - Common authentication patterns

3. **Minimal Framework-Specific Code**:
   - Business logic independent of FastAPI
   - Database operations abstracted
   - Template structure portable

4. **Documentation**:
   - This plan serves as specification
   - Clear requirements for ports
   - Architecture diagrams for reference

### Potential Port Targets

1. **Python Alternatives**:
   - Flask + HTMX
   - Django + HTMX
   - Litestar + HTMX

2. **Other Languages**:
   - Deno + HTMX
   - Node.js (Express) + HTMX
   - Go (Gin/Echo) + Templ
   - Ruby (Rails/Sinatra) + HTMX
   - C# (ASP.NET) + HTMX
   - Java (Spring Boot) + HTMX
   - PHP (Laravel) + HTMX

3. **Database Alternatives**:
   - PostgreSQL directly
   - SQLite for simplicity
   - MySQL/MariaDB
   - MongoDB (document model)

## Success Criteria (MVP)

The MVP is considered complete when:

- [ ] User can register, login, and logout
- [ ] User can create, edit, delete, and reorder multiple todo lists
- [ ] User can create, edit, delete, and complete todos
- [ ] Todos support due dates, priorities, and notes
- [ ] Basic search by title works
- [ ] UI is responsive and works on mobile devices
- [ ] All HTMX interactions work without full page reloads
- [ ] At least 10 basic tests are written and passing
- [ ] Code has inline comments and docstrings
- [ ] README has clear setup and run instructions
- [ ] Application runs without Docker
- [ ] Database has proper RLS policies enforced

## Next Steps

After planning approval:

1. Review and adjust plan based on feedback
2. Set up project structure with uv
3. Configure Supabase project and database
4. Begin Phase 1 implementation
5. Iterate through phases with regular check-ins

## Notes

- **Priority**: Focus on educational value and clarity over complex features
- **Keep It Simple**: Better to have a polished basic app than incomplete advanced features
- **Document As You Go**: Add comments and docstrings for workshop participants
- **Test What Matters**: Focus tests on business logic, not mocked integrations
- **HTMX First**: Always consider if HTMX can handle it before adding JavaScript

---

## Revision History

### Version 2.0 (2025-11-20) - MVP Refocus
**Status**: Ready for Implementation

**Major Changes Based on Review Feedback**:
- ✅ Added explicit MVP scope section limiting features
- ✅ Removed tags/categories from MVP (can be workshop exercise)
- ✅ Removed advanced filtering and statistics
- ✅ Removed drag-and-drop (simplified to up/down buttons)
- ✅ Pinned dependency versions (no more "latest stable")
- ✅ Completed ALL RLS policies (not just SELECT)
- ✅ Clarified authentication/session/cookie strategy
- ✅ Added acceptance criteria for each phase
- ✅ Simplified implementation timeline from 11 days to 5-7 days
- ✅ Removed over-engineering (CI/CD, extensive monitoring, etc.)
- ✅ Clarified service key handling (backend only, never client-side)

**Scope Reductions**:
- No tags (out of scope)
- No advanced filters (only basic search)
- No statistics dashboard
- No password reset/email verification
- No rate limiting
- Simple up/down reorder instead of drag-drop

**Security Improvements**:
- Complete RLS policies for all operations
- Clear JWT/cookie strategy documented
- Service key usage clarified

### Version 1.0 (2025-11-19) - Initial Plan
**Status**: Needed Significant Rework

Initial comprehensive plan with broad feature set
