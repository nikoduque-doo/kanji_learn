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

lis = [None]*100

for i in range(100):
    lis[i] = randKanji(i)

for i in lis:
    print(i, end=", ")
print("")


s = ArrStack(20)
q = ArrQueue(20)
q2 = RefQueue()
l = LinkList()
ol = OrderedLinkList()
bst = BST()
av = AVLTree()
b = BinaryHeap()
for j in range(17):
    i = lis[j]
    s.push(i)
    q.enqueue(i)
    q2.enqueue(i)
    l.pushBack(i)
    ol.insert(i)
    bst.insert(i)
    av.insert(i)
    b.insert(i)



def print2(jw:JWord):
    print(jw, end = " | ")

print("\narrStack: \n", s)
s.traverse(print2)
print("\narrQueue: \n", q)
q.traverse(print2)
print("\nrefQueue: \n", q2)
q2.traverse(print2)
print("\nlinked list: \n", l)
l.traverse(print2)
print("\nordered linked list: \n", ol)
ol.traverse(print2)
print("\nBST: \n", bst)
bst.traverse(print2)
print("\nAVL Tree: \n", av)
av.traverse(print2)
print("\nBinary heap: \n", b)
b.traverse(print2)