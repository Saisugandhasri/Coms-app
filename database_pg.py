from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://vidya:vidya@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_static_profile(user_id: str):
    session = SessionLocal()
    result = session.execute(
        text("""
            SELECT user_id, full_name, usermail
            FROM users
            WHERE user_id = :uid
        """),
        {"uid": user_id}
    ).fetchone()
    session.close()

    if not result:
        return None

    return {
        "user_id": result.user_id,
        "name": result.full_name,
        "email": result.usermail
    }
