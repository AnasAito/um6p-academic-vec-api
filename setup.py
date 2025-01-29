from setuptools import setup, find_packages

setup(
    name="acavec",
    version="0.1.0",
    author="anas ait aomar",
    author_email="anas.aitaomar@um6p.ma",
    description="all um6p papers chunked and vectorized",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "lancedb",
        "polars",
        "numpy",
        "pydantic",
        "tinydb",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
