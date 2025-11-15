from setuptools import setup, find_packages
import os

# Read README.md if it exists
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A machine learning-based book recommender system."

# Read requirements.txt if available
def load_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            requirements = [req.strip() for req in f.read().splitlines() if req.strip() and req.strip() != "-e ."]
    return requirements



# -------------------------------
#   EDIT THESE AS PER YOUR PROJECT
# -------------------------------
PROJECT_NAME = "KLEOS_Book_recommender"
AUTHOR = "Nikini Ekanayaka"
AUTHOR_EMAIL = "nikiniekanayaka00@gmail.com"
REPO_URL = "https://github.com/NikiniEkanayaka/KLEOS.git"
DESCRIPTION = "A machine learning based book recommender system."
VERSION = "0.0.1"


# -------------------------------
#  SETUP CONFIG
# -------------------------------
setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=REPO_URL,
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=load_requirements()
)
