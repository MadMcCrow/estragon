# Estragon 

https://fr.wikipedia.org/wiki/Estragon#Anecdote

## About
Estragon is a simple tool to automate Godot processes on linux and possibly Windows 

## Current Status
Estragon is very much under development. I plan on using it to make, build and deploy Godot games easier.

Feature wise, some things are already functionnal:
- command line interface : you can pass it commands and it will interpret it, making it easy to use with make, sh and bat script
- Downloading the engine : specify a path (or use Estragon folder) to download the latest master branch of Godot
- Build the engine       : will build the engine using all the cpu cores availables

Planned Features :
- Interpret command file       : pass a configuration file as task
- add Modules to the engine    : do all the necessary preparation to implements new features into your Godot install
- build project for platform   : make an executable out of your project

## Requierements

You'll need all Godot's requierements as well as :

- `python3`
- `python3-git` (might be called `python-git` in you distro, you can also install it via pip)

as a reminder, these are the Godot's requierements on linux :

    build-essential scons pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl1-mesa-dev libglu-dev libasound2-dev libpulse-dev libfreetype6-dev libudev-dev libxi-dev libxrandr-dev yasm

if your using Ubuntu or Debian, you can install requierements like this :

    sudo apt install python3 python3-git build-essential scons pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl1-mesa-dev libglu-dev libasound2-dev libpulse-dev libfreetype6-dev libudev-dev libxi-dev libxrandr-dev yasm

## How Can I Help

I'm completely open to changes and improvement wether it would be to the licensing or the code.
You can also suggest features, libraries, etc.
