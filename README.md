# MFP3
Mutual Fund Performance Predictor (MFP3). 
Georgetown Data Science Certificate Cohort 11 Capstone Project

# Team members:
MD Alam
Riley Back
Melissa Burn
Michael Iapalucci
Murali Kannan

# Project coordinator: 
Melissa Burn

# Hypothesis: 
Careful analysis of the language and style used by fund managers in their quarterly reports will reveal manager sentiment that can be used to predict fund performance in the near term.

# Brief description: 
Utilizing commentary published quarterly by mutual fund managers, the team will attempt to score commentary as positive (bullish), negative (bearish) or neutral based on specific language used by the managers.  While this commentary is typically very prosaic and not forward looking due to regulatory requirements, it is typically written by humans (although some has been automated using natural language generation methods) our hypothesis is that there will be subtle differences in the language that will point to underlying manager sentiment that can be positively correlated with fund performance.

# Data sources: 

www.fidelity.com

# Quick Start
This quick start is intended to setup the development environment.

Clone the repository
$ git clone https://github.com/AlamKhorshed/MFP3.git
$ cd MFP3

Create a virtualenv and install the dependencies
$ virtualenv capstone_vm
$ source capstone_vm/bin/activate
$ pip install -r requirements.txt

Run the Fidelity Comentery Scraper (if required). The Comentary direcory is allready populated with baseline 
$ pip FidelityComenteryWebScraper/FidelityScraper.py 
