from tkinter import *
from Game import GameState
from WinExp import WinExpCalculator

# This class provides a visible display of the game's win% as a tk widget
# It is extended from the Canvas widget, and uses the built in drawing
# functions from that class
class WinBar(Canvas):
  
  # Initializer function
  # Variables:
  #  master: tk master widget
  #  hColor: home color
  #  vColor: visitor color
  #  var: initial state of bar (0-100), defaults to 50
  def __init__(self,master,hColor,vColor,var=50):
    Canvas.__init__(self,master,width=400,height=50,bg='#E4E4E4')
    self.hColor = hColor
    self.vColor = vColor
    self.prevWin = var
    self.lastChange = 0
    self.update(var)
  
  # Updates the widget
  # var: value 0-100 to update the display to
  def update(self,var):
    #erases previous drawing
    self.create_rectangle(0,0,402,102,fill='#E4E4E4')
    
    #position in pixels of the dividing point
    posPix = 396*var/100 + 3
    #draw bar display
    self.create_line(3,25,posPix,25,width=12,fill=self.hColor)
    self.create_line(posPix,25,399,25,width=12,fill=self.vColor)
    self.create_line(posPix,0,posPix,50,fill='black')
    
    #previous position
    prevPix = 396*self.prevWin/100 + 3
    #draw arrow if significant change:
    if (var - self.prevWin) > 1:
      aPix = posPix - (posPix-prevPix)/4
      self.create_line(prevPix, 42, posPix, 42, width=2, fill=self.hColor)
      self.create_line(aPix, 35, posPix, 42, width=2, fill=self.hColor)
      self.create_line(aPix, 49, posPix, 42, width=2, fill=self.hColor)
    if (self.prevWin - var) > 1:
      aPix = posPix + (prevPix-posPix)/4
      self.create_line(prevPix, 42, posPix, 42, width=2, fill=self.vColor)
      self.create_line(aPix, 35, posPix, 42, width=2, fill=self.vColor)
      self.create_line(aPix, 49, posPix, 42, width=2, fill=self.vColor)
    
    self.lastChange = var - self.prevWin
    self.prevWin = var

# This class provides the GUI and manages data flow between the other classes
class App(Frame):
  def __init__(self,master=None):
    Frame.__init__(self,master)
    self.pack()
    self.hColor = "blue"
    self.vColor = "maroon"

    #stores information about the game
    self.gameState = GameState()
    #used to calculate win expectancy
    #Run Environment: 4.5
    #Home Team Win %: .5
    self.winCalc = WinExpCalculator(4.5,.5)
    
    self.createWidgets()
    self.updateGameDisplay()
    self.updateStateDisplay()
  
  # This function creates the widgets used in the GUI's display
  def createWidgets(self):
    #current state of game
    self.gameFrm = Frame(self)
    #home score
    self.homeFrm = Frame(self.gameFrm)
    self.homeScoreLbl = Label(self.homeFrm)
    self.homeScoreTxt = StringVar()
    self.homeScoreLbl["textvariable"] = self.homeScoreTxt
    self.homeScoreLbl.pack(side=TOP)
    self.homeScoreLbl.configure(foreground=self.hColor,font=20)
    self.homePctLbl = Label(self.homeFrm)
    self.homePctTxt = StringVar()
    self.homePctLbl["textvariable"] = self.homePctTxt
    self.homePctLbl.configure(foreground=self.hColor)
    self.homePctLbl.pack(side=TOP)
    self.homeFrm.pack(side=LEFT)
    #visitor score
    self.visFrm = Frame(self.gameFrm)
    self.visScoreLbl = Label(self.visFrm)
    self.visScoreTxt = StringVar()
    self.visScoreLbl["textvariable"] = self.visScoreTxt
    self.visScoreLbl.pack(side=TOP)
    self.visScoreLbl.configure(foreground=self.vColor,font=20)
    self.visPctLbl = Label(self.visFrm)
    self.visPctTxt = StringVar()
    self.visPctLbl["textvariable"] = self.visPctTxt
    self.visPctLbl.configure(foreground=self.vColor)
    self.visPctLbl.pack(side=TOP)
    self.visFrm.pack(side=RIGHT)
    #win probability
    self.winFrm = Frame(self.gameFrm)
    self.wBar = WinBar(self.winFrm,self.hColor,self.vColor)
    self.innLbl = Label(self.winFrm)
    self.innTxt = StringVar()
    self.innLbl["textvariable"] = self.innTxt
    self.baseLbl = Label(self.winFrm)
    self.baseTxt = StringVar()
    self.baseLbl["textvariable"] = self.baseTxt
    self.playLbl = Label(self.winFrm)
    self.playTxt = StringVar()
    self.playLbl["textvariable"] = self.playTxt
    self.wBar.pack(side=TOP)
    self.innLbl.pack(side=TOP)
    self.baseLbl.pack(side=TOP)
    self.playLbl.pack(side=TOP)
    self.winFrm.pack(side=TOP)
    
    #visual separator
    self.separator = Frame(self,height=5,borderwidth=5,relief=SUNKEN)
    self.gameFrm.pack(side=TOP)
    self.separator.pack(side=TOP,fill=X, padx=5, pady=5)

    #run specific plays
    self.playFrm = LabelFrame(self, text="Choose Play:", 
        borderwidth=2)
    self.plays = sorted(list(self.gameState.playDict.keys()))
    self.playMenVar = StringVar()
    self.playMenVar.set(self.plays[0])
    self.playSelect = OptionMenu(self.playFrm, self.playMenVar,*self.plays)
    self.playBttn = Button(self.playFrm, text="Run Play", 
        command=self.playClick)
    self.playSelect.pack(side=LEFT)
    self.playBttn.pack(side=LEFT)
    self.playFrm.pack(side=TOP)
    
    #visual separator
    self.separator2 = Frame(self,height=5,borderwidth=5,relief=SUNKEN)
    self.gameFrm.pack(side=TOP)
    self.separator2.pack(side=TOP, padx=5, pady=5)

    #enter a specific game state
    self.stateFrm = LabelFrame(self, text="Go To Specific Game State:", 
        borderwidth=2)
    self.innStFrm = Frame(self.stateFrm)
    self.innStLbl = Label(self.innStFrm, text="Inning: ")
    self.innEnter = Spinbox(self.innStFrm, from_=1, increment=1, to=100)
    self.halfStFrm = Frame(self.stateFrm)
    self.halfLbl = Label(self.halfStFrm, text="Top/Bottom: ")
    self.halfEnter = Spinbox(self.halfStFrm, values=("Bottom","Top"))
    self.outStFrm = Frame(self.stateFrm)
    self.outLbl = Label(self.outStFrm, text="Outs: ")
    self.outEnter = Spinbox(self.outStFrm, from_=0, to=2, increment=1)
    self.hStFrm = Frame(self.stateFrm)
    self.hStLbl = Label(self.hStFrm, text="Home Score: ")
    self.hEnter = Spinbox(self.hStFrm, from_=self.gameState.hScore, 
        increment=1, to=100)
    self.vStFrm = Frame(self.stateFrm)
    self.vStLbl = Label(self.vStFrm, text="Visitor Score: ")
    self.vEnter = Spinbox(self.vStFrm, from_=self.gameState.vScore, 
        increment=1, to=100)
    self.baseStFrm = Frame(self.stateFrm)
    self.stateBttn = Button(self.stateFrm, text="Go", command=self.stateClick)
    self.hStLbl.pack(side=LEFT)
    self.hEnter.pack(side=LEFT)
    self.vStLbl.pack(side=LEFT)
    self.vEnter.pack(side=LEFT)
    self.hStFrm.pack(side=TOP)
    self.vStFrm.pack(side=TOP)
    self.innStLbl.pack(side=LEFT)
    self.innEnter.pack(side=LEFT)
    self.innStFrm.pack(side=TOP)
    self.halfLbl.pack(side=LEFT)
    self.halfEnter.pack(side=LEFT)
    self.halfStFrm.pack(side=TOP)
    self.outStFrm.pack(side=TOP)
    self.outLbl.pack(side=LEFT)
    self.outEnter.pack(side=LEFT)
    self.baseStFrm.pack(side=TOP)
    self.baseStLbl = Label(self.baseStFrm, text="Baserunners: ")
    self.baseStLbl.pack(side=LEFT)
    self.baseInt = []
    self.baseCh = []
    self.baseNames = ["1st", "2nd", "3rd"]
    for i in range(0,3):
      self.baseInt.append(IntVar())
      self.baseCh.append(Checkbutton(self.baseStFrm, 
        variable=self.baseInt[i], text=self.baseNames[i]))
      self.baseCh[i].pack(side=LEFT)
    self.stateBttn.pack(side=TOP)
    self.stateFrm.pack(side=BOTTOM)

  #updates the game to a state provided by input from gui
  def stateClick(self):
    try:
      self.gameState.outs = int(self.outEnter.get())
      if(self.gameState.outs > 2 or self.gameState.outs < 0):
        raise ValueError("Bad Outs value")
      self.gameState.inning = int(self.innEnter.get())
      if(self.gameState.inning < 1):
        raise ValueError("Inning < 1")
      self.gameState.hScore = int(self.hEnter.get())
      if(self.gameState.hScore < 0):
        raise ValueError("Score < 1")
      self.gameState.vScore = int(self.vEnter.get())
      if(self.gameState.vScore < 0):
        raise ValueError("Score < 1")
    except ValueError as e:
      print("Bad Game State Input: " + str(e))
      return
    halfStr = self.halfEnter.get()
    if halfStr == "Bottom":
      self.gameState.half = 1
    elif halfStr == "Top":
      self.gameState.half = 0
    else:
      print("Bad inning half value: " + halfStr)
    for i in range(0,3):
      if self.baseInt[i].get() == 1:
        self.gameState.base[i] = True
      elif self.baseInt[i].get() == 0:
        self.gameState.base[i] = False
      else:
        print("Bad base checkbox value: " + str(self.baseInt[i].get()))
    self.updateGameDisplay()

  #runs a particular play from the drop down
  def playClick(self):
    play = self.playMenVar.get()
    self.gameState.runPlay(play)
    self.updateGameDisplay()
    self.updateStateDisplay()

  #updates the win probabilities displayed
  def updateProb(self):
    prob = self.getWinProb()
    self.wBar.update(prob)
    prob = int(round(prob, 0))
    self.homePctTxt.set("Win Pct: " + str(prob) + "%")
    self.visPctTxt.set("Win Pct: " + str(100-prob) + "%")
  
  # Simple function to call getWinPct with the correct arguments
  def getWinProb(self):
    p = self.winCalc.getWinPct(
        self.gameState.getBaseState(),
        self.gameState.hScore - self.gameState.vScore,
        self.gameState.inning,
        self.gameState.outs,
        self.gameState.half)
    return p*100

  # Updates the display of the state of the game (top) 
  def updateGameDisplay(self):
    # Inning display
    innStr = ""
    if self.gameState.half==0:
      innStr += "Top "
    elif self.gameState.half==1:
      innStr += "Bottom "
    innStr += "of inning "
    innStr += str(self.gameState.inning)
    innStr += ", " + str(self.gameState.outs) + " outs"
    self.innTxt.set(innStr)
    
    # Baserunner display
    baseStr = ""
    if self.gameState.getBaseState() == 1:
      baseStr = "Bases Empty"
    else:
      comma = 0
      if self.gameState.base[0]:
        comma = 1
        baseStr += " 1st"
      if self.gameState.base[1]:
        if comma == 1:
          baseStr += ","
        baseStr += " 2nd"
        comma += 1
      if self.gameState.base[2]:
        if comma > 0:
          baseStr += ","
        comma += 1
        baseStr += " 3rd"
      if comma > 1:
        baseStr = "Runners on:" + baseStr
      else:
        baseStr = "Runner on" + baseStr
    self.baseTxt.set(baseStr)
    
    # Score display
    hScore = self.gameState.hScore
    vScore = self.gameState.vScore
    if(hScore != -1):
        self.homeScoreTxt.set("Home " + str(hScore))
    if(vScore != -1):
        self.visScoreTxt.set("Visitor " + str(vScore))
    
    # Updates win probability and sets win % displays
    self.updateProb()

    # Win % change display
    lc = int(round(self.wBar.lastChange, 0))
    playTxt = "Last W% Change: "
    if lc > 0:
      playTxt += "Home +" + str(lc) + "%"
    elif lc < 0:
      playTxt += "Visitor +" + str(-1*lc) + "%"
    else:
      playTxt += "Change < 1%"
    self.playTxt.set(playTxt)

  # Updates the "Go to specific game state" section to follow the actual
  # game state
  def updateStateDisplay(self):
    while self.gameState.inning > int(self.innEnter.get()):
      self.innEnter.invoke('buttonup')
    while self.gameState.inning < int(self.innEnter.get()):
      self.innEnter.invoke('buttondown')
    if self.gameState.half == 0:
      self.halfEnter.invoke('buttonup')
    else:
      self.halfEnter.invoke('buttondown')
    while self.gameState.outs > int(self.outEnter.get()):
      self.outEnter.invoke('buttonup')
    while self.gameState.outs < int(self.outEnter.get()):
      self.outEnter.invoke('buttondown')
    while self.gameState.hScore > int(self.hEnter.get()):
      self.hEnter.invoke('buttonup')
    while self.gameState.hScore < int(self.hEnter.get()):
      self.hEnter.invoke('buttondown')
    while self.gameState.vScore > int(self.vEnter.get()):
      self.vEnter.invoke('buttonup')
    while self.gameState.vScore < int(self.vEnter.get()):
      self.vEnter.invoke('buttondown')
    for i in range(0,3):
      if self.gameState.base[i] == True:
        self.baseCh[i].select()
      else:
        self.baseCh[i].deselect()
    return

