from fastapi import FastAPI, HTTPException
from database_pg import get_static_profile
from database import get_dynamic_analytics

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Coms-app backend running"}


@app.get("/user/profile-performance/{user_id}")
def profile_performance(user_id: str):

    profile = get_static_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    analytics = get_dynamic_analytics(user_id)

    return {
        "profile": profile,
        "analytics": analytics
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=9001,
        reload=True
    )
