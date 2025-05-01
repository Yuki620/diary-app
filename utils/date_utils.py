from datetime import datetime

# Display entry dates in a user-friendly text format
def format_friendly_date(date_obj):
    today = datetime.now().date()
    entry_date = date_obj.date()
    delta = (today - entry_date).days

    if delta == 0:
        return 'Today'
    elif delta == 1:
        return 'Yesterday'
    elif delta < 7:
        return date_obj.strftime('%A') # eg. 'Monday'
    else:
        return date_obj.strftime('%b %d, %Y') # eg. May 01, 2025