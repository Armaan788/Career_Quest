from flask import Flask, render_template, redirect, url_for, request, session
import json
import os
import random

app = Flask(__name__)
app.secret_key = "career-quest-secret"


# ============================
# SAVE SYSTEM
# ============================

def load_players():

    if not os.path.exists("players.json"):

        return {}

    with open("players.json", "r") as file:

        return json.load(file)


def save_players(players):

    with open("players.json", "w") as file:

        json.dump(players, file, indent=4)


def load_stats():

    if not os.path.exists("stats.json"):

        return {
            "visits": 0
        }

    with open("stats.json", "r") as file:

        return json.load(file)


def save_stats(stats):

    with open("stats.json", "w") as file:

        json.dump(stats, file, indent=4)


# ============================
# CAREER DATA
# ============================

careers = {

    "Software Engineer": [
        {
            "q": "A bug breaks production. You:",
            "skill": "Problem Solving",
            "options": [
                ("Investigate the cause and fix it carefully", 3),
                ("Patch it quickly without testing", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "Code review feedback arrives. You:",
            "skill": "Communication",
            "options": [
                ("Use the feedback to improve your code", 3),
                ("Defend every choice", 1),
                ("Ignore the comments", 0)
            ]
        },
        {
            "q": "A new framework becomes popular. You:",
            "skill": "Technical Skill",
            "options": [
                ("Build a small project with it", 3),
                ("Watch a few videos", 2),
                ("Avoid learning it", 0)
            ]
        },
        {
            "q": "The app is slow. You:",
            "skill": "Technical Skill",
            "options": [
                ("Find bottlenecks and optimize", 3),
                ("Guess randomly", 1),
                ("Do nothing", 0)
            ]
        },
        {
            "q": "Your team disagrees on a solution. You:",
            "skill": "Leadership",
            "options": [
                ("Discuss tradeoffs and guide a decision", 3),
                ("Stay silent", 0),
                ("Force your idea", 1)
            ]
        }
    ],

    "Teacher": [
        {
            "q": "A student is struggling. You:",
            "skill": "Communication",
            "options": [
                ("Help them individually", 3),
                ("Tell them to try harder", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "The class is distracted. You:",
            "skill": "Leadership",
            "options": [
                ("Calmly refocus the class", 3),
                ("Yell immediately", 1),
                ("Give up", 0)
            ]
        },
        {
            "q": "Your lesson plan is not working. You:",
            "skill": "Problem Solving",
            "options": [
                ("Adjust the lesson", 3),
                ("Keep going anyway", 1),
                ("Stop teaching", 0)
            ]
        },
        {
            "q": "Parents ask about progress. You:",
            "skill": "Communication",
            "options": [
                ("Explain clearly and respectfully", 3),
                ("Avoid the conversation", 0),
                ("Blame the student", 1)
            ]
        },
        {
            "q": "Exam scores drop. You:",
            "skill": "Technical Skill",
            "options": [
                ("Analyze what students missed", 3),
                ("Ignore the data", 0),
                ("Make the next exam easier only", 1)
            ]
        }
    ],

    "Entrepreneur": [
        {
            "q": "Your startup is losing money. You:",
            "skill": "Problem Solving",
            "options": [
                ("Analyze costs and pivot strategy", 3),
                ("Panic", 1),
                ("Quit instantly", 0)
            ]
        },
        {
            "q": "An investor rejects your pitch. You:",
            "skill": "Communication",
            "options": [
                ("Improve the pitch using feedback", 3),
                ("Ignore the feedback", 0),
                ("Argue with them", 1)
            ]
        },
        {
            "q": "A competitor launches first. You:",
            "skill": "Leadership",
            "options": [
                ("Differentiate and move faster", 3),
                ("Copy them exactly", 1),
                ("Do nothing", 0)
            ]
        },
        {
            "q": "Customers complain. You:",
            "skill": "Communication",
            "options": [
                ("Listen and improve the product", 3),
                ("Blame customers", 0),
                ("Hide the reviews", 1)
            ]
        },
        {
            "q": "Your team is stressed. You:",
            "skill": "Leadership",
            "options": [
                ("Set priorities and motivate them", 3),
                ("Ignore morale", 0),
                ("Demand more work", 1)
            ]
        }
    ],

    "Doctor": [
        {
            "q": "An emergency patient arrives. You:",
            "skill": "Problem Solving",
            "options": [
                ("Assess and act quickly", 3),
                ("Wait too long", 0),
                ("Guess without checking", 1)
            ]
        },
        {
            "q": "A diagnosis is unclear. You:",
            "skill": "Technical Skill",
            "options": [
                ("Run tests and review symptoms", 3),
                ("Guess immediately", 0),
                ("Ignore uncertainty", 0)
            ]
        },
        {
            "q": "A patient is anxious. You:",
            "skill": "Communication",
            "options": [
                ("Reassure and explain clearly", 3),
                ("Rush them", 1),
                ("Ignore emotions", 0)
            ]
        },
        {
            "q": "You are tired during a long shift. You:",
            "skill": "Leadership",
            "options": [
                ("Stay focused and ask for support if needed", 3),
                ("Lose focus", 0),
                ("Complain constantly", 1)
            ]
        },
        {
            "q": "There is a medication risk. You:",
            "skill": "Technical Skill",
            "options": [
                ("Double-check everything", 3),
                ("Proceed fast", 1),
                ("Ignore warnings", 0)
            ]
        }
    ],

    "Lawyer": [
        {
            "q": "A case needs preparation. You:",
            "skill": "Technical Skill",
            "options": [
                ("Research deeply", 3),
                ("Guess arguments", 0),
                ("Skim quickly", 1)
            ]
        },
        {
            "q": "Court gets intense. You:",
            "skill": "Leadership",
            "options": [
                ("Stay calm and focused", 3),
                ("Panic", 0),
                ("Argue emotionally", 1)
            ]
        },
        {
            "q": "Evidence is weak. You:",
            "skill": "Problem Solving",
            "options": [
                ("Strengthen the case strategy", 3),
                ("Ignore it", 0),
                ("Hope nobody notices", 1)
            ]
        },
        {
            "q": "A client may be lying. You:",
            "skill": "Communication",
            "options": [
                ("Ask questions and verify facts", 3),
                ("Accept everything blindly", 0),
                ("Accuse them immediately", 1)
            ]
        },
        {
            "q": "The opposition is strong. You:",
            "skill": "Problem Solving",
            "options": [
                ("Build a stronger counterargument", 3),
                ("Give up", 0),
                ("Attack personally", 1)
            ]
        }
    ],

    "Designer": [
        {
            "q": "A client dislikes your design. You:",
            "skill": "Communication",
            "options": [
                ("Ask what needs improvement", 3),
                ("Argue", 1),
                ("Ignore them", 0)
            ]
        },
        {
            "q": "You hit a creative block. You:",
            "skill": "Problem Solving",
            "options": [
                ("Experiment with new ideas", 3),
                ("Copy another design", 1),
                ("Stop working", 0)
            ]
        },
        {
            "q": "A deadline is close. You:",
            "skill": "Leadership",
            "options": [
                ("Prioritize and finish strong", 3),
                ("Rush carelessly", 1),
                ("Quit", 0)
            ]
        },
        {
            "q": "A new design tool appears. You:",
            "skill": "Technical Skill",
            "options": [
                ("Practice using it", 3),
                ("Read about it only", 2),
                ("Avoid it", 0)
            ]
        },
        {
            "q": "Feedback is confusing. You:",
            "skill": "Communication",
            "options": [
                ("Clarify expectations", 3),
                ("Guess", 1),
                ("Ignore feedback", 0)
            ]
        }
    ],

    "Pilot": [
        {
            "q": "Bad weather appears. You:",
            "skill": "Problem Solving",
            "options": [
                ("Follow safety protocols", 3),
                ("Take unnecessary risk", 0),
                ("Ignore warnings", 0)
            ]
        },
        {
            "q": "A system warning appears. You:",
            "skill": "Technical Skill",
            "options": [
                ("Use emergency checklist", 3),
                ("Panic", 0),
                ("Guess", 1)
            ]
        },
        {
            "q": "Passengers are nervous. You:",
            "skill": "Communication",
            "options": [
                ("Communicate calmly", 3),
                ("Say nothing", 1),
                ("Sound scared", 0)
            ]
        },
        {
            "q": "A long flight gets tiring. You:",
            "skill": "Leadership",
            "options": [
                ("Stay alert and professional", 3),
                ("Lose focus", 0),
                ("Relax too much", 1)
            ]
        },
        {
            "q": "Navigation data seems wrong. You:",
            "skill": "Technical Skill",
            "options": [
                ("Recheck instruments and route", 3),
                ("Guess the route", 0),
                ("Ignore it", 0)
            ]
        }
    ],

    "Chef": [
        {
            "q": "Orders are flooding in. You:",
            "skill": "Leadership",
            "options": [
                ("Organize the kitchen", 3),
                ("Panic", 0),
                ("Ignore tickets", 0)
            ]
        },
        {
            "q": "A dish gets criticized. You:",
            "skill": "Communication",
            "options": [
                ("Accept feedback and improve", 3),
                ("Argue with the customer", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "A key ingredient is missing. You:",
            "skill": "Problem Solving",
            "options": [
                ("Adapt the recipe", 3),
                ("Cancel everything", 0),
                ("Use a random substitute", 1)
            ]
        },
        {
            "q": "The kitchen is chaotic. You:",
            "skill": "Leadership",
            "options": [
                ("Stay calm and delegate", 3),
                ("Yell at everyone", 1),
                ("Walk out", 0)
            ]
        },
        {
            "q": "You learn a new cooking method. You:",
            "skill": "Technical Skill",
            "options": [
                ("Practice it carefully", 3),
                ("Try once", 1),
                ("Avoid it", 0)
            ]
        }
    ],

    "Data Scientist": [
        {
            "q": "Your dataset is messy. You:",
            "skill": "Technical Skill",
            "options": [
                ("Clean and validate the data", 3),
                ("Ignore bad rows", 0),
                ("Guess the results", 0)
            ]
        },
        {
            "q": "Model accuracy is low. You:",
            "skill": "Problem Solving",
            "options": [
                ("Test improvements carefully", 3),
                ("Randomly change settings", 1),
                ("Give up", 0)
            ]
        },
        {
            "q": "Executives ask for insights. You:",
            "skill": "Communication",
            "options": [
                ("Explain results clearly", 3),
                ("Use confusing jargon", 1),
                ("Avoid answering", 0)
            ]
        },
        {
            "q": "Important data is missing. You:",
            "skill": "Problem Solving",
            "options": [
                ("Handle missing data properly", 3),
                ("Delete everything blindly", 0),
                ("Pretend it's complete", 0)
            ]
        },
        {
            "q": "A new algorithm appears. You:",
            "skill": "Technical Skill",
            "options": [
                ("Study and test it", 3),
                ("Skim an article", 1),
                ("Ignore it", 0)
            ]
        }
    ],

    "Marketing Manager": [
        {
            "q": "A campaign is underperforming. You:",
            "skill": "Problem Solving",
            "options": [
                ("Analyze data and adjust strategy", 3),
                ("Blame the team", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "The target audience is unclear. You:",
            "skill": "Technical Skill",
            "options": [
                ("Research the market", 3),
                ("Guess", 0),
                ("Skip research", 0)
            ]
        },
        {
            "q": "Ad feedback is negative. You:",
            "skill": "Communication",
            "options": [
                ("Listen and improve the message", 3),
                ("Argue online", 1),
                ("Delete feedback", 0)
            ]
        },
        {
            "q": "Budget gets cut. You:",
            "skill": "Leadership",
            "options": [
                ("Prioritize high-impact channels", 3),
                ("Waste the budget", 0),
                ("Stop trying", 0)
            ]
        },
        {
            "q": "A competitor campaign goes viral. You:",
            "skill": "Problem Solving",
            "options": [
                ("Create a unique response", 3),
                ("Copy them", 1),
                ("Do nothing", 0)
            ]
        }
    ],

    "Cybersecurity Analyst": [
        {
            "q": "Your company detects suspicious login attempts. You:",
            "skill": "Technical Skill",
            "options": [
                ("Investigate logs and block threats", 3),
                ("Ignore the alert", 0),
                ("Delete logs", 0)
            ]
        },
        {
            "q": "An employee clicked a phishing email. You:",
            "skill": "Communication",
            "options": [
                ("Explain the risk and secure the account", 3),
                ("Blame them publicly", 1),
                ("Do nothing", 0)
            ]
        },
        {
            "q": "A server may be compromised. You:",
            "skill": "Problem Solving",
            "options": [
                ("Isolate it and investigate", 3),
                ("Restart and hope", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "Leadership wants a security update. You:",
            "skill": "Communication",
            "options": [
                ("Explain clearly without panic", 3),
                ("Use only technical jargon", 1),
                ("Avoid reporting", 0)
            ]
        },
        {
            "q": "A ransomware warning appears. You:",
            "skill": "Leadership",
            "options": [
                ("Activate the response plan", 3),
                ("Panic", 0),
                ("Pay immediately without checking", 1)
            ]
        }
    ],

    "AI Engineer": [
        {
            "q": "Your AI model gives biased results. You:",
            "skill": "Problem Solving",
            "options": [
                ("Investigate data and reduce bias", 3),
                ("Ignore the issue", 0),
                ("Hide the results", 0)
            ]
        },
        {
            "q": "The model is inaccurate. You:",
            "skill": "Technical Skill",
            "options": [
                ("Improve training and evaluation", 3),
                ("Randomly change code", 1),
                ("Give up", 0)
            ]
        },
        {
            "q": "A client asks how the AI works. You:",
            "skill": "Communication",
            "options": [
                ("Explain clearly and honestly", 3),
                ("Overpromise everything", 1),
                ("Avoid details", 0)
            ]
        },
        {
            "q": "The AI system is slow. You:",
            "skill": "Technical Skill",
            "options": [
                ("Optimize the model and infrastructure", 3),
                ("Ignore performance", 0),
                ("Delete features", 1)
            ]
        },
        {
            "q": "Your team debates AI ethics. You:",
            "skill": "Leadership",
            "options": [
                ("Encourage responsible design", 3),
                ("Dismiss concerns", 0),
                ("Let others decide everything", 1)
            ]
        }
    ],

    "Game Developer": [
        {
            "q": "Players say the game is boring. You:",
            "skill": "Problem Solving",
            "options": [
                ("Analyze feedback and improve gameplay", 3),
                ("Ignore players", 0),
                ("Blame them", 1)
            ]
        },
        {
            "q": "A major bug breaks the game. You:",
            "skill": "Technical Skill",
            "options": [
                ("Debug and patch carefully", 3),
                ("Release without testing", 1),
                ("Ignore it", 0)
            ]
        },
        {
            "q": "Your artist and programmer disagree. You:",
            "skill": "Communication",
            "options": [
                ("Help them find a solution", 3),
                ("Pick sides unfairly", 1),
                ("Avoid the issue", 0)
            ]
        },
        {
            "q": "The deadline is close. You:",
            "skill": "Leadership",
            "options": [
                ("Prioritize the most important features", 3),
                ("Add random new features", 1),
                ("Quit", 0)
            ]
        },
        {
            "q": "Performance is bad on phones. You:",
            "skill": "Technical Skill",
            "options": [
                ("Optimize assets and code", 3),
                ("Ignore mobile players", 0),
                ("Remove half the game", 1)
            ]
        }
    ],

    "Architect": [
        {
            "q": "A building design exceeds budget. You:",
            "skill": "Problem Solving",
            "options": [
                ("Revise the design intelligently", 3),
                ("Ignore the budget", 0),
                ("Cut safety features", 0)
            ]
        },
        {
            "q": "A client dislikes the concept. You:",
            "skill": "Communication",
            "options": [
                ("Discuss their needs and adjust", 3),
                ("Argue with them", 1),
                ("Ignore feedback", 0)
            ]
        },
        {
            "q": "A structure needs safety review. You:",
            "skill": "Technical Skill",
            "options": [
                ("Check codes and consult engineers", 3),
                ("Guess", 0),
                ("Skip review", 0)
            ]
        },
        {
            "q": "Your team is behind schedule. You:",
            "skill": "Leadership",
            "options": [
                ("Organize tasks and communicate deadlines", 3),
                ("Blame everyone", 1),
                ("Do nothing", 0)
            ]
        },
        {
            "q": "The site has environmental limits. You:",
            "skill": "Problem Solving",
            "options": [
                ("Design around the constraints", 3),
                ("Ignore regulations", 0),
                ("Complain only", 1)
            ]
        }
    ],

    "Psychologist": [
        {
            "q": "A client is nervous opening up. You:",
            "skill": "Communication",
            "options": [
                ("Create a safe and respectful space", 3),
                ("Rush them", 0),
                ("Dismiss their feelings", 0)
            ]
        },
        {
            "q": "A case is complex. You:",
            "skill": "Problem Solving",
            "options": [
                ("Assess carefully and plan support", 3),
                ("Guess quickly", 0),
                ("Ignore details", 0)
            ]
        },
        {
            "q": "You hear something concerning. You:",
            "skill": "Leadership",
            "options": [
                ("Follow ethical and safety procedures", 3),
                ("Ignore it", 0),
                ("Tell everyone", 0)
            ]
        },
        {
            "q": "Research changes best practices. You:",
            "skill": "Technical Skill",
            "options": [
                ("Study and update your approach", 3),
                ("Ignore new research", 0),
                ("Use old methods only", 1)
            ]
        },
        {
            "q": "A client misunderstands your advice. You:",
            "skill": "Communication",
            "options": [
                ("Clarify calmly", 3),
                ("Get frustrated", 1),
                ("Avoid explaining", 0)
            ]
        }
    ],

    "Veterinarian": [
        {
            "q": "A pet arrives with unclear symptoms. You:",
            "skill": "Technical Skill",
            "options": [
                ("Examine carefully and run tests", 3),
                ("Guess immediately", 0),
                ("Ignore symptoms", 0)
            ]
        },
        {
            "q": "An owner is scared. You:",
            "skill": "Communication",
            "options": [
                ("Explain the situation kindly", 3),
                ("Rush the conversation", 1),
                ("Ignore them", 0)
            ]
        },
        {
            "q": "Emergency surgery may be needed. You:",
            "skill": "Problem Solving",
            "options": [
                ("Assess risks and act responsibly", 3),
                ("Delay without reason", 0),
                ("Panic", 0)
            ]
        },
        {
            "q": "Your clinic is overloaded. You:",
            "skill": "Leadership",
            "options": [
                ("Prioritize urgent cases", 3),
                ("Ignore waiting patients", 0),
                ("Do everything randomly", 1)
            ]
        },
        {
            "q": "A treatment plan is expensive. You:",
            "skill": "Communication",
            "options": [
                ("Discuss options honestly", 3),
                ("Pressure the owner", 1),
                ("Say nothing", 0)
            ]
        }
    ],

    "Firefighter": [
        {
            "q": "A building fire is reported. You:",
            "skill": "Leadership",
            "options": [
                ("Follow command and safety protocols", 3),
                ("Rush in without gear", 0),
                ("Ignore orders", 0)
            ]
        },
        {
            "q": "A teammate is in danger. You:",
            "skill": "Problem Solving",
            "options": [
                ("Call it in and respond safely", 3),
                ("Panic", 0),
                ("Act alone recklessly", 1)
            ]
        },
        {
            "q": "Equipment fails during training. You:",
            "skill": "Technical Skill",
            "options": [
                ("Report and inspect it", 3),
                ("Ignore it", 0),
                ("Use it anyway", 0)
            ]
        },
        {
            "q": "A family is scared after an emergency. You:",
            "skill": "Communication",
            "options": [
                ("Calmly explain next steps", 3),
                ("Walk away", 0),
                ("Speak harshly", 1)
            ]
        },
        {
            "q": "The situation changes quickly. You:",
            "skill": "Problem Solving",
            "options": [
                ("Adapt while staying safe", 3),
                ("Freeze", 0),
                ("Guess blindly", 1)
            ]
        }
    ],

    "Content Creator": [
        {
            "q": "A video performs poorly. You:",
            "skill": "Problem Solving",
            "options": [
                ("Analyze what didn't work", 3),
                ("Quit creating", 0),
                ("Blame viewers", 1)
            ]
        },
        {
            "q": "Your audience gives feedback. You:",
            "skill": "Communication",
            "options": [
                ("Listen and improve content", 3),
                ("Argue with everyone", 1),
                ("Ignore all feedback", 0)
            ]
        },
        {
            "q": "A new editing tool appears. You:",
            "skill": "Technical Skill",
            "options": [
                ("Learn and test it", 3),
                ("Watch one video only", 1),
                ("Avoid it", 0)
            ]
        },
        {
            "q": "You need a posting schedule. You:",
            "skill": "Leadership",
            "options": [
                ("Plan consistently", 3),
                ("Post randomly", 1),
                ("Stop posting", 0)
            ]
        },
        {
            "q": "A trend appears in your niche. You:",
            "skill": "Problem Solving",
            "options": [
                ("Adapt it creatively", 3),
                ("Copy exactly", 1),
                ("Ignore every trend", 0)
            ]
        }
    ],
}

# ============================
# CAREER STORIES
# ============================

career_stories = {

    "Software Engineer": [
        "🚀 Day 1: A major bug crashes the company website.",
        "💻 Day 7: A teammate reviews your code and leaves comments.",
        "🛠 Day 14: Your company wants to adopt a new framework.",
        "⚡ Day 21: Customers complain the app is running slowly.",
        "👥 Day 30: Your team disagrees on the best solution."
    ],

    "Teacher": [
        "📚 Day 1: A student is struggling to keep up.",
        "🏫 Day 7: A disruption interrupts your class.",
        "📝 Day 14: You need to prepare next week's lessons.",
        "📊 Day 21: Exam scores have unexpectedly dropped.",
        "👨‍👩‍👧 Day 30: A parent requests a meeting."
    ],

    "Entrepreneur": [
        "💰 Day 1: Your startup begins losing money.",
        "🎤 Day 7: An investor rejects your pitch.",
        "🚀 Day 14: A competitor launches a similar product.",
        "⭐ Day 21: Customers leave important feedback.",
        "🏦 Day 30: Funding is running low."
    ],

    "Doctor": [
        "🚑 Day 1: An emergency patient arrives.",
        "🩺 Day 7: A diagnosis is unclear.",
        "🌙 Day 14: You're working a long shift.",
        "😟 Day 21: A patient is extremely anxious.",
        "⚠️ Day 30: You notice a possible medical error."
    ],

    "Lawyer": [
        "⚖️ Day 1: You begin preparing a major case.",
        "🏛 Day 7: Court proceedings become stressful.",
        "📂 Day 14: Important evidence is weak.",
        "🤔 Day 21: A client may not be telling the truth.",
        "🎯 Day 30: The opposition has a strong argument."
    ],

    "Designer": [
        "🎨 Day 1: A client dislikes your design.",
        "💡 Day 7: You hit a creative block.",
        "⏰ Day 14: A deadline is approaching fast.",
        "📝 Day 21: Feedback arrives from stakeholders.",
        "🖥 Day 30: A new design tool is released."
    ],

    "Pilot": [
        "✈️ Day 1: Bad weather threatens your flight.",
        "⚙️ Day 7: A system warning appears.",
        "🌎 Day 14: You're on a long international flight.",
        "🧭 Day 21: Navigation data looks incorrect.",
        "👨‍👩‍👧 Day 30: Passenger safety is your priority."
    ],

    "Chef": [
        "🍽 Day 1: Orders are flooding the kitchen.",
        "⭐ Day 7: A customer criticizes a dish.",
        "🔥 Day 14: The kitchen becomes chaotic.",
        "🥘 Day 21: A key ingredient is missing.",
        "👨‍🍳 Day 30: Your team needs coordination."
    ],

    "Data Scientist": [
        "📊 Day 1: Your dataset is full of errors.",
        "🤖 Day 7: Model accuracy is disappointing.",
        "📂 Day 14: Important data is missing.",
        "💼 Day 21: Executives need insights.",
        "🧠 Day 30: A new algorithm is trending."
    ],

    "Marketing Manager": [
        "📢 Day 1: A campaign is underperforming.",
        "🎯 Day 7: Your audience isn't well defined.",
        "💸 Day 14: Marketing budget gets cut.",
        "⭐ Day 21: Feedback on ads turns negative.",
        "🚀 Day 30: A competitor launches a huge campaign."
    ],

    "Cybersecurity Analyst": [
        "🛡 Day 1: Suspicious login attempts hit the company network.",
        "🎣 Day 7: An employee clicks a phishing email.",
        "🚨 Day 14: A server may be compromised.",
        "📢 Day 21: Leadership asks for a security update.",
        "🔐 Day 30: A ransomware warning appears."
    ],

    "AI Engineer": [
        "🤖 Day 1: Your AI model produces biased results.",
        "📉 Day 7: Model accuracy is lower than expected.",
        "💬 Day 14: A client wants a simple explanation of the AI.",
        "⚡ Day 21: The AI system is running too slowly.",
        "⚖️ Day 30: Your team debates AI ethics."
    ],

    "Game Developer": [
        "🎮 Day 1: Players say the game feels boring.",
        "🐛 Day 7: A major bug breaks gameplay.",
        "🎨 Day 14: The art and programming teams disagree.",
        "⏰ Day 21: Launch deadline is getting close.",
        "📱 Day 30: The game runs poorly on phones."
    ],

    "Architect": [
        "🏗 Day 1: Your design is over budget.",
        "🏠 Day 7: A client dislikes the first concept.",
        "📐 Day 14: The structure needs safety review.",
        "📅 Day 21: Your team is behind schedule.",
        "🌱 Day 30: The building site has environmental limits."
    ],

    "Psychologist": [
        "🧠 Day 1: A client is nervous about opening up.",
        "📋 Day 7: A case becomes more complex.",
        "⚠️ Day 14: You hear something concerning.",
        "📚 Day 21: New research changes best practices.",
        "💬 Day 30: A client misunderstands your advice."
    ],

    "Veterinarian": [
        "🐶 Day 1: A pet arrives with unclear symptoms.",
        "😟 Day 7: An owner is worried and scared.",
        "🏥 Day 14: Emergency surgery may be needed.",
        "📋 Day 21: The clinic is overloaded.",
        "💊 Day 30: A treatment plan is expensive."
    ],

    "Firefighter": [
        "🔥 Day 1: A building fire is reported.",
        "🚒 Day 7: A teammate may be in danger.",
        "🧯 Day 14: Equipment fails during training.",
        "👨‍👩‍👧 Day 21: A family is scared after an emergency.",
        "⚠️ Day 30: The situation changes quickly."
    ],

    "Content Creator": [
        "🎥 Day 1: A video performs poorly.",
        "💬 Day 7: Your audience gives feedback.",
        "🛠 Day 14: A new editing tool appears.",
        "📅 Day 21: You need a posting schedule.",
        "🔥 Day 30: A trend appears in your niche."
    ]
}


# ============================
# RANDOM CAREER SCENARIOS
# ============================

career_scenarios = {

    "Software Engineer": [
        "🚨 Production servers suddenly go down during peak traffic.",
        "🤖 Management wants AI added to the product next week.",
        "🔒 A security vulnerability is discovered.",
        "⚡ The app becomes extremely slow after an update.",
        "👨‍💻 A junior developer asks for your help."
    ],

    "Teacher": [
        "📚 A student is falling behind the class.",
        "🎓 A parent questions your teaching methods.",
        "🏫 The principal wants new classroom policies.",
        "📝 Exam scores unexpectedly drop.",
        "👨‍👩‍👧 Parent-teacher conferences begin."
    ],

    "Entrepreneur": [
        "💰 Investors suddenly pull out funding.",
        "🚀 A competitor launches a similar product.",
        "⭐ A customer review goes viral.",
        "📉 Revenue drops this month.",
        "🎤 You must pitch to investors tomorrow."
    ],

    "Doctor": [
        "🚑 Multiple emergency patients arrive at once.",
        "🩺 Test results are inconclusive.",
        "⚠️ A patient has an unexpected reaction.",
        "🌙 You're assigned an extra shift.",
        "💊 A medication shortage affects treatment."
    ],

    "Lawyer": [
        "⚖️ A high-pressure case lands on your desk.",
        "📂 A key document is missing before trial.",
        "🏛 The judge asks a difficult question.",
        "🤝 A client needs legal advice urgently.",
        "🎯 Opposing counsel reveals a surprise argument."
    ],

    "Designer": [
        "🎨 A client wants a complete redesign overnight.",
        "💡 Your creative direction is challenged.",
        "🖥 A design tool crashes before submission.",
        "📱 A mobile layout looks broken.",
        "📝 Stakeholders give conflicting feedback."
    ],

    "Pilot": [
        "✈️ Weather changes mid-flight.",
        "⚙️ A cockpit warning light turns on.",
        "🧭 Navigation data needs verification.",
        "🌎 A long route creates fatigue risk.",
        "🛬 The landing conditions become difficult."
    ],

    "Chef": [
        "🍽 A dinner rush overwhelms the kitchen.",
        "🥘 A key ingredient runs out.",
        "🔥 A mistake delays multiple orders.",
        "⭐ A food critic enters the restaurant.",
        "👨‍🍳 A teammate needs direction."
    ],

    "Data Scientist": [
        "📊 A dataset has thousands of missing values.",
        "🤖 Your model makes strange predictions.",
        "📉 Business leaders question the data.",
        "🧠 A new algorithm may improve results.",
        "💼 Executives need an insight by tomorrow."
    ],

    "Marketing Manager": [
        "📢 A campaign performs worse than expected.",
        "🎯 The target audience is unclear.",
        "💸 The ad budget gets cut.",
        "⭐ Customers react badly to an ad.",
        "🚀 A competitor dominates social media."
    ],

    "Cybersecurity Analyst": [
        "🛡 A suspicious IP address keeps accessing the network.",
        "🎣 Employees report phishing emails.",
        "🚨 A malware alert appears on a company laptop.",
        "🔐 Passwords may have been leaked.",
        "📢 Leadership wants a security report."
    ],

    "AI Engineer": [
        "🤖 Your AI model behaves unpredictably.",
        "📉 The training data creates poor results.",
        "⚖️ A fairness concern is raised.",
        "⚡ The AI system is too slow for users.",
        "💬 A customer asks if the AI can be trusted."
    ],

    "Game Developer": [
        "🎮 Players complain about boring gameplay.",
        "🐛 A bug ruins a boss fight.",
        "📱 Mobile users report lag.",
        "🎨 The art team wants a different style.",
        "🔥 Streamers start playing your game."
    ],

    "Architect": [
        "🏗 A design is too expensive to build.",
        "📐 A structure needs engineering approval.",
        "🏠 The client changes their mind.",
        "🌱 Environmental rules affect the design.",
        "📅 The project timeline gets shortened."
    ],

    "Psychologist": [
        "🧠 A client is afraid to talk openly.",
        "📋 A session reveals complex challenges.",
        "⚠️ Safety concerns appear.",
        "📚 New research changes your approach.",
        "💬 A client misunderstands your guidance."
    ],

    "Veterinarian": [
        "🐶 A pet arrives with strange symptoms.",
        "😟 An owner is extremely worried.",
        "🏥 A clinic emergency happens.",
        "💊 Medication options are limited.",
        "📋 Multiple animals need urgent care."
    ],

    "Firefighter": [
        "🔥 A fire spreads faster than expected.",
        "🚒 A team member needs backup.",
        "🧯 Equipment must be inspected quickly.",
        "👨‍👩‍👧 A family needs calming after an emergency.",
        "⚠️ Conditions change during a rescue."
    ],

    "Content Creator": [
        "🎥 A video flops unexpectedly.",
        "📈 A trend explodes overnight.",
        "💬 Followers ask for different content.",
        "🛠 Editing software fails before posting.",
        "🔥 A viral opportunity appears."
    ]
}


# ============================
# CAREER INFO
# ============================

career_info = {

    "Software Engineer": {
        "salary": "$120,000",
        "education": "Bachelor's Degree in Computer Science",
        "growth": "22%"
    },

    "Teacher": {
        "salary": "$65,000",
        "education": "Bachelor's Degree + Teaching License",
        "growth": "5%"
    },

    "Entrepreneur": {
        "salary": "Varies",
        "education": "No formal requirement",
        "growth": "Unlimited"
    },

    "Doctor": {
        "salary": "$220,000",
        "education": "Medical School + Residency",
        "growth": "3%"
    },

    "Lawyer": {
        "salary": "$135,000",
        "education": "Law Degree (JD)",
        "growth": "8%"
    },

    "Designer": {
        "salary": "$80,000",
        "education": "Design Degree or Portfolio",
        "growth": "13%"
    },

    "Pilot": {
        "salary": "$170,000",
        "education": "Flight Training + License",
        "growth": "6%"
    },

    "Chef": {
        "salary": "$60,000",
        "education": "Culinary School Optional",
        "growth": "15%"
    },

    "Data Scientist": {
        "salary": "$130,000",
        "education": "Bachelor's Degree in Data, CS, Math, or Statistics",
        "growth": "35%"
    },

    "Marketing Manager": {
        "salary": "$115,000",
        "education": "Bachelor's Degree in Marketing or Business",
        "growth": "10%"
    },

    "Cybersecurity Analyst": {
        "salary": "$120,000",
        "education": "Cybersecurity, Computer Science, or Certifications",
        "growth": "32%"
    },

    "AI Engineer": {
        "salary": "$150,000",
        "education": "Computer Science, AI, Machine Learning, or Data Science",
        "growth": "Very High"
    },

    "Game Developer": {
        "salary": "$95,000",
        "education": "Computer Science, Game Design, or Portfolio",
        "growth": "Moderate"
    },

    "Architect": {
        "salary": "$95,000",
        "education": "Architecture Degree + Licensure",
        "growth": "5%"
    },

    "Psychologist": {
        "salary": "$90,000",
        "education": "Graduate Degree in Psychology",
        "growth": "6%"
    },

    "Veterinarian": {
        "salary": "$120,000",
        "education": "Doctor of Veterinary Medicine",
        "growth": "20%"
    },

    "Firefighter": {
        "salary": "$60,000",
        "education": "Fire Academy + EMT Training",
        "growth": "4%"
    },

    "Content Creator": {
        "salary": "Varies",
        "education": "No formal requirement; portfolio and consistency matter",
        "growth": "High"
    }
}


# ============================
# INTERVIEW QUESTIONS
# ============================

career_interviews = {

    "Software Engineer": "Why do you want to become a Software Engineer?",
    "Teacher": "Why do you want to help students learn?",
    "Entrepreneur": "What problem would you like to solve with a business?",
    "Doctor": "Why do you want to help patients?",
    "Lawyer": "Why is justice important to you?",
    "Designer": "What inspires your creativity?",
    "Pilot": "What interests you about aviation?",
    "Chef": "Why do you enjoy cooking?",
    "Data Scientist": "What excites you about working with data?",
    "Marketing Manager": "How would you persuade people to try a new product?",
    "Cybersecurity Analyst": "Why do you want to protect people and companies from cyber threats?",
    "AI Engineer": "What excites you about building intelligent technology?",
    "Game Developer": "What kind of game would you love to create?",
    "Architect": "How would you design spaces that improve people's lives?",
    "Psychologist": "Why do you want to understand and support people's mental health?",
    "Veterinarian": "Why do you want to care for animals?",
    "Firefighter": "Why do you want to help people during emergencies?",
    "Content Creator": "What message or story do you want to share with the world?"
}


# ============================
# ADVICE AND ACHIEVEMENTS
# ============================

def get_coach_advice(score, career):

    if score >= 90:

        return f"""
You showed excellent potential for becoming a {career}.

Keep building your skills, creating projects, and gaining experience.
You're already demonstrating many of the qualities successful professionals in this field need.
"""

    elif score >= 70:

        return f"""
You have strong potential for becoming a {career}.

Focus on improving a few key skills and gaining more real-world experience.
With practice, you could be an excellent fit for this career.
"""

    elif score >= 50:

        return f"""
You show some strengths related to {career}, but there is room for improvement.

Consider learning more about the field, practicing relevant skills, and exploring beginner projects.
"""

    else:

        return f"""
This career may be challenging based on your current responses.

That doesn't mean it's impossible.
Try developing your skills and exploring related careers that match your strengths.
"""


def get_achievement(skills):

    if not skills:

        return (
            "🏅 Career Explorer",
            "Great job completing a simulation!"
        )

    strongest_skill = max(skills, key=skills.get)

    achievements = {

        "Technical Skill": (
            "🏆 Technical Expert",
            "You demonstrated strong technical thinking."
        ),

        "Leadership": (
            "👑 Future Leader",
            "You consistently made leadership-focused decisions."
        ),

        "Communication": (
            "🎤 Master Communicator",
            "You excel at collaboration and communication."
        ),

        "Problem Solving": (
            "🧩 Problem Solver",
            "You consistently found effective solutions."
        )
    }

    return achievements.get(
        strongest_skill,
        (
            "🏅 Career Explorer",
            "Great job completing a simulation!"
        )
    )

# ============================
# ROUTES
# ============================

@app.route("/set_name", methods=["POST"])
def set_name():

    name = request.form["player_name"].strip()

    players = load_players()

    if name not in players:

        players[name] = {
            "xp": 0,
            "careers_completed": 0,
            "achievements": []
        }

        save_players(players)

    session.clear()

    session["player_name"] = name
    session["total_xp"] = players[name]["xp"]

    return redirect(url_for("home"))


@app.route("/reset")
def reset():

    session.clear()

    return redirect(url_for("home"))


@app.route("/")
def home():

    stats = load_stats()
    stats["visits"] += 1
    save_stats(stats)
    visits = stats["visits"]

    xp = session.get("total_xp", 0)
    level = (xp // 100) + 1
    progress = xp % 100

    achievements = 0
    careers_completed = 0

    players = load_players()

    if session.get("player_name"):

        player = players.get(
            session["player_name"],
            {
                "xp": 0,
                "careers_completed": 0,
                "achievements": []
            }
        )

        achievements = len(
            player.get("achievements", [])
        )

        careers_completed = player.get(
            "careers_completed",
            0
        )

    total_players = len(players)

    total_achievements = 0
    total_careers_completed = 0

    for player in players.values():

        total_achievements += len(
            player.get("achievements", [])
        )

        total_careers_completed += player.get(
            "careers_completed",
            0
        )

    return render_template(
        "home.html",
        careers=careers.keys(),
        xp=xp,
        level=level,
        progress=progress,
        achievements=achievements,
        careers_completed=careers_completed,
        visits=visits,
        total_players=total_players,
        total_achievements=total_achievements,
        total_careers_completed=total_careers_completed
    )


@app.route("/dashboard")
def dashboard():

    if not session.get("player_name"):

        return redirect(url_for("home"))

    players = load_players()

    name = session["player_name"]

    player = players.get(
        name,
        {
            "xp": 0,
            "careers_completed": 0,
            "achievements": []
        }
    )

    xp = player.get("xp", 0)

    level = (xp // 100) + 1

    progress = xp % 100

    return render_template(
        "dashboard.html",
        name=name,
        xp=xp,
        level=level,
        progress=progress,
        careers_completed=player.get("careers_completed", 0),
        achievements=player.get("achievements", [])
    )


@app.route("/start/<career>")
def start(career):

    session["career"] = career
    session["index"] = 0
    session["score"] = 0

    if "total_xp" not in session:

        session["total_xp"] = 0

    if career in career_scenarios:

        session["scenario"] = random.choice(
            career_scenarios[career]
        )

    else:

        session["scenario"] = "A challenging day awaits."

    session["skills"] = {
        "Technical Skill": 0,
        "Leadership": 0,
        "Communication": 0,
        "Problem Solving": 0
    }

    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if not session.get("career"):

        return redirect(url_for("home"))

    career = session["career"]
    index = session.get("index", 0)
    score = session.get("score", 0)
    scenario = session.get("scenario")

    questions = careers[career]

    if request.method == "POST":

        answer_score = int(request.form["score"])

        score += answer_score

        total_xp = session.get("total_xp", 0)

        if answer_score == 3:

            total_xp += 15

        elif answer_score == 2:

            total_xp += 10

        else:

            total_xp += 3

        session["total_xp"] = total_xp

        players = load_players()

        name = session.get("player_name")

        if name:

            if name not in players:

                players[name] = {
                    "xp": 0,
                    "careers_completed": 0,
                    "achievements": []
                }

            players[name]["xp"] = total_xp

            save_players(players)

        skill = questions[index].get("skill")

        if skill:

            skills = session.get("skills")

            skills[skill] += answer_score

            session["skills"] = skills

        index += 1

        session["score"] = score
        session["index"] = index

    if index >= len(questions):

        return redirect(url_for("result"))

    return render_template(
        "quiz.html",
        q=questions[index],
        story=career_stories[career][index],
        scenario=scenario,
        index=index,
        total=len(questions),
        career=career
    )


@app.route("/result")
def result():

    if not session.get("career"):

        return redirect(url_for("home"))

    career = session["career"]
    score = session.get("score", 0)

    total = len(careers[career]) * 3
    percent = int((score / total) * 100)

    skills = session.get("skills", {})

    skill_percentages = {}

    highest_skill = max(skills.values()) if skills else 1

    if highest_skill == 0:

        highest_skill = 1

    for skill, value in skills.items():

        skill_percentages[skill] = int(
            (value / highest_skill) * 100
        )

    advice = get_coach_advice(percent, career)

    if percent >= 90:

        achievement_title, achievement_text = get_achievement(skills)

    elif percent >= 70:

        achievement_title = "⭐ Rising Professional"
        achievement_text = (
            "You demonstrated strong potential in this career."
        )

    elif percent >= 50:

        achievement_title = "📚 Career Explorer"
        achievement_text = (
            "You completed the simulation and learned valuable skills."
        )

    else:

        achievement_title = "🌱 Beginner Explorer"
        achievement_text = (
            "More practice is needed before earning a specialization badge."
        )

    players = load_players()

    name = session.get("player_name")

    if name:

        if name not in players:

            players[name] = {
                "xp": session.get("total_xp", 0),
                "careers_completed": 0,
                "achievements": []
            }

        if percent >= 50:

            players[name]["careers_completed"] += 1

        if percent >= 70:

            if achievement_title not in players[name]["achievements"]:

                players[name]["achievements"].append(
                    achievement_title
                )

        bonus_xp = 0

        if percent >= 90:

            bonus_xp = 100

        elif percent >= 70:

            bonus_xp = 50

        elif percent >= 50:

            bonus_xp = 25

        session["total_xp"] += bonus_xp

        players[name]["xp"] = session["total_xp"]

        save_players(players)

    xp = session.get("total_xp", 0)

    level = (xp // 100) + 1

    return render_template(
        "result.html",
        career=career,
        score=percent,
        skills=skill_percentages,
        info=career_info[career],
        advice=advice,
        xp=xp,
        level=level,
        achievement_title=achievement_title,
        achievement_text=achievement_text
    )


@app.route("/interview", methods=["GET", "POST"])
def interview():

    if not session.get("career"):

        return redirect(url_for("home"))

    career = session.get("career")
    scenario = session.get("scenario", "A challenging day awaits.")

    feedback = None

    if request.method == "POST":

        answer = request.form["answer"].lower()

        score = 0

        positive_words = [
            "learn",
            "help",
            "create",
            "solve",
            "build",
            "people",
            "technology",
            "improve",
            "teach",
            "passion",
            "protect",
            "design",
            "lead",
            "care",
            "support"
        ]

        for word in positive_words:

            if word in answer:

                score += 1

        if score >= 5:

            feedback = "🌟 Excellent answer! You showed strong motivation."

        elif score >= 3:

            feedback = "👍 Good answer! You demonstrated interest in the career."

        else:

            feedback = "💡 Try adding more detail about your goals and interests."

    return render_template(
        "interview.html",
        career=career,
        question=career_interviews[career],
        feedback=feedback,
        scenario=scenario
    )


if __name__ == "__main__":

    app.run(debug=True)