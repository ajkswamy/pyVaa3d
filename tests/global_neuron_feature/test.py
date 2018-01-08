from pyVaa3d.global_neuron_features import writeANOfile, readANOFile, parseOpStr, getGlobalNeuronFeatures
import pathlib2 as pl
from filecmp import cmp
import pandas as pd


testFilesPath = pl.Path("tests/global_neuron_feature/testFiles").resolve()


def test_writeANOFile():
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
    expectedOutFilePath = testFilesPath / "expectedOutput.ano"

    writeANOfile(swcList=swcFilesFull, outFile=str(outFilePath))

    assert cmp(str(outFilePath), str(expectedOutFilePath))


def test_readANOFile():
    """
    Testing the readANOFile function
    :return:
    """

    swcFiles = [
        "v_e_purk2.CNG.swc",
        "v_e_moto1.CNG.swc",
        "horton-strahler_test_wiki.swc",
    ]
    swcFilesFull = [str(testFilesPath / x) for x in swcFiles]

    expectedOutFilePath = testFilesPath / "expectedOutput.ano"

    testSWCFiles = readANOFile(str(expectedOutFilePath))

    assert all([x == y for x, y in zip(testSWCFiles, swcFilesFull)])


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
    expectedOPDF = pd.read_excel(expectedOPXL, index_col=0, convert_float=False)

    pd.util.testing.assert_frame_equal(testOPDF, expectedOPDF)
