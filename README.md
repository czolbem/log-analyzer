<h3 align="center">Log Analyzer</h3>

<div>
  <p align="center">
    A simple command-line tool to parse log files and provide statistics
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li>
      <a href="#development">Development</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#local-usage">Local usage</a></li>
        <li><a href="#tests">Tests</a></li>
      </ul>
    </li>
  </ol>
</details>

## Getting Started

### Prerequisites

For simple usage, Docker needs to be installed and running. For development, this tool requires Python >= 3.12.

### Usage

This tool can be run using a Docker container. The tool is configured as the entrypoint for the container.

1. To build the image, run this command from the repository root directory
    ```sh
   docker build --tag=local/analyzer . 
   ```
   You can choose any tag to name the image.
2. To run the image in a container
    ```sh
   docker run --mount type=bind,source=/host/data,target=/container/data local/analyzer /container/data/access.log -o /container/data/results.json --mfip
   ```
   To have access to log files on the local machine and the output file of the tool, we need to mount a host directory into the container.
   This is done using ```--mount```. The ```source``` is the directory on the host machine containing the log files to be analysed.
   The ```target``` is the directory in the container. Both paths need to be absolute.
   Make sure to specify input and output files using the ```target``` path as prefix.

   ```local/analyzer``` specifies the image to run in this container, set this to the tag you used in step 1.

   Everything after this tag is passed through to the command-line tool inside the container, in this case
   ```/container/data/access.log -o /container/data/results.json --mfip```.

Information about the tool's usage can be displayed by calling the tool with ```-h```:
```
usage: analyzer [-h] [-o [OUTPUT]] [--mfip] [--lfip] [--eps] [--bytes] input [input ...]

Analyze log files

positional arguments:
  input                 Path to one or more log files

options:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Path to the output file, default: stdout
  --mfip                Calculate most frequent IP
  --lfip                Calculate least frequent IP
  --eps                 Calculate events per second
  --bytes               Total amount of bytes exchanged
```

For the example in step 2, the tool is called with one input file that is read from the directory mounted into the container (```/container/data/access.log```).
For multiple input files, just call the tool with multiple paths separated by whitespaces.
The output is written to a file (```-o /container/data/results.json```), in this case again to the mounted directory.
With the option ```--mfip```, the output file contains the most frequent IP that is found in the supplied logs.

Some more details about the options:
- ```input```: Currently only supports files in CSV format that follow this example: [Example Log][log-file].
- ```-o``` ```--output```: Currently only writes results to output in JSON format.
- ```--mfip```: Most frequent IP. There can be more than one IP with that property, in that case one IP is chosen.
An alternative would be to use a list with all IPs that share the same count.
- ```--lfip```: Least frequent IP. See ```--mfip``` for details on multiple IPs with that property.
- ```--eps```: Average events per second between min and max time.
- ```--bytes```: Sum of response header and response sizes. A response size is only used in the sum if the size is positive. This is done because the response size
        can be -1 (e.g., when response data is returned 'Chunked'). Adding entries with -1 to the sum would slightly taint the
        overall value.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Development
These commands are tested in Windows 10, adjust them for your OS.

### Installation

1. (Optional) Create a virtual environment
   ```sh
   python -m venv \path\to\myenv
   ```
2. (Optional) Activate the virtual environment
   ```sh
   <venv>\Scripts\activate.ps1
   ```
3. To install the analyzer, run this command from the repository root directory
   ```sh
   python -m pip install -e .
   ```
   This installs the analyzer in editable mode.

### Local usage
Call the tool on a command-line with ```analyzer```, e.g.
   ```sh
   analyzer access.log -o results.json --mfip
   ```
### Tests
1. Install test requirements
   ```sh
   python -m pip install -r requirements-test.txt
   ```
   or
   ```sh
   python -m pip install -e .[test]
   ```
2. Run the test suite with pytest, e.g., from the repository root directory
   ```sh
   pytest .
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

[log-file]: https://www.secrepo.com/squid/access.log.gz
