from model.write_db import Write_db

class Read_db:
    """
    A class for reading user data from Firebase Realtime Database related to journal entries, mood levels, 
    stress levels, and user details. This class interacts with Firebase to retrieve the user's data and 
    provide it in a structured format.

    Attributes:
        write (Write_db): An instance of the Write_db class used for database operations.
        uid (str): The unique user ID for the logged-in user.
        id_token (str): The authentication token for the user.

    Methods:
        read_user_details: Retrieves user details (name, password, email) from the database.
        read_journal: Retrieves the user's journal entries from the database.
        read_stress_level: Retrieves the user's stress levels from the database.
        read_mood_level: Retrieves the user's mood levels from the database.
        get_journal_dates: Returns a sorted list of dates for which the user has journal entries.
        get_mood_stress_dates: Returns a sorted list of unique dates for mood and stress records.
    """
    
    
    def __init__(self, uid=0, id_token=0):
        """
        Initializes the Read_db instance with user ID and authentication token.

        Args:
            uid (str): The unique user ID.
            id_token (str): The authentication token for the user.
        """
        
        self.write = Write_db()
        self.uid = uid
        self.id_token = id_token
        
        
    def read_user_details(self):
        """
        Retrieves user details (name, password, email) from the Firebase Realtime Database.

        Returns:
            tuple: A tuple containing the user's name, password, and email.
        """
        
        name = self.write.database.child('Users').child(self.uid).child('Name').get(token=self.id_token)
        password = self.write.database.child('Users').child(self.uid).child('Password').get(token=self.id_token)
        email = self.write.database.child('Users').child(self.uid).child('Email').get(token=self.id_token)
        
        return name.val(), password.val(), email.val()
        
        
    def read_journal(self):
        """
        Retrieves the user's journal entries from the Firebase Realtime Database.

        Returns:
            dict: A dictionary containing journal entries organized by date. Each date maps to a list of 
                tuples where each tuple contains the time and journal entry text.
            str: A message indicating that there are no journal entries if an error occurs.
        """
        
        journal_list = []
        journal_dict = {}
        
        entries = self.write.database.child('Users').child(self.uid).child('Journal').get(token=self.id_token)
        try:
            for i in entries.each():
                journal_list.append(i.val())
                
            for i in journal_list:
                date = i['Created_at'].split(' ')[0]
                time = i['Created_at'].split(' ')[1]
                
                
                if date in journal_dict and (time, i['Entry']) not in journal_dict[date]:
                    journal_dict[date].append((time, i['Entry']))
                else:
                    journal_dict[date] = [(time, i['Entry'])]
                
            return journal_dict
        except Exception:
            return {}
        
            
    
    def read_stress_level(self):
        """
        Retrieves the user's stress levels from the Firebase Realtime Database.

        Returns:
            dict: A dictionary containing stress levels organized by date. Each date maps to the stress level.
            Exception: If an error occurs during the retrieval process, the error is returned.
        """
        
        stress_level_list = []
        stress_history_dict = {}
        
        stress_levels = self.write.database.child('Users').child(self.uid).child('Stress').get(token=self.id_token)
        try:
            for i in stress_levels.each():
                stress_level_list.append(i.val())
            
            for i in stress_level_list:
                date = i['Created_at'].split(' ')[0]
                stress_history_dict[date] = i['Stress level']
                
            return stress_history_dict
        except Exception:
            return {}
    
    
    def read_mood_level(self):
        """
        Retrieves the user's mood levels from the Firebase Realtime Database.

        Returns:
            dict: A dictionary containing mood levels organized by date. Each date maps to a list containing
                the mood description, mood influence, and mood rating.
            Exception: If an error occurs during the retrieval process, the error is returned.
        """
        
        mood_level_list = []
        mood_history_dict = {}
        
        mood_levels = self.write.database.child('Users').child(self.uid).child('Mood').get(token=self.id_token)
        try:
            for i in mood_levels.each():
                mood_level_list.append(i.val())
            
            for i in mood_level_list:
                date = i['Created_at'].split(' ')[0]
                mood_history_dict[date] = [i['Mood description'], i['Mood influenced by'], i['Mood rating']]
            
            return mood_history_dict
        except Exception:
            return {}
        
        
    def get_journal_dates(self):
        """
        Retrieves all the dates for which the user has journal entries.

        Returns:
            list: A sorted list of dates (in string format) for the journal entries.
        """
        try:
            journal_dates = list(self.read_journal().keys())
            journal_dates.sort()
            return journal_dates
        except Exception:
            return []
        
        
    def get_mood_dates(self):
        """
        Retrieves all the dates for which the user has mood tracker.

        Returns:
            list: A sorted list of dates (in string format) for the mood tracker.
        """
        try:
            mood_dates = list(self.read_mood_level().keys())
            mood_dates.sort()
            return mood_dates
        except Exception:
            return []
        
        
    def get_stress_dates(self):
        """
        Retrieves all the dates for which the user has stress tracker.

        Returns:
            list: A sorted list of dates (in string format) for the stress tracker.
        """
        try:
            stress_dates = list(self.read_stress_level().keys())
            stress_dates.sort()
            return stress_dates
        except Exception:
            return []
    
    
    def get_mood_stress_dates(self):
        """
        Retrieves all unique dates for mood and stress records.

        Returns:
            list: A sorted list of unique dates for both mood and stress records.
        """
        
        try:
            mood_dates = self.read_mood_level().keys()
            stress_dates = self.read_stress_level().keys()
            dates_set = set(stress_dates)
            dates_set.update(set(mood_dates))
            dates_list = list(dates_set)
            dates_list.sort()
            return dates_list
        
        except Exception:
            return []



