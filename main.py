import uvicorn
import define

if __name__ == "__main__":
    uvicorn.run(
        f"app.{define.SERVER_NAME.lower()}:app", host="0.0.0.0", port=9000, reload=True
    )
