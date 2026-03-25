# Micropython code

import json

class AttendanceDB:
    # Known cards are stored in known_cards.json as {uid: name}
    # Attendance records are stored in attendance.json as {day: {uid: [timestamps]}}

    def __init__(self, attendance_filename="attendance.json", known_cards_filename="known_cards.json"):
        self.attendance_filename = attendance_filename
        self.known_cards_filename = known_cards_filename

    def load_json_file(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    
    def save_json_file(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f)


    def register_card(self, uid, name):
        known_cards = self.load_json_file(self.known_cards_filename)
        known_cards[uid] = name
        self.save_json_file(self.known_cards_filename, known_cards)


    def check_in(self, uid, timestamp):
        known_cards = self.load_json_file(self.known_cards_filename)
        if uid not in known_cards:
            return False
        
        attendance = self.load_json_file(self.attendance_filename)
        day = timestamp[2] + "." + timestamp[1] + "." + timestamp[0]  # "DD.MM.YYYY" - assuming timestamp is [YYYY, MM, DD, ...]
        if day not in attendance:
            attendance[day] = {}
        if uid not in attendance[day]:
            attendance[day][uid] = []
        attendance[day][uid].append(timestamp[4] + ":" + timestamp[5] + ":" + timestamp[6])  # "HH:MM:SS" - assuming timestamp is [YYYY, MM, DD, W, HH, MM, SS]
        self.save_json_file(self.attendance_filename, attendance)
        return True