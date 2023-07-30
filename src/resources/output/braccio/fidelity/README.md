# Braccio Robot Arm Fidelity Analysis

## Verifiability

Due to GitHub repository size restrictions, this folder does not include all the alignments that correspond to this analysis.

To regenerate the original content of this folder, execute the following command in the root folder **/src/**:

### For the Servos Angles
```
python align_traces.py --figures --engine kaleido --config braccio_fidelity_servos.yaml
```

### For the Grip's Coordinates
```
python align_traces.py --figures --engine kaleido --config braccio_fidelity_grip.yaml
```



