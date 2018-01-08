from .vaa3dWrapper import runVaa3dPlugin
import typing
import pandas as pd
from io import StringIO
import tempfile


def writeANOfile(swcList: typing.List[str], outFile: str):
    """
    Writes a list of swc files into an ".ano" file that is essentially path strings of the swc files listed
    one per line.
    :param swcList: list of str, each corresponding to the path string an SWC file
    :param outFile: str, where the .ano file is to be written. Must end with ".ano"
    :return:
    """

    assert outFile.endswith(".ano"), f"Specified output ANO file {outFile} does not end with '.ano'."
    swcListWithPrefix = ["SWCFILE=" + x for x in swcList]
    with open(outFile, 'w') as fle:
        fle.write("\n".join(swcListWithPrefix))


def readANOFile(inFile: str) -> typing.List[str]:
    """
    Reads an ".ano" file and
    :param inFile: str, path of the input ANO file, must end with ".ano"
    :return: list of str, list containing the path strings of the swc files in inFile
    """

    assert inFile.endswith(".ano"), f"Specified input ANO file {inFile} does not end with '.ano'."
    with open(inFile) as fle:
        swcListWithPrefix = fle.read().split("\n")
        swcList = []
        for ind, ent in enumerate(swcListWithPrefix):
            if len(ent) <= 8:
                raise(ValueError(f"Improper entry {ent} found on line {ind + 1} of {inFile}"))
            else:
                swcList.append(ent[8:])
        return swcList

def parseOpStr(opStr: str, inputANOfile: str) -> pd.DataFrame:

    """
    Parses the string output of "compute_feature" function of "global_neuron_feature" plugin of Vaa3d
    :param opStr: str, string containing the output of "compute_feature" function of "global_neuron_feature" plugin
    of Vaa3d
    :return: pd.DataFrame,
    """

    swcList = readANOFile(inputANOfile)

    neuronStartIndicatorBase = f"{''.join(['-'] * 14)}Neuron #"

    nNeurons = opStr.count(neuronStartIndicatorBase)

    assert len(swcList) == nNeurons, f"Output not generated for all input SWC files. " \
                                     f"Output String {opStr[:10]}... contains output for {nNeurons} neurons " \
                                     f"while the input file {inputANOfile} has {len(swcList)} neurons"

    allDF = pd.DataFrame()

    for swcInd, swc in enumerate(swcList):
        nrnSeries = pd.Series()
        nrnEntryStartInd = opStr.find(f"{neuronStartIndicatorBase}{swcInd + 1}")
        nrnBuffer = StringIO(opStr[nrnEntryStartInd:])
        nrnBuffer.readline()

        for lneInd in range(22):
            lne = nrnBuffer.readline()
            measureName, valueStr = lne.split(":")
            nrnSeries[measureName] = float(valueStr)
            nrnSeries["SWC File"] = swc
        allDF = allDF.append(nrnSeries, ignore_index=True)

    allDF.set_index(keys=["SWC File"], inplace=True)

    return allDF


def getGlobalNeuronFeatures(swcList: typing.List[str]):
    """
    Get global neuron features using "compute_feature" function of "global_neuron_feature" plugin of Vaa3d and return
    them in a pandas data frame
    :param swcList: list of strings, list of swc file path strings
    :return: pd.DataFrame, this data frame has swc files on indices and features on columns
    """

    inANOFile = tempfile.NamedTemporaryFile(suffix=".ano")
    writeANOfile(swcList, inANOFile.name)
    opStr = runVaa3dPlugin(inFile=inANOFile.name, pluginName="global_neuron_feature", funcName="compute_feature")
    outDF = parseOpStr(opStr, inputANOfile=inANOFile.name)
    return outDF

