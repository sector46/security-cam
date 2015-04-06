# Security-Cam

Security-Cam is a simple security system that detects movement through a UVC compatible webcam, records the movement
with photos and video, which can then be sent to the registered Gmail address (limited to Gmail accounts at the moment). 

This was created as a project for the Intel Edison chip, but it should 
be compatible with all Linux systems that have Python and OpenCV 
installed (python-opencv package). In the setup, I will cover how to set 
it up on the Edison.

## Setup
If you haven't set up your Edison already, please follow this [guide](https://software.intel.com/en-us/iot/getting-started).

## Packages

For this portion, I'll use some of the same packages that drejkim's [edi-cam](https://github.com/drejkim/edi-cam) project uses,
so I'll post their package setup here (be sure to check out their project as well!).

## Configuring the package manager

Edison's operating system is based off Yocto Linux, which uses `opkg` as its package manager. [AlexT's unofficial opkg repository](http://alextgalileo.altervista.org/edison-package-repo-configuration-instructions.html) is highly recommended for adding packages to Edison. It includes many useful packages, such as git and the UVC driver.

To configure the repository, add the following lines to `/etc/opkg/base-feeds.conf`:

    src/gz all http://repo.opkg.net/edison/repo/all
    src/gz edison http://repo.opkg.net/edison/repo/edison
    src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32

The configuration used in this demo is also provided for reference. If `/etc/opkg/base-feeds.conf` is empty, simply copy this file into `/etc/opkg/`.

Update `opkg`:

    opkg update

If the update is successful, the output should look like this:

    Downloading http://repo.opkg.net/edison/repo/all/Packages.gz.
    Inflating http://repo.opkg.net/edison/repo/all/Packages.gz.
    Updated list of available packages in /var/lib/opkg/all.
    Downloading http://repo.opkg.net/edison/repo/edison/Packages.gz.
    Inflating http://repo.opkg.net/edison/repo/edison/Packages.gz.
    Updated list of available packages in /var/lib/opkg/edison.
    Downloading http://repo.opkg.net/edison/repo/core2-32/Packages.gz.
    Inflating http://repo.opkg.net/edison/repo/core2-32/Packages.gz.
    Updated list of available packages in /var/lib/opkg/core2-32.

## Cloning this repository onto Edison

To install git:

    opkg install git

Then clone this repository using `git clone <git repo URL>`.

## Installing Python and OpenCV

This program uses Python and OpenCV so we'll need those packages to run (I'm also including other 
python packages for a complete installation):

    opkg install python-pkgutil python-audio python-image python-email python-netserver python-xmlrpc python-distutils python-ctypes python-html python-json python-compile python-misc python-numbers python-unittest python-difflib opencv python-opencv

## Getting Started

To start with, you'll want to create a configuration file called 'security.conf' by running `./configure.sh`
In addition to just running the command by itself, you can issue other flags (you can find out more
details about them by running the -h or --help flag.

Once the 'security.conf' file is generated, you can run `./run_security.sh` to start the program.
It only runs once at the moment, so once movement is detected, it will save the pictures/video, send out any 
messages (if configured to do so), and then wait for the user to press 'q' to quit.

If you want to remove pictures and/or video to free up space for more pictures/video, you will need to manually remove the "Group <Number>" folder inside the 'Pictures' and 'Video' folders.
