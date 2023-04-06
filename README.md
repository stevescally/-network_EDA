# NEDA (Network Exploratory Data Analysis)

## Overview

This project analyzes publicly available network focused data sets to provide
insight into network activity as well as determine if machine learning concepts
can be implemented to accurately determine a similar conclusion automatically. It
is expected that additional tooling for performing data set maintenance will also
come about.

## Environment Configuration

* [Install Anaconda on Ubuntu 22](docs/anaconda_ubuntu_22.md) 

## (Jupyter) Notebook Templates

This directory contains frequently used notebook templates to quickly setup
common formats, layouts, or commands used within the exploratory process.
Different templates are available depending on the expected analysis work.

## Utils

This directory contains utilities for performing actions related to data set:

* Generation
* Procurement
* Enrichment

Typically the source data sets will be downloaded when you utilize the notebook
or standalone script. If data enrichment is part of the process the new data set
will be located within the data_set/generated sub-directory.

## Analysis

This directory contains notebooks and assorted programs to analyze downloaded
or generated data sets.

## Licenses

The licenses folder lists the open source licensing conditions as they apply
to the original data sets, notebooks, blog posts, or other analysis within this
repository. Check the NOTICE file for an explanation of coverage if a file does
not explicitly have a license defined.

A brief reasoning behind the chosen license's is to allow the content to be used
for learning and understanding while prohibiting implicit commercial use. While
I am not against commercial enterprises, using someone else's work provided
freely for monetary gain or advantage defeats the objective of shared ideas and
learning. If someone gains insight and understanding they should have no issue
writing their own implementation.

