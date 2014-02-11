WE Calculator - written by Jordan Singleton

This is a tool for calculating the Win Expectancy in a baseball game.
It provides a GUI for visualizing the Win Expectancy and for users to 
manipulate the state of the game.  The app is written in Python 3, and uses
the Tkinter package to implement the GUI with Tlc/Tk.

Win Expectancy is a sabermetric measure of the odds that a team has to win
the baseball game.  It is calculated based on the score, the number of outs,
the inning, and the baserunners.  It also factors in constants representing 
the run environment (expected runs per inning) and the home team's expected 
winning percentage vs the visiting team.  Win Expectancy is calculated based
on historical data for the number of runs that are expected to scored in an
inning given outs, runners on, and run environment.  This uses the concept of 
baseruns.  The total Win Expectancy is then calculated using a recursive 
formula, with an iteration occuring per half inning remaining, and the base 
case occuring at inning 9.  The calculations in this app are based on the
WinExp spreadsheet at ftp://ftp.baseballgraphs.com/wpa/

This app consists of four python scripts:
WinExp.py - Implements Win Expectancy calculation
Game.py - Class for keeping track of the game state and performing plays on it
Gui.py - Defines the GUI of the app
Challenge.py - calls methods from other files to run the app

The app also requires baseruns_coefficients.csv, which is a file containing 
some constants necessary for the calculations.

To use the app, run "python Challenge.py" from the directory where the .py and
the .csv files are located.
