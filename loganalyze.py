from collections import defaultdict
from datetime import datetime


def _is_valid_timestamp(ts: str) -> bool:
    try:
        datetime.fromisoformat(ts)
        return True
    except ValueError:
        return False


def analyze_user_activity(log_file_path: str) -> dict:
    users = set()
    action_counts = defaultdict(int)
    user_total_duration = defaultdict(float)
    login_durations = []

    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 4:
            continue

        timestamp, user_id, action, duration_str = parts

        if not _is_valid_timestamp(timestamp):
            continue

        try:
            duration = float(duration_str)
        except ValueError:
            continue

        users.add(user_id)
        action_counts[action] += 1
        user_total_duration[user_id] += duration

        if action == "login":
            login_durations.append(duration)

    total_users = len(users)

    most_active_user = None
    if user_total_duration:
        max_duration = max(user_total_duration.values())
        candidates = [u for u, d in user_total_duration.items() if d == max_duration]
        most_active_user = sorted(candidates)[0]

    average_session_time = (
        round(sum(login_durations) / len(login_durations), 2)
        if login_durations
        else 0.0
    )

    return {
        "total_users": total_users,
        "action_counts": dict(action_counts),
        "most_active_user": most_active_user,
        "average_session_time": average_session_time,
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint

    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}
