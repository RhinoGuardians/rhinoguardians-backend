from setuptools import setup, find_packages

setup(
    name="rhinoguardians-backend",
    version="0.1.0",
    description="FastAPI backend for RhinoGuardians - AI-powered wildlife detection system",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "python-multipart",
        "torch",
        "pytest",
        "pytest-cov",
        "requests",
        "python-dotenv",
        "pillow",
        "psycopg2-binary",
        "ultralytics"
    ],
    python_requires=">=3.10"
)