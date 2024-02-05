
import csv
import requests
from bs4 import BeautifulSoup

list_url = "https://fossbytes.com/a-z-list-linux-command-line-reference/"

def get_command_details():
    response = requests.get(list_url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
    commands_data = []

    # Find all the <h2> headers
    h2_headers = soup.find_all('h2')

    for header in h2_headers:
        section_name = header.text.strip()
        section_table = header.find_next('table', class_='tg')  # Find the table after the header

        if section_table:
            rows = section_table.find_all('tr')[1:]  # Skip the header row (index 0)

            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    command_name = columns[0].text.strip()
                    command_description = columns[1].text.strip()

                    # Debug print
                    print(f"Section: {section_name}, Command: {command_name}, Description: {command_description}")

                    commands_data.append({
                        'section': section_name,
                        'name': command_name,
                        'description': command_description,
                    })

    return commands_data

# Scrape the command details
commands_data = get_command_details()

# Write to CSV
with open('linux_commands.csv', 'w', newline='', encoding='utf-8',) as file:
    writer = csv.DictWriter(file, fieldnames=['section', 'name', 'description'])
    writer.writeheader()
    for command in commands_data:
        writer.writerow(command)