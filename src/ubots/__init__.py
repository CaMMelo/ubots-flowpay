import uvicorn


def main():
    uvicorn.run("ubots.api:app", host="0.0.0.0", port=8000, reload=True)
