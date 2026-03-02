"""
Personalized Guidance – multi-tier creative messages.
Shows ALL matching messages from Ventilator, Boundary Line, Backbencher Pride, and God Mode tiers.
"""

from typing import List, Dict, Any

PRIORITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


def _msg(observation: str, priority: str = "MEDIUM", action: str = "", impact: str = "", deadline: str = "None") -> Dict[str, Any]:
    return {
        "observation": observation,
        "action": action or "Review your progress and take action.",
        "impact": impact,
        "priority": priority,
        "deadline": deadline,
    }


def generate_guidance(student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    attendance = student_data.get("attendance", 0)
    internal_marks = student_data.get("internal_marks", 0)
    submission_rate = student_data.get("submission_rate", 0)
    predicted_score = student_data.get("predicted_score", 0)
    trend = student_data.get("attendance_trend", 0)
    external_marks = student_data.get("external_marks", 0)
    lecture_pct = student_data.get("lecture_pct", 0)
    prac_pct = student_data.get("practical_pct", student_data.get("prac_pct", 0))
    assignments_submitted = student_data.get("assignments_submitted", 0)
    assignments_total = student_data.get("assignments_total", 1)
    rank_in_batch = student_data.get("rank_in_batch")
    total_external = student_data.get("total_external", 75)
    total_internal = student_data.get("total_internal", 20)

    assign_pct = (assignments_submitted / assignments_total * 100) if assignments_total else submission_rate or 0
    external_pct = (external_marks / total_external * 100) if total_external and external_marks is not None else 0
    internal_pct = (internal_marks / total_internal * 100) if total_internal and internal_marks is not None else 0

    # ---------- "Ventilator" Tier (Absolute Danger Zone) ----------
    if attendance < 25:
        out.append(_msg(
            "Your attendance is extremely low (below 25%). In simple terms, you are missing almost all your classes.",
            "CRITICAL",
            "Action Plan: You need to start showing up for every single lecture and lab starting tomorrow. This is the only way to avoid being barred from exams.",
            "Impact: Attending classes will help you understand the topics better, which makes passing much easier and secures your eligibility.",
            "Deadline: Start from the very next class."
        ))
    if internal_marks is not None and internal_marks < 10:
        out.append(_msg(
            "Your internal exam marks are quite poor. You've scored less than half of what's expected.",
            "CRITICAL",
            "Action Plan: Meet your subject teacher to understand where you're going wrong. Focus your study on the most important chapters first.",
            "Impact: Good internal marks act as a safety net. They significantly boost your final result and reduce the pressure of the big final exams.",
            "Deadline: Before the next unit test or internal exam."
        ))
    if assignments_submitted == 0 and (assignments_total or 0) > 0:
        out.append(_msg(
            "You haven't submitted any assignments yet. This is like leaving free marks on the table.",
            "CRITICAL",
            "Action Plan: Even if they are late, finish and submit your pending assignments immediately. Don't let a 'Zero' pull down your entire grade.",
            "Impact: Assignments are the easiest way to score marks and show the faculty that you are putting in effort.",
            "Deadline: By the end of this week."
        ))

    # ---------- "Boundary Line" Tier (Barely Passing) ----------
    if predicted_score is not None and abs(predicted_score - 40) < 1:
        out.append(_msg(
            "You are walking on a thin line. Your predicted score is exactly at the passing mark of 40.",
            "HIGH",
            "Action Plan: You don't have any room for mistakes. Pick one area—either attendance or one specific topic—and improve it just a little bit more to be safe.",
            "Impact: Moving from 40 to 50 gives you a 'buffer'. It means even if one exam goes slightly bad, you will still pass overall.",
            "Deadline: Within the next 15 days."
        ))
    if total_external and external_marks is not None and external_marks > 0 and external_pct < 35:
        out.append(_msg(
            "Your theory exam scores are just barely scraping through. You need a stronger grasp of the concepts.",
            "MEDIUM",
            "Action Plan: Read the textbook more than the short notes. Try explaining the concepts to a friend to see if you really understand them.",
            "Impact: Theory carries the most weight in your final grade. Improving here is the fastest way to jump from a 'Pass' to a 'Good' grade.",
            "Deadline: Before the next major exam."
        ))

    # ---------- "Backbencher Pride" Tier (Average but Improving) ----------
    if trend == 1 and predicted_score is not None and 50 <= predicted_score <= 60:
        out.append(_msg(
            "Good news! Your performance is slowly but surely moving up. You're on the right track.",
            "LOW",
            "Action Plan: Don't stop now. Keep doing what you're doing and try to attend 1-2 more classes per week than you currently do.",
            "Impact: This steady progress will lead to a much better final result than you might expect. You're building solid momentum.",
            "Deadline: Keep this up for the rest of the semester."
        ))
    if external_marks is not None and internal_marks is not None and external_marks > internal_marks:
        out.append(_msg(
            "You're doing great in exams, but your internals (attendance/class tests) are lagging behind.",
            "LOW",
            "Action Plan: You clearly know the subject, so just focus on being more regular in class and submitting work on time.",
            "Impact: If your internals match your exam performance, your overall grade will jump from 'Average' to 'Excellent'.",
            "Deadline: None"
        ))
    if prac_pct is not None and lecture_pct is not None and prac_pct < 50 and lecture_pct >= 70:
        out.append(_msg(
            "Theory attendance is good but practical engagement is low. Improve practical performance.",
            "MEDIUM",
            "Focus: Practicals. Attend labs and complete practical work to balance overall performance.",
            "Better practicals positively affect your overall grade.",
            "This month"
        ))

    # ---------- "Backbencher Pride" Tier (Average but Improving) ----------
    if trend == 1 and predicted_score is not None and 50 <= predicted_score <= 60:
        out.append(_msg(
            "Your trajectory is improving. Maintain consistency to keep momentum.",
            "LOW",
            "Focus: Strengthen your weakest area (attendance, internals, or assignments) while sustaining gains.",
            "Target 65+. Small improvements across components lift the overall grade.",
            "None"
        ))
    if external_marks is not None and internal_marks is not None and external_marks > internal_marks:
        out.append(_msg(
            "External marks exceed internal marks. Balance both components.",
            "LOW",
            "Focus: Raise internal performance to match external strength for a stable overall grade.",
            "Strong internal and external scores yield the best overall results.",
            "None"
        ))
    if attendance < 60 and (predicted_score or 0) >= 70:
        out.append(_msg(
            "You are doing great in studies, but you're missing too many classes. This is risky for your attendance record.",
            "LOW",
            "Action Plan: You've already proven you're smart. Just make sure you attend enough classes to stay out of the 'short-attendance' list.",
            "Impact: Good grades are only useful if you're allowed to sit for the exam. Protect your hard work by being present.",
            "Deadline: Start attending regularly"
        ))

    # ---------- "God Mode" Tier (Top of the Food Chain) ----------
    if total_external and external_marks is not None and external_pct > 95:
        out.append(_msg(
            "Wow! Your theory exam performance is top-tier. You are one of the best in the batch.",
            "LOW",
            "Action Plan: Don't get overconfident. Keep the same study routine and make sure you don't ignore your internal tests or labs.",
            "Impact: Maintaining this level of excellence will make you a standout student and open great future opportunities.",
            "Deadline: Keep it up"
        ))
    if rank_in_batch == 1:
        out.append(_msg(
            "You are currently ranked #1 in your batch! That's a huge achievement.",
            "LOW",
            "Action Plan: The view from the top is great, but everyone is trying to catch up. Keep your focus steady across all subjects.",
            "Impact: Being the batch topper is not just about marks; it's about the consistency and discipline you're showing.",
            "Deadline: None"
        ))
    if assign_pct >= 100 and (predicted_score or 0) >= 90:
        out.append(_msg(
            "Your consistency is amazing. You're hitting 100% in assignments and top marks in predictions.",
            "LOW",
            "Action Plan: You've mastered the balance. Help a friend who is struggling—it will help you understand the topics even more deeply.",
            "Impact: This level of perfection shows you have a deep interest and strong work ethic. Keep shining!",
            "Deadline: None"
        ))

    # Fallback only when NO tier matched
    if not out:
        if (predicted_score or 0) >= 75:
            out.append(_msg(
                "You are performing really well. Just keep doing what you're doing.",
                "LOW",
                "Action Plan: Check if there's any small area where you're losing marks and try to fix it. Otherwise, you're all set.",
                "Impact: Staying consistent is the key to a great final degree. You're doing exactly that.",
                "Deadline: None"
            ))
        elif (predicted_score or 0) >= 50:
            out.append(_msg(
                "You are safe and in the passing zone, but you have the potential to reach the top.",
                "MEDIUM",
                "Action Plan: Identify which one is your weakest—attendance, assignments, or tests—and give it a little extra push this month.",
                "Impact: A small extra effort now can jump your grade from a 'C' to a 'B' or 'A'.",
                "Deadline: This month"
            ))
        else:
            out.append(_msg(
                "You are currently in the danger zone for failing. It's time to take serious action.",
                "HIGH",
                "Action Plan: Don't panic. Start by submitting all your pending work and attending every class. Every single mark counts right now.",
                "Impact: Focusing on the basics now will pull you back into the safe passing range and save your semester.",
                "Deadline: Starting today"
            ))

    # Sort by priority (CRITICAL first), return ALL matching messages (no limit)
    out.sort(key=lambda x: PRIORITY_ORDER.get(x["priority"], 0), reverse=True)
    return out


# Singleton for app
class GuidanceService:
    def generate_guidance(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return generate_guidance(student_data)


guidance_service = GuidanceService()
