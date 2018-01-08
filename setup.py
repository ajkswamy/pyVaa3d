from setuptools import setup, find_packages
setup(
    name="py_vaa3d",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=["^\.", "tests*", "*egg-info"]),
    exclude_package_data={'': ["Readme.txt"]},
    install_requires=["pandas>=0.20",
                      "xlrd>=1.0",
                      "openpyxl>=2.4.7",
                      "pathlib2>=2.2.1",
                      "pillow>=5.0.0",
                      "psutil>=5.4.1",
                      "pyvirtualdisplay>=0.2.1"],
    python_requires=">=3.6",
    package_data={"pyVaa3d": ["bashScripts/*.sh"]}
)