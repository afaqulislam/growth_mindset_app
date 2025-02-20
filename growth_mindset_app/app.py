import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

# Initialize session state (Your existing initialization)
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = pd.DataFrame(columns=['Date', 'Progress', 'Mood', 'Energy'])
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = set()
if 'daily_quote' not in st.session_state:
    st.session_state.daily_quote = ""
if 'avatar' not in st.session_state:
    st.session_state.avatar = "🧑"

# Your existing code for the Streamlit app
# Your existing variables (quotes, challenges, achievements)
quotes = [
    "Your mind is a powerful thing. When you fill it with positive thoughts, your life will start to change. 🌟",
    "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle. 💖",
    "Believe you can and you're halfway there. 🚀",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. 💪",
    "The future belongs to those who believe in the beauty of their dreams. 🌈"
]

challenges = [
    "Learn a new word in a foreign language and use it in a sentence",
    "Do 20 jumping jacks right now!",
    "Write a short story using exactly 50 words",
    "Compliment three people today",
    "Try a new healthy recipe for dinner",
    "Meditate for 5 minutes",
    "Draw a self-portrait without looking at the paper",
    "Learn and practice a new yoga pose"
]

achievements = {
    "Early Bird": "Complete a challenge before 9 AM",
    "Night Owl": "Complete a challenge after 10 PM",
    "Streak Master": "Maintain a 7-day streak",
    "Century Club": "Earn 100 points",
    "Mood Maestro": "Track your mood for 14 consecutive days",
    "Challenge Champion": "Complete 50 challenges"
}

# Your existing functions
def update_points_and_level(points):
    st.session_state.points += points
    st.session_state.level = (st.session_state.points // 100) + 1

def check_achievements():
    if st.session_state.streak >= 7:
        st.session_state.achievements.add("Streak Master")
    if st.session_state.points >= 100:
        st.session_state.achievements.add("Century Club")
    if len(st.session_state.completed_challenges) >= 50:
        st.session_state.achievements.add("Challenge Champion")

# New feature functions
def add_goals_feature():
    st.header("🎯 Custom Goals")
    if 'goals' not in st.session_state:
        st.session_state.goals = []
    
    new_goal = st.text_input("Add a new goal:")
    goal_deadline = st.date_input("Goal deadline:", min_value=datetime.now())
    if st.button("Add Goal"):
        st.session_state.goals.append({
            "goal": new_goal,
            "deadline": goal_deadline,
            "completed": False
        })
        st.success("Goal added successfully!")
    
    if st.session_state.goals:
        st.subheader("Your Goals")
        for i, goal in enumerate(st.session_state.goals):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📌 {goal['goal']}")
            with col2:
                st.write(f"Due: {goal['deadline'].strftime('%Y-%m-%d')}")
            with col3:
                if not goal['completed'] and st.button("Complete", key=f"goal_{i}"):
                    st.session_state.goals[i]['completed'] = True
                    update_points_and_level(20)
                    st.success("Goal completed! +20 points!")

def add_weekly_reflection():
    st.header("📝 Weekly Reflection")
    if 'reflections' not in st.session_state:
        st.session_state.reflections = []
    
    col1, col2 = st.columns(2)
    with col1:
        highlights = st.text_area("Week's Highlights:")
    with col2:
        learnings = st.text_area("Key Learnings:")
    
    next_steps = st.text_area("Next Week's Focus:")
    
    if st.button("Save Reflection"):
        reflection = {
            "date": datetime.now(),
            "highlights": highlights,
            "learnings": learnings,
            "next_steps": next_steps
        }
        st.session_state.reflections.append(reflection)
        update_points_and_level(15)
        st.success("Reflection saved! +15 points!")

def add_skill_tree():
    st.header("🌳 Skill Tree")
    skills = {
        "Mindfulness": ["Meditation", "Breathing", "Present Awareness"],
        "Productivity": ["Time Management", "Goal Setting", "Focus"],
        "Learning": ["Reading", "Note-taking", "Teaching Others"]
    }
    
    if 'skill_levels' not in st.session_state:
        st.session_state.skill_levels = {skill: 0 for category in skills.values() for skill in category}
    
    for category, category_skills in skills.items():
        st.subheader(category)
        cols = st.columns(len(category_skills))
        for i, skill in enumerate(category_skills):
            with cols[i]:
                current_level = st.session_state.skill_levels[skill]
                st.write(f"{skill}: Level {current_level}")
                if st.button(f"Level Up {skill}", key=f"skill_{skill}"):
                    st.session_state.skill_levels[skill] += 1
                    update_points_and_level(10)
                    st.success(f"{skill} leveled up! +10 points!")

# Main app
st.title("🚀 Exciting Growth Mindset Challenge")

# Your existing sidebar
with st.sidebar:
    st.markdown(f"### {st.session_state.avatar} Your Stats")
    st.markdown(f"**Level:** {st.session_state.level}")
    st.markdown(f"**Points:** {st.session_state.points}")
    st.markdown(f"**Streak:** {st.session_state.streak} days 🔥")
    
    st.markdown("### Choose Your Avatar")
    avatars = ["🧑", "👩", "👨", "🧙", "🦸", "🦹", "🧚", "🧛", "🧜", "🧝", "🧞", "🧟"]
    cols = st.columns(4)
    for i, avatar in enumerate(avatars):
        if cols[i % 4].button(avatar, key=f"avatar_{i}"):
            st.session_state.avatar = avatar
            st.success(f"Avatar changed to {avatar}")

# Daily quote
if st.session_state.daily_quote == "":
    st.session_state.daily_quote = random.choice(quotes)
st.markdown(f'<p class="quote">{st.session_state.daily_quote}</p>', unsafe_allow_html=True)

# All tabs (existing + new)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎯 Daily Challenge", "📊 Progress Tracker", "🏆 Achievements", 
    "🧠 Mind Gym", "📌 Goals", "📝 Reflection", "🌳 Skills"
])

# Your existing tabs
with tab1:
    st.header("🎯 Daily Challenge")
    challenge = random.choice(challenges)
    st.markdown(f'<p class="big-font">{challenge}</p>', unsafe_allow_html=True)
    if st.button("Complete Challenge"):
        update_points_and_level(10)
        st.session_state.streak += 1
        st.session_state.completed_challenges.append(challenge)
        st.balloons()
        st.success(f"🎉 Challenge completed! You earned 10 points!")
        check_achievements()

with tab2:
    st.header("📊 Progress Tracker")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        progress = st.slider("Rate your progress (0-100)", 0, 100, 50)
    with col2:
        mood = st.select_slider("How's your mood?", options=["😢", "😐", "😊", "😄", "🤩"])
    with col3:
        energy = st.select_slider("Energy level?", options=["🔋", "🔋🔋", "🔋🔋🔋", "🔋🔋🔋🔋", "🔋🔋🔋🔋🔋"])
    
    if st.button("Log Progress"):
        new_data = pd.DataFrame({
            'Date': [datetime.now()],
            'Progress': [progress],
            'Mood': [mood],
            'Energy': [energy]
        })
        st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_data], ignore_index=True)
        update_points_and_level(5)
        st.success("Progress logged! You earned 5 points!")
        check_achievements()
    
    if not st.session_state.progress_data.empty:
        fig = px.line(st.session_state.progress_data, x='Date', y='Progress', title='Your Growth Journey')
        st.plotly_chart(fig)
        
        fig_mood = px.scatter(st.session_state.progress_data, x='Date', y='Mood', color='Energy', 
                              title='Mood and Energy Tracker', size_max=10)
        st.plotly_chart(fig_mood)

with tab3:
    st.header("🏆 Achievements")
    for achievement, description in achievements.items():
        if achievement in st.session_state.achievements:
            st.markdown(f'<div class="achievement">{achievement}: {description}</div>', unsafe_allow_html=True)
    
    if not st.session_state.achievements:
        st.info("Complete challenges and maintain streaks to unlock achievements!")

with tab4:
    st.header("🧠 Mind Gym")
    st.subheader("Quick Brain Teaser")
    
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    question = f"What's {num1} {operation} {num2}?"
    user_answer = st.number_input(question, value=0, step=1)
    
    if st.button("Check Answer"):
        correct_answer = eval(f"{num1} {operation} {num2}")
        if user_answer == correct_answer:
            update_points_and_level(3)
            st.success("Correct! You earned 3 points!")
        else:
            st.error(f"Not quite. The correct answer is {correct_answer}. Keep practicing!")
    
    st.subheader("Mindfulness Moment")
    if 'meditation_start' not in st.session_state:
        st.session_state.meditation_start = None
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Start 1-Minute Meditation"):
            st.session_state.meditation_start = time.time()
    with col2:
        if st.button("Reset Timer"):
            st.session_state.meditation_start = None
    
    if st.session_state.meditation_start is not None:
        elapsed_time = int(time.time() - st.session_state.meditation_start)
        remaining_time = max(60 - elapsed_time, 0)
        
        progress = min(elapsed_time / 60, 1.0)
        progress_bar = st.progress(progress)
        
        if remaining_time > 0:
            st.markdown(f"### ⏱️ Time remaining: {remaining_time} seconds")
            st.markdown("🧘‍♀️ Close your eyes and focus on your breath...")
            time.sleep(3)
            st.rerun()
        else:
            st.session_state.meditation_start = None
            st.success("🎉 Meditation complete! You've earned 5 points for mindfulness.")
            st.balloons()
            update_points_and_level(5)

# New tabs
with tab5:
    add_goals_feature()

with tab6:
    add_weekly_reflection()

with tab7:
    add_skill_tree()

# Your existing footer
st.markdown("---")
st.markdown("Remember, every small step counts towards your growth! 🌱")
if st.button("Share Your Progress"):
    share_text = f"""
    🚀 My Growth Mindset Journey:
    Level: {st.session_state.level}
    Points: {st.session_state.points}
    Streak: {st.session_state.streak} days
    Achievements: {len(st.session_state.achievements)}
    Latest Mood: {st.session_state.progress_data['Mood'].iloc[-1] if not st.session_state.progress_data.empty else 'Not logged yet'}
    """
    st.code(share_text)
    st.success("Copy the text above to share your amazing progress!")