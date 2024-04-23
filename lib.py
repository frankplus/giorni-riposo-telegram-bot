import random
import os
import json
from constraint import Problem

# Restore data containing problem constraints or set default data
def restore_data_or_default():
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
        print("The file does not exist. No data restored. Setting default data")
        data = {
            "employees": ["Lu", "Cri", "Ayi", "Ferdaus", "Islam", "Saiful", "Ashraful", "JD", "Hosen"],
            "days": ["Lunedì", "Martedì", "Mercoledì", "Giovedì"],
            "same_day_pairs": [["Ferdaus", "Saiful"]],
            "different_day_pairs": [["Lu", "Cri"], ["Cri", "Ayi"], ["Ferdaus", "Islam"], ["Lu", "Islam"]],
            "preferences": {"Cri": "Lunedì", "Ayi": "Martedì"}
        }

    return data

constraints_data = restore_data_or_default()

def solve_rest_days():

    # Initialize the problem
    problem = Problem()

    # Define the days and max number of people per day
    max_people_per_day = 3

    # Add variables for each employee, each can take any of the given days
    for employee in constraints_data['employees']:
        problem.addVariable(employee, constraints_data['days'])

    # Constraint: No more than max_people_per_day can rest on the same day
    for day in constraints_data['days']:
        problem.addConstraint(lambda *args, day=day: args.count(day) <= max_people_per_day, constraints_data['employees'])

    # Constraint: Some pairs must rest on the same day
    for pair in constraints_data['same_day_pairs']:
        problem.addConstraint(lambda x, y: x == y, pair)

    # Constraint: Some pairs must not rest on the same day
    for pair in constraints_data['different_day_pairs']:
        problem.addConstraint(lambda x, y: x != y, pair)

    # Constraint: Fixed day preferences for some employees
    if 'preferences' in constraints_data:
        for employee, day in constraints_data['preferences'].items():
            problem.addConstraint(lambda x, day=day: x == day, [employee])

    # Get solutions
    solutions = problem.getSolutions()

    # return a solution randomly
    return random.choice(solutions) if solutions else None

def schedule_dict_to_weekly_schedule(schedule_dict):
    # Convert the schedule dictionary to a weekly schedule
    weekly_schedule = {day: [] for day in constraints_data["days"]}
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

def describe_scheduling_constraints():
    # Extract data
    employees = ', '.join(constraints_data['employees'])
    days = ', '.join(constraints_data['days'])
    same_day_pairs = ', '.join([' e '.join(pair) for pair in constraints_data['same_day_pairs']])
    different_day_pairs = ', '.join([' e '.join(pair) for pair in constraints_data['different_day_pairs']])

    # Format preferences for easier readability in the output
    if 'preferences' in constraints_data:
        preferences_list = [f"{employee} {day}" for employee, day in constraints_data['preferences'].items()]
        preferences = ', '.join(preferences_list)
    else:
        preferences = "nessuna"
    
    # Compose the message
    message = (
        f"I dipendenti del ristorante sono: {employees}. "
        f"I giorni disponibili per il riposo sono: {days}. "
        f"Ogni giorno, un massimo di 3 persone può riposare. "
        f"Alcune coppie di dipendenti devono riposare lo stesso giorno: {same_day_pairs}. "
        f"Altre coppie non devono riposare lo stesso giorno: {different_day_pairs}. "
        f"Preferenze di giorni fissi: {preferences}."
    )
    
    return message

# Process the constraints specified in natural language into a structured object
def process_constraints_to_object(constraints_text):
    # Define the API key and setup
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    example_data = {
        "employees": ["Lu", "Cri", "Ayi", "Ferdaus", "Islam", "Saiful", "Ashraful", "JD", "Hosen"],
        "days": ["Lunedì", "Martedì", "Mercoledì", "Giovedì"],
        "same_day_pairs": [["Ferdaus", "Saiful"]],
        "different_day_pairs": [["Lu", "Cri"], ["Cri", "Ayi"], ["Ferdaus", "Islam"], ["Lu", "Islam"]],
        "preferences": {"Cri": "Lunedì", "Ayi": "Martedì"}
    }

    example_output = str(example_data)

    # Prepare the prompt for the language model
    prompt = f"Translate the following problem constraints into a structured object in json format :\n\n{constraints_text}\n\n" \
            f"The output should have the same structure of this example:\n\n{example_output}"
    
    print(prompt)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={ "type": "json_object" },
        messages=[{"role": "user", "content": prompt}]
    )

    # Assuming the response is correctly formatted in json format 
    # convert it to a python object
    response_message = response.choices[0].message.content

    #check if the response is a valid json
    try:
        result_data = json.loads(response_message)
        print("Valid JSON")
    except json.JSONDecodeError:
        print("Invalid JSON")
        return None
    
    if 'employees' not in result_data or \
        'days' not in result_data or \
        'same_day_pairs' not in result_data or \
        'different_day_pairs' not in result_data:

        print("Invalid JSON")
        return None

    return result_data

def set_new_constraints_data_from_text(constraints_text):
    new_data = process_constraints_to_object(constraints_text)
    if new_data:
        global constraints_data
        constraints_data = new_data
        with open('data.json', 'w') as f:
            json.dump(constraints_data, f, indent=4)
        return True
    return False
