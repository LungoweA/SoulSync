from model.write_db import Write_db
from datetime import datetime

class Stress_db:
    def __init__(self):
        self.sums = 0
        self.total = 25
        self.db = Write_db()
        
    def stress_test(self):
        questions = ["I often have difficulty concentrating.", "I often forget meetings or the names of people I know very well.",
                    "I get easily angered and sometimes lose my composure which is abnormal for me.",
                    "Sometimes I sleep restlessly, wake at night, and don't feel rested after a night's sleep.",
                    "I get abnormally tired from daily chores and socializing with others."]
        
        return questions

    def result(self, sum):
        score = (sum/self.total) * 100

        if 80 <= score <= 100:
            return "Low"
        elif 40 < score < 80:
            return "Moderate"
        elif score <= 40:
            return "High"
        
    def exercises(self):
        exercise_dict = {"Low": ["Walking or Light Jogging", "Yoga (Gentle Flow or Hatha Yoga)", "Cycling (Recreational)",
                                "Bodyweight Strength Training", "Swimming"],
                        "Moderate": ["Brisk Walking (Outside, If Possible)", "Strength Training", "Pilates or Vinyasa Yoga",
                                    "Dancing or Zumba", "Tai Chi"],
                        "High": ["Slow, Controlled Breathing Exercises", "Gentle Yoga (Restorative or Yin Yoga)", "Progressive Muscle Relaxation",
                                "Light Stretching or Foam Rolling", "Nature Walks or Forest Bathing"]}
        
        return exercise_dict
    
    def tips(self):
        tip_dict = {"Low": ["Stay Active e.g. exercise regularly", "Maintain Good Sleep", "Practice Gratitude",
                            "Enjoy Hobbies", "Stay Social"],
                    "Moderate": ["Take Short Breaks e.g. use the Pomodoro technique.", "Try Deep Breathing e.g. practice box breathing.",
                                "Reduce Stimulants like caffeine and processed sugar.", "Practice Mindful Journaling", "Listen to Music"],
                    "High": ["Limit Social Media & News", "Sleep Well e.g. aim for 7-9 hours", "Eat A Healthy Diet e.g. focus on stress reducing food",
                            "Try Laugh Therapy", "Engage In A Distraction Activity e.g. play a game or puzzle"]}
        
        return tip_dict
        
    def quotes(self):
        quote_dict = {"Low": [("Robert Brault", "Enjoy the little things, for one day you may look back and realize they were the big things."),
                            ("Thomas Merton", "Happiness is not a matter of intensity but of balance, order, rhythm, and harmony.")],
                    "Moderate": [("Robert H. Schuller", "Tough times never last, but tough people do."), ("Anne Lamott",
                                "Almost everything will work again if you unplug it for a few minutes… including you.")],
                    "High": [("Persian Proverb", "This too shall pass. No storm lasts forever."), ("Brené Brown",
                                "Give yourself the same care and kindness you so freely give to others.")]}
    
        return quote_dict
    
    
    def save_data(self, id_token, result):
        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        stress_data = {"Stress level": result,
                        "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            self.db.database.child("Users").child(user_id).child("Stress").push(stress_data, id_token)
        except Exception as err:
            return err
        
    
    
class Journal_db:
    
    def __init__(self):
        self.db = Write_db()
        
        
    def save(self, id_token, journal):
        # Saving data to Firebase
        user_id = self.db.auth.get_account_info(id_token)['users'][0]['localId']
        journal_data = {"Entry": journal,
                        "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        try:
            self.db.database.child("Users").child(user_id).child("Journal").push(journal_data, id_token)
        except Exception as err:
            return err
        
        
        