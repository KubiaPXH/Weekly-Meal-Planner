## Introduction

The need for this project is quite mundane :). After countless times asking the struggling questions: "What do we eat tonight/today?". I think I have to build up this simple **Weekly Meals Planner** to make our life easier. 

## How it works?

### Database
This Weekly Meals Planner using a really simple database which I built in Excel (can be found at [data](https://github.com/KubiaPXH/weekly_meal_planner/blob/main/data) folder), that includes:
- One dimensional table of dishes in Dishes sheet
- One dimensional table of ingredients in Ingredients sheet
- One fact table of relation between dishes and ingredient in Prep_Ingredients sheet

### The core
One of the reason I decided to use PowerBI is to make the visual more pleasant, but the most important thing is that PowerBI allow to intergrate Python code which I use to write a snippet for allocate dishes to weekdays. All PowerBI file and Python snippet can be found at [scr](https://github.com/KubiaPXH/weekly_meal_planner/tree/main/src) folder

## How to use it?
The **Weekly Meals Planner** need to be opened in PowerBI, its interface is below:

![weekly_meals_planner](https://user-images.githubusercontent.com/62499070/163591607-07b7db21-dfdb-409a-9215-7e32fd196e8a.png)

- The main part of the planner is the upper part where all dishes in the week are allocated in each weekday (to minimize cooking time, we only cook the dishes one time but each them for both lunch and dinner)
- The right lower part is the list of all ingredients we need to buy for the week and where to buy them
- The left lower part is the ingredients and recipe for choosen dish (we need to choose a dish to have the corresponding ingredients and recipe)

To generate a new meals plan for a new week: we can easily right click on Weekly_Meals_Table on Fields sidebar, then choose "Refresh data".
