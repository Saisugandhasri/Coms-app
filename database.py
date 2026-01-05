from pymongo import MongoClient

client = MongoClient("mongodb+srv://Pranay:Pranay%409671610@pdfextraction.mj0vgph.mongodb.net/")
db = client["AssessmentApp"]

practice_user_scores = db["practice_user_scores"]


def get_dynamic_analytics(user_id: str):
    user_doc = practice_user_scores.find_one({"user_id": user_id})

    if not user_doc:
        return {"levels": {}}

    level_scores = {}

    for date, levels in user_doc.items():
        if date in ["_id", "user_id"]:
            continue

        for level, attempts in levels.items():
            level_scores.setdefault(level, [])

            for _, data in attempts.items():
                if isinstance(data, dict):
                    score = data.get("score", 0)
                else:
                    score = data

                if isinstance(score, (int, float)):
                    level_scores[level].append(score)

    analytics = {
        level: {
            "attempts": len(scores),
            "average_score": sum(scores) / len(scores) if scores else 0
        }
        for level, scores in level_scores.items()
    }

    return {"levels": analytics}
