# Math Animator

A web application that generates mathematical animations from natural language descriptions using GPT-4 and Manim.

## Features

- Natural language to animation conversion
- Multiple quality options (480p, 720p, 1080p)
- Example templates for common mathematical concepts
- Real-time animation preview
- Caching for improved performance
- Rate limiting and API key management

## Tech Stack

- Frontend: React, TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- Animation: Manim Community v0.17.3
- AI: GPT-4o
- Database: PostgreSQL
- Cache: Redis
- Container: Docker

## Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker
- PostgreSQL
- Redis

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

### Docker Setup

1. Build and run with Docker Compose:
```bash
cd backend/docker
docker-compose up --build
```

## Usage

1. Visit `http://localhost:3000`
2. Enter a description of the mathematical concept
3. Select quality options
4. Click "Generate Animation"
5. Wait for the animation to render
6. View and download the result

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 