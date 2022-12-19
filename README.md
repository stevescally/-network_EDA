# NEDA (Network Exploratory Data Analysis)

## Overview

This project analizes publicly available network focused datasets to provide
insight into network activity as well as determine if machine learning concepts
can be implemented to accurately determine a similar conclusion automaticly. It
is expected that additional tooling for performing dataset maintence will also
come about.

## Environment Configuration

* [Install Anaconda on Ubuntu 22](docs/anaconda_ubuntu_22.md) 

## (Jupyter) Notebook Templates

This directory contains frequently used notebook templates to quickly setup
common formats, layouts, or commands used within the exploratory process.
Different templates are available depending on the expected analysis work.

## Utils

This directory contains utilities for dataset:

* Generation
* Procurement 
* Eenrichment

Typically the source dataset(s) will be downloaded when you utilze the notebook
or standalone script. If data enrichment is part of the process the new dataset
will be located within the dataset/generated subdirectory. 

## Analysis

This directory contains notebooks and assorted programs to analyze downloaded
or generated datasets.

## Licenses

The licenses folder lists the open source licensing conditions as they apply
to the original datasets, notebooks, blog posts, or other analysis within this
repository. Check the NOTICE file for an explaination of coverage if a file does
not explicitly have a license defined.

A brief reasoning behind the choosen liceses is to allow the content to be used
for learning and understanding while prohibting implicit commercial use. While
I am not against commercial enterprises, using someone elses work provided
freely for monitary gain or advantage defeats the objective of shared ideas and
learning. If someone gains insight and understanding they should have no issue
writing their own implementation.

