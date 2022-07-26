# DICVA
Speech recognition Linux GUI Application

## Description

DICVA is an intelligent voice command detection and interpretation system that can effectively recognize a limited set of commands. After recognition, the application runs varying operating system tasks on the user's computer in order to automate everyday mundane tasks.

## Supported commands

<ul>
<li>code: opens an application of the integrated development environment (IDE) type.</li>
<li>hello: allows the user to verify that the system is listening, will be greeted by the application.</li> 
<li>ip: displays in a browser window the user’s public IP address.</li>
<li>load: displays the proccesses consuming resources on the users computer.</li>
<li>news: displays in a browser window the most recent news.</li>
<li>stop: allows the user to terminate the listening state of the application</li>
<li>terminal: opens a new terminal window.</li>
<li>weather: displays in a browser window the weather for today in the user’s current location</li>
<li>write: opens a text editor</li>
</ul>

## About

The project is layed out in multiple folders and each folder contains scripts that serve a certain purpose:

<ul>
<li>building_model: scripts related to building the AI model, dataset preparation and augmentation, model architecture definition, performance evaluation</li>
<li>gui: source code for the entire GUI application, can only recognize the limited set of supported commands</li>
<li>gui2: source code for updated version of GUI application, this version can recognize any set of voice commands using Google Speech Recognition API</li>
<li>mydataset: contains the script that allows for users to record voice commands that can be added to the dataset. All audio files will be saved in this folder</li>
</ul>
