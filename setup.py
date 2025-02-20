from setuptools import setup, find_packages

setup(
    name='jufo-pptx-script',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-pptx>=1.0.2',
        'lark>=1.2.2',
        'pillow>=11.1.0',
        "tqdm>=4.67.1"
    ],
    package_data={
        'jufo-pptx-script': ['templater/*.lark'],
    },
    include_package_data=True,
    author='Noah Albers',
    author_email='albers-noah@pm.me',
    description='Rewritten code of python-pptx to easily generate jufo presentations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Noah-Albers/Jufo-pptx-script',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.11',
)
