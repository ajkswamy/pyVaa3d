from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import zip
from future import standard_library
standard_library.install_aliases()
import sys
if sys.version_info[0] == 2:
    import subprocess32 as subprocess
elif sys.version_info[0] == 3:
    import subprocess
else:
    raise NotImplementedError
import logging
from .executables import vaa3d
from .auxFuncs import log_subprocess_output
import pathlib2 as pl
import pandas as pd
from pyvirtualdisplay import Display


def runVaa3dPlugin(inFile, pluginName,
                   funcName, vaa3dExec = vaa3d, timeout = 30 * 60):

    assert pl.Path(inFile).is_file(), "Input File {} not found".format(inFile)

    pluginLabel = "{}_{}".format(pluginName, funcName)

    virtDisplay = Display(visible=False, use_xauth=True, bgcolor="white")
    virtDisplay.start()

    toRun = [
        vaa3dExec, "-i", inFile, "-x", pluginName, "-f", funcName
    ]
    logging.info("[{}] Running {}".format(pluginLabel, toRun))

    try:
        compProc = subprocess.run(toRun,
                                  timeout=timeout,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  )
        log_subprocess_output(compProc.stdout, pluginLabel)
        procOutput = compProc.stdout.decode("utf-8")
    except subprocess.TimeoutExpired as te:
        log_subprocess_output(te.stdout, pluginLabel)
        procOutput = compProc.stdout.decode("utf-8")
        logging.error("{} Process did not finish within {} seconds!!!".format(pluginLabel, timeout))
        log_subprocess_output(te.stderr, pluginLabel)
    except OSError as ose:
        log_subprocess_output(ose.stdout, pluginLabel)
        procOutput = compProc.stdout.decode("utf-8")
        logging.error("{} OSError while running vaa3d plugin, for example,"
                      "a file is non existant".format(pluginLabel))
        log_subprocess_output(ose.stderr, pluginLabel)
    except ValueError as ve:
        log_subprocess_output(ve.stdout, pluginLabel)
        procOutput = compProc.stdout.decode("utf-8")
        logging.error("{} Invalid arguments passed to the subprocess".format(pluginLabel))
        log_subprocess_output(ve.stderr, pluginLabel)
    except subprocess.CalledProcessError as spe:
        log_subprocess_output(spe.stdout, pluginLabel)
        procOutput = compProc.stdout.decode("utf-8")
        logging.error("{} Subprocess exited with an unknown error!".format(pluginLabel))
        log_subprocess_output(spe.stderr, pluginLabel)

    virtDisplay.stop()
    return procOutput

def runEnsembleNeuronTracerv2s(inFile):

    runVaa3dPlugin(inFile=inFile, pluginName="EnsembleNeuronTracerV2s",
                   funcName="tracing_func")

    return "{}_EnsembleNeuronTracerV2s.swc".format(inFile)

def runFastMarching_SpanningTree(inFile):

    runVaa3dPlugin(inFile=inFile, pluginName="fastmarching_spanningtree",
                   funcName="tracing_func")

    return "{}_fastmarching_spanningtree.swc".format(inFile)

def getVaa3dHelp():

    try:
        completedProcess = subprocess.run([vaa3d, '-h'], stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as cpe:

        print(cpe.stderr)
        raise cpe

    return completedProcess.stdout.decode("utf-8")


def getVaa3dPluginHelp(pluginName):

    try:
        completedProcess = subprocess.run([vaa3d, '-h', '-x', pluginName],
                                          stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as cpe:

        print(cpe.stderr)
        raise cpe

    return completedProcess.stdout.decode("utf-8")


def getVaa3dPluginMenuFuncs(pluginName):

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
        raise(ValueError("No menus found for {}".format(pluginName)))
    if funcsStart is None:
        raise (ValueError("No funcs found for {}".format(pluginName)))

    menus = []
    funcs = []

    for lne in lnes[menusStart: funcsStart]:

        menu = lne[8:]
        menus.append(menu)

    for lne in lnes[funcsStart:]:

        func = lne[8:]
        funcs.append(func)

    return menus, funcs



def getNeuronTracingPlugins():

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

        pluginLibPath = pl.Path(pluginLibPathStr)

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





