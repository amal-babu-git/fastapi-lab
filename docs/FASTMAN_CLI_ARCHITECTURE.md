# FastMan CLI - Architecture Diagram

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FastMan CLI System                           │
└─────────────────────────────────────────────────────────────────────┘

                              manage.py
                                  │
                                  ▼
                         ┌────────────────┐
                         │  FastMan CLI   │
                         │  (Typer App)   │
                         └────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ startapp │  │ listapps │  │  version │
              │ Command  │  │ Command  │  │ Command  │
              └──────────┘  └──────────┘  └──────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  String Utils    │
          │  - to_snake_case │
          │  - to_pascal_case│
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  Templates       │
          │  - Models        │
          │  - Schemas       │
          │  - CRUD          │
          │  - Services      │
          │  - Routes        │
          │  - Exceptions    │
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  File Generator  │
          │  - Create dirs   │
          │  - Write files   │
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │  Generated       │
          │  Module          │
          │  (app/order/)    │
          └──────────────────┘
```

## 📦 Package Structure

```
fastman_cli/
│
├── __init__.py                    # Package entry point
│   └── Exports: app, __version__
│
├── cli.py                         # Main Typer application
│   ├── app = Typer()
│   ├── @app.command("startapp")
│   ├── @app.command("listapps")
│   ├── @app.command("version")
│   └── @app.callback()
│
├── commands/                      # Command implementations
│   ├── __init__.py
│   ├── startapp.py               # Module generation logic
│   │   ├── startapp_command()
│   │   ├── validate_name()
│   │   ├── create_structure()
│   │   └── display_summary()
│   │
│   └── listapps.py               # List modules logic
│       ├── listapps_command()
│       ├── scan_directory()
│       └── display_table()
│
├── templates/                     # Code generation templates
│   ├── __init__.py
│   ├── model_template.py         # SQLAlchemy model
│   ├── schema_template.py        # Pydantic schemas
│   ├── crud_template.py          # CRUD operations
│   ├── service_template.py       # Business logic
│   ├── route_template.py         # FastAPI routes
│   ├── exception_template.py     # Custom exceptions
│   ├── init_template.py          # Module __init__
│   └── readme_template.py        # Documentation
│
└── utils/                         # Helper utilities
    ├── __init__.py
    └── helpers.py                # String & file utilities
        ├── to_snake_case()
        ├── to_pascal_case()
        ├── to_camel_case()
        ├── to_upper_case()
        ├── ensure_directory()
        └── write_file()
```

## 🔄 Data Flow

### startapp Command Flow

```
User Input: "python manage.py startapp Order"
    │
    ▼
┌─────────────────────────────────────────┐
│ 1. Parse Arguments                      │
│    - app_name: "Order"                  │
│    - directory: "app"                   │
│    - force: False                       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 2. Convert Names                        │
│    - module_name: "order" (snake_case)  │
│    - class_name: "Order" (PascalCase)   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 3. Check Existing Directory             │
│    - app/order/ exists?                 │
│    - If yes && !force: ERROR            │
│    - If no || force: CONTINUE           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 4. Create Directory Structure           │
│    - mkdir app/order/                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 5. Generate Code from Templates         │
│    ┌─────────────────────────────────┐  │
│    │ For each template:              │  │
│    │  - generate_model()             │  │
│    │  - generate_schemas()           │  │
│    │  - generate_crud()              │  │
│    │  - generate_service()           │  │
│    │  - generate_routes()            │  │
│    │  - generate_exceptions()        │  │
│    │  - generate_init()              │  │
│    │  - generate_readme()            │  │
│    └─────────────────────────────────┘  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 6. Write Files                          │
│    - models.py                          │
│    - schemas.py                         │
│    - crud.py                            │
│    - services.py                        │
│    - routes.py                          │
│    - exceptions.py                      │
│    - __init__.py                        │
│    - README.md                          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 7. Display Summary                      │
│    - Rich table with stats              │
│    - Next steps panel                   │
│    - Success message                    │
└─────────────────────────────────────────┘
    │
    ▼
Generated Module Ready! ✅
```

## 🎨 Template Processing

```
Template Function Call:
generate_model("order", "Order")
    │
    ▼
┌──────────────────────────────────────────┐
│ Template String with Placeholders        │
│                                          │
│ from sqlalchemy.orm import Mapped        │
│                                          │
│ class {class_name}(Base):                │
│     __tablename__ = "{module_name}s"     │
│     id: Mapped[int] = ...                │
│     name: Mapped[str] = ...              │
│     ...                                  │
└──────────────────────────────────────────┘
    │
    │ f-string formatting
    ▼
┌──────────────────────────────────────────┐
│ Generated Code                           │
│                                          │
│ from sqlalchemy.orm import Mapped        │
│                                          │
│ class Order(Base):                       │
│     __tablename__ = "orders"             │
│     id: Mapped[int] = ...                │
│     name: Mapped[str] = ...              │
│     ...                                  │
└──────────────────────────────────────────┘
    │
    ▼
Written to: app/order/models.py
```

## 🧩 Component Interactions

```
┌─────────────────────────────────────────────────────────────┐
│                     Generated Module                         │
│                                                              │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐        │
│  │ routes.py│──────▶│services.py│──────▶│ crud.py  │        │
│  │          │       │           │       │          │        │
│  │ FastAPI  │       │ Business  │       │ Database │        │
│  │ Endpoints│       │ Logic     │       │ Ops      │        │
│  └──────────┘       └──────────┘       └──────────┘        │
│       │                   │                   │             │
│       │                   │                   │             │
│       ▼                   ▼                   ▼             │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐        │
│  │schemas.py│       │exceptions│       │models.py │        │
│  │          │       │   .py    │       │          │        │
│  │ Pydantic │       │ Custom   │       │SQLAlchemy│        │
│  │ Models   │       │ Errors   │       │ Model    │        │
│  └──────────┘       └──────────┘       └──────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ Imports
                         ▼
            ┌────────────────────────┐
            │   app/core/            │
            │   - database.py (Base) │
            │   - crud.py (CRUDBase) │
            │   - logging.py         │
            │   - settings.py        │
            └────────────────────────┘
```

## 🔧 Request Flow in Generated Module

```
HTTP Request
    │
    ▼
┌─────────────────────────┐
│ FastAPI Route           │
│ routes.py               │
│ @router.post("/")       │
└─────────────────────────┘
    │
    │ Dependency Injection
    ▼
┌─────────────────────────┐
│ Pydantic Validation     │
│ schemas.py              │
│ OrderCreate             │
└─────────────────────────┘
    │
    │ Pass validated data
    ▼
┌─────────────────────────┐
│ Service Layer           │
│ services.py             │
│ OrderService.create()   │
└─────────────────────────┘
    │
    │ Business Logic
    │ - Validate duplicates
    │ - Log operations
    ▼
┌─────────────────────────┐
│ CRUD Layer              │
│ crud.py                 │
│ order_crud.create()     │
└─────────────────────────┘
    │
    │ Database operation
    ▼
┌─────────────────────────┐
│ SQLAlchemy Model        │
│ models.py               │
│ Order (Base)            │
└─────────────────────────┘
    │
    │ Insert/Update
    ▼
┌─────────────────────────┐
│ PostgreSQL Database     │
│ orders table            │
└─────────────────────────┘
    │
    │ Return data
    ▼
┌─────────────────────────┐
│ Pydantic Response       │
│ schemas.py              │
│ Order                   │
└─────────────────────────┘
    │
    ▼
HTTP Response (JSON)
```

## 📊 Layer Responsibilities

```
┌──────────────────────────────────────────────────────────┐
│ LAYER            │ RESPONSIBILITIES                      │
├──────────────────────────────────────────────────────────┤
│ Routes           │ • HTTP request/response               │
│ (routes.py)      │ • URL routing                         │
│                  │ • Dependency injection                │
│                  │ • Exception handling                  │
├──────────────────────────────────────────────────────────┤
│ Schemas          │ • Data validation                     │
│ (schemas.py)     │ • Serialization                       │
│                  │ • API contract definition             │
│                  │ • Type conversion                     │
├──────────────────────────────────────────────────────────┤
│ Services         │ • Business logic                      │
│ (services.py)    │ • Validation rules                    │
│                  │ • Transaction orchestration           │
│                  │ • Logging                             │
├──────────────────────────────────────────────────────────┤
│ CRUD             │ • Database queries                    │
│ (crud.py)        │ • Common operations (CRUD)            │
│                  │ • Custom queries                      │
│                  │ • Data filtering                      │
├──────────────────────────────────────────────────────────┤
│ Models           │ • Database schema                     │
│ (models.py)      │ • Table definition                    │
│                  │ • Relationships                       │
│                  │ • Constraints                         │
├──────────────────────────────────────────────────────────┤
│ Exceptions       │ • Custom error types                  │
│ (exceptions.py)  │ • Error messages                      │
│                  │ • Business rule violations            │
│                  │ • Domain-specific errors              │
└──────────────────────────────────────────────────────────┘
```

## 🎯 Extension Points

```
┌────────────────────────────────────────────────────────┐
│ HOW TO EXTEND                                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│ 1. Add New Command                                     │
│    ┌──────────────────────────────────────┐           │
│    │ fastman_cli/commands/newcmd.py       │           │
│    │ def newcmd_command():                │           │
│    │     # Implementation                 │           │
│    └──────────────────────────────────────┘           │
│    ┌──────────────────────────────────────┐           │
│    │ fastman_cli/cli.py                   │           │
│    │ @app.command("newcmd")               │           │
│    │ def newcmd(): newcmd_command()       │           │
│    └──────────────────────────────────────┘           │
│                                                        │
│ 2. Customize Template                                  │
│    ┌──────────────────────────────────────┐           │
│    │ fastman_cli/templates/               │           │
│    │ model_template.py                    │           │
│    │ - Edit generate_model()              │           │
│    │ - Add custom fields                  │           │
│    │ - Modify structure                   │           │
│    └──────────────────────────────────────┘           │
│                                                        │
│ 3. Add New Template                                    │
│    ┌──────────────────────────────────────┐           │
│    │ fastman_cli/templates/               │           │
│    │ test_template.py                     │           │
│    │ def generate_tests():                │           │
│    │     # Generate test code             │           │
│    └──────────────────────────────────────┘           │
│    ┌──────────────────────────────────────┐           │
│    │ fastman_cli/commands/startapp.py     │           │
│    │ files["test.py"] = generate_tests()  │           │
│    └──────────────────────────────────────┘           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 🔐 Security Considerations

```
┌─────────────────────────────────────────┐
│ SECURITY LAYER                          │
├─────────────────────────────────────────┤
│ ✓ Input Validation (Pydantic)           │
│ ✓ SQL Injection Protection (SQLAlchemy) │
│ ✓ Type Safety (Python Type Hints)       │
│ ✓ Async Database Operations             │
│ ✓ Dependency Injection                  │
│ ✓ Exception Handling                    │
└─────────────────────────────────────────┘
```

## 📈 Scalability

```
Project Growth Path:

Small Project (1-5 modules)
    ↓
├─ app/
│  ├─ product/
│  ├─ order/
│  └─ customer/

Medium Project (5-20 modules)
    ↓
├─ app/
│  ├─ products/
│  ├─ orders/
│  ├─ customers/
│  ├─ payments/
│  ├─ invoices/
│  └─ ...

Large Project (20+ modules)
    ↓
├─ app/
│  ├─ products/
│  ├─ orders/
│  ├─ customers/
│  ├─ payments/
│  ├─ shipping/
│  ├─ inventory/
│  ├─ analytics/
│  └─ ... (unlimited modules)

All managed with the same CLI! 🚀
```

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2025-10-04
