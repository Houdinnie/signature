# Signature Project Setup Instructions

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If you encounter timeout issues, try installing packages in smaller groups or individually.

3. Start the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   The API will be available at http://localhost:8000

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## Project Structure

```
Signature/
├── backend/              # FastAPI backend
│   └── app/
│       ├── api/          # API endpoints
│       ├── agents/       # AI agent implementations
│       ├── core/         # Core business logic
│       ├── models/       # Database models
│       ├── schemas/      # Pydantic schemas
│       ├── services/     # Business services
│       └── utils/        # Utility functions
├── frontend/             # Next.js frontend
│   ├── pages/            # Next.js pages
│   ├── components/       # React components
│   ├── styles/           # CSS/Tailwind styles
│   ├── utils/            # Utility functions
│   ├── lib/              # Library code
│   └── public/           # Static assets
└── docker/               # Docker configuration (if needed)
```

## API Endpoints

- GET / - Welcome message
- GET /health - Health check
- GET /health/db - Database health check
- GET /health/redis - Redis health check
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/register - User registration
- GET /api/v1/auth/logout - User logout
- GET /api/v1/agents - List all agents
- POST /api/v1/agents - Create a new agent
- GET /api/v1/agents/{id} - Get agent by ID
- PUT /api/v1/agents/{id} - Update agent
- DELETE /api/v1/agents/{id} - Delete agent
- POST /api/v1/agents/{id}/run - Run an agent
- GET /api/v1/agents/{id}/runs - Get agent runs

## Next Steps for Development

1. Implement the remaining agent types (Planning, Competitor Research, etc.)
2. Create additional API endpoints for task management, notifications, etc.
3. Implement the frontend dashboard components
4. Add real-time updates using WebSockets
5. Implement the approval workflow system
6. Add integration with external services (PayPal, SendGrid, etc.)
7. Set up the memory system with ChromaDB
8. Configure Celery for background task processing

## Troubleshooting

If you encounter import errors:
1. Make sure you are in the correct directory when running commands
2. Check that all required packages are installed
3. Verify that your Python environment is activated
4. Try restarting the terminal/IDE

If you encounter port conflicts:
1. Change the port number in the uvicorn command
2. Update the frontend API URL if needed

## Important Notes

- The backend uses SQLite by default for simplicity. For production, configure PostgreSQL.
- The frontend uses Tailwind CSS for styling.
- Authentication is implemented using JWT tokens.
- Agent execution is currently simulated; actual AI agent execution will require integration with Claude Code CLI or similar.

Happy coding!