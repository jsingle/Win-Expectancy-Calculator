# This class stores information about the state of a baseball game.
# Information stored:
#       Inning
#       Inning half
#       Outs
#       Score (home score, visitor score)
#       Baserunners - boolean value per base
#       
# It also includes functions to perform basic plays on that game state.
class GameState():
  #initialize to the beginning of a game; top of the first
  def __init__(self):
    self.inning = 1
    self.half = 0
    self.hScore = 0
    self.vScore = 0
    self.base = []
    for i in range(0,3):
      self.base.append(False)
    self.outs = 0
    self.playDict = {
        "Strike Out": self.playK,
        "Walk": self.playBB,
        "Ground Out": self.playGO,
        "Fly Out": self.playFO,
        "Sac Fly": self.playSF,
        "Double Play": self.playDP,
        "Stolen Base": self.playSB,
        "Single": self.play1B,
        "Double": self.play2B,
        "Triple": self.play3B,
        "Home Run": self.playHR
        }

  # returns an integer code (1-8) representing a base runner configuration
  def getBaseState(self):
    #bases empty:
    if (not self.base[0]  and not self.base[1] and not self.base[2]):
      return 1
    #1st:
    elif (self.base[0] and not self.base[1] and not self.base[2]):
      return 2
    #2nd:
    elif (not self.base[0] and self.base[1] and not self.base[2]):
      return 3
    #1st, 2nd:
    elif (self.base[0] and self.base[1] and not self.base[2]):
      return 4
    #3rd:
    elif (not self.base[0] and not self.base[1] and self.base[2]):
      return 5
    #1st, 3rd:
    elif (self.base[0] and not self.base[1] and self.base[2]):
      return 6
    #2md, 3rd:
    elif (not self.base[0] and self.base[1] and self.base[2]):
      return 7
    #bases loaded
    elif (self.base[0] and self.base[1] and self.base[2]):
      return 8
    else:
      return 0
  
  #finds a play in the dictionary and calls the corresponding class function
  def runPlay(self, play):
    try:
      funct = self.playDict[play]
    except KeyError:
      print("Play not found in dictionary...")
      return 
    funct()
  
  #Strikeout
  def playK(self):
    self.outs += 1
    self.out3Check()
  
  #Walk
  def playBB(self):
    if self.base[0]:
      if self.base[1]:
        if self.base[2]:
          self.score(1)
        else:
          self.base[2] = True
      else:
        self.base[1] = True
    else:
      self.base[0] = True
  
  #Ground out: runners advance
  def playGO(self):
    self.outs += 1
    self.out3Check()
    if self.outs != 0:
      self.advAllRunners()
  
  #Fly out
  def playFO(self):
    self.outs += 1
    self.out3Check()
  
  #Sacrifice Fly: 
  #  A runner from 2nd base will advance, a runner on 1st will not
  def playSF(self):
    if self.base[2]==False and self.base[1]==False:
      print("SF not valid (baserunners)")
      return
    if self.outs == 2:
      print("SF not valid (2 outs)")
      return
    self.outs += 1
    self.advAllRunners()
    if self.base[1] == True:
      self.base[1] = False
      self.base[0] = True
  
  #Double Play: trailing runner is out, others advance
  def playDP(self):
    if self.getBaseState()==1:
      print("DP not valid (no baserunners)")
      return
    if self.outs == 2:
      print("DP not valid (2 outs)")
      return
    self.outs += 2
    #trailing runner is thrown out, other runners advance
    if self.outs == 2:
      if self.base[0]:
        self.base[0] = False
      elif self.base[1]:
        self.base[1] = False
      elif self.base[2]:
        self.base[2] = False
      self.advAllRunners()
    self.out3Check()
  
  #Stolen base
  def playSB(self):
    self.advAllRunners()
  
  #Single
  def play1B(self):
    self.advAllRunners()
    self.base[0] = True
  
  #double
  def play2B(self):
    for i in range(0,2):
      self.advAllRunners()
    self.base[1] = True
  
  #tripple
  def play3B(self):
    for i in range(0,3):
      self.advAllRunners()
    self.base[2] = True
  
  #Home run
  def playHR(self):
    for i in range(0,3):
      self.advAllRunners()
    self.score(1)
  
  #checks if 3 outs; if so, moves on to next inning half
  def out3Check(self):
    if self.outs >= 3:
      self.outs = 0
      self.inning += self.half%2
      self.half = (self.half+1)%2
      for i in range(0,3):
        self.base[i] = False
  
  #advance each baserunner 1 base, 3rd base scores, 1st base left empty
  def advAllRunners(self):
    if self.base[2]:
      self.score(1)
    self.base[2] = self.base[1]
    self.base[1] = self.base[0]
    self.base[0] = False

  #scores a number of runs, crediting the correct team based on half
  def score(self,score):
    if self.half==0:
      self.vScore += score
    elif self.half==1:
      self.hScore += score
    else:
      print("GameState bad half: " + str(self.half))
