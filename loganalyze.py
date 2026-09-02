from collections import defaultdict
from datetime import datetime


def analyze_user_activity(log_file_path: str) -> dict:
    """
    Expected log line format (whitespace separated):
        YYYY-MM-DD HH:MM:SS  user_id  action

    e.g. "2024-01-15 10:00:00 u001 login"
    """
    action_counts = defaultdict(int)
    user_action_counts = defaultdict(int)
    users = set()

    open_logins = {}          # user_id -> login timestamp (unmatched)
    session_durations = []    # completed login->logout durations, seconds

    with open(log_file_path, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 4:
                continue  # skip malformed lines

            date_str, time_str, user_id, action = parts[0], parts[1], parts[2], parts[3]

            try:
                timestamp = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue

            action_counts[action] += 1
            user_action_counts[user_id] += 1
            users.add(user_id)

            if action == "login":
                open_logins[user_id] = timestamp
            elif action == "logout" and user_id in open_logins:
                login_time = open_logins.pop(user_id)
                session_durations.append((timestamp - login_time).total_seconds())

    average_session_time = (
        sum(session_durations) / len(session_durations) if session_durations else 0.0
    )

    most_active_user = None
    if user_action_counts:
        most_active_user = max(sorted(user_action_counts), key=lambda u: user_action_counts[u])

    return {
        "action_counts": dict(action_counts),
        "average_session_time": average_session_time,
        "most_active_user": most_active_user,
        "total_users": len(users),
    }
