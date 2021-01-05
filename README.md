<p align="center">
  <img src="https://i.imgur.com/yLuFUF5.jpg" />
  <h1 align="center">Telesource</h1>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
Telesource is a self-initiated project done out of pure interest. As the source academy website (from NUS module CS1101S) then was not built to be mobile friendly, this project was conceived to create a simple telegram bot that will allow users to type and execute source code directly. As of the last update to this project, the telegram bot runs source code on version 4. Note that this repository contains work pertaining to the telegram bot of the project only. Work for the API that is responsible for taking in and executing the source code can be found here:
```
https://github.com/tjtanjin/telesource_api
```
You may check out the bot at the link below:
```
https://t.me/telesourcebot
```

### Features
Telesource is usable with a few simple commands. Upon registering with the /register command, users can immediately toggle coding mode on with the /code command. At any point, should the user wish to look at the current code, the /view command will return a beautified view of the code. Finally, once the code is deemed to be complete, the user can execute the code with just the /run command! An option to select the source version is also available with /version <number>
##### Supported Source Versions:
```
1
2
3
4
```
In addition to the above commands, administrators also have access to /broadcast to announce updates to all registered users as well as /logs to retrieve logs of all executed codes (for debugging purposes).

### Technologies
Technologies used by Telesource are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Deployed on:
<p align="center">
  <img height="150" width="150" src="https://pbs.twimg.com/profile_images/1089877713408557056/aO_IAlp__400x400.jpg" />
</p>
<p align="center">
Upcloud
</p>

##### Project Repository
```
https://github.com/tjtanjin/telesourcebot
```

### Setup
The following section will guide you through setting up your own Telesource (telegram account required).
* First, head over to [BotFather](https://t.me/BotFather) and create your own telegram bot with the /newbot command. After choosing an appropriate name and telegram handle for your bot, note down the bot token provided to you.
* Next, cd to the directory of where you wish to store the project and clone this repository. An example is provided below:
```
$ cd /home/user/exampleuser/projects/
$ git clone https://github.com/tjtanjin/telesourcebot.git
```
* Following which, create a config folder and within it, create a token.json file, saving the token you received from [BotFather](https://t.me/BotFather) as a value to the key "token" as shown below:
```
{"token": "your bot token here"}
```
* Under the same config folder, create another file called endpoint.json which would contain the API endpoint as value to the endpoint key. An example is shown below:
```
{"endpoint": "your_endpoint_ip_address/api/v1/run"}
```
* Next, create two empty folders (logs & userinfo) in the base directory of the project:
```
$ mkdir logs
$ mkdir userinfo
```
* Finally, from the base directory of the project, execute the following command and the terminal should print "Running..." if everything has been setup correctly!
```
$ python3 telesource.py
```
* Note that with all these setup, only the telegram bot is working. Executing /run will not yield any result until the API for executing source code is setup. For that, please refer to the setup guide [here](https://github.com/tjtanjin/telesource_api#setup).
* If you wish to host your telegram bot online 24/7, do checkout the guide [here](https://gist.github.com/tjtanjin/ce560069506e3b6f4d70e570120249ed).

### Team
* [Tan Jin](https://github.com/tjtanjin)

### Contributing
If you have code to contribute to the project, open a pull request and describe clearly the changes and what they are intended to do (enhancement, bug fixes etc). Alternatively, you may simply raise bugs or suggestions by opening an issue.

### Others
For any questions regarding the implementation of the project, please drop an email to: cjtanjin@gmail.com.
