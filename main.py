import math, threading, time, random, string, tkinter
spaces = [" ","\t","\n"]
#Fix 2d array weights problem -> caffeinated Coach Alex figured it out of class

threads = []
numchildren = 20
numgenerations = 500
currentgeneration = 0

def parse(text):
  words = []
  start = 0
  for cur, char in enumerate(text):
    if text[start] in spaces:
       start = cur
    if char in spaces :
      word = text[start:cur]
      words.append(word) 
      start = cur 
  if start < len(text):
    word = text[start:]
    words.append(word) 
  return words

c = "Passwords.txt"
f = open(c)
data = f.read()
words = parse(data)
#word = random.choice(words)
#print(word)
#word = input("Enter your password: ")


def bubbleSort(arr):
  n = len(arr)
  for i in range(n-1):
    for j in range(0, n-i-1):
        if arr[j].fitness > arr[j + 1].fitness :
              arr[j], arr[j + 1] = arr[j + 1], arr[j]

class myThread (threading.Thread):
  def __init__(self, threadID, name, generation, length):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.generation = generation
    self.length = length
    self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9", "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","!","@","#","$","%","^","&","*",")","(",",",".","?",">","<","/",";",":","]","[","+","-","\\","|","}","{","`","~","=","_","\'","\"",""]
    self.weights = [[1/len(self.alphabet)]*len(self.alphabet) for j in range(length)]
    self.fitness = 0
  def run(self):
    for i in range(self.length):
      wordGuess = random.choices(self.alphabet, weights = self.weights[i], k = 1)
      if wordGuess[0] == word[i]:
        self.fitness += 1
        self.weights[i][self.alphabet.index(word[i])] += 0.01
      elif wordGuess[0] != word[i]:
        self.weights[i][self.alphabet.index(wordGuess[0])] -= 0.001
    self.generation+=1
  def copythread(self, other):
    self.generation = other.generation
    self.length = other.length
    self.weights = other.weights

def gui():
  global word, e, frame, results2, results
  screen = tkinter.Tk()
  screen.geometry("400x600+200+0")
  screen.configure(background='lightblue')
  screen.title('Password Checker')
  frame = tkinter.Frame(master = screen, width = 400, height = 600, bg = "lightblue")
  frame.pack(expand = True, fill = tkinter.BOTH)
  e = tkinter.Entry(frame, width = 40, borderwidth = 4, bg = "white")
  e.grid(row = 0, column = 0, padx = 10, pady = 15, ipady = 10, columnspan = 4)
  enter = tkinter.Button(frame, text = "Enter", width = 20, height = 5, bd = 4, command = btn, bg = "lightgreen")
  enter.place(x = 100, y = 200)
  instructions = tkinter.Label(frame,text = "Enter your password and the program will check how safe", justify = "center",  bg = "lightblue")
  instructions.place(x=0, y= 100)
  instructions2 = tkinter.Label(frame,text = " it is against an AI password guesser", justify = "center", bg = "lightblue")
  instructions.place(x=0, y= 100)
  instructions2.place(x=70, y= 125)
  results2 = tkinter.Label(frame)
  results = tkinter.Label(frame)

def btn():
  global word, e, threads, results2, results
  results.place_forget()
  results2.place_forget()
  strength = ""
  word = e.get()
  threads = []
  for i in range(numchildren):
    threads.append(myThread(i, i, 0, len(word)))
  for i in range(numgenerations):
    if main() == True:
      print("It took " + str(currentgeneration) + " attempts to break your password")
      results = tkinter.Label(frame,text = "It took " + str(currentgeneration) + " attempts to break your password" , justify = "center", bg = "lightblue")
      results.place(x=55, y= 325)
      if (currentgeneration) >= 50:
        strength = "You have a very strong password"
      elif (currentgeneration) >= 40:
        strength = "You have a strong password. You could make it stronger by adding special characters, numbers, or capital letters"
      elif (currentgeneration) >= 30:
        strength = "You have a moderately strong password. You could make it stronger by adding special characters, numbers, or capital letters"
      elif (currentgeneration) >= 20:
        strength = "You have a weak password. You should make it stronger by adding special characters, numbers, or capital letters"
      elif (currentgeneration) >= 10:
        strength = "You have a very weak password. You should make it stronger by adding special characters, numbers, or capital letters"
      else:
        strength = "Your password is extremely weak. Make it stronger by adding special characters, numbers, or capital letters"
      results2 = tkinter.Label(frame,text = strength  , justify = "center", bg = "lightblue", wraplength = 300)
      results2.place(x=60, y = 350)
      break
  

def main():
  global word, threads, currentgeneration
  for t in threads:
    t.start()
  for t in threads:
    t.join()  
  bubbleSort(threads)
  if threads[0].generation % 1 == 0:
    print("Generation: " + str(threads[0].generation))
    currentgeneration = threads[0].generation
    for t in threads:
      print (str(t.name) + ": " + str(t.fitness))
    if threads[numchildren - 1].fitness == len(word):
      print("Password: " + word)
      return True
  if threads[0].generation == 500:
    print(str(t.name) + ": " + str(t.weights))
  for t in range(len(threads)//2+1):
    threads[t] = threads[len(threads) - 1]
  tempThreads = []
  for i in range(numchildren):
    tempThreads.append(myThread(i, i, 0, len(word)))
    tempThreads[i].copythread(threads[0])
  threads = tempThreads  
  
gui()

