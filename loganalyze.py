from datetime import datetime
from collections import Counter


def analyze_user_activity(log_file_path: str) -> dict:
    action_counts = Counter()
    users = set()
    sessions = {}
    session_times = []

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            # รูปแบบ: timestamp,user_id,action
            parts = line.split(",")

            timestamp = datetime.fromisoformat(parts[0])
            user_id = parts[1]
            action = parts[2]

            action_counts[action] += 1
            users.add(user_id)

            # เก็บเวลา login และ logout
            if action == "login":
                sessions[user_id] = timestamp

            elif action == "logout" and user_id in sessions:
                duration = (timestamp - sessions[user_id]).total_seconds()
                session_times.append(duration)
                del sessions[user_id]

    # ค่าเฉลี่ยเวลา session
    average_session_time = (
        sum(session_times) / len(session_times)
        if session_times
        else 0.0
    )

    # หาผู้ใช้ที่มีกิจกรรมมากที่สุด
    user_activity = Counter()

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")
            user_id = parts[1]
            user_activity[user_id] += 1

    most_active_user = (
        user_activity.most_common(1)[0][0]
        if user_activity
        else None
    )

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": len(users)
    }


if __name__ == "main":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)
