from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crewai.flow.flow import Flow, start
from pydantic import BaseModel
from litellm import completion

class AgentState(BaseModel):
    # Note: 'id' field is automatically added to all states
    message: str = ""


app = FastAPI(
title="CrewAI API",
description="API for CrewAI application",
version="1.0.0",
servers=[
    {"url": "http://localhost:8000", "description": "Local server"},
    # {"url": "https://", "description": "Production server"}
]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class SimpleFlow(Flow[AgentState]):

    @start()
    def root(self):
        response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{ "content": "Say Hello World with you model name and input, output tokens size?","role": "user"}]
        )
        self.state.message = response["choices"][0]["message"]["content"]
    

@app.get("/kickoff")
def kickoff():
    agent = SimpleFlow()
    agent.kickoff()
    return { "agent_id": agent.state.id,"message" : agent.state.message}



