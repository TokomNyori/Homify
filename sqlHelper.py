from cs50 import SQL
import os

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///home.db")

sqlTables = ['properties', 'bhk_types', 'bhk_details', 'facade_images',
             'interiors', 'nearby', 'features', 'property_audios']
# Other tables: partners

'''
justin = db.execute("SELECT id FROM gamify")
if not justin:
    gamers = db.execute("INSERT INTO gamify (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                        1.0, 'Tokom', 'Nyori', 'Male', '+91', '4521365478', 'tyrfd@jhv', 'yhtfchgchg')
else:
    g_id = justin[-1]['id']
    g_id = g_id + 1.0
    gamers = db.execute("INSERT INTO gamify (id, first_name, last_name, gender, isd_code, phone_number, email_id, hash) VALUES(?,?,?,?,?,?,?,?)",
                        g_id, 'koj', 'Page', 'Male', '+91', '4521365478', 'tyrfd@jhv', 'yhtfchgchg')
'''

'''
update = db.execute(
    "CREATE TABLE user_surveys (sl_no INTEGER, u_id REAL NOT NULL, p_id INTEGER NOT NULL, p_name TEXT, type TEXT, price INTEGER, survey_date_txt TEXT, survey_date DATETIME, PRIMARY KEY(sl_no))")
'''

'''
DROP = db.execute("DROP TABLE user_surveys")
'''

'''
deletee = db.execute("DELETE FROM partners WHERE id = 31")
'''

'''
insert = db.execute("INSERT INTO user_homes (u_id, p_id, p_name, type, price) VALUES(?,?,?,?,?)",
                    5.0, 12, 'james towers', '4 BHK', 195)
'''


'''
db.execute(
    "UPDATE bhk_details SET pricing_four_plus = ? WHERE property_id BETWEEN ? AND ?", 155, 1, 100)
'''
# ju = db.execute("DELETE FROM users")
