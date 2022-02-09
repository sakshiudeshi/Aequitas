from setuptools import setup, find_packages

VERSION = '0.1.8' 
DESCRIPTION = 'A Python library aims to determine the Fairness of machine learning datasets'
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()
# Setting up

setup(
       # the name must match the folder name 'verysimplemodule'
        name="Phemus", 
        version=VERSION,
        author="Yunping Wang",
        author_email="<wangj6@carleton.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'machine learning fairness'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)