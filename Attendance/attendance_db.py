# Micropython code

import json

class AttendanceDB:
    # Known cards are stored in known_cards.json as {uid: name}
    # Attendance records are stored in attendance.json as {day: {uid: {check_in_time}, {check_out_time}}}

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


    def get_attendance_records_by_day(self, timestamp):
        attendance = self.load_json_file(self.attendance_filename)
        day = "{:02d}.{:02d}.{:04d}".format(timestamp[2], timestamp[1], timestamp[0])  # "DD.MM.YYYY"
        return attendance.get(day, {})

    def check_in(self, uid, timestamp):
        known_cards = self.load_json_file(self.known_cards_filename)
        if uid not in known_cards:
            return False, "Card not registered"
        
        attendance = self.load_json_file(self.attendance_filename)
        day = "{:02d}.{:02d}.{:04d}".format(timestamp[2], timestamp[1], timestamp[0])  # "DD.MM.YYYY"
        if day not in attendance:
            attendance[day] = {}
        
        if uid not in attendance[day]:
            attendance[day][uid] = []
        
        if len(attendance[day][uid]) is None:
            attendance[day][uid] = []
        
        if len(attendance[day][uid]) >= 2:
            return False, "Already checked in and out for today"
        elif len(attendance[day][uid]) == 1:
            message = "Checked out"
        elif len(attendance[day][uid]) == 0:
            message = "Checked in"

        attendance[day][uid].append("{:02d}:{:02d}:{:02d}".format(timestamp[4], timestamp[5], timestamp[6]))  # "HH:MM:SS"
        self.save_json_file(self.attendance_filename, attendance)
        return True, message
    
    def clear_db(self):
        self.save_json_file(self.attendance_filename, {})
        self.save_json_file(self.known_cards_filename, {})