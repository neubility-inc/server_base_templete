from imp import reload
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.robot_api:app", host="0.0.0.0", port=8033, reload=True)