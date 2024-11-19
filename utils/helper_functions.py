import json
import os
from datetime import datetime, timezone
import yaml
from textwrap import wrap

def load_config(file_path):
    # Define default values
    default_values = {
        'OPENAI_API_KEY': 'default_openai_api_key',
    }
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            if not value:
                os.environ[key] = default_values.get(key, '')
            else:
                os.environ[key] = value

def get_current_utc_datetime():
    now_utc = datetime.now(timezone.utc)
    current_time_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
    return current_time_utc

def check_for_content(var):
    if var:
        try:
            var = var.content
            return var.content
        except:
            return var
    else:
        return var

def custom_print(message, stdscr=None, scroll_pos=0):
    if stdscr:
        max_y, max_x = stdscr.getmaxyx()
        max_y -= 2

        wrapped_lines = []
        for line in message.split("\n"):
            wrapped_lines.extend(wrap(line, max_x))

        num_lines = len(wrapped_lines)
        visible_lines = wrapped_lines[scroll_pos:scroll_pos + max_y]

        stdscr.clear()
        for i, line in enumerate(visible_lines):
            stdscr.addstr(i, 0, line[:max_x])

        stdscr.addstr(max_y, 0, f"Lines {scroll_pos + 1} - {scroll_pos + len(visible_lines)} of {num_lines}")
        stdscr.refresh()

        return num_lines
    else:
        print(message)

def print_sql_query(query_generator_state=None):
    generator_value = query_generator_state() if callable(query_generator_state) else query_generator_state
    generator_value = check_for_content(generator_value)
    print("SQL Query: ", json.loads(generator_value)["sql_query"])

    