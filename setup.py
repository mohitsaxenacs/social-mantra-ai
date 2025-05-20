from setuptools import setup, find_packages

setup(
    name="social_media_shorts_automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.28.0',
        'google-api-python-client>=2.86.0',
        'pandas>=1.5.0',
        'altair>=5.0.0',
        'tenacity>=8.2.0',
        'pyyaml>=6.0',
    ],
    python_requires='>=3.8',
)
