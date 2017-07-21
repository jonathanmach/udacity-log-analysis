## Log Analysis Project
Source code for Udacity Log Analysis Project.

The project involves creating a reporting tool that prints out reports (in plain text) based on a mock database for a news website.
The database contains information about articles, its authors and a table containing the log of the website views.


## Run the project
For this project, we are using a VM that contains Python and a PostgreeSQL server installed.
You can skip the VM installation in case you already have Python and a PostgreeSQL server installed.

### Installing the Virtual Machine
We're using Vagrant to install and manage the VM.

* You can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
* Change to this directory in your terminal with cd.
* Inside, you will find another directory called vagrant. Change directory to the vagrant directory.

### Start the virtual machine
* From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!


### Download the data
To run the reporting tool, you'll need to load the site's data into your local database.

* Download the file: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
* You will need to unzip this file after downloading it.
* The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
* To load the data, use the command: psql -d news -f newsdata.sql.

### Running the report
* Make sure you're inside the /vagrant directory 
* Execute the command: python report.py
* It will print out the report in plain text.

## Screenshot
![Alt text](https://raw.githubusercontent.com/jonathanfmachado/udacity-log-analysis/master/report_screenshot.png "Screenshot Sample")