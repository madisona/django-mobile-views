
from setuptools import setup, find_packages

REQUIREMENTS = (
    'django>=1.3',
)
TEST_REQUIREMENTS = (
    'mock',
)

from mobile_views import VERSION

setup(
    name="django-mobile-views",
    version=VERSION,
    author="Aaron Madison",
    description="Some mixins to serve mobile templates when mobile detected.",
    long_description=open('README', 'r').read(),
    url="https://github.com/madisona/django-mobile-views",
    packages=find_packages(exclude=["example"]),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        ],
    )