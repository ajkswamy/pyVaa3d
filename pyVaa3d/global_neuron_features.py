from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import range
from future import standard_library
standard_library.install_aliases()
from .vaa3dWrapper import runVaa3dPlugin
import pandas as pd
from io import StringIO
import tempfile



def writeANOfile(swcList, outFile):
    """
    Writes a list of swc files into an ".ano" file that is essentially path strings of the swc files listed
    one per line.
    :param swcList: list of str, each corresponding to the path string an SWC file
    :param outFile: str, where the .ano file is to be written. Must end with ".ano"
    :return:
    """

    assert outFile.endswith(".ano"), "Specified output ANO file {} does not end with '.ano'.".format(outFile)
    swcListWithPrefix = ["SWCFILE=" + x for x in swcList]
    with open(outFile, 'w') as fle:
        fle.write("\n".join(swcListWithPrefix))


def readANOFile(inFile):
    """
    Reads an ".ano" file and
    :param inFile: str, path of the input ANO file, must end with ".ano"
    :return: list of str, list containing the path strings of the swc files in inFile
    """

    assert inFile.endswith(".ano"), "Specified input ANO file {} does not end with '.ano'.".format(inFile)
    with open(inFile) as fle:
        swcListWithPrefix = fle.read().split("\n")
        swcList = []
        for ind, ent in enumerate(swcListWithPrefix):
            if len(ent) <= 8:
                raise(ValueError("Improper entry {} found on line {} of {}".format(ent, ind + 1, inFile)))
            else:
                swcList.append(ent[8:])
        return swcList

def parseOpStr(opStr, inputANOfile):

    """
    Parses the string output of "compute_feature" function of "global_neuron_feature" plugin of Vaa3d
    :param opStr: str, string containing the output of "compute_feature" function of "global_neuron_feature" plugin
    of Vaa3d
    :return: pd.DataFrame,
    """

    swcList = readANOFile(inputANOfile)

    neuronStartIndicatorBase = "{}Neuron #".format(''.join(['-'] * 14))

    nNeurons = opStr.count(neuronStartIndicatorBase)

    assert len(swcList) == nNeurons, "Output not generated for all input SWC files. " \
                                     "Output String {}... contains output for {} neurons " \
                                     "while the input file {} has {} neurons".format(opStr[:10],
                                                                                     nNeurons,
                                                                                     inputANOfile,
                                                                                     len(swcList))

    allDF = pd.DataFrame()

    for swcInd, swc in enumerate(swcList):
        nrnSeries = pd.Series()
        nrnEntryStartInd = opStr.find("{}{}".format(neuronStartIndicatorBase, swcInd + 1))
        nrnBuffer = StringIO(opStr[nrnEntryStartInd:])
        nrnBuffer.readline()
        nrnBuffer.readline()

        for lneInd in range(28):
            lne = nrnBuffer.readline().rstrip("\n")
            measureName, valueStr = lne.split(":")
            valueStr = valueStr.replace(",", ".")
            nrnSeries[measureName] = float(valueStr)
            nrnSeries["SWC File"] = swc
        allDF = allDF.append(nrnSeries, ignore_index=True)

    allDF.set_index(keys=["SWC File"], inplace=True)

    return allDF


def getGlobalNeuronFeatures(swcList):
    """
    Get global neuron features using "compute_feature" function of "global_neuron_feature" plugin of Vaa3d and return
    them in a pandas data frame
    :param swcList: list of strings, list of swc file path strings
    :return: pd.DataFrame, this data frame has swc files on indices and features on columns
    """

    inANOFile = tempfile.NamedTemporaryFile(suffix=".ano", delete=False)
    writeANOfile(swcList, inANOFile.name)
    opStr = runVaa3dPlugin(inFile=inANOFile.name, pluginName="global_neuron_feature", funcName="compute_feature")
    outDF = parseOpStr(opStr, inputANOfile=inANOFile.name)
    return outDF

