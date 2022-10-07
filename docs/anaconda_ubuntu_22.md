# Overview

We will be using the [Anaconda
Distribution](https://www.anaconda.com/products/distribution) to setup our
Jupyter Lab environment. Anaconda includes a number of packages for data
analysis as well as managing multiple virtual programing environments. While
there is a GUI interface will will launch most of our items remotely through
terminal and SSH port forwarding / tunneling. This allows us to use server type
hardware for our processing verses our local machine.

# Installation

1. Navigate to the [Anaconda Repo](https://repo.anaconda.com/archive/) and download the
64-Bit(x86) installer.  
``curl -o Anaconda3-2022.05-Linux-x86_64.sh https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh``
2. Copy the SHA256 sum value to and confirm the calculated sha256sum matches the posted sha256sum.
``sha256sum Anaconda3-<downloaded-version>-Linux-x86_64.sh | grep <downloaded-version-sha256sume-value>`` 
3. Run the installation script after a successful sha256sum match.
``sh Anaconda3-<downloaded-version>-Linux-x86_64.sh``
4. After the installation you can source your .bashrc file to update any new paths. Your command prompt should also change to reflect the current anaconda environment. The default is ``(base)``
``sscally@eda01:~$ source .bashrc
  (base) sscally@eda01:~$
``
5. Install the [Jupyterlab git extension](https://github.com/jupyterlab/jupyterlab-git) from the command line.
``conda install -c conda-forge jupyterlab-git``

# Starting JupyterLab Application

1. Run the following command: ``jupyter lab --no-browser --port 8080`` Make note of the provided *token* value.
2. Setup SSH port forwarding tunnel. In another terminal window on your local device run the following:
``ssh -L8080:localhost:8080 <remote node / IP address>``
3. Open a local browser window to http://localhost:8080. Use the token value from the jupter lab start-up logs. 

