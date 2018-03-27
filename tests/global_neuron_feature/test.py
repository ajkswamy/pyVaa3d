from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import open
from builtins import str
from builtins import zip
from future import standard_library
standard_library.install_aliases()
from pyVaa3d.global_neuron_features import writeANOfile, readANOFile, parseOpStr, getGlobalNeuronFeatures
import pathlib2 as pl
from filecmp import cmp
import pandas as pd


testFilesPath = pl.Path("tests/global_neuron_feature/testFiles").resolve()


def test_rwANOFile():
    """
    Testing the writeANOFile function
    :return:
    """

    swcFiles = [
        "v_e_purk2.CNG.swc",
        "v_e_moto1.CNG.swc",
        "horton-strahler_test_wiki.swc",
    ]
    swcFilesFull = [str(testFilesPath / x) for x in swcFiles]

    outFilePath = testFilesPath / "testOutput.ano"
    if outFilePath.is_file():
        outFilePath.unlink()

    writeANOfile(swcList=swcFilesFull, outFile=str(outFilePath))

    readSWCFiles = readANOFile(str(outFilePath))

    assert all([x == y for x, y in zip(readSWCFiles, swcFilesFull)])


def test_parseOPStr():
    """
    Testing the postOPStr function
    :return:
    """

    testOpStrFilePath = testFilesPath / "testOPStr.txt"
    expectedOutFilePath = testFilesPath / "expectedOutput.ano"
    expectedOPXL = testFilesPath / "expectedOutputXL.xlsx"

    with open(str(testOpStrFilePath)) as fle:
        testOpStr = fle.read()

    testOPDF = parseOpStr(opStr=testOpStr, inputANOfile=str(expectedOutFilePath))
    testOPDF.index = [pl.Path(x).name for x in testOPDF.index]
    testOPDF.index.name = "SWC File"
    expectedOPDF = pd.read_excel(expectedOPXL, index_col=0, convert_float=False)

    pd.util.testing.assert_frame_equal(testOPDF, expectedOPDF)


def test_getGlobalNeuronFeatures():
    """
    Testing the getGlobalNeuronFeatures function
    :return:
    """

    swcFiles = [
        "v_e_purk2.CNG.swc",
        "v_e_moto1.CNG.swc",
        "horton-strahler_test_wiki.swc",
    ]
    swcFilesFull = [str(testFilesPath / x) for x in swcFiles]

    expectedOPXL = testFilesPath / "expectedOutputXL.xlsx"

    testOPDF = getGlobalNeuronFeatures(swcFilesFull)
    testOPDF.index = [pl.Path(x).name for x in testOPDF.index]
    testOPDF.index.name = "SWC File"
    expectedOPDF = pd.read_excel(expectedOPXL, index_col=0, convert_float=False)

    pd.util.testing.assert_frame_equal(testOPDF, expectedOPDF)
