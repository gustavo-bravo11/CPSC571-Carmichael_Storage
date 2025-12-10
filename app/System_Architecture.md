app/
├── backend/
│   ├── server.js              # Express server (entry point)
│   ├── db/
│   │   ├── DatabaseInterface.js    # Abstract interface
│   │   ├── OneTableDB.js           # PostgreSQL implementation
|   |   └── ...                     # Any other implementations
│   ├── package.json
│   └── node_modules/
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js