import cs50
from time import sleep

'''
For testing:
colors-appartments-sj.jpg
colors-appartments-ny.jpg
'''

def deleteTables(file, db):
    for i in file:
        db.execute(f"DELETE FROM {i}")


def insert_type(db):
    exOne = ['countryside appartments', 'paradise appartments', 'tradition society', 'beach appartments'] # 2, 3, 4, 4+ BHK
    exTwo = ['english society', 'greezers appartments', 'florian appartments', 'miami appartments'] # 3, 4, 4+ BHK
    exThree = ['sweet appartment', 'dream house', 'scott home',] # 4 BHK
    exFour = ['rivera appartment'] # 4+ BHK

    count = db.execute("SELECT count(id) FROM buildings")
    n = count[0]['count(id)']
    for i in range(n):
        ids = i + 1
        house = db.execute("SELECT name FROM buildings WHERE id = ?", ids)
        if house[0]['name'] in exOne:
            db.execute("INSERT INTO house_type (building_id, one_bhk, two_bhk, three_bhk, four_bhk, four_plus_bhk) VALUES(?, ?, ?, ?, ?, ?)",
                        ids, 0, 1, 1, 1, 1)
            print(f"Succesfully inserted {house[0]['name']} in exOne")
        elif house[0]['name'] in exTwo:
            db.execute("INSERT INTO house_type (building_id, one_bhk, two_bhk, three_bhk, four_bhk, four_plus_bhk) VALUES(?, ?, ?, ?, ?, ?)",
                        ids, 0, 0, 1, 1, 1)
            print(f"Succesfully inserted {house[0]['name']} in exTwo")
        elif house[0]['name'] in exThree:
            db.execute("INSERT INTO house_type (building_id, one_bhk, two_bhk, three_bhk, four_bhk, four_plus_bhk) VALUES(?, ?, ?, ?, ?, ?)",
                        ids, 0, 0, 0, 1, 0)
            print(f"Succesfully inserted {house[0]['name']} in exThree")
        elif house[0]['name'] in exFour:
            db.execute("INSERT INTO house_type (building_id, one_bhk, two_bhk, three_bhk, four_bhk, four_plus_bhk) VALUES(?, ?, ?, ?, ?, ?)",
                        ids, 0, 0, 0, 0, 1)
            print(f"Succesfully inserted {house[0]['name']} in exFour")
        # General insertion
        else:
            db.execute("INSERT INTO house_type (building_id, one_bhk, two_bhk, three_bhk, four_bhk, four_plus_bhk) VALUES(?, ?, ?, ?, ?, ?)",
                        ids, 1, 1, 1, 1, 1)
            print(f"Succesfully inserted {house[0]['name']} in general")




def insert_building(img, nm, psn, db):
    owner_id = db.execute("SELECT id FROM owners WHERE name = ?", nm)
    o_id = owner_id[0]['id']
    split = img.split('-')
    building = split[0] + ' ' + split[1]

    # San Jose
    if '-sj' in img:
        image = 'sanjose/' + img
        if psn == '1':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'bailey avenue street', 'san jose', 'california', 'USA')
            print('Done! psn:1')
        elif psn == '2':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'the alameda street', 'san jose', 'california', 'USA')
            print('Done! psn:2')
        elif psn == '3':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'blossom hill street', 'san jose', 'california', 'USA')
            print('Done! psn:3')

    # New York
    elif '-ny' in img:
        image = 'newyork/' + img
        if psn == '1':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        '1st broadway street', 'new york', 'new york', 'USA')
            print('Done! psn:1')
        elif psn == '2':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        '5th avenue street', 'new york', 'new york', 'USA')
            print('Done! psn:2')
        elif psn == '3':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'lexington street', 'new york', 'new york', 'USA')
            print('Done! psn:3')

    # San Francisco
    elif '-sf' in img:
        image = 'sanfrancisco/' + img
        if psn == '1':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        '5th lombard street', 'san francisco', 'california', 'USA')
            print('Done! psn:1')
        elif psn == '2':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'columbus avenue street', 'san francisco', 'california', 'USA')
            print('Done! psn:2')
        elif psn == '3':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'skyline boulevard street', 'san francisco', 'california', 'USA')
            print('Done! psn:3')

    # Miami
    elif '-mi' in img:
        image = 'miami/' + img
        if psn == '1':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'ocean drive street', 'miami', 'florida', 'USA')
            print('Done! psn:1')
        elif psn == '2':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'miracle mile street', 'miami', 'florida', 'USA')
            print('Done! psn:2')
        elif psn == '3':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'brickell avenue street', 'miami', 'florida', 'USA')
            print('Done! psn:3')

    # Houston
    elif '-ht' in img:
        image = 'houston/' + img
        if psn == '1':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'tacquard ranch street', 'houston', 'texas', 'USA')
            print('Done! psn:1')
        elif psn == '2':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        'old dikinson street', 'houston', 'texas', 'USA')
            print('Done! psn:2')
        elif psn == '3':
            db.execute("INSERT INTO buildings (owner_id, name, image, street, city, state, country) VALUES(?, ?, ?, ?, ?, ?, ?)", o_id, building , image,
                        '1st mcclendon street', 'houston', 'texas', 'USA')
            print('Done! psn:3')