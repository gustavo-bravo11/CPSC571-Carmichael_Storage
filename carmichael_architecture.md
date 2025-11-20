# Carmichael Numbers Database Project - Architecture Document

## Project Overview

A two-component system for managing and querying a database of Carmichael numbers (CNs):
1. **Scientific Testing Component**: Automated performance comparison of two PostgreSQL implementations
2. **User Interface Component**: Web-based query interface for the mathematics community

**Dataset**: 310M rows (~18GB), CNs with 3-14 prime factors

---

## Database Implementations Being Tested

### Implementation 1: Single Table with Array
- **Structure**: One table with CN as primary key, factors stored as PostgreSQL array
- **Indexing**: GIN index on factors array
- **Pros**: Simple schema, single query point
- **Cons**: May have performance overhead for array operations

### Implementation 2: Multi-Table by Factor Count
- **Structure**: 12 separate tables (CN_3, CN_4, ..., CN_14)
- **Organization**: Each table contains CNs with exactly n prime factors
- **Optimization**: Query can skip tables with fewer columns than required factors
- **Pros**: Targeted queries, automatic table elimination
- **Cons**: More complex query logic, schema maintenance

---

## Component 1: Scientific Testing System

### Purpose
Automated performance testing and visualization comparing both database implementations against predefined test cases (3-10 factors, varying complexity).

### Recommended Technology Stack

**Core Language**: Python 3.x (standard library focused)

**Required Packages**:
- **subprocess** (standard library) - Database access via `psql` commands
- **time** (standard library) - Query timing with `time.perf_counter()`
- **json** (standard library) - Test case definitions and configuration
- **csv** (standard library) - Results export
- **abc** (standard library) - Abstract base classes for interface design
- **matplotlib** - Visualization library for generating graphs

**Optional but Helpful**:
- **typing** (standard library) - Type hints for clarity
- **pathlib** (standard library) - File path handling
- **argparse** (standard library) - Command-line interface

### Project Structure

```
carmichael_testing/
├── config/
│   ├── db_config.json          # Database connection details
│   └── test_cases.json         # Predefined test queries (already created)
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base_interface.py   # Abstract database interface (ABC)
│   │   ├── impl1_interface.py  # Single table implementation
│   │   └── impl2_interface.py  # Multi-table implementation
│   ├── testing/
│   │   ├── __init__.py
│   │   ├── test_runner.py      # Executes test suite
│   │   └── timer.py            # Query timing utilities
│   └── visualization/
│       ├── __init__.py
│       └── plotter.py          # Matplotlib visualization
├── results/
│   └── [generated CSV/JSON files]
└── run_tests.py                # Main entry point
```

### Key Design Patterns

**Abstract Database Interface**:
- Create an abstract base class `DatabaseInterface` using Python's ABC
- Define abstract methods: `query_by_factors()`, `build_query()`
- Implement concrete classes for each database implementation
- Common method `execute_psql()` handles subprocess calls to psql

**Test Execution Flow**:
1. Load test cases from JSON
2. For each test case, run N times (e.g., 10 runs) on both implementations
3. Record timing data: min, max, average
4. Export results to CSV for analysis

**Visualization Requirements**:
- Generate comparison charts (bar charts or line graphs)
- Group by number of factors (3-10)
- Show avg, min, max times for each implementation
- Save as PNG/PDF for inclusion in reports

### Implementation Checklist

- [ ] Create abstract `DatabaseInterface` class with ABC
- [ ] Implement `SingleTableInterface` (Implementation 1)
- [ ] Implement `MultiTableInterface` (Implementation 2)
- [ ] Build test runner that loads JSON test cases
- [ ] Implement timing mechanism using `time.perf_counter()`
- [ ] Create CSV export functionality
- [ ] Build matplotlib visualization module
- [ ] Create main entry point script
- [ ] Write configuration file parser

---

## Component 2: User Interface System

### Purpose
Web-based query interface for mathematics community to search CNs by prime factors.

### Recommended Technology Stack

**Backend**:
- **Flask** - Lightweight Python web framework (easy to learn, minimal dependencies)
  - Why Flask: Simple, well-documented, your partner can modify templates easily
  - Alternative: If you want more structure later, FastAPI (but Flask is better for simplicity)
- **subprocess** (standard library) - Database access (consistent with testing component)

**Required Flask Extensions**:
- **flask** (core) - Web framework
- **flask-cors** (optional) - If you need CORS for development

**Frontend**:
- **HTML5** - Structure
- **CSS3** - Styling (you'll write custom CSS)
- **Vanilla JavaScript** - Dynamic input boxes (no framework needed)
  - Why vanilla: Your use case is simple (dynamic input boxes), no need for React
  - You only need basic DOM manipulation

**Optional Frontend Enhancements**:
- **CSS Framework (pick ONE)**:
  - **Water.css** or **Simple.css** - Classless CSS (just include, instant styling)
  - **Bootstrap 5** - If you want more control and components
  - **Tailwind CSS** - If you want utility-first approach
  - Recommendation: Start with Water.css for simplicity, upgrade if needed

### Project Structure

```
carmichael_web/
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── config.py               # Configuration management
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base_interface.py   # SAME abstract interface from testing
│   │   ├── impl1_interface.py  # SAME implementation classes
│   │   └── impl2_interface.py  # Reuse your testing code!
│   ├── routes/
│   │   ├── __init__.py
│   │   └── query_routes.py     # API endpoints
│   └── utils/
│       └── validators.py       # Input validation
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css      # Custom CSS
│   │   └── js/
│   │       └── app.js          # Dynamic input logic
│   └── templates/
│       ├── base.html           # Base template
│       └── index.html          # Main query page
└── run.py                      # Application runner
```

### Key Design Patterns

**Backend Architecture**:
- **Pluggable Database Layer**: Reuse the abstract interface from testing component
- **RESTful API**: Flask routes return JSON responses
- **Stateless**: No session management needed for simple queries

**Frontend User Flow**:
1. User sees single empty input box
2. User enters a prime factor
3. On input (blur or change event), new empty box appears below
4. Repeat until 14 boxes or user stops
5. Submit button sends non-empty values to backend
6. Display results (list of CN numbers)

**API Design**:
```
POST /api/query
Request Body: { "factors": [3, 5, 7] }
Response: { "results": [561, 1105, ...], "count": 125 }
```

### Frontend Implementation Notes

**Dynamic Input Boxes (Vanilla JavaScript)**:
- Start with one input element
- Event listener on input: if value is non-empty and it's the last box, append new input
- On submit: collect all non-empty values, send to API
- Max 14 inputs

**Styling Approach**:
- Use a classless CSS framework for baseline (Water.css or Simple.css)
- Write custom CSS for:
  - Input box styling
  - Results display (could be a simple list or table)
  - Responsive layout
- Keep it clean and minimal

### Implementation Checklist

**Backend**:
- [ ] Set up Flask application structure
- [ ] Copy abstract database interface from testing component
- [ ] Create Flask route for POST /api/query
- [ ] Implement input validation (factors must be prime, reasonable range)
- [ ] Test API with curl or Postman
- [ ] Add error handling

**Frontend**:
- [ ] Create base HTML template
- [ ] Implement dynamic input box logic in JavaScript
- [ ] Add CSS styling (start simple, iterate)
- [ ] Connect frontend to backend API
- [ ] Test user flow end-to-end
- [ ] Add loading states for queries
- [ ] Format results display

---

## Deployment Considerations

### University Server Constraints
- Limited package installation (approval process required)
- Must use subprocess for database access
- Python version: [confirm with server admin]

### Deployment Strategy

**Testing Component**:
- Can run locally or on server
- Outputs: CSV files and PNG/PDF graphs
- No web server needed

**Web Application**:
- Flask development server for initial testing
- For production: Use university's existing web server setup
  - If Apache: Use mod_wsgi
  - If Nginx: Use gunicorn or uWSGI
- Single server deployment (frontend + backend together)

### Package Installation Plan

**Start with standard library only**:
- subprocess, json, csv, time, abc
- Test both components with minimal dependencies

**Request approval for**:
1. **matplotlib** - Required for scientific visualization
2. **flask** - Required for web interface

**Justify to administrators**:
- Matplotlib: Standard scientific package, widely used in academia
- Flask: Minimal, secure web framework, actively maintained

---

## Development Roadmap

### Phase 1: Scientific Testing (Week 1-2)
1. Set up project structure
2. Implement abstract database interface
3. Implement both database implementation classes
4. Create test runner
5. Test with existing test cases
6. Generate CSV results
7. Create matplotlib visualizations

### Phase 2: Backend API (Week 3)
1. Set up Flask application
2. Reuse database interfaces from Phase 1
3. Implement query API endpoint
4. Add input validation
5. Test API independently

### Phase 3: Frontend (Week 4)
1. Create HTML template
2. Implement dynamic input JavaScript
3. Style with CSS
4. Connect to backend API
5. Test complete user flow

### Phase 4: Integration & Deployment (Week 5)
1. Choose winning database implementation based on Phase 1 results
2. Configure web application to use chosen implementation
3. Deploy to university server
4. User testing with math community
5. Iterate based on feedback

---

## Key Advantages of This Architecture

### Modularity
- Abstract interface allows swapping database implementations without touching business logic
- Testing component and web component share the same database layer

### Simplicity
- Minimal dependencies (can start with standard library)
- Flask is easy for non-developers to modify (Jinja2 templates)
- Vanilla JavaScript is straightforward

### Maintainability
- Clear separation of concerns
- Your partner can modify HTML/CSS templates without Python knowledge
- Future improvements (e.g., adding caching) are straightforward

### Extensibility
- Want to add NoSQL later? Just implement `DatabaseInterface`
- Want to add more query types? Add methods to interface
- Want to add user authentication? Flask makes it easy

---

## Next Steps

1. **Confirm Python version** on university server
2. **Confirm matplotlib availability** or start approval process
3. **Start with Phase 1** (testing component) - uses only standard library + matplotlib
4. **Request Flask approval** while building testing component
5. **Create this document as your specification** for implementation

---

## Questions for Further Refinement

- Do you want real-time query results, or is a few seconds of load time acceptable?
- Should results be paginated (e.g., show first 100, load more)?
- Do you need query history or session management?
- Should there be an admin interface for database management?
- Do you want to export results (CSV download for users)?

---

## Summary

**For Scientific Testing**: Python + matplotlib, subprocess for DB, abstract interfaces, automated test runner

**For User Interface**: Flask backend (reusing DB interfaces), vanilla HTML/CSS/JavaScript frontend, simple and maintainable

**Philosophy**: Start simple, stay modular, make it easy for your partner to maintain
    