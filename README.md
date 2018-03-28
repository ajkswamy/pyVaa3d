# pyVaa3d
Python wrapper for running Vaa3d functions

# Features:
1. A method that is equivalent of running a specific function of a specific plugin of vaa3d (essentially, `vaa3d -i <...> -x <...> -f <...>`). It returns printed output on stdout.
2. Convenience method to generate all global features of neurons, specified using a SWC files, and returning features as pandas tables.
3. Python 2/3 support
4. Linux, MacOS and Windows support 
5. Unit testing

# Installation
See the file INSTALL.md

# Example Usages

## Basic commandline functionality
Here we call the function "tracing_func" of plugin "EnsembleNeuronTracerV2s" on the file "input.tiff". This plugin reconstructs neuron morphology from "input.tiff" using the "EnsembleNeuronTracerV2s" plugin.

```
from pyVaa3d.vaa3dWrapper import runVaa3dPlugin
runVaa3dPlugin(inFile=inFile, pluginName="EnsembleNeuronTracerV2s",
                   funcName="tracing_func")
```

## Computing Global features of SWC morphologies

Global neuron features are calculated for the SWC morphologies "1.swc" and "2.swc" and save it to the excel file "GlobalNeuronFeatures.xlsx".
```
from pyVaa3d.global_neuron_features import getGlobalNeuronFeatures
swcFiles = ["1.swc", "2.swc"]
outDF = getGlobalNeuronFeatures(swcFiles)
outDF.to_excel("GlobalNeuronFeatures.xlsx") 
```                   
        