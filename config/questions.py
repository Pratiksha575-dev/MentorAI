# config/questions.py

# 20-Question Faculty Mentor Test
MENTOR_QUESTIONS = [
    # Extraversion (Communication)
    ("EXT", "I enjoy giving lectures and leading large group discussions."),
    ("EXT", "I prefer one-on-one advising over group advising."),
    ("EXT", "I easily start conversations with new students."),
    ("EXT", "I am quiet during faculty meetings."),

    # Neuroticism (Stress/Patience)
    ("EST", "I get easily stressed when students miss deadlines."),
    ("EST", "I remain calm even when a project is failing."),
    ("EST", "I worry about my students' academic performance."),
    ("EST", "I rarely feel overwhelmed by my advising load."),

    # Agreeableness (Empathy)
    ("AGR", "I am highly empathetic to students' personal struggles."),
    ("AGR", "I can be blunt and highly critical of students' work."),
    ("AGR", "I respect students' ideas even when they contradict mine."),
    ("AGR", "I believe I am always right when advising a project."),

    # Conscientiousness (Structure)
    ("CSN", "I expect students to follow a strict timeline and syllabus."),
    ("CSN", "I am okay with students taking a chaotic, unstructured approach."),
    ("CSN", "I pay close attention to the details of my students' code/writing."),
    ("CSN", "I often forget to reply to student emails."),

    # Openness (Innovation)
    ("OPN", "I encourage students to pursue highly experimental, risky ideas."),
    ("OPN", "I prefer students to use proven, traditional methodologies."),
    ("OPN", "I enjoy learning completely new frameworks alongside my students."),
    ("OPN", "I dislike it when students want to change the project direction.")
]

# 20-Question Student Teamwork Test
STUDENT_QUESTIONS = [
    # Extraversion (Communication)
    ("EXT", "I naturally take the lead during group brainstorming."),
    ("EXT", "I prefer to code or research quietly by myself."),
    ("EXT", "I feel comfortable presenting our project to the class."),
    ("EXT", "I let my teammates do most of the talking."),

    # Neuroticism (Stress)
    ("EST", "I get stressed easily as project deadlines approach."),
    ("EST", "I remain relaxed even the night before a presentation."),
    ("EST", "I worry a lot about the quality of our team's work."),
    ("EST", "I rarely feel overwhelmed by university assignments."),

    # Agreeableness (Teamwork)
    ("AGR", "I always make sure every team member feels heard."),
    ("AGR", "I am blunt and will criticize bad ideas immediately."),
    ("AGR", "I am willing to compromise my vision for the sake of the team."),
    ("AGR", "I often start arguments over how to approach a task."),

    # Conscientiousness (Structure)
    ("CSN", "I am always prepared for group meetings and deadlines."),
    ("CSN", "I often leave my part of the project until the last minute."),
    ("CSN", "I double-check all code and formatting before submitting."),
    ("CSN", "I tend to act impulsively without looking at the project plan."),

    # Openness (Innovation)
    ("OPN", "I have a highly creative approach to solving coding problems."),
    ("OPN", "I have difficulty understanding abstract theories."),
    ("OPN", "I enjoy brainstorming unusual, out-of-the-box ideas."),
    ("OPN", "I prefer straightforward, practical tasks over creative design.")
]

SCALE_OPTIONS = [1, 2, 3, 4, 5]
SCALE_LABELS = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly Agree"
}
