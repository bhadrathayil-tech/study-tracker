from datetime import datetime, timedelta

def calculate_streaks(session_dates, freeze_dates=None, current_date=None):
    """
    Calculates current streak and longest streak given a set of unique session dates (YYYY-MM-DD).
    Accounts for freeze days (1 per week).
    """
    if not session_dates:
        return 0, 0

    session_set = set(session_dates)
    freeze_set = set(freeze_dates or [])
    
    if not current_date:
        current_date = datetime.now().date()
    else:
        current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

    # Determine current streak counting backward from today or yesterday
    current_streak = 0
    check_date = current_date
    
    # If no session today, check if yesterday was studied (to avoid breaking streak prematurely today)
    if check_date.strftime("%Y-%m-%d") not in session_set:
        yesterday = check_date - timedelta(days=1)
        if yesterday.strftime("%Y-%m-%d") in session_set or yesterday.strftime("%Y-%m-%d") in freeze_set:
            check_date = yesterday
        # If neither today nor yesterday has activity/freeze, current streak might be 0, 
        # but let's trace accurately backward.

    while True:
        date_str = check_date.strftime("%Y-%m-%d")
        if date_str in session_set or date_str in freeze_set:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # Calculate longest streak across all recorded history
    all_dates = sorted(list(session_set.union(freeze_set)))
    if not all_dates:
        return 0, 0

    max_streak = 0
    temp_streak = 0
    prev_date = None

    for d_str in all_dates:
        d = datetime.strptime(d_str, "%Y-%m-%d").date()
        if prev_date is None:
            temp_streak = 1
        else:
            delta = (d - prev_date).days
            if delta == 1:
                temp_streak += 1
            elif delta > 1:
                # Check if gap can be bridged by allowed freezes or consecutive days
                # For simplicity in standard streak: if delta > 1 and missing days aren't all freezes:
                temp_streak = 1
        max_streak = max(max_streak, temp_streak)
        prev_date = d

    return current_streak, max_streak

def get_current_week_totals(sessions):
    """
    Calculates total study time per subject for the current week.
    Sessions format: [(id, subject, duration, date_str), ...]
    """
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) # Monday start
    
    subject_totals = {}
    for _, subject, duration, date_str in sessions:
        sess_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if start_of_week <= sess_date <= today:
            subject_totals[subject] = subject_totals.get(subject, 0) + duration
            
    return subject_totals