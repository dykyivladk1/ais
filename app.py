import time
import subprocess
from datetime import datetime
import openai
import sys
import os

activity_log = {}
session_start = datetime.now()
current_app = None
app_start_time = None

def get_hobby_from_file(filename='personality.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().strip()
    return None

def get_api(filename='token.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().strip()
    return None

def get_chatgpt_response(prompt, tokens_len, model='gpt-4o-mini'):
    openai.api_key = get_api()
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=tokens_len,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].message['content'].strip()

def get_active_application():
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    active_app = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return active_app.stdout.strip()

def track_active_applications():
    global current_app, app_start_time
    last_check_time = time.time()

    while True:
        app_name = get_active_application()

        if app_name:
            current_time = time.time()
            if app_name != current_app:
                if current_app and app_start_time:
                    elapsed_time = current_time - app_start_time.timestamp()
                    activity_log[current_app] = activity_log.get(current_app, 0) + elapsed_time

                current_app = app_name
                app_start_time = datetime.now()

            if current_time - last_check_time >= 1:
                last_check_time = current_time

        time.sleep(0.1)

def type_effect(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def print_activity_table(activity_log, total_time):
    print("\nActivity Summary:")
    print("{:<30} {:<10}".format("Application", "Time Spent (s)"))
    print("-" * 40)
    for app, time_spent in activity_log.items():
        print("{:<30} {:<10.2f}".format('Visual Studio Code' if app == 'Electron' else app, time_spent))
    print("-" * 40)
    print(f"Total Time: {total_time:.2f} seconds")

# Check if the token and hobby are set
if get_api() is None or get_hobby_from_file() is None:
    subprocess.run(['python3', 'ask.py'])
else:
    try:
        print("Tracking session started...")
        track_active_applications()
    except KeyboardInterrupt:
        session_end = datetime.now()
        if current_app and app_start_time:
            elapsed_time = (datetime.now() - app_start_time).total_seconds()
            activity_log[current_app] = activity_log.get(current_app, 0) + elapsed_time

        total_time = (session_end - session_start).total_seconds()
        activity_summary = "\n".join([f"{'Visual Studio Code' if app == 'Electron' else app}: {time_spent:.2f} seconds" for app, time_spent in activity_log.items()])

        hobby = get_hobby_from_file()

        prompt = (
            "Please analyze the following time spent on each application and provide comments on productivity:\n"
            f"Total session time: {total_time:.2f} seconds.\n"
            f"Activity log:\n{activity_summary}\n"
            f"Based on this information, do you think the time spent was productive? Why or why not? And finally give the percentage of total productivity considering I am a {hobby}. DO NOT SEND ANY FORMULAS, JUST ONLY THE VALUES!!!"
        )

        response = get_chatgpt_response(prompt, 400)
        print('\n')
        type_effect(response)

        # Print the table summary
        print_activity_table(activity_log, total_time)
