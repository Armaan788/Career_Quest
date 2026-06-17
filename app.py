from flask import Flask, render_template, redirect, url_for, request, session
import random
from database import get_db, initialize_database
from datetime import date

app = Flask(__name__)
app.secret_key = "career-quest-secret"
initialize_database()


# ============================
# SAVE SYSTEM
# ============================




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

careers["Artist"] = [
    {
        "q": "Your first concept feels weak. You:",
        "skill": "Problem Solving",
        "options": [
            ("Explore new ideas and references", 3),
            ("Submit it unchanged", 1),
            ("Give up", 0)
        ]
    },
    {
        "q": "Someone criticizes your artwork. You:",
        "skill": "Communication",
        "options": [
            ("Listen and consider useful feedback", 3),
            ("Argue immediately", 1),
            ("Stop creating", 0)
        ]
    },
    {
        "q": "You try an unfamiliar medium. You:",
        "skill": "Technical Skill",
        "options": [
            ("Practice and experiment with it", 3),
            ("Avoid learning it", 0),
            ("Use it without preparation", 1)
        ]
    },
    {
        "q": "An exhibition deadline is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Create a realistic completion plan", 3),
            ("Ignore the deadline", 0),
            ("Rush everything at the end", 1)
        ]
    },
    {
        "q": "Your work is not getting attention. You:",
        "skill": "Problem Solving",
        "options": [
            ("Improve your portfolio and presentation", 3),
            ("Copy another artist", 1),
            ("Quit sharing your work", 0)
        ]
    }
]

career_stories["Artist"] = [
    "Day 1: You begin planning an original artwork.",
    "Day 7: Your work receives challenging feedback.",
    "Day 14: You experiment with a new artistic medium.",
    "Day 21: An exhibition deadline approaches.",
    "Day 30: You prepare your portfolio for an audience."
]

career_scenarios["Artist"] = [
    "A gallery asks you to revise a piece.",
    "Your creative idea is not working as expected.",
    "An important art supply becomes unavailable.",
    "You are invited to join a public exhibition.",
    "A client requests major last-minute changes."
]

career_info["Artist"] = {
    "salary": "$56,260",
    "education": "Art degree optional; a strong portfolio is essential",
    "growth": "Little or no change"
}

career_interviews["Artist"] = (
    "What ideas or experiences inspire your artwork?"
)

careers["Artist"] = [
    {
        "q": "Your first concept feels weak. You:",
        "skill": "Problem Solving",
        "options": [
            ("Explore new ideas and references", 3),
            ("Submit it unchanged", 1),
            ("Give up", 0)
        ]
    },
    {
        "q": "Someone criticizes your artwork. You:",
        "skill": "Communication",
        "options": [
            ("Listen and consider useful feedback", 3),
            ("Argue immediately", 1),
            ("Stop creating", 0)
        ]
    },
    {
        "q": "You try an unfamiliar medium. You:",
        "skill": "Technical Skill",
        "options": [
            ("Practice and experiment with it", 3),
            ("Avoid learning it", 0),
            ("Use it without preparation", 1)
        ]
    },
    {
        "q": "An exhibition deadline is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Create a realistic completion plan", 3),
            ("Ignore the deadline", 0),
            ("Rush everything at the end", 1)
        ]
    },
    {
        "q": "Your work is not getting attention. You:",
        "skill": "Problem Solving",
        "options": [
            ("Improve your portfolio and presentation", 3),
            ("Copy another artist", 1),
            ("Quit sharing your work", 0)
        ]
    }
]

career_stories["Artist"] = [
    "Day 1: You begin planning an original artwork.",
    "Day 7: Your work receives challenging feedback.",
    "Day 14: You experiment with a new artistic medium.",
    "Day 21: An exhibition deadline approaches.",
    "Day 30: You prepare your portfolio for an audience."
]

career_scenarios["Artist"] = [
    "A gallery asks you to revise a piece.",
    "Your creative idea is not working as expected.",
    "An important art supply becomes unavailable.",
    "You are invited to join a public exhibition.",
    "A client requests major last-minute changes."
]

career_info["Artist"] = {
    "salary": "$56,260",
    "education": "Art degree optional; a strong portfolio is essential",
    "growth": "Little or no change"
}

career_interviews["Artist"] = (
    "What ideas or experiences inspire your artwork?"
)

careers["Animator"] = [
    {
        "q": "A character movement looks unnatural. You:",
        "skill": "Technical Skill",
        "options": [
            ("Study the motion and refine each frame", 3),
            ("Leave it unchanged", 1),
            ("Delete the project", 0)
        ]
    },
    {
        "q": "The director changes the scene. You:",
        "skill": "Communication",
        "options": [
            ("Confirm the changes and revise the animation", 3),
            ("Ignore the feedback", 0),
            ("Argue immediately", 1)
        ]
    },
    {
        "q": "Rendering is taking too long. You:",
        "skill": "Problem Solving",
        "options": [
            ("Optimize the scene and rendering settings", 3),
            ("Keep restarting randomly", 1),
            ("Give up", 0)
        ]
    },
    {
        "q": "Your team has a tight deadline. You:",
        "skill": "Leadership",
        "options": [
            ("Prioritize scenes and coordinate the workload", 3),
            ("Work without a plan", 1),
            ("Ignore the deadline", 0)
        ]
    },
    {
        "q": "A new animation tool is released. You:",
        "skill": "Technical Skill",
        "options": [
            ("Test it with a small project", 3),
            ("Avoid learning it", 0),
            ("Use it without understanding it", 1)
        ]
    }
]

career_stories["Animator"] = [
    "Day 1: You begin bringing a new character to life.",
    "Day 7: The director requests changes to an important scene.",
    "Day 14: A complex animation causes rendering problems.",
    "Day 21: Your team races toward a production deadline.",
    "Day 30: You experiment with a new animation tool."
]

career_scenarios["Animator"] = [
    "A character's movement does not look believable.",
    "Your animation software crashes before a review.",
    "A client requests a different visual style.",
    "A scene takes far too long to render.",
    "The sound and animation timing no longer match."
]

career_info["Animator"] = {
    "salary": "$99,800",
    "education": "Animation, art, or computer graphics degree; portfolio expected",
    "growth": "2%"
}

career_interviews["Animator"] = (
    "What kind of characters or worlds would you love to animate?"
)

careers["Fashion Designer"] = [
    {
        "q": "You need ideas for a new collection. You:",
        "skill": "Problem Solving",
        "options": [
            ("Research trends and develop an original theme", 3),
            ("Copy another collection", 1),
            ("Wait without creating", 0)
        ]
    },
    {
        "q": "A fabric behaves differently than expected. You:",
        "skill": "Technical Skill",
        "options": [
            ("Test alternatives and adjust the design", 3),
            ("Ignore the problem", 0),
            ("Use it without testing", 1)
        ]
    },
    {
        "q": "The production team misunderstands your sketch. You:",
        "skill": "Communication",
        "options": [
            ("Clarify the design and construction details", 3),
            ("Blame the team", 1),
            ("Say nothing", 0)
        ]
    },
    {
        "q": "A fashion show deadline is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Prioritize tasks and coordinate the team", 3),
            ("Change everything at the last moment", 1),
            ("Ignore the deadline", 0)
        ]
    },
    {
        "q": "Customers dislike part of the collection. You:",
        "skill": "Communication",
        "options": [
            ("Study their feedback and improve future designs", 3),
            ("Argue with customers", 1),
            ("Stop designing", 0)
        ]
    }
]

career_stories["Fashion Designer"] = [
    "Day 1: You begin creating a theme for a new collection.",
    "Day 7: A chosen fabric creates an unexpected problem.",
    "Day 14: The production team reviews your design sketches.",
    "Day 21: Your collection must be ready for a fashion show.",
    "Day 30: Customers and buyers respond to your work."
]

career_scenarios["Fashion Designer"] = [
    "A supplier cannot deliver your chosen fabric.",
    "A prototype does not fit as intended.",
    "A retailer requests changes to your collection.",
    "Your production budget is reduced.",
    "A new trend suddenly changes customer demand."
]

career_info["Fashion Designer"] = {
    "salary": "$80,690",
    "education": "Bachelor's degree in fashion design or fashion merchandising",
    "growth": "2%"
}

career_interviews["Fashion Designer"] = (
    "How would you create clothing that is original and practical?"
)

careers["Writer"] = [
    {
        "q": "You cannot find a strong opening. You:",
        "skill": "Problem Solving",
        "options": [
            ("Draft several openings and compare them", 3),
            ("Copy another writer", 1),
            ("Abandon the project", 0)
        ]
    },
    {
        "q": "An editor gives detailed criticism. You:",
        "skill": "Communication",
        "options": [
            ("Review the feedback and ask useful questions", 3),
            ("Reject every suggestion", 1),
            ("Ignore the editor", 0)
        ]
    },
    {
        "q": "Your research sources disagree. You:",
        "skill": "Technical Skill",
        "options": [
            ("Verify facts using reliable sources", 3),
            ("Choose one randomly", 1),
            ("Publish without checking", 0)
        ]
    },
    {
        "q": "A deadline is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Plan the remaining writing and editing work", 3),
            ("Keep rewriting the first paragraph", 1),
            ("Ignore the deadline", 0)
        ]
    },
    {
        "q": "Readers misunderstand your message. You:",
        "skill": "Communication",
        "options": [
            ("Clarify the language and structure", 3),
            ("Blame the readers", 1),
            ("Remove the entire piece", 0)
        ]
    }
]

careers["Photographer"] = [
    {
        "q": "A client gives you an unclear idea. You:",
        "skill": "Communication",
        "options": [
            ("Ask questions and confirm their vision", 3),
            ("Guess what they want", 1),
            ("Ignore their request", 0)
        ]
    },
    {
        "q": "The lighting at a shoot is difficult. You:",
        "skill": "Technical Skill",
        "options": [
            ("Adjust the camera and lighting setup", 3),
            ("Hope the photos work", 1),
            ("Cancel immediately", 0)
        ]
    },
    {
        "q": "Your camera stops working. You:",
        "skill": "Problem Solving",
        "options": [
            ("Troubleshoot it and use backup equipment", 3),
            ("Panic", 0),
            ("Continue without checking", 1)
        ]
    },
    {
        "q": "You have hundreds of photos to edit. You:",
        "skill": "Leadership",
        "options": [
            ("Organize and prioritize the best images", 3),
            ("Edit randomly", 1),
            ("Avoid the work", 0)
        ]
    },
    {
        "q": "A client dislikes the final photos. You:",
        "skill": "Communication",
        "options": [
            ("Listen and discuss reasonable revisions", 3),
            ("Argue with them", 1),
            ("Delete everything", 0)
        ]
    }
]

career_stories["Photographer"] = [
    "Day 1: A client explains their vision for a photo shoot.",
    "Day 7: Difficult lighting challenges your camera skills.",
    "Day 14: Your equipment develops a problem.",
    "Day 21: You begin selecting and editing the best images.",
    "Day 30: The client reviews your finished photographs."
]

career_scenarios["Photographer"] = [
    "Bad weather threatens an outdoor photo shoot.",
    "Your memory card is nearly full during an event.",
    "A client requests a completely different style.",
    "The location has poor lighting.",
    "You receive an opportunity to photograph a major event."
]

career_info["Photographer"] = {
    "salary": "$20.44 per hour",
    "education": "Photography training or degree optional; portfolio required",
    "growth": "2%"
}

career_interviews["Photographer"] = (
    "How would you use photography to tell a meaningful story?"
)

career_stories["Writer"] = [
    "Day 1: You begin developing an original story.",
    "Day 7: An editor sends detailed feedback.",
    "Day 14: Conflicting research needs verification.",
    "Day 21: Your publishing deadline approaches.",
    "Day 30: Readers respond to your finished work."
]

career_scenarios["Writer"] = [
    "Your story has a major plot problem.",
    "An editor requests a complete rewrite.",
    "An important source appears unreliable.",
    "You struggle to meet a publishing deadline.",
    "A reader interprets your message differently than intended."
]

career_info["Writer"] = {
    "salary": "$72,270",
    "education": "Bachelor's degree commonly preferred; strong writing portfolio",
    "growth": "4%"
}

career_interviews["Writer"] = (
    "What kinds of stories or ideas would you like to share?"
)

careers["Musician"] = [
    {
        "q": "A difficult section sounds inconsistent. You:",
        "skill": "Technical Skill",
        "options": [
            ("Practice it slowly and improve the technique", 3),
            ("Skip the section", 1),
            ("Stop rehearsing", 0)
        ]
    },
    {
        "q": "Your group disagrees about the arrangement. You:",
        "skill": "Communication",
        "options": [
            ("Discuss the ideas and test different versions", 3),
            ("Refuse to listen", 1),
            ("Leave the rehearsal", 0)
        ]
    },
    {
        "q": "Equipment fails before a performance. You:",
        "skill": "Problem Solving",
        "options": [
            ("Troubleshoot it and prepare a backup", 3),
            ("Panic", 0),
            ("Perform without checking anything", 1)
        ]
    },
    {
        "q": "A major performance is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Plan rehearsals and focus on weak sections", 3),
            ("Practice randomly", 1),
            ("Ignore preparation", 0)
        ]
    },
    {
        "q": "The audience reacts differently than expected. You:",
        "skill": "Communication",
        "options": [
            ("Learn from the response and adapt future performances", 3),
            ("Insult the audience", 0),
            ("Ignore every reaction", 1)
        ]
    }
]

career_stories["Musician"] = [
    "Day 1: You begin rehearsing a challenging new piece.",
    "Day 7: Your group debates how the music should sound.",
    "Day 14: Equipment fails shortly before a performance.",
    "Day 21: An important show is quickly approaching.",
    "Day 30: You perform and receive an unexpected response."
]

career_scenarios["Musician"] = [
    "A band member cannot attend an important rehearsal.",
    "Your instrument develops a problem before a show.",
    "A venue requests a shorter performance.",
    "You must learn a difficult piece quickly.",
    "A recording session is running behind schedule."
]

career_info["Musician"] = {
    "salary": "$42.45 per hour",
    "education": "Formal education varies; years of practice and performance experience",
    "growth": "1%"
}

career_interviews["Musician"] = (
    "What emotions or ideas would you want your music to express?"
)

careers["Museum Curator"] = [
    {
        "q": "A new artifact arrives with limited information. You:",
        "skill": "Technical Skill",
        "options": [
            ("Research its history and document carefully", 3),
            ("Guess its background", 1),
            ("Ignore the missing details", 0)
        ]
    },
    {
        "q": "Visitors seem confused by an exhibit. You:",
        "skill": "Communication",
        "options": [
            ("Improve labels and explanations", 3),
            ("Blame the visitors", 1),
            ("Do nothing", 0)
        ]
    },
    {
        "q": "An exhibit budget is reduced. You:",
        "skill": "Problem Solving",
        "options": [
            ("Redesign the exhibit within the budget", 3),
            ("Cancel everything immediately", 0),
            ("Spend anyway", 1)
        ]
    },
    {
        "q": "Your museum team is preparing a major opening. You:",
        "skill": "Leadership",
        "options": [
            ("Organize tasks and coordinate the team", 3),
            ("Let everyone figure it out alone", 1),
            ("Ignore the schedule", 0)
        ]
    },
    {
        "q": "A cultural item requires sensitive handling. You:",
        "skill": "Communication",
        "options": [
            ("Consult experts and respect the culture", 3),
            ("Display it without research", 0),
            ("Make assumptions", 1)
        ]
    }
]

career_stories["Museum Curator"] = [
    "Day 1: A new artifact arrives at the museum.",
    "Day 7: Visitors struggle to understand an exhibit.",
    "Day 14: Your exhibit budget is reduced.",
    "Day 21: A major museum opening is approaching.",
    "Day 30: A cultural item requires careful decision-making."
]

career_scenarios["Museum Curator"] = [
    "A donated artifact has an unclear history.",
    "An exhibit needs to be redesigned for younger visitors.",
    "A rare item must be preserved safely.",
    "A guest speaker cancels before an event.",
    "A community group raises concerns about an exhibit."
]

career_info["Museum Curator"] = {
    "salary": "$61,770",
    "education": "Master's degree in museum studies, history, art history, or related field",
    "growth": "6%"
}

career_interviews["Museum Curator"] = (
    "How would you help people understand history, art, or culture?"
)

careers["Civil Engineer"] = [
    {
        "q": "A bridge design has a safety concern. You:",
        "skill": "Technical Skill",
        "options": [
            ("Review calculations and fix the design", 3),
            ("Ignore the concern", 0),
            ("Guess a solution", 1)
        ]
    },
    {
        "q": "A city project is over budget. You:",
        "skill": "Problem Solving",
        "options": [
            ("Find safer, cost-effective design options", 3),
            ("Cut random materials", 1),
            ("Stop the project", 0)
        ]
    },
    {
        "q": "Residents are worried about construction. You:",
        "skill": "Communication",
        "options": [
            ("Explain the plan and listen to concerns", 3),
            ("Dismiss them", 0),
            ("Argue with everyone", 1)
        ]
    },
    {
        "q": "Your engineering team is behind schedule. You:",
        "skill": "Leadership",
        "options": [
            ("Organize tasks and update the timeline", 3),
            ("Blame the team", 1),
            ("Do nothing", 0)
        ]
    },
    {
        "q": "Heavy rain affects the worksite. You:",
        "skill": "Problem Solving",
        "options": [
            ("Adjust the plan and protect the site", 3),
            ("Ignore the weather", 0),
            ("Rush unsafely", 1)
        ]
    }
]

career_stories["Civil Engineer"] = [
    "Day 1: A bridge design needs a careful safety review.",
    "Day 7: A city project becomes too expensive.",
    "Day 14: Residents ask questions about construction.",
    "Day 21: Your team falls behind schedule.",
    "Day 30: Weather creates problems at the worksite."
]

career_scenarios["Civil Engineer"] = [
    "A road design must handle heavier traffic.",
    "A construction site has drainage problems.",
    "A city asks you to improve an old bridge.",
    "A public meeting becomes tense.",
    "A project needs safer materials."
]

career_info["Civil Engineer"] = {
    "salary": "$99,590",
    "education": "Bachelor's degree in civil engineering; licensure may be required",
    "growth": "5%"
}

career_interviews["Civil Engineer"] = (
    "How would you design infrastructure that keeps communities safe?"
)


careers["Mechanical Engineer"] = [
    {
        "q": "A machine prototype keeps failing. You:",
        "skill": "Problem Solving",
        "options": [
            ("Test the parts and redesign the weak point", 3),
            ("Ignore the failure", 0),
            ("Replace parts randomly", 1)
        ]
    },
    {
        "q": "Your design needs better efficiency. You:",
        "skill": "Technical Skill",
        "options": [
            ("Analyze performance and improve the system", 3),
            ("Guess what might help", 1),
            ("Do nothing", 0)
        ]
    },
    {
        "q": "Manufacturing reports a problem. You:",
        "skill": "Communication",
        "options": [
            ("Work with them to understand the issue", 3),
            ("Blame manufacturing", 1),
            ("Ignore their report", 0)
        ]
    },
    {
        "q": "The project has multiple moving parts. You:",
        "skill": "Leadership",
        "options": [
            ("Coordinate testing, design, and production", 3),
            ("Let everyone work separately", 1),
            ("Avoid making decisions", 0)
        ]
    },
    {
        "q": "A new simulation tool is available. You:",
        "skill": "Technical Skill",
        "options": [
            ("Use it to test and improve the design", 3),
            ("Avoid learning it", 0),
            ("Use it without checking results", 1)
        ]
    }
]

career_stories["Mechanical Engineer"] = [
    "Day 1: A machine prototype fails during testing.",
    "Day 7: Your design needs to become more efficient.",
    "Day 14: Manufacturing reports a production issue.",
    "Day 21: You coordinate a complex engineering project.",
    "Day 30: A new simulation tool could improve your work."
]

career_scenarios["Mechanical Engineer"] = [
    "A device overheats during testing.",
    "A prototype part wears out too quickly.",
    "A machine needs to use less energy.",
    "A manufacturing process creates defects.",
    "A client asks for a lighter design."
]

career_info["Mechanical Engineer"] = {
    "salary": "$102,320",
    "education": "Bachelor's degree in mechanical engineering or mechanical engineering technology",
    "growth": "9%"
}

career_interviews["Mechanical Engineer"] = (
    "What kind of machine, tool, or system would you want to design?"
)

careers["Electrical Engineer"] = [
    {
        "q": "A circuit is not working correctly. You:",
        "skill": "Technical Skill",
        "options": [
            ("Test the circuit and trace the fault", 3),
            ("Replace random parts", 1),
            ("Ignore the issue", 0)
        ]
    },
    {
        "q": "A device uses too much power. You:",
        "skill": "Problem Solving",
        "options": [
            ("Redesign the system for better efficiency", 3),
            ("Accept the waste", 1),
            ("Remove important features", 0)
        ]
    },
    {
        "q": "A teammate misunderstands your wiring plan. You:",
        "skill": "Communication",
        "options": [
            ("Explain the design clearly and update diagrams", 3),
            ("Blame them", 1),
            ("Say nothing", 0)
        ]
    },
    {
        "q": "A project has strict safety rules. You:",
        "skill": "Leadership",
        "options": [
            ("Make sure the team follows safe procedures", 3),
            ("Skip safety checks", 0),
            ("Rush the work", 1)
        ]
    },
    {
        "q": "Testing reveals signal interference. You:",
        "skill": "Problem Solving",
        "options": [
            ("Analyze the source and adjust the design", 3),
            ("Ignore the signal problem", 0),
            ("Guess without testing", 1)
        ]
    }
]

career_stories["Electrical Engineer"] = [
    "Day 1: A circuit fails during testing.",
    "Day 7: Your device needs better power efficiency.",
    "Day 14: A teammate needs clarification on your wiring plan.",
    "Day 21: The project must meet strict safety rules.",
    "Day 30: Signal interference appears during final testing."
]

career_scenarios["Electrical Engineer"] = [
    "A circuit board overheats.",
    "A sensor gives unstable readings.",
    "A power system needs a safer design.",
    "A prototype fails inspection.",
    "A client asks for longer battery life."
]

career_info["Electrical Engineer"] = {
    "salary": "$111,910",
    "education": "Bachelor's degree in electrical engineering or related field",
    "growth": "9%"
}

career_interviews["Electrical Engineer"] = (
    "What kind of electronic system would you want to design or improve?"
)


careers["Robotics Engineer"] = [
    {
        "q": "A robot moves unpredictably. You:",
        "skill": "Technical Skill",
        "options": [
            ("Check the sensors, code, and mechanical parts", 3),
            ("Let it keep running", 0),
            ("Guess one random fix", 1)
        ]
    },
    {
        "q": "The robot cannot complete its task. You:",
        "skill": "Problem Solving",
        "options": [
            ("Break the problem into hardware and software tests", 3),
            ("Start over immediately", 1),
            ("Ignore the failure", 0)
        ]
    },
    {
        "q": "Software and hardware teammates disagree. You:",
        "skill": "Communication",
        "options": [
            ("Help both sides understand the full system", 3),
            ("Pick sides instantly", 1),
            ("Avoid the discussion", 0)
        ]
    },
    {
        "q": "A demo is coming soon. You:",
        "skill": "Leadership",
        "options": [
            ("Prioritize core features and test carefully", 3),
            ("Add risky new features", 1),
            ("Do no testing", 0)
        ]
    },
    {
        "q": "A robot must work safely near people. You:",
        "skill": "Problem Solving",
        "options": [
            ("Design safeguards and test edge cases", 3),
            ("Assume it will be fine", 0),
            ("Disable warnings", 1)
        ]
    }
]

career_stories["Robotics Engineer"] = [
    "Day 1: A robot moves in an unexpected way.",
    "Day 7: The robot struggles to complete its task.",
    "Day 14: Hardware and software teammates disagree.",
    "Day 21: A live robotics demo is approaching.",
    "Day 30: The robot must operate safely around people."
]

career_scenarios["Robotics Engineer"] = [
    "A sensor gives the robot bad information.",
    "A robot arm misses its target.",
    "The control software reacts too slowly.",
    "A demo robot stops working minutes before presentation.",
    "A robot needs better safety limits."
]

career_info["Robotics Engineer"] = {
    "salary": "$102,320",
    "education": "Bachelor's degree in mechanical, electrical, robotics, or computer engineering",
    "growth": "9%"
}

career_interviews["Robotics Engineer"] = (
    "What kind of robot would you build to help people?"
)

careers["Nurse"] = [
    {
        "q": "A patient reports new symptoms. You:",
        "skill": "Technical Skill",
        "options": [
            ("Assess carefully and report changes", 3),
            ("Ignore the symptoms", 0),
            ("Guess what is happening", 1)
        ]
    },
    {
        "q": "A family member is worried. You:",
        "skill": "Communication",
        "options": [
            ("Explain calmly and answer questions", 3),
            ("Rush away", 1),
            ("Dismiss their concern", 0)
        ]
    },
    {
        "q": "Several patients need help at once. You:",
        "skill": "Leadership",
        "options": [
            ("Prioritize urgent needs and coordinate care", 3),
            ("Help randomly", 1),
            ("Do nothing", 0)
        ]
    },
    {
        "q": "Medication instructions are unclear. You:",
        "skill": "Problem Solving",
        "options": [
            ("Verify the order before acting", 3),
            ("Guess the dosage", 0),
            ("Skip the check", 1)
        ]
    },
    {
        "q": "A patient is scared before treatment. You:",
        "skill": "Communication",
        "options": [
            ("Comfort them and explain what to expect", 3),
            ("Tell them to stop worrying", 1),
            ("Ignore their fear", 0)
        ]
    }
]

career_stories["Nurse"] = [
    "Day 1: A patient reports new symptoms.",
    "Day 7: A worried family member asks for help.",
    "Day 14: Several patients need attention at once.",
    "Day 21: Medication instructions need verification.",
    "Day 30: A patient feels scared before treatment."
]

career_scenarios["Nurse"] = [
    "A patient suddenly feels worse.",
    "A family asks for a clear update.",
    "The unit becomes very busy.",
    "A chart has missing information.",
    "A patient needs reassurance before a procedure."
]

career_info["Nurse"] = {
    "salary": "$93,600",
    "education": "Nursing degree or diploma and state licensure",
    "growth": "5%"
}

career_interviews["Nurse"] = (
    "Why do you want to care for people during difficult moments?"
)


careers["Physical Therapist"] = [
    {
        "q": "A patient struggles with an exercise. You:",
        "skill": "Communication",
        "options": [
            ("Encourage them and adjust the exercise safely", 3),
            ("Push them too hard", 0),
            ("Ignore their struggle", 1)
        ]
    },
    {
        "q": "Recovery is slower than expected. You:",
        "skill": "Problem Solving",
        "options": [
            ("Reassess progress and update the plan", 3),
            ("Keep everything the same", 1),
            ("Give up on the plan", 0)
        ]
    },
    {
        "q": "You create a treatment plan. You:",
        "skill": "Technical Skill",
        "options": [
            ("Use assessment results and patient goals", 3),
            ("Copy a random plan", 1),
            ("Avoid planning", 0)
        ]
    },
    {
        "q": "A clinic schedule is crowded. You:",
        "skill": "Leadership",
        "options": [
            ("Manage time and keep care organized", 3),
            ("Rush every patient", 1),
            ("Ignore the schedule", 0)
        ]
    },
    {
        "q": "A patient loses motivation. You:",
        "skill": "Communication",
        "options": [
            ("Explain progress and encourage small wins", 3),
            ("Criticize them", 0),
            ("Say nothing", 1)
        ]
    }
]

career_stories["Physical Therapist"] = [
    "Day 1: A patient struggles with a movement exercise.",
    "Day 7: Recovery is slower than expected.",
    "Day 14: You build a personalized treatment plan.",
    "Day 21: The clinic schedule becomes crowded.",
    "Day 30: A patient needs motivation to keep going."
]

career_scenarios["Physical Therapist"] = [
    "A patient has pain during an exercise.",
    "A recovery goal needs to be adjusted.",
    "A patient wants to return to sports quickly.",
    "A clinic day becomes overloaded.",
    "A patient feels frustrated by slow progress."
]

career_info["Physical Therapist"] = {
    "salary": "$101,020",
    "education": "Doctor of Physical Therapy degree and state licensure",
    "growth": "11%"
}

career_interviews["Physical Therapist"] = (
    "How would you help someone recover strength and confidence?"
)

careers["Accountant"] = [
    {
        "q": "A financial report has mismatched numbers. You:",
        "skill": "Technical Skill",
        "options": [
            ("Review the records and find the error", 3),
            ("Guess the missing amount", 1),
            ("Ignore the mismatch", 0)
        ]
    },
    {
        "q": "A client does not understand their budget. You:",
        "skill": "Communication",
        "options": [
            ("Explain the numbers clearly", 3),
            ("Use confusing terms", 1),
            ("Avoid the question", 0)
        ]
    },
    {
        "q": "Tax rules change. You:",
        "skill": "Technical Skill",
        "options": [
            ("Study the update and apply it correctly", 3),
            ("Use old rules", 0),
            ("Guess what changed", 1)
        ]
    },
    {
        "q": "A deadline is approaching. You:",
        "skill": "Leadership",
        "options": [
            ("Organize documents and finish on schedule", 3),
            ("Wait until the last minute", 1),
            ("Miss the deadline", 0)
        ]
    },
    {
        "q": "A company is spending too much. You:",
        "skill": "Problem Solving",
        "options": [
            ("Analyze costs and suggest improvements", 3),
            ("Cut random expenses", 1),
            ("Ignore the issue", 0)
        ]
    }
]

career_stories["Accountant"] = [
    "Day 1: A financial report does not balance.",
    "Day 7: A client needs help understanding their budget.",
    "Day 14: New tax rules affect your work.",
    "Day 21: A major filing deadline approaches.",
    "Day 30: A company asks how to reduce overspending."
]

career_scenarios["Accountant"] = [
    "A receipt is missing from a financial record.",
    "A client asks for a budget summary.",
    "A tax deadline is coming soon.",
    "An audit reveals a possible error.",
    "A company needs help tracking expenses."
]

career_info["Accountant"] = {
    "salary": "$81,680",
    "education": "Bachelor's degree in accounting or related field",
    "growth": "5%"
}

career_interviews["Accountant"] = (
    "How would you help people or businesses make smarter financial decisions?"
)


careers["Financial Analyst"] = [
    {
        "q": "An investment looks risky. You:",
        "skill": "Problem Solving",
        "options": [
            ("Analyze the data and explain the risk", 3),
            ("Recommend it without checking", 0),
            ("Guess based on hype", 1)
        ]
    },
    {
        "q": "Market data changes suddenly. You:",
        "skill": "Technical Skill",
        "options": [
            ("Update your model and review assumptions", 3),
            ("Ignore the new data", 0),
            ("Panic and start over", 1)
        ]
    },
    {
        "q": "A client asks what your numbers mean. You:",
        "skill": "Communication",
        "options": [
            ("Explain the insight in simple terms", 3),
            ("Overload them with jargon", 1),
            ("Avoid explaining", 0)
        ]
    },
    {
        "q": "Your team must present recommendations. You:",
        "skill": "Leadership",
        "options": [
            ("Organize findings and guide the presentation", 3),
            ("Let everyone improvise", 1),
            ("Skip preparation", 0)
        ]
    },
    {
        "q": "Two financial strategies both look good. You:",
        "skill": "Problem Solving",
        "options": [
            ("Compare risks, returns, and goals", 3),
            ("Pick randomly", 0),
            ("Choose the flashier option", 1)
        ]
    }
]

career_stories["Financial Analyst"] = [
    "Day 1: You evaluate a risky investment.",
    "Day 7: Market data changes quickly.",
    "Day 14: A client asks for a clear explanation.",
    "Day 21: Your team prepares financial recommendations.",
    "Day 30: Two strategies compete for attention."
]

career_scenarios["Financial Analyst"] = [
    "A company's earnings report surprises investors.",
    "A client wants to compare investment choices.",
    "Market prices change before your presentation.",
    "A spreadsheet model gives strange results.",
    "A business asks whether expansion is affordable."
]

career_info["Financial Analyst"] = {
    "salary": "$101,350",
    "education": "Bachelor's degree in finance, economics, accounting, or related field",
    "growth": "6%"
}

career_interviews["Financial Analyst"] = (
    "How would you use data to make better money decisions?"
)


careers["Project Manager"] = [
    {
        "q": "A project falls behind schedule. You:",
        "skill": "Leadership",
        "options": [
            ("Reorganize tasks and communicate the plan", 3),
            ("Blame the team", 1),
            ("Ignore the delay", 0)
        ]
    },
    {
        "q": "Team members disagree on priorities. You:",
        "skill": "Communication",
        "options": [
            ("Clarify goals and help the team align", 3),
            ("Let the conflict grow", 0),
            ("Pick randomly", 1)
        ]
    },
    {
        "q": "The budget is reduced. You:",
        "skill": "Problem Solving",
        "options": [
            ("Adjust scope and protect key goals", 3),
            ("Cut important work blindly", 1),
            ("Keep spending normally", 0)
        ]
    },
    {
        "q": "A stakeholder asks for a major change. You:",
        "skill": "Communication",
        "options": [
            ("Discuss impact on time, cost, and goals", 3),
            ("Say yes without reviewing", 1),
            ("Ignore the request", 0)
        ]
    },
    {
        "q": "A launch is coming soon. You:",
        "skill": "Leadership",
        "options": [
            ("Check risks, deadlines, and team readiness", 3),
            ("Hope everything works", 1),
            ("Stop tracking progress", 0)
        ]
    }
]

career_stories["Project Manager"] = [
    "Day 1: A project begins falling behind schedule.",
    "Day 7: Team members disagree about priorities.",
    "Day 14: The project budget is reduced.",
    "Day 21: A stakeholder requests a major change.",
    "Day 30: Launch day is quickly approaching."
]

career_scenarios["Project Manager"] = [
    "A key team member is unavailable.",
    "A deadline moves up unexpectedly.",
    "A stakeholder changes the project requirements.",
    "The project budget becomes smaller.",
    "The team needs a clearer plan."
]

career_info["Project Manager"] = {
    "salary": "$101,190",
    "education": "Bachelor's degree often preferred; project management experience or certification helpful",
    "growth": "9%"
}

career_interviews["Project Manager"] = (
    "How would you keep a team focused and organized during a difficult project?"
)

careers["Social Worker"] = [
    {
        "q": "A family needs urgent support. You:",
        "skill": "Communication",
        "options": [
            ("Listen carefully and connect them with help", 3),
            ("Rush the conversation", 1),
            ("Ignore their needs", 0)
        ]
    },
    {
        "q": "A case has many complicated details. You:",
        "skill": "Problem Solving",
        "options": [
            ("Assess the situation and plan next steps", 3),
            ("Guess quickly", 1),
            ("Skip the details", 0)
        ]
    },
    {
        "q": "You notice a safety concern. You:",
        "skill": "Leadership",
        "options": [
            ("Follow proper safety and reporting procedures", 3),
            ("Ignore it", 0),
            ("Tell random people", 1)
        ]
    },
    {
        "q": "A client does not trust the process. You:",
        "skill": "Communication",
        "options": [
            ("Build trust through respect and honesty", 3),
            ("Pressure them", 1),
            ("Stop helping", 0)
        ]
    },
    {
        "q": "Resources are limited. You:",
        "skill": "Problem Solving",
        "options": [
            ("Prioritize needs and find available services", 3),
            ("Give up immediately", 0),
            ("Choose randomly", 1)
        ]
    }
]

career_stories["Social Worker"] = [
    "Day 1: A family asks for urgent support.",
    "Day 7: A case becomes more complicated.",
    "Day 14: You notice a possible safety concern.",
    "Day 21: A client struggles to trust the process.",
    "Day 30: Limited resources make support harder."
]

career_scenarios["Social Worker"] = [
    "A family needs housing support.",
    "A client is nervous about asking for help.",
    "A school reports a concerning situation.",
    "A community program has limited funding.",
    "A client needs multiple services at once."
]

career_info["Social Worker"] = {
    "salary": "$61,330",
    "education": "Bachelor's or master's degree in social work; license may be required",
    "growth": "6%"
}

career_interviews["Social Worker"] = (
    "Why do you want to help people and communities through difficult situations?"
)



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

def get_player(name):

    conn = get_db()

    player = conn.execute(
        "SELECT * FROM players WHERE name = ?",
        (name,)
    ).fetchone()

    conn.close()

    return player


def create_player(name):

    conn = get_db()

    conn.execute(
        "INSERT INTO players (name, xp, careers_completed) VALUES (?, ?, ?)",
        (name, 0, 0)
    )

    conn.commit()

    conn.close()


def update_player_xp(name, xp):

    conn = get_db()

    conn.execute(
        "UPDATE players SET xp = ? WHERE name = ?",
        (xp, name)
    )

    conn.commit()

    conn.close()


def update_player_progress(name, xp, careers_completed):

    conn = get_db()

    conn.execute(
        "UPDATE players SET xp = ?, careers_completed = ? WHERE name = ?",
        (xp, careers_completed, name)
    )

    conn.commit()

    conn.close()

# ============================
# ROUTES
# ============================

@app.route("/set_name", methods=["POST"])
def set_name():

    name = request.form["player_name"].strip()

    player = get_player(name)

    if not player:

        create_player(name)

        player = get_player(name)

    update_login_streak(name)

    player = get_player(name)

    session.clear()

    session["player_name"] = name

    session["total_xp"] = player["xp"]

    return redirect(url_for("home"))

def get_all_players():

    conn = get_db()

    players = conn.execute(
        "SELECT * FROM players"
    ).fetchall()

    conn.close()

    return players

def increment_visits():

    conn = get_db()

    conn.execute(
        "UPDATE site_stats SET visits = visits + 1 WHERE id = 1"
    )

    visits = conn.execute(
        "SELECT visits FROM site_stats WHERE id = 1"
    ).fetchone()["visits"]

    conn.commit()
    conn.close()

    return visits

def get_player_achievements(name):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT title
        FROM achievements
        WHERE player_name = ?
        ORDER BY title
        """,
        (name,)
    ).fetchall()

    conn.close()

    return [row["title"] for row in rows]


def add_player_achievement(name, title):

    conn = get_db()

    conn.execute(
        """
        INSERT OR IGNORE INTO achievements
        (player_name, title)
        VALUES (?, ?)
        """,
        (name, title)
    )

    conn.commit()
    conn.close()


def get_total_achievements():

    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) AS total FROM achievements"
    ).fetchone()["total"]

    conn.close()

    return total

career_categories = {
    "Art": [
        "Designer",
        "Artist",
        "Photographer",
        "Animator",
        "Fashion Designer"
    ],

    "Culture": [
        "Chef",
        "Content Creator",
        "Writer",
        "Musician",
        "Museum Curator"
    ],

    "Engineering": [
        "Architect",
        "Civil Engineer",
        "Mechanical Engineer",
        "Electrical Engineer",
        "Robotics Engineer"
    ],

    "Health": [
        "Doctor",
        "Psychologist",
        "Veterinarian",
        "Nurse",
        "Physical Therapist"
    ],

    "Service": [
        "Teacher",
        "Lawyer",
        "Firefighter",
        "Pilot",
        "Social Worker"
    ],

    "Business": [
        "Entrepreneur",
        "Marketing Manager",
        "Accountant",
        "Financial Analyst",
        "Project Manager"
    ],

    "Technology": [
        "Software Engineer",
        "Data Scientist",
        "Cybersecurity Analyst",
        "AI Engineer",
        "Game Developer"
    ]
}

career_match_questions = [
    {
        "question": "Which area sounds most exciting to explore?",
        "options": [
            {
                "text": "Art and visual creativity",
                "careers": [
                    "Designer",
                    "Artist",
                    "Photographer",
                    "Animator",
                    "Fashion Designer"
                ]
            },
            {
                "text": "Culture, food, stories, and performance",
                "careers": [
                    "Chef",
                    "Content Creator",
                    "Writer",
                    "Musician",
                    "Museum Curator"
                ]
            },
            {
                "text": "Engineering and building real-world systems",
                "careers": [
                    "Architect",
                    "Civil Engineer",
                    "Mechanical Engineer",
                    "Electrical Engineer",
                    "Robotics Engineer"
                ]
            },
            {
                "text": "Health and helping people recover",
                "careers": [
                    "Doctor",
                    "Psychologist",
                    "Veterinarian",
                    "Nurse",
                    "Physical Therapist"
                ]
            },
            {
                "text": "Service, safety, teaching, and guidance",
                "careers": [
                    "Teacher",
                    "Lawyer",
                    "Firefighter",
                    "Pilot",
                    "Social Worker"
                ]
            },
            {
                "text": "Business, money, and leadership",
                "careers": [
                    "Entrepreneur",
                    "Marketing Manager",
                    "Accountant",
                    "Financial Analyst",
                    "Project Manager"
                ]
            },
            {
                "text": "Technology, data, games, and AI",
                "careers": [
                    "Software Engineer",
                    "Data Scientist",
                    "Cybersecurity Analyst",
                    "AI Engineer",
                    "Game Developer"
                ]
            }
        ]
    },
    {
        "question": "What kind of work feels most natural to you?",
        "options": [
            {
                "text": "Making things look or feel beautiful",
                "careers": [
                    "Designer",
                    "Artist",
                    "Fashion Designer",
                    "Animator"
                ]
            },
            {
                "text": "Explaining ideas to people",
                "careers": [
                    "Teacher",
                    "Writer",
                    "Lawyer",
                    "Marketing Manager"
                ]
            },
            {
                "text": "Solving technical problems",
                "careers": [
                    "Software Engineer",
                    "Mechanical Engineer",
                    "Electrical Engineer",
                    "Robotics Engineer"
                ]
            },
            {
                "text": "Caring for people or animals",
                "careers": [
                    "Doctor",
                    "Nurse",
                    "Veterinarian",
                    "Physical Therapist"
                ]
            },
            {
                "text": "Leading plans and decisions",
                "careers": [
                    "Entrepreneur",
                    "Project Manager",
                    "Financial Analyst",
                    "Architect"
                ]
            }
        ]
    },
    {
        "question": "Which challenge would you choose?",
        "options": [
            {
                "text": "Create a new character, image, or design",
                "careers": [
                    "Artist",
                    "Animator",
                    "Photographer",
                    "Designer"
                ]
            },
            {
                "text": "Build a safer bridge, machine, or robot",
                "careers": [
                    "Civil Engineer",
                    "Mechanical Engineer",
                    "Electrical Engineer",
                    "Robotics Engineer"
                ]
            },
            {
                "text": "Help someone through a difficult moment",
                "careers": [
                    "Psychologist",
                    "Social Worker",
                    "Nurse",
                    "Doctor"
                ]
            },
            {
                "text": "Protect people from danger",
                "careers": [
                    "Firefighter",
                    "Cybersecurity Analyst",
                    "Pilot",
                    "Lawyer"
                ]
            },
            {
                "text": "Study numbers and make smart decisions",
                "careers": [
                    "Accountant",
                    "Financial Analyst",
                    "Data Scientist",
                    "Marketing Manager"
                ]
            }
        ]
    },
    {
        "question": "Where would you rather spend your day?",
        "options": [
            {
                "text": "A studio, gallery, kitchen, or stage",
                "careers": [
                    "Artist",
                    "Chef",
                    "Musician",
                    "Museum Curator",
                    "Photographer"
                ]
            },
            {
                "text": "A hospital, clinic, or care setting",
                "careers": [
                    "Doctor",
                    "Nurse",
                    "Physical Therapist",
                    "Psychologist",
                    "Veterinarian"
                ]
            },
            {
                "text": "A lab, workshop, job site, or design room",
                "careers": [
                    "Architect",
                    "Civil Engineer",
                    "Mechanical Engineer",
                    "Electrical Engineer",
                    "Robotics Engineer"
                ]
            },
            {
                "text": "An office, meeting room, or business setting",
                "careers": [
                    "Entrepreneur",
                    "Accountant",
                    "Financial Analyst",
                    "Project Manager",
                    "Marketing Manager"
                ]
            },
            {
                "text": "A computer, control room, or creative tech space",
                "careers": [
                    "Software Engineer",
                    "AI Engineer",
                    "Game Developer",
                    "Data Scientist",
                    "Cybersecurity Analyst"
                ]
            }
        ]
    },
    {
        "question": "What kind of impact do you want to make?",
        "options": [
            {
                "text": "Inspire people creatively",
                "careers": [
                    "Content Creator",
                    "Writer",
                    "Musician",
                    "Fashion Designer",
                    "Animator"
                ]
            },
            {
                "text": "Improve health and well-being",
                "careers": [
                    "Doctor",
                    "Nurse",
                    "Physical Therapist",
                    "Psychologist",
                    "Social Worker"
                ]
            },
            {
                "text": "Make communities safer and stronger",
                "careers": [
                    "Teacher",
                    "Lawyer",
                    "Firefighter",
                    "Civil Engineer",
                    "Pilot"
                ]
            },
            {
                "text": "Build useful technology",
                "careers": [
                    "Software Engineer",
                    "AI Engineer",
                    "Robotics Engineer",
                    "Electrical Engineer",
                    "Game Developer"
                ]
            },
            {
                "text": "Help organizations grow",
                "careers": [
                    "Entrepreneur",
                    "Marketing Manager",
                    "Accountant",
                    "Financial Analyst",
                    "Project Manager"
                ]
            }
        ]
    }
]

def get_leaderboard_data():

    conn = get_db()

    players = conn.execute("""
        SELECT
            p.name,
            p.xp,
            p.careers_completed,
            COUNT(a.title) AS achievements
        FROM players p
        LEFT JOIN achievements a
            ON p.name = a.player_name
        GROUP BY
            p.name,
            p.xp,
            p.careers_completed
        ORDER BY
            p.xp DESC,
            p.careers_completed DESC,
            achievements DESC,
            p.name ASC
    """).fetchall()

    stats = conn.execute("""
        SELECT
            (SELECT COUNT(*) FROM players)
                AS total_players,

            (SELECT COALESCE(SUM(careers_completed), 0)
             FROM players)
                AS total_careers_completed,

            (SELECT COUNT(*) FROM achievements)
                AS total_achievements,

            (SELECT visits FROM site_stats WHERE id = 1)
                AS visits
    """).fetchone()

    conn.close()

    return players, stats

def add_career_history(name, career, score):

    conn = get_db()

    conn.execute(
        """
        INSERT INTO career_history
            (player_name, career, score)
        VALUES (?, ?, ?)
        """,
        (name, career, score)
    )

    conn.commit()
    conn.close()


def get_career_history(name):

    conn = get_db()

    history = conn.execute(
        """
        SELECT career, score, completed_at
        FROM career_history
        WHERE player_name = ?
        ORDER BY completed_at DESC
        """,
        (name,)
    ).fetchall()

    conn.close()

    return history

def award_progress_achievements(name):

    player = get_player(name)

    if not player:
        return

    xp = player["xp"]
    careers_completed = player["careers_completed"]
    history = get_career_history(name)
    achievements = get_player_achievements(name)

    completed_categories = set()

    for item in history:

        career = item["career"]

        for category, category_careers in career_categories.items():

            if career in category_careers:
                completed_categories.add(category)

    new_achievements = []

    if careers_completed >= 1:
        new_achievements.append("First Career Completed")

    if careers_completed >= 5:
        new_achievements.append("Career Explorer")

    if careers_completed >= 10:
        new_achievements.append("Career Adventurer")

    if careers_completed >= 20:
        new_achievements.append("Career Master")

    if xp >= 500:
        new_achievements.append("Level Grinder")

    if xp >= 1000:
        new_achievements.append("XP Champion")

    if len(completed_categories) >= 3:
        new_achievements.append("Category Sampler")

    if len(completed_categories) >= 7:
        new_achievements.append("Career Quest Legend")

    for achievement in new_achievements:

        if achievement not in achievements:
            add_player_achievement(name, achievement)

def get_career_category(career):

    for category, category_careers in career_categories.items():

        if career in category_careers:
            return category

    return "Career"

all_achievements = [
    {
        "title": "First Career Completed",
        "description": "Complete your first career simulation."
    },
    {
        "title": "Career Explorer",
        "description": "Complete 5 career simulations."
    },
    {
        "title": "Career Adventurer",
        "description": "Complete 10 career simulations."
    },
    {
        "title": "Career Master",
        "description": "Complete 20 career simulations."
    },
    {
        "title": "Level Grinder",
        "description": "Reach 500 XP."
    },
    {
        "title": "XP Champion",
        "description": "Reach 1,000 XP."
    },
    {
        "title": "Category Sampler",
        "description": "Complete careers from at least 3 categories."
    },
    {
        "title": "Career Quest Legend",
        "description": "Complete careers from all 7 categories."
    },
    {
        "title": "Rising Professional",
        "description": "Score 70% or higher on a career simulation."
    },
    {
        "title": "Technical Expert",
        "description": "Show strong technical thinking in a simulation."
    },
    {
        "title": "Future Leader",
        "description": "Show strong leadership decisions in a simulation."
    },
    {
        "title": "Master Communicator",
        "description": "Show strong communication skills in a simulation."
    },
    {
        "title": "Problem Solver",
        "description": "Show strong problem-solving skills in a simulation."
    }
]

def get_profile_summary(name):

    history = get_career_history(name)

    if not history:

        return {
            "best_score": None,
            "recent_career": None,
            "favorite_category": None
        }

    best_score = max(
        item["score"]
        for item in history
    )

    recent_career = history[0]["career"]

    category_counts = {}

    for item in history:

        career = item["career"]

        category = get_career_category(career)

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

    favorite_category = max(
        category_counts,
        key=category_counts.get
    )

    return {
        "best_score": best_score,
        "recent_career": recent_career,
        "favorite_category": favorite_category
    }

def get_saved_careers(name):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT career
        FROM saved_careers
        WHERE player_name = ?
        ORDER BY career
        """,
        (name,)
    ).fetchall()

    conn.close()

    return [row["career"] for row in rows]


def is_career_saved(name, career):

    conn = get_db()

    saved = conn.execute(
        """
        SELECT 1
        FROM saved_careers
        WHERE player_name = ? AND career = ?
        """,
        (name, career)
    ).fetchone()

    conn.close()

    return saved is not None


def toggle_saved_career(name, career):

    conn = get_db()

    saved = conn.execute(
        """
        SELECT 1
        FROM saved_careers
        WHERE player_name = ? AND career = ?
        """,
        (name, career)
    ).fetchone()

    if saved:
        conn.execute(
            """
            DELETE FROM saved_careers
            WHERE player_name = ? AND career = ?
            """,
            (name, career)
        )
    else:
        conn.execute(
            """
            INSERT INTO saved_careers
                (player_name, career)
            VALUES (?, ?)
            """,
            (name, career)
        )

    conn.commit()
    conn.close()

def save_match_result(name, recommendations):

    if not recommendations:
        return

    top = recommendations[0]["name"]

    second = None
    third = None

    if len(recommendations) > 1:
        second = recommendations[1]["name"]

    if len(recommendations) > 2:
        third = recommendations[2]["name"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO match_results
            (player_name, top_career, second_career, third_career)
        VALUES (?, ?, ?, ?)
        """,
        (name, top, second, third)
    )

    conn.commit()
    conn.close()


def get_latest_match_result(name):

    conn = get_db()

    match = conn.execute(
        """
        SELECT top_career, second_career, third_career, completed_at
        FROM match_results
        WHERE player_name = ?
        ORDER BY completed_at DESC
        LIMIT 1
        """,
        (name,)
    ).fetchone()

    conn.close()

    return match

def get_category_progress(name):

    history = get_career_history(name)

    completed_careers = {
        item["career"]
        for item in history
    }

    progress = []

    for category, category_careers in career_categories.items():

        completed = 0

        for career in category_careers:

            if career in completed_careers:
                completed += 1

        total = len(category_careers)

        progress.append({
            "category": category,
            "completed": completed,
            "total": total,
            "percent": int((completed / total) * 100)
        })

    return progress

def get_daily_challenge():

    all_careers = sorted(careers.keys())

    today = date.today().isoformat()

    random.seed(today)

    challenge_career = random.choice(all_careers)

    random.seed()

    return {
        "date": today,
        "career": challenge_career,
        "category": get_career_category(challenge_career),
        "info": career_info[challenge_career]
    }

def update_login_streak(name):

    player = get_player(name)

    if not player:
        return

    today = date.today()
    today_text = today.isoformat()

    last_active = player["last_active"]

    if last_active == today_text:
        return

    current_streak = player["current_streak"]
    best_streak = player["best_streak"]

    if not last_active:

        current_streak = 1

    else:

        last_active_date = date.fromisoformat(last_active)
        days_since_active = (today - last_active_date).days

        if days_since_active == 1:
            current_streak += 1
        else:
            current_streak = 1

    if current_streak > best_streak:
        best_streak = current_streak

    conn = get_db()

    conn.execute(
        """
        UPDATE players
        SET current_streak = ?,
            best_streak = ?,
            last_active = ?
        WHERE name = ?
        """,
        (current_streak, best_streak, today_text, name)
    )

    conn.commit()
    conn.close()

def clean_daily_challenge_career(challenge):

    if isinstance(challenge, str):
        return challenge

    if isinstance(challenge, dict):

        possible_value = (
            challenge.get("career")
            or challenge.get("name")
            or challenge.get("title")
        )

        if isinstance(possible_value, str):
            return possible_value

        if isinstance(possible_value, dict):
            return (
                possible_value.get("career")
                or possible_value.get("name")
                or possible_value.get("title")
                or list(career_info.keys())[0]
            )

    return list(career_info.keys())[0]

def get_daily_challenge_status(name):

    today_text = date.today().isoformat()

    challenge = get_daily_challenge()

    career = clean_daily_challenge_career(challenge)

    conn = get_db()

    row = conn.execute(
        """
        SELECT * FROM daily_challenges
        WHERE player_name = ?
        AND challenge_date = ?
        """,
        (name, today_text)
    ).fetchone()

    if not row:

        conn.execute(
            """
            INSERT INTO daily_challenges
            (player_name, challenge_date, career, completed)
            VALUES (?, ?, ?, ?)
            """,
            (name, today_text, career, 0)
        )

        conn.commit()

        row = conn.execute(
            """
            SELECT * FROM daily_challenges
            WHERE player_name = ?
            AND challenge_date = ?
            """,
            (name, today_text)
        ).fetchone()

    conn.close()

    return row

def complete_daily_challenge(name):

    status = get_daily_challenge_status(name)

    completed = int(status["completed"] or 0)

    if completed == 1:
        return False

    player = get_player(name)
    new_xp = player["xp"] + 30

    today_text = date.today().isoformat()

    conn = get_db()

    conn.execute(
        """
        UPDATE daily_challenges
        SET completed = 1
        WHERE player_name = ?
        AND challenge_date = ?
        """,
        (name, today_text)
    )

    conn.execute(
        """
        UPDATE players
        SET xp = ?
        WHERE name = ?
        """,
        (new_xp, name)
    )

    conn.commit()
    conn.close()

    session["total_xp"] = new_xp

    return True

def get_personality_type(strongest_skill, career):

    category = get_career_category(career)

    if strongest_skill == "Technical Skill":

        return {
            "title": "The Builder",
            "description": "You like creating, improving, testing, and making things work.",
            "category": category
        }

    if strongest_skill == "Leadership":

        return {
            "title": "The Leader",
            "description": "You are strong at making decisions, guiding others, and staying organized under pressure.",
            "category": category
        }

    if strongest_skill == "Communication":

        return {
            "title": "The Communicator",
            "description": "You are strong at explaining ideas, understanding people, and working with others.",
            "category": category
        }

    if strongest_skill == "Problem Solving":

        return {
            "title": "The Strategist",
            "description": "You are strong at thinking through challenges, adapting, and finding smart solutions.",
            "category": category
        }

    return {
        "title": "The Explorer",
        "description": "You are still discovering your strongest career style.",
        "category": category
    }

def get_activity_personality(name):

    history = get_career_history(name)
    saved_careers = get_saved_careers(name)
    latest_match = get_latest_match_result(name)

    category_scores = {}

    for category in career_categories:
        category_scores[category] = 0

    def add_career_points(career, points):

        category = get_career_category(career)

        if category:
            category_scores[category] += points

    for item in history:

        score_bonus = item["score"] // 25

        add_career_points(
            item["career"],
            3 + score_bonus
        )

    for career in saved_careers:

        add_career_points(
            career,
            2
        )

    if latest_match:

        add_career_points(
            latest_match["top_career"],
            5
        )

        add_career_points(
            latest_match["second_career"],
            3
        )

        add_career_points(
            latest_match["third_career"],
            2
        )

    ranked_categories = sorted(
        category_scores.items(),
        key=lambda item: (-item[1], item[0])
    )

    top_category = ranked_categories[0][0]
    top_score = ranked_categories[0][1]

    if top_score == 0:

        return {
            "title": "The Explorer",
            "category": "Undiscovered",
            "description": "You are still exploring careers and building your profile.",
            "confidence": 0
        }

    personality_map = {

        "Technology": {
            "title": "The Builder",
            "description": "You are drawn to systems, problem-solving, tools, and building useful things."
        },

        "Engineering": {
            "title": "The Inventor",
            "description": "You are drawn to designing, improving, testing, and solving real-world problems."
        },

        "Art": {
            "title": "The Creator",
            "description": "You are drawn to visual ideas, originality, expression, and creative work."
        },

        "Culture": {
            "title": "The Storyteller",
            "description": "You are drawn to people, ideas, food, media, stories, and cultural impact."
        },

        "Health": {
            "title": "The Healer",
            "description": "You are drawn to helping people or animals improve, recover, and thrive."
        },

        "Service": {
            "title": "The Helper",
            "description": "You are drawn to supporting others, solving human problems, and serving communities."
        },

        "Business": {
            "title": "The Strategist",
            "description": "You are drawn to planning, leadership, money, growth, and decision-making."
        }
    }

    personality = personality_map.get(
        top_category,
        {
            "title": "The Explorer",
            "description": "You are still discovering your career personality."
        }
    )

    confidence = min(
        100,
        40 + (top_score * 8)
    )

    return {
        "title": personality["title"],
        "category": top_category,
        "description": personality["description"],
        "confidence": confidence
    }

def get_career_roadmap(career):

    category = get_career_category(career)

    default_roadmaps = {

        "Technology": {
            "skills": [
                "Problem solving",
                "Programming basics",
                "Debugging",
                "Logical thinking"
            ],
            "subjects": [
                "Computer Science",
                "Math",
                "Technology",
                "Statistics"
            ],
            "tools": [
                "Python",
                "GitHub",
                "VS Code",
                "Online documentation"
            ],
            "project": f"Build a beginner project related to {career}.",
            "next_step": "Learn one beginner tool and create a small portfolio project."
        },

        "Business": {
            "skills": [
                "Planning",
                "Communication",
                "Decision making",
                "Money awareness"
            ],
            "subjects": [
                "Business",
                "Economics",
                "Math",
                "English"
            ],
            "tools": [
                "Spreadsheets",
                "Presentations",
                "Budget trackers",
                "Research tools"
            ],
            "project": f"Create a simple plan or case study for a {career} scenario.",
            "next_step": "Practice explaining a business idea clearly in one page."
        },

        "Health": {
            "skills": [
                "Care",
                "Attention to detail",
                "Communication",
                "Problem solving"
            ],
            "subjects": [
                "Biology",
                "Chemistry",
                "Health Science",
                "Psychology"
            ],
            "tools": [
                "Anatomy resources",
                "Medical references",
                "Note-taking tools",
                "Practice case studies"
            ],
            "project": f"Research a real-world day in the life of a {career}.",
            "next_step": "Learn the education path and shadow/interview someone in the field."
        },

        "Engineering": {
            "skills": [
                "Design thinking",
                "Math",
                "Testing",
                "Problem solving"
            ],
            "subjects": [
                "Physics",
                "Math",
                "Engineering",
                "Computer Science"
            ],
            "tools": [
                "CAD software",
                "Sketching tools",
                "Calculators",
                "Prototype materials"
            ],
            "project": f"Design a small prototype or model related to {career}.",
            "next_step": "Try a beginner engineering design challenge."
        },

        "Art": {
            "skills": [
                "Creativity",
                "Visual thinking",
                "Style development",
                "Feedback"
            ],
            "subjects": [
                "Art",
                "Design",
                "Media",
                "English"
            ],
            "tools": [
                "Sketchbook",
                "Canva",
                "Adobe tools",
                "Portfolio website"
            ],
            "project": f"Create a small portfolio piece inspired by {career}.",
            "next_step": "Build a simple portfolio with 3 examples of your work."
        },

        "Culture": {
            "skills": [
                "Storytelling",
                "Communication",
                "Creativity",
                "Audience awareness"
            ],
            "subjects": [
                "English",
                "History",
                "Media",
                "Social Studies"
            ],
            "tools": [
                "Writing tools",
                "Camera or phone",
                "Editing software",
                "Research sources"
            ],
            "project": f"Create a short story, post, recipe, song, or media piece related to {career}.",
            "next_step": "Study examples from professionals and make your own small project."
        },

        "Service": {
            "skills": [
                "Leadership",
                "Empathy",
                "Communication",
                "Responsibility"
            ],
            "subjects": [
                "English",
                "Social Studies",
                "Psychology",
                "Public Speaking"
            ],
            "tools": [
                "Planning tools",
                "Communication tools",
                "Checklists",
                "Training resources"
            ],
            "project": f"Research how a {career} helps people in real situations.",
            "next_step": "Volunteer, interview someone, or learn the required training path."
        }
    }

    roadmap = default_roadmaps.get(
        category,
        {
            "skills": [
                "Communication",
                "Problem solving",
                "Responsibility",
                "Curiosity"
            ],
            "subjects": [
                "English",
                "Math",
                "Technology",
                "Social Studies"
            ],
            "tools": [
                "Research tools",
                "Notes",
                "Practice projects",
                "Portfolio"
            ],
            "project": f"Create a beginner project related to {career}.",
            "next_step": "Research the career and try one small beginner activity."
        }
    )

    return {
        "category": category,
        "skills": roadmap["skills"],
        "subjects": roadmap["subjects"],
        "tools": roadmap["tools"],
        "project": roadmap["project"],
        "next_step": roadmap["next_step"]
    }

@app.route("/feedback")
def feedback():

    return render_template("feedback.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/reset")
def reset():

    session.clear()

    return redirect(url_for("home"))

@app.route("/")
def home():

    visits = increment_visits()

    xp = 0
    level = 1
    progress = 0
    achievements = 0
    careers_completed = 0
    personality_profile = None

    players = get_all_players()

    if session.get("player_name"):

        name = session["player_name"]

        player = get_player(name)

        if player:

            xp = player["xp"]
            level = (xp // 100) + 1
            progress = xp % 100

            session["total_xp"] = xp

            achievements = len(
                get_player_achievements(name)
            )

            careers_completed = player["careers_completed"]

            personality_profile = get_activity_personality(name)

    total_players = len(players)

    total_achievements = get_total_achievements()

    total_careers_completed = 0

    for player in players:

        total_careers_completed += player["careers_completed"]

    return render_template(
        "home.html",
        careers=careers.keys(),
        career_categories=career_categories,
        xp=xp,
        level=level,
        progress=progress,
        achievements=achievements,
        careers_completed=careers_completed,
        visits=visits,
        total_players=total_players,
        total_achievements=total_achievements,
        total_careers_completed=total_careers_completed,
        personality_profile=personality_profile
    )

@app.route("/leaderboards")
def leaderboards():

    players, stats = get_leaderboard_data()

    return render_template(
        "leaderboards.html",
        players=players,
        stats=stats
    )

@app.route("/dashboard")
def dashboard():

    if not session.get("player_name"):
        return redirect(url_for("home"))

    name = session["player_name"]

    player = get_player(name)

    if not player:
        create_player(name)
        player = get_player(name)

    xp = player["xp"]
    level = (xp // 100) + 1
    progress = xp % 100

    achievements = get_player_achievements(name)
    saved_careers = get_saved_careers(name)
    history = get_career_history(name)
    latest_match = get_latest_match_result(name)
    category_progress = get_category_progress(name)

    profile_summary = {
        "name": name,
        "xp": xp,
        "level": level,
        "progress": progress,
        "careers_completed": player["careers_completed"],
        "achievements_count": len(achievements),
        "saved_count": len(saved_careers),
        "quizzes_taken": len(history),
        "current_streak": player["current_streak"],
        "best_streak": player["best_streak"],
    }

    return render_template(
        "dashboard.html",
        name=name,
        xp=xp,
        level=level,
        progress=progress,
        careers_completed=player["careers_completed"],
        achievements=achievements,
        saved_careers=saved_careers,
        history=history,
        latest_match=latest_match,
        category_progress=category_progress,
        profile_summary=profile_summary
    )


@app.route("/start/<career>")
def start(career):

    if career not in careers:
        return redirect(url_for("home"))

    session["career"] = career
    session["index"] = 0
    session["score"] = 0
    session["result_saved"] = False

    if "total_xp" not in session:
        session["total_xp"] = 0

    session["scenario"] = random.choice(
        career_scenarios.get(
            career,
            ["A challenging day awaits."]
        )
    )

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

        name = session.get("player_name")

        if name:
            update_player_xp(name, total_xp)

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

    career = session.get("career")

    if not career or career not in careers:
        return redirect(url_for("home"))

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

    strongest_skill = None
    growth_skill = None

    if skills:

        strongest_skill = max(
            skills,
            key=skills.get
        )

        growth_skill = min(
            skills,
            key=skills.get
        )

    next_career = None

    category = get_career_category(career)

    if category and category in career_categories:

        for possible_career in career_categories[category]:

            if possible_career != career:

                next_career = possible_career

                break

        personality = get_personality_type(
            strongest_skill,
            career
        )

    advice = get_coach_advice(percent, career)

    if percent >= 90:

        achievement_title, achievement_text = get_achievement(
            skills
        )

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

    name = session.get("player_name")

    if name and not session.get("result_saved", False):

        player = get_player(name)

        if player:

            careers_completed = player["careers_completed"]

            if percent >= 50:
                careers_completed += 1

            if percent >= 70:
                add_player_achievement(
                    name,
                    achievement_title
                )

            bonus_xp = 0

            if percent >= 90:
                bonus_xp = 100
            elif percent >= 70:
                bonus_xp = 50
            elif percent >= 50:
                bonus_xp = 25

            session["total_xp"] = (
                session.get("total_xp", 0) + bonus_xp
            )

            update_player_progress(
                name,
                session["total_xp"],
                careers_completed
            )

            add_career_history(
                name,
                career,
                percent
            )

            award_progress_achievements(name)

            session["result_saved"] = True

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
        achievement_text=achievement_text,
        strongest_skill=strongest_skill,
        growth_skill=growth_skill,
        next_career=next_career,
        saved=is_career_saved(name, career) if name else False,
        personality=personality,
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

@app.route("/career-match/start")
def start_career_match():

    session["match_index"] = 0
    session["match_scores"] = {}
    session["match_result_saved"] = False

    return redirect(url_for("career_match"))


@app.route("/career-match", methods=["GET", "POST"])
def career_match():

    index = session.get("match_index", 0)
    scores = session.get("match_scores", {})

    if request.method == "POST":

        option_index = int(request.form["option"])
        question = career_match_questions[index]
        selected_option = question["options"][option_index]

        for career in selected_option["careers"]:
            scores[career] = scores.get(career, 0) + 1

        index += 1

        session["match_scores"] = scores
        session["match_index"] = index

    if index >= len(career_match_questions):
        return redirect(url_for("career_match_result"))

    return render_template(
        "career_match.html",
        question=career_match_questions[index],
        index=index,
        total=len(career_match_questions)
    )


@app.route("/career-match/result")
def career_match_result():

    scores = session.get("match_scores", {})

    if not scores:
        return redirect(url_for("start_career_match"))

    ranked_careers = sorted(
        scores.items(),
        key=lambda item: (-item[1], item[0])
    )

    recommendations = []

    for career, score in ranked_careers[:3]:
        if career in career_info:
            recommendations.append({
                "name": career,
                "score": score,
                "info": career_info[career]
            })

    if session.get("player_name") and not session.get("match_result_saved"):
        save_match_result(
            session["player_name"],
            recommendations,
        )
        personality_profile = get_activity_personality(
            session["player_name"]
        )

        session["match_result_saved"] = True

    return render_template(
        "match_results_v2.html",
        recommendations=recommendations
    )

@app.route("/compare", methods=["GET", "POST"])
def compare():

    selected_careers = []

    if request.method == "POST":
        selected_careers = request.form.getlist("careers")

    selected_careers = [
        career
        for career in selected_careers
        if career in career_info
    ][:3]

    compared = [
        {
            "name": career,
            "info": career_info[career]
        }
        for career in selected_careers
    ]

    return render_template(
        "compare.html",
        careers=career_info.keys(),
        selected_careers=selected_careers,
        compared=compared
    )

@app.route("/admin/career-check")
def career_check():

    if not session.get("is_admin"):
        return redirect(url_for("home"))

@app.route("/career/<career>")
def career_detail(career):

    if career not in career_info:

        return redirect(url_for("home"))

    name = session.get("player_name")

    saved = False

    if name:

        saved = is_career_saved(name, career)

    roadmap = get_career_roadmap(career)

    preview_stories = career_stories.get(career, [])[:3]

    preview_scenarios = career_scenarios.get(career, [])[:3]

    return render_template(
        "career_detail.html",
        career=career,
        info=career_info[career],
        category=get_career_category(career),
        saved=saved,
        roadmap=roadmap,
        preview_stories=preview_stories,
        preview_scenarios=preview_scenarios
    )

@app.route("/achievements")
def achievements_page():

    if not session.get("player_name"):
        return redirect(url_for("home"))

    name = session["player_name"]
    unlocked = get_player_achievements(name)

    achievements = []

    for achievement in all_achievements:

        achievements.append({
            "title": achievement["title"],
            "description": achievement["description"],
            "unlocked": achievement["title"] in unlocked
        })

    return render_template(
        "achievements.html",
        achievements=achievements,
        unlocked_count=len(unlocked),
        total_count=len(all_achievements)
    )

@app.route("/save-career/<career>", methods=["POST"])
def save_career(career):

    if not session.get("player_name"):
        return redirect(url_for("home"))

    if career not in careers:
        return redirect(url_for("home"))

    toggle_saved_career(
        session["player_name"],
        career
    )

    return redirect(url_for("career_detail", career=career))


@app.route("/saved-careers")
def saved_careers_page():

    if not session.get("player_name"):
        return redirect(url_for("home"))

    name = session["player_name"]

    saved = get_saved_careers(name)

    saved_items = [
        {
            "name": career,
            "category": get_career_category(career),
            "info": career_info[career]
        }
        for career in saved
        if career in career_info
    ]

    return render_template(
        "saved_careers.html",
        saved_items=saved_items
    )

@app.route("/privacy")
def privacy():

    return render_template("privacy.html")


@app.route("/support")
def support():

    return render_template("support.html")

@app.route("/daily-challenge", methods=["GET", "POST"])
def daily_challenge():

    if not session.get("player_name"):
        return redirect(url_for("home"))

    name = session["player_name"]

    status = get_daily_challenge_status(name)

    message = None

    if request.method == "POST":

        completed_now = complete_daily_challenge(name)

        if completed_now:
            message = "Daily challenge completed. You earned 30 XP."
        else:
            message = "You already completed today's daily challenge."

        status = get_daily_challenge_status(name)

    return render_template(
        "daily_challenge.html",
        career=status["career"],
        completed=int(status["completed"] or 0),
        message=message
    )

if __name__ == "__main__":
    app.run(debug=True)