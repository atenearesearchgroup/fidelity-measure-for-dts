# How to measure fidelity in a Digital Twin System? - A trace alignment algorithm

## Index

- [How to measure fidelity in a Digital Twin System? - A trace alignment algorithm](#how-to-measure-fidelity-in-a-digital-twin-system---a-trace-alignment-algorithm)
  - [Index](#index)
  - [Overview](#overview)
  - [Requirements and installation](#requirements-and-installation)
    - [Execution environment](#execution-environment)
    - [Required packages](#required-packages)
  - [Repository structure](#repository-structure)
  - [Usage and examples](#usage-and-examples)

## Overview

Digital twins are gaining relevance in many domains to improve the operation and maintenance of complex systems. Despite their importance, most efforts are currently focuses on their design, development and deployment, but do not fully address their validation. 

In this work, we are interested in assessing the fidelity of physical and digital twins, and more specifically whether they exhibit twinned behaviors. This will enable engineers to test the suitability of the digital twin for its intended purpose.  Our approach assesses their fidelity by comparing the behavioral traces of the two twins. In our context, traces are sequences of snapshots. Each snapshot represents the state of the system at a given moment in time. Thus, we try to check whether the two systems have gone through the same states at the same times, i.e., they exhibit similar behaviors. 

Our contribution is threefold. First, we have defined a measure of equivalence between individual snapshots capable of deciding whether two snapshots are sufficiently similar. Second, we have developed a trace alignment algorithm to align the corresponding equivalent states reached by the two twins. Finally, we measure the fidelity of the behavior of the two twins using the level of alignment achieved, in terms of the percentage of matched snapshots, and the distance between the aligned traces. 

This repository describes the *dynamic programming algorithm* that we have developed for aligning the behavioral traces of two systems, the digital and the physical twin. It is mainly based on the Needleman-Wunsch global alignment algorithm, although it also incorporates some of the optimizations proposed in the BLAST algorithm for aligning biological sequences, such as the possibility of defining strategies for deciding how to deal with sequences of gaps, or for masking low-complexity regions. We have also defined the *Maximum Acceptable Distance* (MAD), a threshold that determines when two snapshots are far enough apart to be matched. 

Our proposal has been validated with the digital twins of three cyber-physical systems: an elevator, an incubator and a robotic arm. We were able to determine which systems were sufficiently faithful and which parts of their behaviors failed to emulate their counterparts.

This repository also contains all artefacts and programs developed around this algorithm. It serves as a companion to the paper entitled _'Measuring the Fidelity of a Physical and a Digital Twin Using Trace Alignments,'_ which is currently under review. This repository can be cited using [CITATION.cff](CITATION.cff) or [CITATION.bib](CITATION.bib). 

The repository contains four technical reports in the [/docs](/docs) directory. [One of them](./docs/Technical_Report_General_Concepts.pdf) provides the detailed description of the algorithm and the precise definitions of all the metrics we have defined to assess the fidelity of two twins. The other three technical reports contain the detailed experiments we have performed to assess the fidelity of the three digital twins that have been used in our journal paper to demonstrate our proposal: an [elevator](./docs/Technical_Report_Elevator.pdf), an [incubator](./docs/Technical_Report_Incubator.pdf) and a [robotic arm](./docs/Technical_Report_Robotic_Arm.pdf).

<!--
This repository includes a dynamic programming algorithm based on the Needleman-Wunsch global alignment algorithm
applied to behavioral traces. The repository serves as a companion to the paper titled _'Measuring the Fidelity of a
Physical and a Digital Twin Using Trace Alignments,'_ which is currently under review and can be cited
using [CITATION.cff](CITATION.cff).

To obtain more information about the algorithm and the different examples and case studies with which it has been
validated, you can access the [/docs](/docs) directory and find the Technical Reports that accompany the article.
-->
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