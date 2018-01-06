import subprocess
import logging
from .executables import vaa3d
from .auxFuncs import \
    log_subprocess_output, isProcessRunning, pkill
import pathlib
import typing
import pandas as pd

def runVaa3dPlugin(inFile: str, pluginName: str,
                   funcName: str, vaa3dExec: str = vaa3d, timeout: int = 30 * 60):

    assert pathlib.Path(inFile).is_file(), f"Input File {inFile} not found"

    filePath = pathlib.Path(__file__)
    # pluginBashScriptPath = filePath.parent / "bashScripts" / "runVaa3dPlugin.sh"
    xvfbBashScriptPath = filePath.parent / "bashScripts" / "startXvfb.sh"
    pluginLabel = f"{pluginName}_{funcName}"

    if not isProcessRunning("Xvfb"):
        toRun = ["bash", str(xvfbBashScriptPath)]
        logging.info(f"[starting Xvfb] Running {toRun}")
        compProc = subprocess.run(toRun, stdout=subprocess.PIPE)
        log_subprocess_output(compProc.stdout, "starting Xvfb")

    toRun = [
        vaa3dExec, "-i", inFile, "-x", pluginName, "-f", funcName
    ]
    logging.info(f"[{pluginLabel}] Running {toRun}")
    env = pathlib.os.environ.copy()
    env["DISPLAY"] = ":30"
    try:
        compProc = subprocess.run(toRun,
                                  timeout=timeout,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  env=env)
        log_subprocess_output(compProc.stdout, pluginLabel)
    except subprocess.TimeoutExpired as te:
        log_subprocess_output(te.stdout, pluginLabel)
        logging.error(f"{pluginLabel} Process did not finish within {timeout} seconds!!!")
        log_subprocess_output(te.stderr, pluginLabel)
    except OSError as ose:
        log_subprocess_output(ose.stdout, pluginLabel)
        logging.error(f"{pluginLabel} OSError while running vaa3d plugin, for example,"
                      f"a file is non existant")
        log_subprocess_output(ose.stderr, pluginLabel)
    except ValueError as ve:
        log_subprocess_output(ve.stdout, pluginLabel)
        logging.error(f"{pluginLabel} Invalid arguments passed to the subprocess")
        log_subprocess_output(ve.stderr, pluginLabel)
    except subprocess.SubprocessError as spe:
        log_subprocess_output(spe.stdout, pluginLabel)
        logging.error(f"{pluginLabel} Subprocess exited with an unknown error!")
        log_subprocess_output(spe.stderr, pluginLabel)

    logging.info(f"[Killing Xvfb]...")
    pkill("Xvfb")

def runEnsembleNeuronTracerv2s(inFile: str) -> str:


    runVaa3dPlugin(inFile=inFile, pluginName="EnsembleNeuronTracerV2s",
                   funcName="tracing_func")

    return f"{inFile}_EnsembleNeuronTracerV2s.swc"

def runFastMarching_SpanningTree(inFile: str) -> str:

    runVaa3dPlugin(inFile=inFile, pluginName="fastmarching_spanningtree",
                   funcName="tracing_func")

    return f"{inFile}_fastmarching_spanningtree.swc"

def getVaa3dHelp() -> str:

    try:
        completedProcess = subprocess.run([vaa3d, '-h'], stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as cpe:

        print(cpe.stderr)
        raise cpe

    return completedProcess.stdout.decode("utf-8")


def getVaa3dPluginHelp(pluginName) -> str:

    try:
        completedProcess = subprocess.run([vaa3d, '-h', '-x', pluginName],
                                          stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as cpe:

        print(cpe.stderr)
        raise cpe

    return completedProcess.stdout.decode("utf-8")


def getVaa3dPluginMenuFuncs(pluginName) -> typing.Tuple[list, list]:

    pluginHelpStr = getVaa3dPluginHelp(pluginName)

    lnes = pluginHelpStr.splitlines()

    menusStart = None
    funcsStart = None
    for lneInd, lne in enumerate(lnes):

        if lne.startswith("menu"):

            menusStart = lneInd

        if lne.startswith("func"):

            funcsStart = lneInd

    if menusStart is None:
        raise(ValueError(f"No menus found for {pluginName}"))
    if funcsStart is None:
        raise (ValueError(f"No funcs found for {pluginName}"))

    menus = []
    funcs = []

    for lne in lnes[menusStart: funcsStart]:

        menu = lne[8:]
        menus.append(menu)

    for lne in lnes[funcsStart:]:

        func = lne[8:]
        funcs.append(func)

    return menus, funcs



def getNeuronTracingPlugins() -> pd.DataFrame:

    vaa3dHelpStr = getVaa3dHelp()
    vaa3dHelpLines = vaa3dHelpStr.splitlines()

    neuronTracingPlugins = pd.DataFrame()

    for lneInd, lne in enumerate(vaa3dHelpLines):

        if lne.startswith("Found") and lne.endswith("plugins"):
            pluginStartLineNo = lneInd + 1
            break
    else:
        return neuronTracingPlugins

    for pluginLne in vaa3dHelpLines[pluginStartLineNo:]:

        pluginNo, pluginLibPathStr = pluginLne.split()

        pluginLibPath = pathlib.Path(pluginLibPathStr)

        if pluginLibPath.parts[-3] == "neuron_tracing":

            pluginName = pluginLibPath.parts[-1][3:-3]

            menus, funcs = getVaa3dPluginMenuFuncs(pluginName)

            for menu, func in zip(menus, funcs):

                dict2Append = {"Plugin Name": pluginName,
                               "Menu Name": menu,
                               "Function Name": func}
                neuronTracingPlugins = neuronTracingPlugins.append(dict2Append,
                                                                   ignore_index=True)

    neuronTracingPlugins = neuronTracingPlugins.set_index(keys="Plugin Name")


    return neuronTracingPlugins


def getFromFileVaa3dNTPlugData(vaa3dNTPluginDataFile: pathlib.Path
                               = vaa3DNeuronTracingPlugins):

    vaa3dNTPluginDF = pd.read_excel(str(vaa3dNTPluginDataFile), index_col=0)

    return vaa3dNTPluginDF


