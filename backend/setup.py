from setuptools import setup, find_packages

setup(
    name="lottawords",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "lottawords": ["templates/*.html", "data/*.txt"],
    },
    include_package_data=True,
    install_requires=[
        "flask>=3.0.2",
        "selenium>=4.18.1",
        "python-dotenv>=1.0.1",
        "flask-cors>=4.0.0",
        "flask-caching>=2.1.0",
        "python-json-logger>=2.0.7",
    ],
    python_requires=">=3.8",
) 