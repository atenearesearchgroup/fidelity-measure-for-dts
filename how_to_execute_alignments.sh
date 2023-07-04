#!/bin/bash
# shellcheck disable=SC2164
# Source the utils.sh script
source utils.sh

# Welcome to the Alignment script instructions
# This script explains how to use the repository files to align a set of traces

echo "Step 1: Install Python 10 and git"
echo ""
ask_question "Do you have git and Python 10 installed?"
if [[ $? -eq 1 ]]; then
    exit 0
fi
echo ""
echo ""

echo "Step 2: Clone the repository"
echo ""
echo "git clone https://github.com/atenearesearchgroup/fidelity-measure-for-dts"
ask_question "Do you want to clone the repository?"
if [[ $? -eq 0 ]]; then
    python3.10 git clone https://github.com/atenearesearchgroup/fidelity-measure-for-dts
fi
echo ""
echo ""

echo "Step 3: Install the required packages"
echo ""
echo "python -m pip install -r requirements.txt"
ask_question "Do you want to install the required packages?"
if [[ $? -eq 0 ]]; then
    python3.10 -m pip install -r requirements.txt
fi
echo ""
echo ""

echo "Step 4: Navigate to the script's directory."
echo ""
cd src
echo "cd src"
echo ""
echo ""

echo "Step 5: Run the Python script with various options."
echo ""
echo "To display help message:"
echo "python align_traces.py -h"
ask_question "Do you want to check the help message?"
if [[ $? -eq 0 ]]; then
    python3.10 align_traces.py -h
fi
echo ""
echo ""

# Example to execute a batch of alignments
echo "Step 6: How to execute a batch of alignments using the example file incubator.yaml:"
echo ""
echo "This command will:"
echo "    - Create a figure in pdf for each alignment (--figures)"
echo "    - Use kaleido as the processing engine for the pdf"
echo "    - Use the example incubator.yaml config file as the alignment configuration."
echo "        Also available: lift.yaml and robotic_arm.yaml"
echo ""
echo "python align_traces.py --figures --engine kaleido --config_ex incubator.yaml"
ask_question "Do you want to execute the previous command?"
if [[ $? -eq 0 ]]; then
    python3.10 align_traces.py --figures --engine kaleido --config_ex incubator.yaml
fi
echo ""
echo ""

