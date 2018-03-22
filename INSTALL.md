# Installation
LINUX ONLY

## 1. Make environment

`conda create --name pyVaa3d -c conda-forge pandas xlrd openpyxl psutil pillow pyvirtualdisplay`

## 2. Activate environment
`source activate pyVaa3d`

## 3. Install package
`pip install \<path to package\>`

## 4. Configure Vaa3D binary executable
`python -c "import pyVaa3D"`

When asked for, enter the path to the file "start_vaa3d.sh" within Vaa3D Installation folder.

# Testing

conda install nose

cd \<path to package\>

nosetests
