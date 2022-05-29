from Vocabulary import Kanji, JWord
from AVLTree import AVLTree, BST
from BinaryHeap import BinaryHeap
from ArrQueue import ArrQueue
from RefQueue import RefQueue
from LinkList import LinkList
from StaticStack import ArrStack
from OrderedLinkList import OrderedLinkList
import random
r = random.randint

kanjiCount = 0

def randKanji(id):
    kanji = ""
    for i in range(r(1,4)):
        kanji += chr(r(19968, 40879))
    jw = JWord("english {}".format(id), 
                kanji, 
                "use {}".format(id), 
                "meaning {}".format(id), 
                "reading {}".format(id))
    return jw

l = [None]*100

for i in range(100):
    l[i] = randKanji(i)

for i in l:
    print(i, end=", ")
