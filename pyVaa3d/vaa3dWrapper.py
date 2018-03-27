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
from .generalAuxFuncs import log_subprocess_output
from .vaa3dAuxFuncs import getVaa3DExecutable
import pathlib2 as pl
import pandas as pd
from pyvirtualdisplay import Display
import platform


def startVirtDisplay():

    if platform.system() == "Linux":
        virtDisplay = Display(visible=False, use_xauth=True, bgcolor="white")
        virtDisplay.start()
        return virtDisplay

def stopVirtualDisplay(virtDisplay):

    if platform.system() == "Linux":
        virtDisplay.stop()


def runVaa3dPlugin(inFile, pluginName,
                   funcName, timeout = 30 * 60):

    assert pl.Path(inFile).is_file(), "Input File {} not found".format(inFile)

    vaa3dExec = getVaa3DExecutable()
    pluginLabel = "{}_{}".format(pluginName, funcName)

    virtDisplay = startVirtDisplay()

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

    stopVirtualDisplay(virtDisplay)
    return procOutput

def runEnsembleNeuronTracerv2s(inFile):

    runVaa3dPlugin(inFile=inFile, pluginName="EnsembleNeuronTracerV2s",
                   funcName="tracing_func")

    return "{}_EnsembleNeuronTracerV2s.swc".format(inFile)

def runFastMarching_SpanningTree(inFile):

    runVaa3dPlugin(inFile=inFile, pluginName="fastmarching_spanningtree",
                   funcName="tracing_func")

    return "{}_fastmarching_spanningtree.swc".format(inFile)






