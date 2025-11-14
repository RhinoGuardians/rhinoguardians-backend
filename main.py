from alembic import op
import sqlalchemy as sa

def upgrade():
    op.alter_column('alerts', 'detection', new_column_name='detection_id', existing_type=sa.String())

def downgrade():
    op.alter_column('alerts', 'detection_id', new_column_name='detection', existing_type=sa.String())

"""
RhinoGuardians Backend API

This is the main FastAPI application module that sets up the API server
and includes all route handlers. The API provides endpoints for rhino detection,
alerts, and system health monitoring.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router
from routes.alerts import router as alerts_router
from routes.notifications import router as notifications_router

app = FastAPI(
    title="RhinoGuardians API",
    description="API for rhino detection and alert system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(alerts_router)
app.include_router(notifications_router)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message dictionary
    """
    return {"message": "Welcome to RhinoGuardians API"}
