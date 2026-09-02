from collections import Counter, defaultdict


def analyze_user_activity(log_file_path: str) -> dict:
    users = set()
    action_counts = Counter()
    user_activity = Counter()
    session_times = []

    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()

                # ข้ามบรรทัดที่ข้อมูลไม่ครบหรือผิดรูปแบบ
                if len(parts) != 4:
                    continue

                timestamp, user_id, action, duration = parts

                try:
                    duration = float(duration)
                except ValueError:
                    continue

                # เก็บข้อมูลผู้ใช้และจำนวน Action
                users.add(user_id)
                action_counts[action] += 1
                user_activity[user_id] += 1

                # เก็บระยะเวลา
                session_times.append(duration)

    except (FileNotFoundError, OSError):
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0
        }

    # หาค่าเฉลี่ยระยะเวลา
    if session_times:
        average_session_time = sum(session_times) / len(session_times)
    else:
        average_session_time = 0.0

    # หาผู้ใช้ที่มีกิจกรรมมากที่สุด
    if user_activity:
        most_active_user = max(
            user_activity,
            key=user_activity.get
        )
    else:
        most_active_user = None

    return {
        "total_users": len(users),
        "action_counts": dict(action_counts),
        "most_active_user": most_active_user,
        "average_session_time": average_session_time
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")

    from pprint import pprint
    pprint(result)
