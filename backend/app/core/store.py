from typing import List
import random

ASSESSMENTS: dict = {}


TOPICS: List[str] = [
    "Ethical trade-offs of AI decision-making in healthcare",
    "Algorithmic bias and its societal consequences",
    "Scientific uncertainty and public trust",
    "Innovation versus risk in scientific research",
    "The role of failure in scientific and technological progress",
    "Interdisciplinary research and major breakthroughs",
    "Technology’s influence on scientific discovery",

    "Civic responsibility in democratic societies",
    "The role of media in shaping public opinion",
    "Balancing individual rights and public safety",
    "Transparency and accountability in governance",
    "Youth participation in political and civic processes",
    "Freedom versus security in modern societies",

    "The psychology of habit formation and self-discipline",
    "Why humans resist change even when it is beneficial",
    "Cognitive biases in everyday decision-making",
    "Stress, motivation, and productivity in modern life",
    "Emotional intelligence and its role in leadership",

    "Traditional education versus skill-based learning",
    "The effectiveness and limitations of online learning",
    "Memorization versus conceptual understanding",
    "The role of curiosity in deep learning",
    "Assessment systems and their impact on creativity",

    "The impact of automation on employment",
    "The rise of the gig economy",
    "Remote work and work–life balance",
    "Inflation and its effect on middle-class households",
    "Consumerism and financial decision-making",
    "The future of entrepreneurship in a digital economy",

    "Individual responsibility versus government policy in climate action",
    "Sustainable development and economic growth conflicts",
    "Urbanization and its environmental impact",
    "Challenges in renewable energy adoption",
    "Water scarcity and global inequality",

    "The importance of active listening in effective communication",
    "How language shapes perception and thought",
    "Miscommunication in digital conversations",
    "Persuasion techniques in everyday communication",
    "Cultural differences in communication styles",

    "Moral responsibility in technological innovation",
    "Fairness in competitive environments",
    "Individualism versus collectivism",
    "Is success defined by society or the individual?",
    "Long-term thinking in a short-term world",

    "Discipline versus motivation in achieving goals",
    "The role of failure in personal growth",
    "Confidence versus arrogance",
    "Defining success beyond material achievement"
]

def get_random_topic() -> str:
    return random.choice(TOPICS)
