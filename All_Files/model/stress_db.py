from model.write_db import Write_db
from datetime import datetime

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
