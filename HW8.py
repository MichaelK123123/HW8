# Your name: Michael Keoleian
# Your student id: 2044 4110
# Your email: Keoleian@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # select all data from the restaurants table
    c.execute("SELECT * FROM restaurants")
    rows = c.fetchall()

    c.execute("SELECT * FROM buildings")
    rower = c.fetchall()

    dic = {}
    for row in rower:
        id = row[0]
        num = row[1]
        dic[id] = num


    # create a nested dictionary to store restaurant data
    rest_data = {}
    for row in rows:
        rest_name = row[1]
        category = row[2]
        building = row[3]
        rating = row[4]

        if category == 1:
            category = 'Cafe'
        elif category == 2:
            category = 'Deli'
        elif category == 3:
            category = 'Bubble Tea Shop'
        elif category == 4:
            category = 'Sandwich Shop'
        elif category == 5:
            category = 'Cookie Shop'
        elif category == 6:
            category = 'Bar'
        elif category == 7:
            category = 'Pizzeria'
        elif category == 8:
            category = 'Mexican Restaurant'
        elif category == 9:
            category = 'Korean Restaurant'
        elif category == 10:
            category = 'Asian Cuisine'
        elif category == 11:
            category = 'Mediterranean Restaurant'
        elif category == 12:
            category = 'Thai Restaurant'
        elif category == 13:
            category = 'Japanses Restaurant'
        elif category == 14:
            category = 'Juice Shop'

        building = dic.get(building)

        # add restaurant data to dictionary
        rest_data[rest_name] = {'category': category, 'building': building, 'rating': rating}

    # close the database connection and return the restaurant data
    conn.close()
    return rest_data

def plot_rest_categories(db):

    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get the restaurant categories and counts from the database
    c.execute("SELECT categories.category, COUNT(restaurants.id) FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category")
    rows = c.fetchall()
    result_dict = {row[0]: row[1] for row in rows}
    
    

    # Plot the bar chart
    plt.bar(result_dict.keys(), result_dict.values())
    plt.xlabel("Restaurant Categories")
    plt.ylabel("Number of Restaurants")
    plt.title("Number of Restaurants in Each Category")
    plt.show()

    # Close the database connection
    conn.close()
    
    return result_dict


def find_rest_in_building(building_num, db):

    conn = sqlite3.connect(db)
    c = conn.cursor()


    c.execute("SELECT restaurants.name,restaurants.rating,buildings.building FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id")
    rower = c.fetchall()

    lst = []
    s = sorted(rower, key = lambda x: x[1], reverse = True)
    for x in s:
        if building_num == x[2]:
            lst.append(x[0])
            
    return lst


#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    conn = sqlite3.connect(db)
    c = conn.cursor()


    c.execute("SELECT restaurants.name,restaurants.rating,buildings.building FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id")
    rower = c.fetchall()
    
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    load_rest_data('South_U_Restaurants.db')
    plot_rest_categories('South_U_Restaurants.db')
    find_rest_in_building(1101,'South_U_Restaurants.db' )
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
