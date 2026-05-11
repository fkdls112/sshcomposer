from setuptools import setup, find_packages

setup(
    name="sshcomposer",
    version="1.0.0",
    description="Docker Compose Deployment Tool",
    author="fkdls112",
    author_email="baggy1917@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5>=5.15.0",
        "paramiko>=2.7.0",
        "scp>=0.13.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "sshcomposer=main:main",
        ],
    },
)
