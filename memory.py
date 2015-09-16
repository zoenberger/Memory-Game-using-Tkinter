#Basic Memory Game
#All images should be in folder named "Images"
#Images used are W:100px H:150px, though any size works if all images same size
#Line 32 has some commented out code to print the key to terminal for testing.


from tkinter import *
from tkinter import ttk, messagebox
import os, random, time




class Memory:

    def __init__(self, master):  
        
        master.title("Test Your Memory")
        master.geometry('800x675+10+10')
        master.configure(background = 'pink')

           
        #define how big game is...can be useful for making skill options later
        self.numPairs = 12
        
     
        #get all images in directory called "Images" & shuffle order
        
        imageDir = os.path.join(os.path.dirname(__file__),"GIF\\")
        imageArray = GetGifList(imageDir)
                
        #create array with how many cards needed and double it to make matched pairs        
        self.imagePairs = imageArray[0:self.numPairs]
        self.imagePairs = self.imagePairs * 2

        #because we doubled, we need to re-shuffle order
        random.shuffle(self.imagePairs)
        cardDir = os.path.join(os.path.dirname(__file__),"card.gif")
        self.card = PhotoImage(file = cardDir)

        
        self.cardImages =[]
        self.blankCards = []
        row = 0
        column = 0
        for i in range(len(self.imagePairs)):
            self.blankCards.append(ttk.Label(master))
            self.cardImages.append(PhotoImage(file = self.imagePairs[i]))
            self.blankCards[i].img = self.card
            self.blankCards[i].config(image = self.blankCards[i].img)
            self.blankCards[i].config(text = self.imagePairs[i])
            self.blankCards[i].grid(row = row, column = column, padx = 5, pady = 5)
            self.blankCards[i].bind('<ButtonPress>', self.onClick)
            column += 1
            if column == 6: 
                column = 0
                row +=1


        self.foundMatches= 0 #Keeps track to see if you've won.
        self.clickCount = 0 #keeps track of 1st or second click.
        self.card1 = '' #holding spot if it's first click
        self.newCard = ''
        self.totalTries = 0
        self.matchList = []
        

    def onClick(self,event):
        self.clickCount += 1

        self.newCard = event.widget
        img = PhotoImage(file = self.newCard.cget('text'))
        self.newCard.img = img
        self.newCard.config(image = img)
    
        if self.clickCount == 1:
            self.card1 = self.newCard #put into holding space if 1st click
            self.card1.unbind('<ButtonPress>')

        else:
            for item in self.blankCards:
                item.unbind('<ButtonPress>')
            #FOUND MATCH: Unbind click events. Update match tracker
            if (self.newCard.cget('text') == self.card1.cget('text')):
                self.matchList.append(self.newCard.cget('text'))
                self.foundMatches += 1
                print(self.foundMatches)
                self.totalTries += 1
                self.clickCount = 0
                for item in self.blankCards:
                    if item.cget('text') not in self.matchList:
                        item.bind('<ButtonPress>', self.onClick)
                if self.foundMatches == self.numPairs:
                    Winner()
                    print("Total Tries = " + str(self.totalTries))

            else:
                for item in self.blankCards:
                    item.unbind('<ButtonPress>')
                self.newCard.after(1000, self.checkmatch)

    def checkmatch(self):    

        #FOUND MATCH: Unbind click events. Update match tracker
        self.totalTries += 1
        #NO MATCH: Wait then hide both cards again.
        self.newCard.img = self.card
        self.newCard.config(image = self.newCard.img)
        self.card1.img = self.card
        self.card1.config(image = self.card1.img)

        for item in self.blankCards:
            if item.cget('text') not in self.matchList:
                item.bind('<ButtonPress>', self.onClick)

        self.clickCount = 0

def Winner():
    print("WINNER WINNER WINNER!")
    
#get all JPEGs in a directory that is passed and return image names array
#Note I found this code snippet here:   http://wiki.wxpython.org/wxStaticBitmap
def GetGifList(loc):
    gifs = [f for f in os.listdir(loc) if f[-4:] == ".gif"]
    #print("GIFs are:", gifs)
    return [os.path.join(loc, f) for f in gifs]

            
def main():            
    
    root = Tk()
    memory = Memory(root)
    root.mainloop()
    
if __name__ == "__main__": main()