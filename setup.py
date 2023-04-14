import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recommendation-68911",
    version="0.0.1",
    author="Lubomir Gernath",
    author_email="lubomir.gernath@student.tuke.sk",
    packages=["recommendation_68911"],
    description="Package for recommendation system (68911) integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gernathlub/recommendation_68911",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
         "Django>=3.2",
         "requests>=2.25",
    ]
)