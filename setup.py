from setuptools import find_packages, setup

setup(
    name="house_temp_hum",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt>=1.6.1",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "structlog>=23.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.4.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pre-commit>=3.3.0",
            "types-paho-mqtt>=1.6.0",
        ],
    },
    python_requires=">=3.11",
)
