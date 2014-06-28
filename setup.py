from distutils.core import setup

setup(
    name='NettiAuto',
    version='0.1.0',
    author='Jaro Spisak',
    author_email='jarospisak@gmail.com',
    scripts=['nettiauto.py'],
    license='LICENSE.txt',
    description='Script for tracking prices of cars on nettiauto.com on a daily basis.',
    # long_description=open('README.txt').read(),
    requires=[
        "requests",
        "gspread",
        "BeautifulSoup"
    ],
)
