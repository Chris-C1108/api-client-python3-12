# Project Structure

## Root Directory
```
gophish/                    # Main package directory
├── __init__.py            # Package entry point, exports Gophish class
├── client.py              # Core client classes (GophishClient, Gophish)
├── models.py              # Data models for all API resources
└── api/                   # API endpoint modules
    ├── __init__.py        # Exports APIEndpoint base class
    ├── api.py             # Base APIEndpoint class with CRUD operations
    ├── campaigns.py       # Campaign management endpoints
    ├── groups.py          # Target group management
    ├── templates.py       # Email template management
    ├── pages.py           # Landing page management
    ├── smtp.py            # SMTP configuration
    ├── webhooks.py        # Webhook management
    └── imap.py            # IMAP configuration
```

## Architecture Organization

### Core Components
- **client.py**: Contains the main `Gophish` class and `GophishClient` HTTP wrapper
- **models.py**: All data models (Campaign, Group, Template, etc.) with JSON parsing
- **api/**: Modular API endpoints, each inheriting from `APIEndpoint`

### Design Patterns
- **Single Entry Point**: `gophish/__init__.py` exports only the main `Gophish` class
- **Composition Over Inheritance**: Main client composes API endpoint instances
- **Consistent API Structure**: All endpoints follow the same CRUD pattern
- **Model-First**: Rich model classes with validation and serialization

### File Naming Conventions
- **Snake Case**: All Python files use snake_case naming
- **Descriptive Names**: File names match their primary class/functionality
- **API Modules**: Each API resource gets its own module in `api/` directory

### Import Structure
- **Absolute Imports**: Use full package paths for clarity
- **Selective Imports**: Import only needed classes/functions
- **Clean Namespace**: Main package exports minimal public interface

### Extension Points
- **New API Endpoints**: Add new modules to `api/` directory following existing pattern
- **New Models**: Add to `models.py` with proper parsing methods
- **Custom Clients**: Extend `GophishClient` for specialized HTTP handling