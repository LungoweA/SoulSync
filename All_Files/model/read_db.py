from All_Files.model.write_db import Write_db


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

    def __init__(self, uid, id_token):
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
        email = self.write.database.child('Users').child(self.uid).child('Email').get(token=self.id_token)

        return name.val(), email.val()

    def read_journal(self):
        """
        Retrieves the user's journal entries from the Firebase Realtime Database.

        Returns:
            dict: A dictionary containing journal entries organized by date. Each date maps to a list of 
                tuples where each tuple contains the time and journal entry text.
            str: A message indicating that there are no journal entries if an error occurs.
        """
        
        self.journal_list = []
        journal_dict = {}
        self.entry_keys = []

        entries = self.write.database.child('Users').child(self.uid).child('Journal').get(token=self.id_token)
        self.journal_entries = entries.val()
        try:
            for i in entries.each():
                self.journal_list.append(i.val())
                self.entry_keys.append(i.key())

            for i in self.journal_list:
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
        self.stress_key = []
        self.stress_date = []
        stress_level = self.write.database.child('Users').child(self.uid).child('Stress').get(token=self.id_token)
        self.stress_result = stress_level.val()
        
        try:
            for i in stress_level.each():
                stress_level_list.append(i.val())
                self.stress_key.append(i.key())
            
            
            for i in stress_level_list:
                date = i['Created_at'].split(' ')[0]
                stress_history_dict[date] = i['Stress level']
                self.stress_date.append(i['Created_at'])
                
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
        self.mood_key = []
        self.mood_date = []
        mood_level = self.write.database.child('Users').child(self.uid).child('Mood').get(token=self.id_token)
        self.mood_result = mood_level.val()
        try:
            for i in mood_level.each():
                mood_level_list.append(i.val())
                self.mood_key.append(i.key())

            for i in mood_level_list:
                date = i['Created_at'].split(' ')[0]
                mood_history_dict[date] = [i['Mood description'], i['Mood influenced by'], i['Mood rating']]
                self.mood_date.append(i['Created_at'])

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
            self.mood_dates_list = list(self.read_mood_level().keys())
            self.mood_dates_list.sort()
            return self.mood_dates_list
        except Exception:
            return []

    def get_stress_dates(self):
        """
        Retrieves all the dates for which the user has stress tracker.

        Returns:
            list: A sorted list of dates (in string format) for the stress tracker.
        """
        try:
            self.stress_dates_list = list(self.read_stress_level().keys())
            self.stress_dates_list.sort()
            return self.stress_dates_list
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
        
        
    def delete_journal_entry(self, date):
        """
        Deletes a specific journal entry for the given date.

        This method retrieves the user's journal entries, identifies the entry 
        associated with the given date, and removes it from the Firebase database.

        Args:
            date (str): The date of the journal entry to be deleted.

        Returns:
            tuple: A boolean indicating success (True) or failure (False) along 
            with a corresponding message.
        """
    
        value = ''
        self.read_journal()
        for i in self.entry_keys:
            if self.journal_entries[i]['Created_at'] == date:
                value = i
        
        try:
            self.write.database.child('Users').child(self.uid).child('Journal').child(value).remove(self.id_token)
            return True, 'Journal entry has been deleted.'
            
        except Exception:
            return False, 'Unknown error occured!'
        
        
    def delete_stress_level(self, date):
        """
        Deletes the stress level entry for a given date.

        This method reads the user's stored stress levels, identifies the entry 
        for the specified date, and removes it from the Firebase database.

        Args:
            date (str): The date of the stress entry to be deleted.

        Returns:
            tuple: A boolean indicating success (True) or failure (False), 
            and a message string describing the result.
        """
    
        stress_date_time = ''
        stress_value = ''
        self.read_stress_level()
        self.get_stress_dates()
        
        if date not in self.stress_dates_list:
            return False, 'No stress history available!'
        
        for i in self.stress_date:
            if date in i:
                stress_date_time = i
        
        for i in self.stress_key:
            if self.stress_result[i]['Created_at'] == stress_date_time:
                stress_value = i
                
        try:
            self.write.database.child('Users').child(self.uid).child('Stress').child(stress_value).remove(self.id_token)
            return True, 'Stress level has been deleted.'
            
        except Exception:
            return False, 'Unknown error occurred!'
        
            
            
    def delete_mood_level(self, date):
        """
        Deletes a mood level entry for a given date.

        This method looks up the mood entry associated with the provided date and 
        removes it from the Firebase database.

        Args:
            date (str): The date of the mood entry to be deleted.

        Returns:
            tuple: A boolean indicating success (True) or failure (False), along with
            a corresponding message.
        """
    
        mood_date_time = ''
        mood_value = ''
        self.read_mood_level()
        self.get_mood_dates()
        
        if date not in self.mood_dates_list:
            return False, 'No mood history available!'
        
        for i in self.mood_date:
            if date in i:
                mood_date_time = i
                
        
        for i in self.mood_key:
            if self.mood_result[i]['Created_at'] == mood_date_time:
                mood_value = i
                
        try:
            self.write.database.child('Users').child(self.uid).child('Mood').child(mood_value).remove(self.id_token)
            return True, 'Mood level has been deleted.'
            
        except Exception:
            return False, 'Unknown error occurred!'
        
        
        