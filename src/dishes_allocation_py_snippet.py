# 'dishes_df' holds the input data for this script
# useful link: Python in Power Query https://www.youtube.com/watch?v=bmwB24TbyDU

from calendar import weekday
from copy import copy
from random import random
from tkinter import W
from numpy import NaN, apply_along_axis
import pandas as pd
import random
import copy
import os.path

dishes_df = pd.read_excel(os.path.join(os.path.dirname(__file__), "../data/meals_planner_data.xlsx"), sheet_name='Dishes')

def create_weekly_meals_table(dishes_df):
    '''
    Create new dishes row for dishes whose Repeat Times > 1 -> complete pool of possible dishes
    e.g. if a dish has its Repeat Times = 2 -> 2 rows in dishes_df
    '''
    # Form a add_rows_df which contains the repeated dishes should be added
    add_rows_df = pd.DataFrame()
    for index, row in dishes_df[dishes_df['Repeat Times'] > 1].iterrows():
        for i in range(row['Repeat Times']-1):
            add_rows_df = pd.concat([add_rows_df,row], axis=1)

    add_rows_df_transposed = add_rows_df.T.reset_index()
    add_rows_df_transposed.drop(['index'], axis=1, inplace=True)

    # Add add_rows_df to the pooled dishes_df
    dishes_df = pd.concat([dishes_df,add_rows_df_transposed], ignore_index=True)
    dishes_df.drop(['Repeat Times'], axis=1, inplace=True)

    # Random sample the dishes from pooled dishes_df to the weekly_dishes
    nb_breakfast = 7
    nb_main_side_dishes = 6
    nb_nb_one_dish = 1
    breakfast_df = dishes_df[dishes_df['Category'] == "Breakfast"].sample(nb_breakfast)
    main_dish_df = dishes_df[dishes_df['Category'] == "Main dish"].sample(nb_main_side_dishes)
    side_dish_df = dishes_df[dishes_df['Category'] == "Side dish"].sample(nb_main_side_dishes)
    one_dish_df = dishes_df[dishes_df['Category'] == "One-dish"].sample(nb_nb_one_dish)
    dishes_df = pd.concat([breakfast_df,main_dish_df, side_dish_df, one_dish_df])
    
    return dishes_df

def allocate_dishes_to_weekday(weekly_dishes):
    def allocate_category_dishes(weekly_dishes, weekday_list, dish_type):
        for index, row in weekly_dishes[weekly_dishes['Category'] == dish_type].iterrows():
            weekday = weekday_list.pop(random.randint(0,len(weekday_list)-1))
            weekly_dishes.loc[index,'Weekday'] = weekday
        return weekly_dishes

    weekly_dishes = weekly_dishes.astype(
        {'Dish Name':'string',
        'Category':'category',
        'Cooking Time':'int32'
        }
        )
    
    '''
    Here we use weekday_list to generate a list of normal weekday
    But, an idea for further development: To create weekday based on current date time? how for next week?   
    '''
    weekday_list = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday'
        ]
    weekly_dishes['Weekday'] = NaN
    wkday_list = []
    wkday_list.append(copy.deepcopy(weekday_list))

    # First, assign breakfast to all the week
    weekly_dishes = allocate_category_dishes(weekly_dishes, wkday_list[0], 'Breakfast')

    # First, assign Saturday to One-dish as we should eat delicious things on Saturday
    for index, row in weekly_dishes[weekly_dishes['Category'] == 'One-dish'].iterrows():
        weekday = weekday_list.pop(5)
        weekly_dishes.loc[index,'Weekday'] = weekday

    # Then, assign other weekday to the remain dishes
    wkday_list.append(copy.deepcopy(weekday_list))
    wkday_list.append(copy.deepcopy(weekday_list))

    weekly_dishes = allocate_category_dishes(weekly_dishes, wkday_list[1], 'Main dish')
    weekly_dishes = allocate_category_dishes(weekly_dishes, wkday_list[2], 'Side dish')

    # After, map weekday to weekday number
    weekday_dict = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
        }
    weekly_dishes['Weekday Number'] = weekly_dishes['Weekday'].map(weekday_dict)

    # Finally, change all Category 'One-dish' to 'Main dish' and drop unecessary column (Cooking Time, Recipe)
    weekly_dishes.loc[weekly_dishes['Category'] == 'One-dish', 'Category'] = 'Main dish'
    weekly_dishes.drop(['Cooking Time', 'Recipe'], axis=1, inplace=True)

    return weekly_dishes

weekly_dishes = create_weekly_meals_table(dishes_df)
Weekly_Meals_Table = allocate_dishes_to_weekday(weekly_dishes)

print(Weekly_Meals_Table)