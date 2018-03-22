import sys
import os
import platform
from .configFilePaths import linuxConfigFile
import json
import pathlib2 as pl
import logging
if sys.version_info[0] == 2:
    import subprocess32 as subprocess
elif sys.version_info[0] == 3:
    import subprocess
else:
    raise NotImplementedError
from builtins import input
import pandas as pd


def checkVaa3dExecutable(vaa3dExec):

    try:
        vaa3dHelpText = getVaa3dHelpInternal(vaa3dExec)
        vaa3dHelpTextLines = vaa3dHelpText.split("\n")
        if vaa3dHelpTextLines[3] == \
            "Vaa3D: a 3D image visualization and analysis platform developed by Hanchuan Peng and colleagues.":
            logging.info("Working Vaa3d executable found at {}!".format(vaa3dExec))
            print("Working Vaa3d executable found at {}!".format(vaa3dExec))
            return True
    except subprocess.CalledProcessError:
        return False


def askForVaa3dExec():

    vaa3dExecutable = \
        input(
            "pyVaa3d cannot find Vaa3D Binary Executable. If you haven't yet, please download and install Vaa3d from "
            "pyVaa3d cannot find Vaa3d. If you haven't yet, please download and install Vaa3d from "
            "https://github.com/Vaa3D/release and enter the complete path of the file 'start_vaa3d.sh'"
            "(or press q to quit):"
        )
    assert checkVaa3dExecutable(vaa3dExecutable), "The specified vaa3d installation does not exist or" \
                                                  "could not be found"
    return vaa3dExecutable

def getVaa3DExecutable():

    if platform.system() == "Linux":

        if os.path.exists(linuxConfigFile):
            try:
                with open(linuxConfigFile, 'r') as fle:
                    configDict = json.load(fle)
            except json.decoder.JSONDecodeError:
                print("Configuration file has been corrupted! Creating new one...")

                configDict = {}


            if not "vaa3dExecutable" in configDict:
                vaa3dExec = askForVaa3dExec()
                configDict["vaa3dExecutable"] = vaa3dExec
                with open(linuxConfigFile, 'w') as fle:
                    print("Adding path of Vaa3D Binary Executable to internal config file")
                    json.dump(configDict, fle)

            else:
                vaa3dExec = configDict["vaa3dExecutable"]
                checkVaa3dExecutable(vaa3dExec)
        else:
            vaa3dExec = askForVaa3dExec()
            configDict = {"vaa3dExecutable": vaa3dExec}
            with open(linuxConfigFile, 'w') as fle:
                print("Adding path of Vaa3D Binary Executable to internal config file")

                json.dump(configDict, fle)

    else:
        raise NotImplementedError

    return vaa3dExec

def getVaa3dHelpInternal(vaa3d):

    try:
        completedProcess = subprocess.run([vaa3d, '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except subprocess.CalledProcessError as cpe:

        print(cpe.stderr)
        raise cpe

    return completedProcess.stdout.decode("utf-8")


def getVaa3dHelp():

    vaa3d = getVaa3DExecutable()
    return getVaa3dHelpInternal(vaa3d)


def getVaa3dPluginHelp(pluginName):

    vaa3d = getVaa3DExecutable()
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
