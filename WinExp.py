#!/usr/bin/python
import sqlite3 as sql;
import math;

# This class is used to calculate the win expectancy at any point in the game
# It requires a number of pre-calculated coefficients, which are read from a 
# .csv file and stored in a sql database
class WinExpCalculator:

  # Initializer function
  # runEnv: the run environment, in average runs per team per game.
  #     A standard/modern value would be 4.5; calculations will be slightly 
  #     less accurate if values very different from this are used
  # homeWin: the expected win percentage of the home team.  This variable
  #     can be used to model a home team advantage, or to model a difference
  #     in talent level between the two teams.  Calculations will be slightly
  #     less accurate if values very different from .5 are used
  def __init__(self,runEnv,homeWin):
    self.setupDatabase()
    self.runEnv = runEnv
    self.homeWin = homeWin
    self.homeRpi = (2*runEnv/(1 + math.pow(1/self.homeWin - 1,1/1.8)))/9
    self.visRpi = (2*runEnv/(1 + math.pow(1/(1-self.homeWin) - 1,1/1.8)))/9
    self.extrasWin = self.getExtrasWin()
    self.calcedDict = {}
  
  def setupDatabase(self):
    coeffFile = "baseruns_coefficients.csv"
    self.conn = sql.connect('baseruns_coefficients_db.db')
    self.c = self.conn.cursor()
    try:
      self.c.execute("""create table run_coefficients 
      (baseouts text,slope float, intercept float, 
      r1 float, r2 float, r3 float, r4 float, r5 float, 
      r6 float, r7 float, r8 float, r9 float, r10 float)""")
    except sql.OperationalError as sqlErr:
      print("sql message: " + str(sqlErr))
      print("Database probably already exists, continuing...")
      return
    skip = 1
    for line in open(coeffFile):
      if skip == 1:
        skip = 0
        continue
      vals = line.split(",")
      self.c.execute(
          "insert into run_coefficients values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
          vals)
    self.conn.commit()
 
  # returns an array containing the odds that each number of runs will
  # be scored in a given inning
  # rpi: average runs per inning
  def getRunPct(self,rpi):
    pcnts = []
    for i in range(0,11):
      bot = math.pow(rpi*.761 + 1,i+1)
      if i==0:
        top = 1
      else:
        top = rpi*.761*.761*math.pow(rpi*.761 - .761 + 1,i-1)
      pcnts.append(top/bot)
    return pcnts

  # gets the win% of the home team in extra innings
  def getExtrasWin(self):
    homeWinPct = 0
    visWinPct = 0
    homeScorePct = self.getRunPct(self.homeRpi)
    visitScorePct = self.getRunPct(self.visRpi)
    #Calculate odds that home team scores more runs:
    for hRuns in range(1,11):
      for vRuns in range(0,hRuns):
        homeWinPct += homeScorePct[hRuns]*visitScorePct[vRuns]
    #Calculate odds that visitors score more runs:
    for vRuns in range(1,11):
      for hRuns in range(0,vRuns):
        visWinPct += homeScorePct[hRuns]*visitScorePct[vRuns]
    homeExtrasWin = homeWinPct/(visWinPct+homeWinPct)
    return homeExtrasWin

  # returns an array containing the odds that each number of runs
  # will be scored in the remainder of the inning, given a number of outs
  # and runner configuration
  # Variables:
  #     baseSt: integer 1-8 representing different baserunner configurations
  #     outs: number of outs in the inning
  #     rpi: average runs per inning
  def getExptRuns(self,baseSt,outs,rpi):
    baseOuts = str(baseSt) + str(outs);
    if baseOuts == '10':
      return self.getRunPct(rpi);
    for row in self.c.execute("select * from run_coefficients where baseouts=?",
        (baseOuts,)):
      coeffs = row
    adjPcnts = []
    adjPcnts.append(rpi*coeffs[1] + coeffs[2])
    for run in range(1,11):
      adjPcnts.append((1-adjPcnts[0])*coeffs[run+2])
    return adjPcnts

  # getWinPct
  # This function recursively calculates the odds that the home team will win.
  # It calculates these odds based on the inning, the runners on base, the
  # number of outs, and the score
  # Variables:
  #  baseState: integers 1-8 designate different base runner configurations
  #  scoreDiff: number of runs that the home team leads by (can be negative)
  #  inning: integer representing inning of play
  #  outs: number of outs; 0-2
  #  half: 0 signifies top of inning, 1 signifies bottom
  def getWinPct(self,baseState,scoreDiff,inning,outs,half):
    
    #innings 9 and later are treated the same in this model
    if inning > 9:
      inning=9
    #game is very close to decided:
    if scoreDiff > 15:
      return 1
    if scoreDiff < -15:
      return 0

    #see if this particular state has already been calculated;
    #this prevents many unnecessary recursive calls
    key = str(baseState) + str(scoreDiff) + str(inning) + str(outs) + str(half)
    try:
      prob = self.calcedDict[key]
    except KeyError:
      prob = 0
    else:
      return prob
   
    mod = 1 #so that runs are added/subtracted to scoreDiff correctly
    if half == 0:
      runPcts = self.getExptRuns(baseState,outs,self.visRpi)
      mod = -1
    elif half == 1:
      runPcts = self.getExptRuns(baseState,outs,self.homeRpi)
      #bottom 9
      if inning==9:
        if scoreDiff > 0: #home team has won
          return 1
        if scoreDiff == 0: 
          #odds home doesn't score 0, plus their win% in extras
          return (1-runPcts[0]) + self.extrasWin*runPcts[0]
        if scoreDiff < 0: #home is behind
          prob = 0
          for run in range(1,11):
            if scoreDiff + run > 0: #home wins
              prob += runPcts[run]
            if scoreDiff + run == 0: #home ties
              prob += runPcts[run]*self.extrasWin
          return prob
    prob = 0
    # for each possible number of runs scored in the rest of the inning, 
    # recursively calculate the win% based on that new game state:
    for run in range(0,11):
      prob += runPcts[run] * self.getWinPct(1, scoreDiff + mod*run, 
          inning + half, 0, (half+1)%2)
      self.calcedDict[key] = prob
    return prob
