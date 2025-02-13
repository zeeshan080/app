# CrewAI API

CrewAI API is a FastAPI-based application that demonstrates an AI-driven workflow using CrewAI flows integrated with a language model from litellm. This API defines a simple flow that triggers a model completion and returns the result via a REST endpoint.

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Environment Configuration](#environment-configuration)
6. [Running the Application](#running-the-application)
   - [Development Mode](#development-mode)
   - [Production Mode](#production-mode)
7. [API Endpoints](#api-endpoints)
8. [Project Overview](#project-overview)
9. [Contributing](#contributing)
10. [License](#license)

## 1. Overview

CrewAI API uses FastAPI to create a RESTful service. It leverages CrewAI's `Flow` class to build a simple AI workflow and uses litellm's `completion` function to interact with a Gemini model (e.g., `gemini/gemini-1.5-flash`). The application includes separate Dockerfiles for development and production to optimize your workflow.

## 2. File Structure

```
.
├── Dockerfile.dev        # Dockerfile for development with live-reload
├── Dockerfile.prod       # Production Dockerfile (multi-stage build, optimized image)
├── docker-compose.yaml   # Docker Compose file for development
├── pyproject.toml        # Project dependency and configuration file
├── README.md             # This file
├── .env.example          # Template for environment variables
└── src/
    └── app/
        ├── __init__.py
        └── main.py       # Main FastAPI application file
```

## 3. Prerequisites

- **Docker** installed on your system.
- **Python 3.11** if running locally without Docker.
- An active internet connection to pull base images and install dependencies.

## 4. Installation

### Clone the Repository

```bash
git clone https://your-repository-url.git
cd your-repository
```

### (Optional) Create a Virtual Environment for Local Development

If you prefer to run the project without Docker:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Install Dependencies

This project uses the `uv` package manager and dependencies are defined in `pyproject.toml`.

#### Install `uv`:
```bash
pip install uv
```

#### Install dependencies:
```bash
uv pip install --system --requirements pyproject.toml
```

Alternatively, if you have a `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## 5. Environment Configuration

Before running the application, copy the provided environment file and update it:

```bash
cp .env.example .env
```

Open `.env` and update the values:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MODEL=gemini/gemini-1.5-flash
```

## 6. Running the Application

There are separate configurations for development and production.

### Development Mode

The development Dockerfile (`Dockerfile.dev`) is designed for live code reloading and volume mapping.

#### Using Docker Compose

A sample `docker-compose.yaml` file:

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
```

To build and run the container:
```bash
docker-compose up --build
```

This starts your FastAPI app on `http://localhost:8000` with live reload enabled.

#### Running Directly with Docker

```bash
docker build -f Dockerfile.dev -t crewai-api-dev .
docker run -p 8000:8000 -v "$(pwd)":/app crewai-api-dev
```

### Production Mode

For production, use `Dockerfile.prod`, which utilizes a multi-stage build to create a smaller image.

#### Build the Production Image
```bash
docker build -f Dockerfile.prod -t crewai-api-prod .
```

#### Run the Production Container
```bash
docker run -p 8000:8000 crewai-api-prod
```

Your FastAPI application will run on `http://localhost:8000` without live-reload.

## 7. API Endpoints

Once the application is running, FastAPI provides interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Example Endpoint: `/kickoff`

- **Method**: `GET`
- **Description**: Initiates a CrewAI flow that triggers the model completion. The response contains an agent ID and the generated message.
- **Response Example**:

```json
{
  "agent_id": "<agent_id>",
  "message": {
    "message": "Generated message from the model..."
  }
}
```

## 8. Project Overview

### Main Application (`src/app/main.py`)

```python
from fastapi import FastAPI
from crewai.flow.flow import Flow, start
from pydantic import BaseModel
from litellm import completion

class AgentState(BaseModel):
    message: str = ""

app = FastAPI(
    title="CrewAI API",
    description="API for CrewAI application",
    version="1.0.0",
    servers=[{"url": "http://localhost:8000", "description": "Local server"}]
)

class SimpleFlow(Flow[AgentState]):
    @start()
    def root(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"content": "Say Hello World with your model name?", "role": "user"}]
        )
        self.state.message = response["choices"][0]["message"]["content"]

@app.get("/kickoff")
def kickoff():
    agent = SimpleFlow()
    agent.kickoff()
    return {"agent_id": agent.state.message["id"], "message": agent.state}
```

## 9. Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m "Add your commit message"`
4. Push to your fork and submit a pull request.

For major changes, please open an issue first.

## 10. License

This project is licensed under the MIT License. See the LICENSE file for details.

