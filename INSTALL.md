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

## 3. Clone and Install package
### Clone Package
`git clone https://github.com/dEvasEnApati/pyVaa3d.git`
### Install package 
`pip install \<path to cloned pyVaa3d package\>`

## 4. Configure Vaa3D binary executable
Download Vaa3d v3.447 from https://github.com/Vaa3D/release and make sure it is working.

`python -c "import pyVaa3D"`

When asked for, enter the path to the file "start_vaa3d.sh" within Vaa3D Installation folder.

# Testing

conda install nose

cd \<path to cloned pyVaa3d package\>

nosetests
