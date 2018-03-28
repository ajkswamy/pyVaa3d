# Installation


## 1. Make environment
### Linux
`conda create --name pyVaa3d -c conda-forge pandas xlrd openpyxl psutil pillow pyvirtualdisplay`
### Windows and MacOS
`conda create --name pyVaa3d -c conda-forge pandas xlrd openpyxl psutil pillow`
## 2. Activate environment
### Linux
`conda activate pyVaa3d`
### MacOS
`source activate pyVaa3d`
### Windows
`activate pyVaa3d`

## 3. Install package
`pip install \<path to package\>`

## 4. Configure Vaa3D binary executable
`python -c "import pyVaa3D"`

When asked for, enter the path to the file "start_vaa3d.sh" within Vaa3D Installation folder.

# Testing

conda install nose

cd \<path to package\>

nosetests
