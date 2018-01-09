from setuptools import setup, find_packages
import sys
install_requires = ["pandas>=0.20",
                      "xlrd>=1.0",
                      "openpyxl>=2.4.7",
                      "pathlib2>=2.2.1",
                      "pillow>=5.0.0",
                      "psutil>=5.4.1",
                      "pyvirtualdisplay>=0.2.1",
                      "future>=0.16.0"]
if sys.version_info[0] == 2:
    install_requires.append("subprocess32>=3.5.0rc1")
elif sys.version_info[0] != 3:
    raise NotImplementedError
setup(
    name="py_vaa3d",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=["^\.", "tests*", "*egg-info"]),
    exclude_package_data={'': ["Readme.txt"]},
    install_requires=install_requires,
    python_requires=">=2.7",
    package_data={"pyVaa3d": ["bashScripts/*.sh"]}
)