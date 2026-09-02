from datetime import datetime
from collections import Counter


def analyze_user_activity(log_file_path: str) -> dict:
    action_counts = Counter()
    users = set()
    user_activity = Counter()
    login_times = {}
    session_times = []

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = [x.strip() for x in line.split(",")]

            timestamp = datetime.fromisoformat(parts[0])
            user_id = parts[1]
            action = parts[2]

            # นับจำนวน action
            action_counts[action] += 1

            # เก็บ user
            users.add(user_id)

            # นับกิจกรรมของ user
            user_activity[user_id] += 1

            # คำนวณ session
            if action == "login":
                login_times[user_id] = timestamp

            elif action == "logout":
                if user_id in login_times:
                    duration = (
                        timestamp - login_times[user_id]
                    ).total_seconds()

                    session_times.append(duration)
                    del login_times[user_id]

    # ค่าเฉลี่ย session time
    if session_times:
        average_session_time = sum(session_times) / len(session_times)
    else:
        average_session_time = 0.0

    # user ที่มีกิจกรรมมากที่สุด
    if user_activity:
        most_active_user = user_activity.most_common(1)[0][0]
    else:
        most_active_user = None

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": len(users)
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)
