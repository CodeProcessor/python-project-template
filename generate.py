"""
Copyright (C) CUBE Content Governance Global Limited - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dulan Jayasuriya <dulan.jayasuriya@cube.global>, 11 February 2022
"""
import json
import os.path
from datetime import datetime


class Generator:
    def __init__(self, config_path='config.json'):
        self.configs = json.load(open(config_path))
        self.project_name = self.configs['project_name']
        self.library_name = self.configs['library_name']

    def write_content(self, file_path, content):
        """
        Write content to file
        :param file_path:
        :param content:
        :return:
        """
        _dir = os.path.dirname(file_path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        with open(file_path, 'w') as f:
            f.write(content)

    def get_banner(self):
        banner = f"\"\"\"\n\
Copyright (C) {self.configs['library_author_company']} - All Rights Reserved \n\
Unauthorized copying of this file, via any medium is strictly prohibited \n\
Proprietary and confidential \n\
Written by {self.configs['library_author']} <{self.configs['library_author_email']}>, {datetime.now().strftime('%d %B %Y')} \n\
\"\"\"\n\n"
        return banner

    def get_setup_content(self):
        content = f"import {self.library_name} \n\
from setuptools import setup, find_packages \n\
\n\
\n\
setup(\n\
    name='{self.library_name}', \n\
    version={self.library_name}.__version__, \n\
    description='{self.configs['library_description']}', \n\
    url='{self.configs['library_author_url']}',   \n\
    author='{self.configs['library_author']}', \n\
    author_email='{self.configs['library_author_email']}', \n\
    license='{self.configs['library_license']}', \n\
    packages=find_packages(), \n\
    zip_safe=False\n\
)\n"

        return content

    def generate(self):
        """
        Main function
        :return:
        """
        self.write_content(os.path.join(self.project_name, 'README.md'), f"#{self.project_name}")
        self.write_content(os.path.join(self.project_name, 'LICENSE'), f"#{self.project_name}")
        self.write_content(os.path.join(self.project_name, self.library_name, '__init__.py'),
                           self.get_banner() + f"__version__ = '{self.configs['library_version']}'\n")
        self.write_content(os.path.join(self.project_name, 'setup.py'), self.get_banner() + self.get_setup_content())
        self.write_content(os.path.join(self.project_name, 'requirements.txt'), "")
        self.write_content(os.path.join(self.project_name, "tests", 'README.md'),
                           "#Package integration and unit tests.")
        self.write_content(os.path.join(self.project_name, "docs", 'README.md'), "#Package reference documentation.")

    def clean(self):
        """
        Clean the project
        :return:
        """
        pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate a new project')
    parser.add_argument('--config_file', help='Path to the config file', default='config.json')

    args = parser.parse_args()
    # get input filename from user

    # generate the project

    gen = Generator(args.config_file)
    gen.generate()
    print('Generated!')
