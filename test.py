def def_readme():
    """Check Readme Markdown"""
    readme = ""
    with open('README.md', encoding="utf-8") as file_content:
        readme = file_content.read()
    return readme
import os
print(os.getcwd())
print(def_readme())