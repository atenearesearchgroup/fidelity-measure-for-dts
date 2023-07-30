# How to measure fidelity in a Digital Twin System? - A trace alignment algorithm

## Index

- [Overview](#overview)
- [Requirements and Installation](#requirements-and-installation)
- [Repository structure](#repository-structure)
- [Usage and examples](#usage-and-examples)

---

## Overview

This repository includes a dynamic programming algorithm based on the Needleman-Wunsch global alignment algorithm
applied to behavioral traces. The repository serves as a companion to the paper titled _'Measuring the Fidelity of a
Physical and a Digital Twin Using Trace Alignments,'_ which is currently under review and can be cited
using [CITATION.cff](CITATION.cff).

To obtain more information about the algorithm and the different examples and case studies with which it has been
validated, you can access the [/docs](/docs) directory and find the Technical Reports that accompany the article.

---

## Requirements and installation

### Execution environment

The algorithm was developed using **Python 3.10**, so we recommend installing this version of Python for executing the
alignments and analysis.

We strongly recommend using **Linux or the Linux Subsystem for Windows** for the alignments, as the required library for
generating the graphics (kaleido) may encounter some issues when running on Windows.

### Required packages

To install all the required packages:

1. Open the command line in the _blast_ folder.
2. Install the required packages with pip:
   ```python -m pip install -r requirements.txt```

---

## Repository structure

```
├── /src
│   ├── align_traces.py
│   ├── /algorithm
│   │   ├── needleman_wunsch_affine_gap.py
│   │   ├── needleman_wunsch_base.py
│   │   └── needleman_wunsch_tolerance.py
│   ├── /metrics
│   │   ├── alignment.py
│   │   └── alignment_lca.py
│   ├── /systems
│   │   ├── lift.py
│   │   └── system.py
│   ├── /evaluation
│   │   ├── /incubator
│   │   │   ├── incubator_gap_tuning.ipynb
│   │   │   └── incubator_variability_analysis.ipynb    
│   │   ├── /lift
│   │   │   ├── lift_comparison_analysis.ipynb
│   │   │   ├── lift_gap_tuning.ipynb
│   │   │   └── lift_variability_analysis.ipynb  
│   │   └── /braccio
│   │       ├── braccio_gap_tuning.yaml
│   │       └── braccio_fidelity_analysis.yaml
│   ├── /config_files
│   ├── /result_analysis
│   │   ├── alignment_graphic.py
│   │   ├── gap_tuning.py
│   │   └── statistical_graphics.py
│   ├── /packages
│   ├── /util
├── /resources
│   ├── /input
│   └── /output
├── /docs
│   ├── Technical_Report_General_Concepts.pdf
│   ├── Technical_Report_Elevator.pdf
│   ├── Technical_Report_Incubator.pdf
│   └── Technical_Report_Robotic_Arm.pdf
├── CITATION.cff
├── LICENSE
├── README.md
└── requirements.txt
```

Breakdown of the repository structure:

- /src:
    - /algorithm:
        - needleman_wunsch_base.py: abstract class with general alignment logic.
        - needleman_wunsch_tolerance.py: alignment implementation using _Simple Gap_.
        - needleman_wunsch_affine_gap.py: alignment implementation using _Affine Gap_.
    - /metrics
        - alignment.py: calculates the fidelity metrics for an alignment.
        - alignment_lca.py: extension of alignment.py including analysis of low-complexity areas.
    - /systems
        - System.py: general class that defines the **Comparison Function** between snapshots and the **Low Complexity
          Area** condition.
        - Lift.py: it extends System.py redefining the **Low Complexity Area** condition.
    - /evaluation: it includes the Jupyter Notebooks to reproduce all the analysis performed in
      the [Technical Reports](/docs).
    - /config_files: YAML configuration file to execute all the alignments included in the [Technical Reports](/docs).
    - /result analysis: auxiliary classes for data analysis.

    - /resources: raw traces for the alignments.
    - align_traces.py: main file to perform alignments. Instructions on how to use it
      in [Usage and examples](#usage-and-examples).

---

## Usage and examples

1. Open a _Linux/Windows Subsystem Linux_ command line
2. Navigate to the /src directory
3. Using Python 3.10, you can execute the following command to display the help information of our alignment script.

```python python3.10 align_traces.py -h```

```usage: align_traces.py [-h] [--figures] [--engine ENGINE] [--config CONFIG]
options:
  -h, --help       show this help message and exit
  --figures        It processes the alignment and generates figures as image files
  --engine ENGINE  Engine to process output pdf figures (orca or kaleido). By default, kaleido.
  --config CONFIG  Config file name stored in the /src/config folder
```

4. To execute alignments for the Incubator case study using one of the predefined YAML configuration files:

```
python3.10 align_traces.py --figures --engine kaleido --config incubator_comparison.yaml
```

---