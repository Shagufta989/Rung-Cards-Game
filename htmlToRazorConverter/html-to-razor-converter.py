import os
from bs4 import BeautifulSoup

html_directory = './htmlFiles'
razor_directory = './razorFiles'

def extract_html_part(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_part = soup.find('div', {'class': 'container'})
    return str(extracted_part) if extracted_part else ''


def create_razor_content(filename, extracted_data):
    razor_content = f'@page "/{filename}"\n\n{extracted_data}\n\n@code {{}}'
    return razor_content


os.makedirs(razor_directory, exist_ok=True)
try:
    for html_file in os.listdir(html_directory):
        if html_file.endswith('.html'):
            html_path = os.path.join(html_directory, html_file)
            with open(html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            extracted_data = extract_html_part(html_content)

            filename_without_extension = os.path.splitext(html_file)[0]
            razor_content = create_razor_content(filename_without_extension, extracted_data)

            razor_path = os.path.join(razor_directory, f'{filename_without_extension}.razor')
            with open(razor_path, 'w', encoding='utf-8') as file:
                file.write(razor_content)

    print("Razor files generated successfully.")
except (FileNotFoundError):
    print("File wasn't found.")