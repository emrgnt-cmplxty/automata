from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt", "r") as req_file:
        return req_file.readlines()


setup(
    name="automata-docs",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.9",  # Adjust this to your desired minimum Python version
)
