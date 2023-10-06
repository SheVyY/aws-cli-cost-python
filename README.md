AWS CLI Cost Tool
=================

A Python-based command-line interface tool to retrieve and display AWS cost data in various formats.

Features
--------

-   Retrieve AWS cost data for a specific account.
-   Display cost data in multiple formats: CSV, JSON, plain text, and fancy display.
-   Send cost data notifications to Slack.
-   Configurable settings for different AWS accounts and regions.
-   Built-in logging for debugging and monitoring.

Installation
------------

1.  Clone the repository:

    bashCopy code

    `git clone https://github.com/SheVyY/aws-cli-cost-python.git`

2.  Navigate to the project directory:

    `cd aws-cli-cost-python`

3.  Install the required packages:

    Copy code

    `pip install -r requirements.txt`

Usage
-----

1.  Configure your AWS credentials and settings using `config.py`.

2.  Run the tool:

    `python main.py`

3.  Use the various flags and options to customize the output format and destination.
