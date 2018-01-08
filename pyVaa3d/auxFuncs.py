from PIL import Image
from PIL.TiffImagePlugin import TiffImageFile
import os
import logging
import numpy as np
from contextlib import contextmanager
import pandas as pd
import psutil
import typing


def tifStack2ImageSeq(tifFile: str, tiffOutDir: str):

    logging.info("[tifStack2ImageSeq] Got Input File: {}\nOutput directory: {}".format(tifFile, tiffOutDir))
    fileName = os.path.split(tifFile)[1]
    inStub, inExt = fileName.split('.')

    assert inExt in ["tif", "tiff"], \
        "tifFile must have '.tif' or '.tiff' extension"

    if not os.path.isdir(tiffOutDir):
        os.makedirs(tiffOutDir)

    try:
        logging.info("[tifStack2ImageSeq] Opening {}".format(tifFile))
        tif = Image.open(tifFile)
    except Exception as e:
        raise(IOError('Error opening {} as an image.'.format(tifFile)))

    assert isinstance(tif, TiffImageFile), "{} could not be read a TIFF Image Stack".format(tifFile)

    logging.info("[tifStack2ImageSeq] Writing individual slices as "
                 "{}xxxx.bmp to {}".format(inStub, tiffOutDir))
    for ind in range(tif.n_frames):
        tif.seek(ind)
        opFile = os.path.join(tiffOutDir, "{}{:04d}.bmp".format(inStub, ind))
        tif.save(opFile)

# from http://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging/21978778#21978778
def log_subprocess_output(pipe: typing.Union[bytes, None], subproc_name: str= '??'):

    if pipe:
        for line in pipe.split(b"\n"):
            logging.info('[subprocess {}] {}'.format(subproc_name, line.decode("utf-8")))

#***********************************************************************************************************************

def readSWC_numpy(swcFile):
    '''
    Read the return the header and matrix data in a swcFile
    :param swcFile: filename
    :return: header (string), matrix data (ndarray)
    '''
    headr = ''
    with open(swcFile, 'r') as fle:
        lne = fle.readline()
        while lne[0] == '#':
            headr = headr + lne[1:]
            lne = fle.readline()

    headr = headr.rstrip('\n')

    swcData = np.loadtxt(swcFile)

    return headr, swcData

#***********************************************************************************************************************

def writeSWC_numpy(fName, swcData, headr=''):
    '''
    Write SWC file from matrix data and header
    :param fName: str, filename
    :param swcData: numpy.ndarray, 7 column matrix data
    :param headr: str, SWC header
    :return: 
    '''

    swcData = np.array(swcData)
    assert swcData.shape[1] in [7, 8], 'Width given SWC Matrix data is incompatible.'


    formatStr = '%d %d %0.6f %0.6f %0.6f %0.6f %d'

    if swcData.shape[1] == 8:
         formatStr += ' %0.6f'

    np.savetxt(fName, swcData, formatStr, header=headr, comments='#')

#***********************************************************************************************************************

def shiftSWC(inputSWC: str, xLeft: float, yLeft: float, outputSWC: str):

    headr, swcData = readSWC_numpy(inputSWC)

    swcData[:, 2] += xLeft
    swcData[:, 3] += yLeft

    writeSWC_numpy(outputSWC, swcData, headr)




@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def stripTIFIfPresent(fileName:str) -> str:

    if fileName.endswith(".tif"):
        return fileName[:-4]
    else:
        return fileName



def isProcessRunning(procName):

    for proc in psutil.process_iter():
        try:
            if proc.name() == procName:
                return True
        except psutil.NoSuchProcess:
            pass
    return False

def pkill(procName):

    for proc in psutil.process_iter():
        try:
            if proc.name() == procName:
                proc.kill()
        except psutil.NoSuchProcess:
            pass
