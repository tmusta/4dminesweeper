"""
4D-miinantallaaja, Ohjelmoinnin perusteet- lopputyö. Toni Musta (2497530). Koodin alussa on muutamia yleisesti käytettäviä funktioita, joille en löytänyt järkevämpää paikkaa. Ohjelman pääfunktio koostuu pelkästään start()-funktiosta(rivi 98), josta voidaan suurinpiirtein seurata koodia ohjelman suorittamassa järjestyksessä. Mikäli haluat arvioida vain normaalin miinaharavan koodin, jätä rivit 127-136, 160-168, 194-213 ja 436-820 lukematta, niissä suoritetaan kolme- ja neljäulotteinen miinaharava.
Ohjelmassa on käytetty python 3.5.1-versiota.
"""
import csv
import random
import re
import datetime
import os
import math
import _thread

# Näitä global muuttujia käytetään käyttäjän antamien x ja z koordinaattien määrittämiseen
LETTERS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
C_LETTERS = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]		

def question(options, q): #Tämä funktio kysyy käyttäjältä kysymystä, kunnes saa hyväksyttävän vastauksen.
  while True:
    a = input(q)
    if a == "q" or a == "quit":
      quit()
    elif a == "h" or a =="help":
      os.system('clear')
      help()
    elif options == "int":
      try:
        return int(a)
      except(TypeError, ValueError):
        print("Invalid input")
    elif options == "all":
      return a
    elif not a in options:
      print("Invalid input")
    else:
      return a
      
def scale_question(dimension):#Kysyy käyttäjältä miinakentän koon ja tarkistaa, ovatko mitat laillisia. 26, koska eng. aakkosia on 26; 60, koska w-koordinaatit otetaan minuutin jakojäännöksestä ja 3, koska huvin vuoksi. Laitoin selvyyden vuoksi omaan funktioon.
  while True:
    bx = question("int","\n Now, Write a number for the width of the field(min 3, max 26 ): ")
    if int(bx) <= 26 and int(bx) >= 3:
      break
    else:
      print("Invalid input. Number must be bigger than 3, but smaller than 26")
  while True:
    by = question("int","\n Write a number for the height of the field(min 3): ")
    if int(by) >= 3:
      break
    else:
      print("Invalid input. Number must be bigger than 3")
  if dimension == "3" or dimension == "4":
    while True:
      bz = question("int","\n Write a number for the depth of the field (min 3, max 26): ")
      if int(bz) <= 26 and int(bz) >= 3:
        break
      else:
        print("Invalid input. Number must be bigger than 3, but smaller than 26")
  if dimension == "4":
    while True:
      bw = question("int","\n Write a number for the duration of the field (min 3, max 60): ")
      if int(bw) <= 60 and int(bw) >= 3:
        break
      else:
        print("Invalid input. Number must be bigger than 3, but smaller than 60")
  if dimension == "2":
    return bx, by
  elif dimension == "3":
    return bx, by, bz
  elif dimension == "4":
    return bx, by, bz, bw
          
def help(): #Tulostaa ohjeet, kun käyttäjä syöttää 'help' tai 'h'
  with open("minerake_help.txt") as source:
    for line in source:
      print(line.rstrip())
      
def opening_screen(): #Tulostaa alkukuvan kun ohjelma käynnistetään
  with open("minerake_sick_graphics.txt") as source:
    for line in source:
      print(line.rstrip())
      
def write_stats(dim, scale ,mines, turn, time, date, result):
  with open("minerake_stats.txt", "a",newline="") as source:
    csv.writer(source).writerow([dim, scale, mines, turn, time, date, result])
    
def read_stats():
  try:
    with open("minerake_stats.txt") as source:
      print("Dimensions \tSize \tMines \tTurns \tTime \t\tDate \t\t\tEndresult \n")
      lines = list(csv.reader(source))
      for line in reversed(lines):
        #line = str.split(line,",")
        print(line[0] + "\t\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + line[4] + "\t" + line[5] + "\t"  + line[6])
      print("\n") 
  except(IOError):
    print("No current stats")
  except(IndexError):
    pass
    
def start(): # "Pääohjelma"
  os.system("clear")
  start = "ON"
  opening_screen()
  print("\nWelcome to the 4D-minerake. Made by Toni Musta to Ohjelmoinnin peruskurssi-final work.\n")
  while start != "OFF":
    print(" Write 'play' for a new game, 'stats ' for list of played games and 'help' for instructions. Write 'quit' at any point for quitting.")
    n = question(["play", "stats"],"Write command: ")
    if n == 'play':
      start = game()
    elif n == 'stats':
      read_stats()
    
def game(): # Tässä alustetaan peli, eli kysytään kentän mitat, miinojen määrät ja uudelleen peluu.
  bx = 0
  by = 0
  bz = 0
  bw = 0
  os.system("clear")
  game = "ON"
  vol = 0
  while game != "OFF":
    a = question(["2","3","4"],"\n Great! Now pick the amount of dimensions you want (2,3 or 4):")    
    if a == "2": 
      bx, by = scale_question("2")
      if int(bx) < 7 and int(by) < 7:
        print("\nWhew, that's a small square. Well, I suppose size doesn't really matter :^)") 
      vol = bx * by
    if a == "3": 
      bx, by, bz = scale_question("3")
      if int(bx) < 7 and int(by) < 7 and int(bz) < 7:
        print("\nWhew, that's a small cube. Well, I suppose size doesn't really matter :^)")   
      vol = bx * by * bz  
    if a == "4":
      bx, by, bz, bw = scale_question("4")
      if int(bx) < 7 and int(by) < 7 and int(bz) and int(bw) < 7:
        print("\nWhew, that's a small terasect. Well, I suppose size doesn't really matter :^)") 
      vol = bx * by * bz * bw
    c = question("int","\nHow many mines do you want in it? ( Must be lesser than previous numbers multiplied with each other): ")
    while not (int(c) > 0 and int(c) < vol):
      print("Invalid amount of mines!")
      c = question("int","\nHow many mines do you want in it? ( Must be lesser than previous numbers multiplied with each other): ")
    if int(c) < math.sqrt(vol):
      print("\nWell, you sure do know how to play it safe :v)")
    print("\nLet's start the game!\n")
    play(int(a), int(c), int(bx), int(by), int(bz), int(bw))
    m = input("Do you want to play again?(y/n)")
    if not m == "y":
      game = "OFF"
  return game    

def play(dimension, bombs, scalex, scaley, scalez = 0, scalew = 0): # Pelin käyttöliittymä. Ottaa vain vastaan pelaajan käskyt. new-olio huolehtii itse pelin toimimisesta.
  os.system("clear")
  play = "ON"
  while True:
    if dimension == 2:
      new = Plane(scalex, scaley, bombs)
      print("Mines: "+str(bombs))
      new.pic()
      new.print_pic()
      break
    elif dimension == 3:
      new = Space(scalex, scaley, scalez, bombs)
      print("Mines: "+ str(bombs))
      new.pic(1)
      break
    elif dimension == 4:
      new = Time(scalex, scaley, scalez, scalew, bombs)
      print("Mines: " + str(bombs))
      new.pic(1, 0)
      break
    else:
      print("Invalid input!")
  while new.status != "OFF":
    try:
      c = question("all","Your next move: ")
      d = c.split(sep=" ")
      if not len(d) == 2:
        print("Invalid input")
      else:
        if re.compile(r'[a-z]+').search(d[1]):
          x = int(LETTERS.index(re.compile('[a-z]+').search(d[1]).group(0)) + 1)
        if re.compile(r'[1-9]+').search(d[1]):
          y = int(re.compile('[0-9]+').search(d[1]).group(0))
        if re.compile(r'[A-Z]+').search(d[1]):
          z = int(C_LETTERS.index(re.compile('[A-Z]+').search(d[1]).group(0)) + 1)
        if dimension == 2:
          if d[0] == "step" or d[0] == "s":
            if not new.step(x, y) == "Stop":
              new.evaluate_empties()
          elif d[0] == "flag" or d[0] == "f":
            new.flag(x, y)
            new.evaluate_flags()
          else:
            print("Invalid input: Unrecognized command")
        elif dimension == 3:
          if d[0] == "step" or d[0] == "s":
            if not new.step(x, y, z) == "Stop":
              new.evaluate_empties()
          elif d[0] == "flag" or d[0] == "f":
            new.flag(x, y, z)
            new.evaluate_flags()
          elif d[0] == "go" or d[0] == "g":
            new.pic(z)
          else:
            print("Invalid input: Unrecognized command")
        elif dimension == 4:
          if d[0] == "step" or d[0] == "s":
            if not new.wait_step(x, y, z) == "Stop":
              new.evaluate_empties()
          elif d[0] == "flag" or d[0] == "f":
            new.wait_flag(x, y, z)
            new.evaluate_flags()
          elif d[0] == "go" or d[0] == "g":
            new.wait(z)
          else:
            print("Invalid input: Unrecognized command")
    except(IndexError, ValueError):
      print("Invalid coordinate!")
      new.evaluate_empties()
    except(UnboundLocalError, TypeError):
      new.evaluate_empties()
      if dimension == 3:
        new.pic(1)
      elif dimension == 4:
        new.pic(1,1)
      print("Invalid input: Incorrect coordinates")
    x, y, z = "empty", "empty", "empty"
  del new
  return "OFF"

class Plane: 
  status = "ON"
  start = datetime.datetime.now() #Pelin päättyessä tällä mitataan, kauan meni
  turns = 0

  def __init__(self, nox, noy, bomb):
    self.number_of_mines = bomb   #number_of_minesiä käytetään vain tulosten kirjaamisessa
    self.scalex=nox
    self.scaley=noy
    self.boxes_left = nox * noy # Tällä arvioidaan, päättyykö peli
    self.picture = [] # Tulostettavan kentän multiarray
    self.flags=[]
    self.empty_boxes=[] # Tämän avulla loopataan tulvatäyttö, väliaikainen
    self.number_boxes=[] #Tänne talletetaan numerolaatikot, väliaikainen
    self.bombs=[]
    while len(self.bombs) < bomb:
      x=random.randint(1,nox)
      y=random.randint(1,noy)
      coordinate = []
      coordinate.append(x)
      coordinate.append(y)
      if not coordinate in self.bombs:
        self.bombs.append(coordinate)
    self.pic_init()
  
  def pic_init(self): # Rakentaa tyhjän kentän
    firstline = " " 
    for i in range(self.scalex):
      firstline += " _"
    self.picture.append(firstline)
    for i in range(self.scaley):
      row = ""
      row +=  " |"
      for j in range(self.scalex):
        row += "_|"
      row += " " + str(i+1) 
      self.picture.append(row) 
    x_coord = "  "
    for k in range(self.scalex):
      x_coord += LETTERS[k] + " "
    self.picture.append(x_coord)

  def pic(self): #Jokaisen käyttäjän teon yhteydessä tällä tehdään muutokset picture-listiin.
    for j in self.empty_boxes:
      t = list(self.picture[j[1]])
      t[j[0]*2] = "#"  # # kuvaa tyhjää ruutua
      t = "".join(t)
      self.picture[j[1]] = t
      self.empty_boxes = []
    for i in self.number_boxes:
      s = list(self.picture[i[1]])
      s[i[0]*2] = str(i[2]) 
      s = "".join(s)
      self.picture[i[1]] = s
      
  def print_pic(self): # Tämä varsinaisesti tulostaa picturen joka vuorossa
    for k in self.picture:
      print(k)
     
  def hit_bomb(self): # Tekee muutokset kuvaan, kun käyttäjä astuu miinaan. Auts!
    for i in self.bombs:
      s = list(self.picture[i[1]])
      s[i[0]*2 ] = "X"
      s = "".join(s)
      self.picture[i[1]] = s
    self.print_pic()
 
  def is_bomb(self,x,y): #Tarkistaa, onko pelaajan antamissa koordinaateissa pommi
    step_coord=[]
    step_coord.append(x)
    step_coord.append(y)
    if step_coord in self.bombs:
      return True
    else:
      return False
 
  def if_next_to_bomb(self,x,y): # Tarkistaa, onko koordinaattien ympärillä miinoja, eli onko kyseisessä koordinaatissa numerolaatikko
    number=0
    for k in self.bombs:
      l=x-k[0]
      m=y-k[1]
      if l<=1 and m <=1 and l>=-1 and m>=-1:
        number+=1
    if number>0:
      insertion = []
      insertion.append(x)
      insertion.append(y)
      insertion.append(number)
      self.number_boxes.append(insertion)
      return number
    else:
      return 0

  def add_to_empties(self,x,y): # Jos yllä oleva palauttaa 0, niin tämä lisää ymppäröivät laatikot empty_boxes - listaan, mikäli kyseisiä koordinaatteja ei jo ole siellä
    x=x-1
    y=y-1
    for v in [0,1,2]:
      x1=x+v
      if x1==0 or x1 > self.scalex:
        continue
      else:
        for w in [0,1,2]:
          y1=y+w
          if y1==0 or y1 > self.scaley:
            continue
          else:
            temp_coord = []
            temp_coord.append(x1)
            temp_coord.append(y1)
            if temp_coord in self.empty_boxes:
              continue
            elif temp_coord in self.number_boxes:
              continue
            elif temp_coord in self.bombs:
              continue
            else:
              self.empty_boxes.append(temp_coord)
              self.boxes_left -= 1
      
  def step(self, a, b): # Pelaajan kutsuttava funktio, joka avaa koordinaatin ja tulvatäyttää kentän.
    self.turns += 1
    if self.is_bomb(a, b) == True:
      os.system("clear")
      self.hit_bomb()
      print("\n BOOOOOOOOM! You're dead. Hope you had a good life. \n")
      print(" You're such a square :3 \n")
      self.end_game("Lost")
      return "Stop"
    elif self.picture[b][2*a] != "_" and self.picture[b][2*a] != "F":
      print("Invalid coordinate")
    else:    
      os.system("clear")                                                     
      if self.if_next_to_bomb(a, b) > 0:  
        self.boxes_left -= 1
        self.pic()   
        self.print_pic()                       
      else:                                     
        self.add_to_empties(a, b)              
        for i in self.empty_boxes:   #Tulvatäyttö          
          c = i[0]                             
          d = i[1]
          if self.if_next_to_bomb(c, d) == False:
            self.add_to_empties(c, d)
        self.pic()
        self.print_pic()
   
  def flag(self, a, b): # Asettaa lipun sinne, missä pelaaja epäilee miinan olevan.
    os.system("clear")
    f_coord = []
    f_coord.append(a)
    f_coord.append(b)
    if self.picture[b][a*2] == "_" or self.picture[b][2*a] == "F":
      if not f_coord in self.flags:
        self.flags.append(f_coord)
        f = list(self.picture[b])
        f[a*2] = "F" 
        f = "".join(f)
        self.picture[b] = f
      else:
        self.flags.remove(f_coord)
        f = list(self.picture[b])
        f[a*2] = "_" 
        f = "".join(f)
        self.picture[b] = f
    else:
      print("Invalid input!")
    self.pic()
    self.print_pic()

  def evaluate_empties(self): # Joka vuoro tämä tarkistaa, onko avaamattomia ruutuja enemmän kuin miinoja. Jos ei, pelaaja voittaa. Poistaa myös liput pois aukaistuista luukuista.
    for i in self.flags:
      if self.picture[i[1]][2*i[0]] != "_" or self.picture[i[1]][2*i[0]] != "F":
        self.flags.remove(i)
    if self.boxes_left == len(self.bombs):
      print("You won! Congratulations!")
      self.pic()
      self.end_game("Won")
    else:
      self.pic()
      return False
        
  def evaluate_flags(self): # Jos pelaajan asettamia lippuja yhtä paljon kuin miinoja, tämä ohjelma tarkistaa, ovatko pelaajan epäilykset osoittautuneet oikeiksi.
    if len(self.flags) == len(self.bombs):
      q = input("Do you want to see if you got it? (y/n)")
      if q == "y":
        result = ""
        for e in self.flags:
          if not e in self.bombs:
            result = "fail"
            break
          else:
            result = "win"
        if result == "win":
          print("You won! Congratulations!")
          self.end_game("Won")
        else:
          print("Try again!")
          self.pic()
      
  def end_game(self, result): #Kirjoittaa tiedostoon pelin päätyttyä
    time = (datetime.datetime.now() - self.start).seconds
    write_stats(2, self.scalex * self.scaley, self.number_of_mines, self.turns, str(time// 60)+" min "+str(time%60) + " sec ", datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"), result)
    self.empty()
    
  def empty(self): #Tuhoaa olion muuttujat. En tiennyt, onko tämä tarpeen Pythonissa, mutta ainakin käsittääkseni näin pitää toimia C++:ssa
    self.scalex = 0
    self.scaley = 0
    self.bombs = []
    self.flags = []
    self.empty_boxes = []
    self.number_boxes = []
    self.picture = []
    self.boxes_left = 0
    self.status = "OFF"
    
class Space: # Tästä alkaa 3D ja 4D oliot. Nämä sisältävät suurimmaksi osaksi saman nimiset funktiot, kuin Planekin, jotka tekevät samat asiat, joskin erillä tavalla. Näiden jälkeen tulee vain yhden rivin pääohjelma: start()
  status = "ON"
  start = datetime.datetime.now()
  turns = 0
  
  def __init__(self, nox, noy, noz, bombs):
    self.empty_planes = []
    self.scalex = nox
    self.scaley = noy
    self.scalez = noz
    self.planes = []
    self.number_of_mines = bombs
    local_bombs = []
    for l in range(noz):
      local_bombs.append(0)
    while bombs > 0:
      local = random.randint(1, noz)
      local_bombs[local - 1] += 1
      bombs -= 1
    for num in local_bombs:
      self.planes.append(Plane(nox, noy, num)) # Eli Space kappale koostuu z- määrästä kaksiulotteisia tasoja. Ne eivät suoranaisesti vaikuta keskenään, vaan Space huolehtii esim. kolmiulotteisesta tulvatäytöstä.
    self.pic_init()
    
  def pic_init(self):
    for pic in range(len(self.planes)):
      self.planes[pic].picture[1] += " " + C_LETTERS[pic]
    #print(self.planes[0].bombs)
      
  def pic(self, z):
    os.system("clear")
    self.planes[z - 1].pic()
    self.planes[z - 1].print_pic()

  def is_bomb(self, x, y, z):
    return self.planes[z - 1].is_bomb(x, y)

  def if_next_to_bomb(self, x, y, z):
    front = 0
    back = 0
    if z < self.scalez:
      front = self.planes[z].if_next_to_bomb(x, y)
    middle = self.planes[z - 1].if_next_to_bomb(x, y)
    if z > 1:
      back = self.planes[z - 2].if_next_to_bomb(x, y)
    if front == 0 and back == 0:
      return middle
    else:
      if middle == 0:
        add = []
        add.append(x)
        add.append(y)
        add.append(0)
        self.planes[z - 1].number_boxes.append(add)
      self.planes[z - 1].number_boxes[-1][2] += front
      self.planes[z - 1].number_boxes[-1][2] += back
      if front != 0:
        self.planes[z].number_boxes.pop()
      if back != 0:
        self.planes[z - 2].number_boxes.pop()
      return back + middle + front
  
  def add_to_empties(self, x, y, z):
    if z < self.scalez:
      self.planes[z].add_to_empties(x, y)
    self.planes[z - 1].add_to_empties(x, y)
    if z > 1:
      self.planes[z - 2].add_to_empties(x, y)
      
  def add_to_empty_planes(self, z): #3D mallissa tulvatäytössä pitää myös luupata tasoja sitä mukaa, kuin niistä löytyy tyhjiä ruutuja. Muuten tyhjiä ruutuja alkaa ilmestymään omituisiin kohtiin.
    try:
      add = []
      if z < self.scalez:
        add.append(z + 1)
        add.append(len(self.planes[z].empty_boxes))
        if not add in self.empty_planes:
          self.empty_planes.append(add)
        add = []  
      add.append(z)
      add.append(len(self.planes[z - 1].empty_boxes))
      if not add in self.empty_planes:
        self.empty_planes.append(add)
      add = []
      if z > 1:
        add.append(z - 1)
        add.append(len(self.planes[z - 2].empty_boxes))
        if not add in self.empty_planes:
          self.empty_planes.append(add)
        add = []
    except(IndexError):
      print(z)
      
  def step(self, a, b, c):
    self.turns += 1
    current = self.planes[c - 1]
    if self.is_bomb(a, b, c) == True:
      os.system("clear")
      current.hit_bomb()
      print("\n BOOOOOOOOM! You're dead. Hope you had a good life. \n")
      print("\n Remember, 3D-minesweeper is just like regular one, just deeper :] \n")
      self.end_game("Lost")  
      return "Stop"  
    elif current.picture[b][2*a] != "_" and current.picture[b][2*a] != "F":
      print("Invalid coordinate!")
    else:  
      os.system("clear")                                        
      if self.if_next_to_bomb(a, b, c) > 0:
        current.boxes_left -= 1  
        self.pic(c)                      
      else:                      
        self.add_to_empties(a, b, c)
        self.add_to_empty_planes(c)
        for j in self.empty_planes:
          for i in self.planes[j[0] - 1].empty_boxes:
            d = i[0]                             
            e = i[1]
            f = j[0]
            if self.if_next_to_bomb(d, e, f) == 0:
              self.add_to_empties(d, e, f)
              self.add_to_empty_planes(j[0])
        self.pic(c)
        
  def flag(self, a, b, c):    
    os.system("clear")
    self.planes[c - 1].flag(a, b)

  def evaluate_empties(self):
    for a in self.planes:
      for e in a.flags:
        if a.picture[e[1]][2*e[0]] != "_" or a.picture[e[1]][2*e[0]] != "F":
          a.flags.remove(e)
    check = True
    for a in self.planes:
      if not len(a.bombs) == a.boxes_left:
        check = False
    if check == True:
      print("You won! Congratulations!")
      self.end_game("Won")
     
  def evaluate_flags(self):
    f_length = 0
    b_length = 0
    for a in self.planes:
      f_length += len(a.flags)
      b_length += len(a.bombs)
    if f_length == b_length:
      q = input("Do you want to see if you got it? (y/n)")
      if q == "y":
        result = ""
        for e in self.planes:
          for f in e.flags:
            if not f in e.bombs:
              result = "fail"
              break
            else:
              result = "win"
        if result == "win":
          print("You won! Congratulations!")
          self.end_game("Won")
        else:
          print("Try again")
          #self.pic()
      
  def end_game(self, result):
    time = (datetime.datetime.now() - self.start).seconds
    write_stats(3, self.scalex * self.scaley * self.scalez, self.number_of_mines, self.turns, str(time// 60)+" min "+str(time%60) + " sec ", datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"), result)
    self.empty()
    
  def empty(self): 
    for a in self.planes:
      a.empty()
    self.empty_planes = []
    self.scalex = 0
    self.scaley = 0
    self.scalez = 0
    self.planes = []
    local_bombs = []
    self.status = "OFF"
    
class Time:
  status = "ON"
  start = datetime.datetime.now()
  turns = 0
  
  def __init__(self, nox, noy, noz, now, bombs):
    self.empty_spaces = []
    self.scalex = nox
    self.scaley = noy
    self.scalez = noz
    self.scalew = now
    self.spaces = []
    self.number_of_mines = bombs
    local_bombs = []    
    for l in range(now):
      local_bombs.append(0)
    while bombs > 0:
      local = random.randint(1, now)
      local_bombs[local - 1] += 1
      bombs -= 1
    for num in local_bombs:
      self.spaces.append(Space(nox, noy, noz, num))
    self.pic_init()
    
  def pic_init(self):
    for sp in range(len(self.spaces)):
      for pic in range(len(self.spaces)):
        self.spaces[sp].planes[pic].picture[1] += " Time: " + str(sp)
      
  def pic(self, z, w):
    self.spaces[w].pic(z)
    
  def is_bomb(self, x, y, z, w):
    return self.spaces[w].planes[z - 1].is_bomb(x, y)

  def if_next_to_bomb(self, x, y, z, w):
    before = 0
    after = 0
    if w < self.scalew - 1:
      after = self.spaces[w + 1].if_next_to_bomb(x, y, z)
    now = self.spaces[w].if_next_to_bomb(x, y, z)
    if w > 0:
      before = self.spaces[w - 1].if_next_to_bomb(x, y, z)
    if before == 0 and after == 0:
      return now
    else:
      if now == 0:
        add = []
        add.append(x)
        add.append(y)
        add.append(0)
        self.spaces[w].planes[z - 1].number_boxes.append(add)
      self.spaces[w].planes[z - 1].number_boxes[-1][2] += after
      self.spaces[w].planes[z - 1].number_boxes[-1][2] += before
      if after != 0:
        self.spaces[w + 1].planes[z - 1].number_boxes.pop()
      if before != 0:
        self.spaces[w - 1].planes[z - 1].number_boxes.pop()
      return before + now + after
  
  def add_to_empties(self, x, y, z, w):
    if w < self.scalew - 1:
      self.spaces[w + 1].add_to_empties(x, y, z)
    self.spaces[w].add_to_empties(x, y, z)
    if w > 0:
      self.spaces[w - 1].add_to_empties(x, y, z)
      
  def add_to_empty_planes(self, z, w):
    if w < self.scalew - 1:
      self.spaces[w + 1].add_to_empty_planes(z)
    self.spaces[w].add_to_empty_planes(z)
    if w > 0:
      self.spaces[w - 1].add_to_empty_planes(z)
      
  def add_to_empty_spaces(self, w): # Täällä taas pitää loopata myös tilat
    add = []
    if w < self.scalew - 1:
      add.append(w + 1)
      add.append(len(self.spaces[w + 1].empty_planes))
      if not add in self.empty_spaces:
        self.empty_spaces.append(add)      
      add = []
    add.append(w)
    add.append(len(self.spaces[w].empty_planes))
    if not add in self.empty_spaces:
      self.empty_spaces.append(add)
    add = []
    if w > 0: 
      add.append(w - 1)
      add.append(len(self.spaces[w - 1].empty_planes))
      if not add in self.empty_spaces:
        self.empty_spaces.append(add)
      add = []
      
  def input_thread(self, list, prompt): #Tämä pikkufunktio on kopioitu StackOverflowista. Tällä käyttäjä pysäyttää alemman funktion
    input(prompt)
    list.append(None)
        
  def wait(self, c, prompt = "stop"): #Neliulotteisuuden saavuttamiseksi ohjelma tulostaa eri tasoja ajan kuluessa. Ohjelma tulostaa yhdessä threadissa sekunnin välein tasoja ja toisessa odottaa käyttäjän inputtia. Inputin tapahtuessa funktio pysähtyy.
    a = self.spaces[c]
    del a
    then =  int('{0:%S}'.format(datetime.datetime.now()))% self.scalew
    list = []
    _thread.start_new_thread(self.input_thread, (list, ""))
    while not list:
      if then == int('{0:%S}'.format(datetime.datetime.now()))% self.scalew:
        continue
      else:    
        self.pic(c, then)
        print("Press Enter when you want to {}".format(prompt))
        then =  int('{0:%S}'.format(datetime.datetime.now()))% self.scalew
    return then - 1
    
  def wait_step(self, a, b, c): #Ottaa vastaan käyttäjän step-funktion aikakoordinaatin
    d = self.wait(c, "step")
    if self.step(a, b, c, d) == "Stop":
      return "Stop"
  
  def step(self, a, b, c, w):  
    self.turns += 1
    zed = c - 1
    current = self.spaces[w].planes[zed]
    if self.is_bomb(a, b, c, w) == True:
      os.system("clear")
      current.hit_bomb()
      print("\n BOOOOOOOOM! You're dead. Hope you had a good life. \n")
      print("\n Perhaps 4 dimensions are too much for you :v) :>) :7) :^) \n")
      self.end_game("Lost")
      return "Stop"
    elif current.picture[b][2*a] != "_" and current.picture[b][2*a] != "F":
      print("Invalid coordinate!")
    else:     
      os.system("clear")                             
      if self.if_next_to_bomb(a, b, c, w) > 0:  
        current.boxes_left -= 1
        self.pic(c, w)                          
      else:                      
        self.add_to_empties(a, b, c, w)
        self.add_to_empty_planes(c, w)
        self.add_to_empty_spaces(w)
        for i in self.empty_spaces:
          g = i[0]
          for j in self.spaces[g].empty_planes:
            f = j[0]
            for k in self.spaces[g].planes[f - 1].empty_boxes:
              d = k[0]                             
              e = k[1]
              if self.if_next_to_bomb(d, e, f, g) == 0:
                self.add_to_empties(d, e, f, g)
                self.add_to_empty_planes(f, g)
                self.add_to_empty_spaces(g)   
        self.pic(c, w)
        
  def wait_flag(self, a, b, c): #Ottaa käyttäjän flag-funktion aikakoordinaatin
    d = self.wait(c, "flag")
    self.flag(a, b, c, d)
    
  def flag(self, a, b, c, d):
    os.system("clear")
    self.spaces[d].planes[c - 1].flag(a, b)
    
  def evaluate_empties(self):
    for a in self.spaces:
      for e in a.planes:
        for i in e.flags:
          if e.picture[i[1]][2*i[0]] != "_" or a.picture[i[1]][2*i[0]] != "F":
            e.flags.remove(i)
    check = True
    for a in self.spaces:
      for b in a.planes:
        if not b.boxes_left == len(b.bombs):
          check = False
    if check == True:
      print("You won! Congratulations!")
      self.end_game("Won")
        
  def evaluate_flags(self):
    length = "yes"
    f_length = 0
    b_length = 0
    if not len(self.spaces) == 0:
      for a in self.spaces:
        for b in a.planes:
          f_length += len(b.flags)
          b_length += len(b.bombs)
      if f_length == b_length:
        q = input("Do you want to see if you got it? (y/n)")
        if q == "y":
          result = ""
          for d in self.spaces:
            for e in d.planes:
              for f in e.flags:
                if not f in e.bombs:
                  result = "fail"
                  break
                else:
                  result = "win"
          if result == "win":
            print("You won! Congratulations!")
            self.end_game("Won")
          else:
            print("Wrong. Try again!")
      
  def end_game(self, result):
    time = (datetime.datetime.now() - self.start).seconds
    write_stats(4, self.scalex * self.scaley * self.scalez * self.scalew, self.number_of_mines, self.turns, str(time// 60)+" min "+str(time%60)+" sec", datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"), result)
    for a in self.spaces:
      a.empty()
    self.empty_spaces = []
    self.scalex = 0
    self.scaley = 0
    self.scalez = 0
    self.scalew = 0
    self.spaces = []
    local_bombs = []
    self.status = "OFF"
    
start()
