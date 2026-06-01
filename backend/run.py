#!/usr/bin/env python3
import uvicorn
import sys
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    print("HISTAR REST API Server Starting...")
    uvicorn.run("main:app", host="[IP_ADDRESS]", port=8000, reload=True)
