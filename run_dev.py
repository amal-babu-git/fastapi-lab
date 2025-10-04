#!/usr/bin/env python3
"""
Development server runner for FastAPI Learn application.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.core.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )