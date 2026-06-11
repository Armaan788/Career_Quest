from flask import Flask, render_template, redirect, url_for, request, session
import json
import os

app = Flask(__name__)
app.secret_key = "career-quest-secret"

# ----------------------------
# CAREER DATA
# ----------------------------
careers = {




"Software Engineer": [
    {
        "q": "A bug breaks production. You:",
        "skill": "Problem Solving",
        "options": [("Fix immediately",3),("Investigate first",2),("Ignore it",0)]
    },
    {
        "q": "Code review feedback:",
        "skill": "Communication",
        "options": [("Improve code",3),("Defend it",1),("Ignore",0)]
    },
    {
        "q": "New framework:",
        "skill": "Technical Skill",
        "options": [("Build project",3),("Watch tutorials",2),("Avoid it",0)]
    },
    {
        "q": "System is slow:",
        "skill": "Technical Skill",
        "options": [("Optimize it",3),("Ignore",0),("Rebuild everything",1)]
    },
    {
        "q": "Team disagreement:",
        "skill": "Leadership",
        "options": [("Discuss solution",3),("Stay silent",0),("Force opinion",1)]
    }
],
"Teacher": [
    {"q": "Student is struggling:", "skill": "Communication", "options": [("Help individually",3),("Ignore",0),("Scold",1)]},
    {"q": "Class disruption:", "skill": "Leadership", "options": [("Handle calmly",3),("Ignore",0),("Yell",1)]},
    {"q": "Lesson planning:", "skill": "Technical Skill", "options": [("Adapt lesson",3),("Reuse old plan",1),("Skip planning",0)]},
    {"q": "Exam results drop:", "skill": "Problem Solving", "options": [("Improve teaching",3),("Blame students",0),("Ignore",0)]},
    {"q": "Parent meeting:", "skill": "Communication", "options": [("Communicate clearly",3),("Avoid",0),("Argue",1)]}
],
"Entrepreneur": [
    {"q": "Startup losing money:", "skill": "Problem Solving", "options": [("Pivot",3),("Wait",1),("Quit",0)]},
    {"q": "Investor rejects pitch:", "skill": "Communication", "options": [("Improve pitch",3),("Ignore feedback",0),("Quit",1)]},
    {"q": "Competitor launches product:", "skill": "Leadership", "options": [("Innovate faster",3),("Do nothing",0),("Copy",1)]},
    {"q": "Customer feedback:", "skill": "Communication", "options": [("Improve product",3),("Ignore",0),("Argue",1)]},
    {"q": "Funding runs out:", "skill": "Problem Solving", "options": [("Seek investors",3),("Stop",0),("Panic",1)]}
],
"Doctor": [
    {"q": "Emergency patient arrives:", "skill": "Problem Solving", "options": [("Act immediately",3),("Wait",0),("Pass to someone else",1)]},
    {"q": "Diagnosis unclear:", "skill": "Technical Skill", "options": [("Run tests",3),("Guess",0),("Ignore",0)]},
    {"q": "Long shift:", "skill": "Leadership", "options": [("Stay focused",3),("Lose focus",1),("Quit",0)]},
    {"q": "Patient anxious:", "skill": "Communication", "options": [("Reassure",3),("Ignore emotions",0),("Rush treatment",1)]},
    {"q": "Medical mistake risk:", "skill": "Technical Skill", "options": [("Double-check",3),("Proceed fast",1),("Ignore",0)]}
],

"Lawyer": [
    {"q": "Case preparation:", "skill": "Technical Skill", "options": [("Research deeply",3),("Guess arguments",0),("Skip prep",0)]},
    {"q": "Court pressure:", "skill": "Leadership", "options": [("Stay calm",3),("Panic",0),("Argue emotionally",1)]},
    {"q": "Weak evidence:", "skill": "Problem Solving", "options": [("Strengthen case",3),("Ignore issue",0),("Proceed blindly",1)]},
    {"q": "Client lies:", "skill": "Communication", "options": [("Verify facts",3),("Accept blindly",0),("Ignore",0)]},
    {"q": "Opposition strong:", "skill": "Problem Solving", "options": [("Strategize",3),("Give up",0),("Argue poorly",1)]}
],

"Designer": [
    {"q": "Client dislikes design:", "skill": "Communication", "options": [("Revise",3),("Ignore",0),("Argue",1)]},
    {"q": "Creative block:", "skill": "Problem Solving", "options": [("Experiment",3),("Stop work",0),("Copy others",1)]},
    {"q": "Deadline close:", "skill": "Leadership", "options": [("Prioritize quality",3),("Rush badly",1),("Quit",0)]},
    {"q": "Feedback received:", "skill": "Communication", "options": [("Improve design",3),("Ignore",0),("Reject feedback",1)]},
    {"q": "New tool learned:", "skill": "Technical Skill", "options": [("Practice it",3),("Avoid it",0),("Ignore",0)]}
],

"Pilot": [
    {"q": "Bad weather:", "skill": "Problem Solving", "options": [("Follow safety rules",3),("Take risk",0),("Ignore warnings",0)]},
    {"q": "System failure:", "skill": "Technical Skill", "options": [("Emergency protocol",3),("Panic",0),("Ignore",0)]},
    {"q": "Long flight:", "skill": "Leadership", "options": [("Stay alert",3),("Lose focus",0),("Relax too much",1)]},
    {"q": "Navigation issue:", "skill": "Technical Skill", "options": [("Recalculate route",3),("Guess",0),("Ignore",0)]},
    {"q": "Passenger safety:", "skill": "Communication", "options": [("Prioritize safety",3),("Rush landing",1),("Ignore",0)]}
],
"Chef": [
    {"q": "Order overload:", "skill": "Leadership", "options": [("Prioritize dishes",3),("Panic",0),("Ignore",0)]},
    {"q": "Dish criticism:", "skill": "Communication", "options": [("Improve recipe",3),("Argue",0),("Ignore",0)]},
    {"q": "Kitchen stress:", "skill": "Leadership", "options": [("Stay calm",3),("Lose focus",0),("Quit",0)]},
    {"q": "Ingredient missing:", "skill": "Problem Solving", "options": [("Adapt recipe",3),("Cancel dish",0),("Guess substitute",1)]},
    {"q": "Team coordination:", "skill": "Communication", "options": [("Organize team",3),("Do everything alone",1),("Ignore team",0)]}
],

"Data Scientist": [
    {"q": "Data is messy:", "skill": "Technical Skill", "options": [("Clean dataset",3),("Ignore errors",0),("Guess results",0)]},
    {"q": "Model accuracy low:", "skill": "Problem Solving", "options": [("Improve model",3),("Random tweak",1),("Ignore",0)]},
    {"q": "Missing data:", "skill": "Technical Skill", "options": [("Handle properly",3),("Delete blindly",0),("Ignore",0)]},
    {"q": "Business asks insight:", "skill": "Communication", "options": [("Analyze deeply",3),("Guess",0),("Delay",0)]},
    {"q": "New algorithm:", "skill": "Technical Skill", "options": [("Learn it",3),("Avoid it",0),("Ignore",0)]}
],

"Marketing Manager": [
    {"q": "Campaign underperforming:", "skill": "Problem Solving", "options": [("Adjust strategy",3),("Ignore",0),("Blame team",1)]},
    {"q": "Audience unclear:", "skill": "Technical Skill", "options": [("Research market",3),("Guess",0),("Skip research",0)]},
    {"q": "Budget cut:", "skill": "Leadership", "options": [("Optimize spend",3),("Stop campaign",0),("Waste budget",0)]},
    {"q": "Ad feedback negative:", "skill": "Communication", "options": [("Improve ad",3),("Ignore",0),("Argue",1)]},
    {"q": "Competitor campaign:", "skill": "Problem Solving", "options": [("Innovate",3),("Copy",1),("Ignore",0)]}
],
}
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
    ]
}
import random

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

    "Doctor": [
        "🚑 Multiple emergency patients arrive at once.",
        "🩺 Test results are inconclusive.",
        "⚠️ A patient has an unexpected reaction.",
        "🌙 You're assigned an extra shift.",
        "💊 A medication shortage affects treatment."
    ],

    "Entrepreneur": [
        "💰 Investors suddenly pull out funding.",
        "🚀 A competitor launches a similar product.",
        "⭐ A customer review goes viral.",
        "📉 Revenue drops this month.",
        "🎤 You must pitch to investors tomorrow."
    ]
}
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
        "education": "Culinary School (Optional)",
        "growth": "15%"
    },

    "Data Scientist": {
        "salary": "$130,000",
        "education": "Bachelor's Degree",
        "growth": "35%"
    },

    "Marketing Manager": {
        "salary": "$115,000",
        "education": "Bachelor's Degree",
        "growth": "10%"
    }
}

career_interviews = {

    "Software Engineer":
        "Why do you want to become a Software Engineer?",

    "Teacher":
        "Why do you want to help students learn?",

    "Entrepreneur":
        "What problem would you like to solve with a business?",

    "Doctor":
        "Why do you want to help patients?",

    "Lawyer":
        "Why is justice important to you?",

    "Designer":
        "What inspires your creativity?",

    "Pilot":
        "What interests you about aviation?",

    "Chef":
        "Why do you enjoy cooking?",

    "Data Scientist":
        "What excites you about working with data?",

    "Marketing Manager":
        "How would you persuade people to try a new product?"
}

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


def load_players():

    if not os.path.exists("players.json"):

        with open("players.json", "w") as file:
            json.dump({}, file)

        return {}

    with open("players.json", "r") as file:
        return json.load(file)



def save_players(players):

    with open("players.json", "w") as file:
        json.dump(players, file, indent=4)



@app.route("/set_name", methods=["POST"])
def set_name():

    name = request.form["player_name"]

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

    xp = session.get("total_xp", 0)

    level = (xp // 100) + 1

    progress = xp % 100

    achievements = 0
    careers_completed = 0

    if session.get("player_name"):

        players = load_players()

        player = players.get(
            session["player_name"],
            {}
        )

        achievements = len(
            player.get("achievements", [])
        )

        careers_completed = player.get(
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
        careers_completed=careers_completed
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

    career = session["career"]
    index = session.get("index", 0)
    score = session.get("score", 0)
    scenario = session.get("scenario")

    questions = careers[career]

    if request.method == "POST":

        answer_score = int(request.form["score"])

        score += answer_score

        total_xp = session.get("total_xp", 0)

        total_xp += answer_score * 10

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
        index=index,
        total=len(questions),
        career=career
    )

@app.route("/result")
def result():

    career = session["career"]
    score = session.get("score", 0)

    total = len(careers[career]) * 3
    percent = int((score / total) * 100)

    skills = session.get("skills", {})

    skill_percentages = {}

    highest_skill = max(skills.values()) if skills else 1

    for skill, value in skills.items():
        skill_percentages[skill] = int((value / highest_skill) * 100)

    advice = get_coach_advice(percent, career)
    xp = session.get("total_xp", 0)

    level = (xp // 100) + 1
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

    if session.get("player_name"):

        players = load_players()

        name = session["player_name"]

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

        save_players(players)



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
    )
@app.route("/interview", methods=["GET", "POST"])
def interview():
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
                "passion"
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
            scenario = scenario
        )
if __name__ == "__main__":
    app.run(debug=True)