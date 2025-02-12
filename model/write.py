import pyrebase
import urllib

firebaseConfig = {
        'apiKey': "AIzaSyBAykN0AhVRw6BwVVl3z3iGrSq1ht7ZjBU",
        'authDomain': "fir-cd-930d6.firebaseapp.com",
        'databaseURL': "https://fir-cd-930d6-default-rtdb.firebaseio.com",
        'projectId': "fir-cd-930d6",
        'storageBucket': "fir-cd-930d6.firebasestorage.app",
        'messagingSenderId': "540343245106",
        'appId': "1:540343245106:web:a2f757c8dcac2272281f2b",
        'measurementId': "G-BBXHR4FVVJ"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# Authentication
'''auth = firebase.auth()

#Signup
email = input("Enter your email: ")
password = input("Enter your password: ")
confirm_password = input("Enter your password: ")
if password == confirm_password:
    try:
        auth.create_user_with_email_and_password(email, password)
    except Exception:
        print('Account exists, sign in')
        
        
#Login
email = input("Enter your email: ")
password = input("Enter your password: ")
try:
    auth.sign_in_with_email_and_password(email, password)
    
except Exception:
    print('Invalid email!')'''
    
    
# User Data Storage
'''storage = firebase.storage()

# Upload file
filename = 'peom.txt'
cloud_filename = 'Poem/My love peom/peom.txt'
storage.child(cloud_filename).put(filename)

print(storage.child(cloud_filename).get_url(None))

# Download file
cloud_filename_to_download_from = 'My love peom'
storage.child(cloud_filename_to_download_from).download('', 'dove.txt')

# code to read data from the url
url = storage.child(cloud_filename_to_download_from).get_url(None)
peom = urllib.request.urlopen(url).read()
print(peom)'''

# Database
'''sp = {
    'Name': 'Bruce Wayne',
    'Superhero Name': 'Batman',
    'Age': 30,
    'Job': 'CEO of Wayne Enterprises',
    'Parents Dead?': True
}
database = firebase.database()
# Create user info in database
# This to just push user info to database
database.child('superheroes').push(sp)
# This to push user info to database and set unique user id
database.child('superheroes').child('smart').set(sp)

# Update user info in database knowing the user id
database.child('superheroes').child('speed').update({'Name': 'Harrison Wells', 'Superhero Name': 'Reverse Flash'})

# Update user info in database without knowing the user id
sups = database.child('superheroes').get()
for heroes in sups.each():
    if heroes.val()['Name'] == 'Clark Kent':
        database.child('superheroes').child(heroes.key()).update({'Name': 'Bruce Wayne'})

# Delete user info in database knowing the user id
database.child('superheroes').child('speed').remove()

# Delete user info in database without knowing the user id
sups = database.child('superheroes').get()
for heroes in sups.each():
    if heroes.val()['Name'] == 'Clark Kent':
        database.child('superheroes').child(heroes.key()).remove(   )




# Read user info from the database
sups = database.child('superheroes').order_by_child('Parents Dead?').equal_to(True).get()
for i in sups.each():
    print(i.val()['Name'])

# To set range of age you want to read
sups = database.child('superheroes').order_by_child('Age').start_at(20).end_at(28).get()
for i in sups.each():
    print(i.val())
    
# To limit the number the number of results
sups = database.child('superheroes').order_by_child('Age').start_at(25).limit_to_first(1).get()
for i in sups.each():
    print(i.val())'''