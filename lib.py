import random
import itertools
import os
import json

data = {
    "employees": ["Lu", "Cri", "Coli", "Ayi", "Ferdaus", "Islam", "Saiful", "Xili", "Ashraful", "JD", "Hosen"],
    "days": ["Lunedì", "Martedì", "Mercoledì", "Giovedì"],
    "same_day_pairs": [["Ferdaus", "Saiful"]],
    "different_day_pairs": [["Lu", "Cri"], ["Coli", "Ayi"], ["Ferdaus", "Islam"]]
}

# Path to the JSON file
file_path = 'data.json'

# Check if the file exists
if os.path.exists(file_path):
    # File exists, read and load the data
    with open(file_path, 'r') as f:
        restored_data = json.load(f)
    print("Data restored successfully.")
    data = restored_data
else:
    print("The file does not exist. No data restored.")

def set_employees(new_employees):
    data["employees"] = new_employees
    # Writing the updated data back to the file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def valid_day_assignment(schedule, max_per_day=3):
    # Check for max 3 people per day constraint
    day_counts = {day: list(schedule.values()).count(day) for day in set(schedule.values())}
    if any(count > max_per_day for count in day_counts.values()):
        return False
    return True

def solve_rest_days():
    # Generate all possible assignments
    all_possible_schedules = itertools.product(data["days"], repeat=len(data["employees"]))
    all_possible_schedules = list(all_possible_schedules)
    random.shuffle(all_possible_schedules)

    for schedule in all_possible_schedules:
        schedule_dict = dict(zip(data["employees"], schedule))

        # Check same day constraints
        if any(schedule_dict[a] != schedule_dict[b] for a, b in data["same_day_pairs"]):
            continue

        # Check different day constraints
        if any(schedule_dict[a] == schedule_dict[b] for a, b in data["different_day_pairs"]):
            continue

        # Check for max 3 people per day constraint
        if not valid_day_assignment(schedule_dict):
            continue

        return schedule_dict

    return None

def schedule_dict_to_weekly_schedule(schedule_dict):
    # Convert the schedule dictionary to a weekly schedule
    weekly_schedule = {day: [] for day in data["days"]}
    for employee, day in schedule_dict.items():
        weekly_schedule[day].append(employee)
    return weekly_schedule

def weekly_schedule_to_string(weekly_schedule):
    string = ""
    for day, employees in weekly_schedule.items():
        string += f"{day}: {', '.join(employees)}" + "\n"
    return string

def generate_weekly_schedule():
    schedule_dict = solve_rest_days()
    if schedule_dict:
        weekly_schedule = schedule_dict_to_weekly_schedule(schedule_dict)
        return weekly_schedule_to_string(weekly_schedule)
    else:
        return "No valid schedule found."
