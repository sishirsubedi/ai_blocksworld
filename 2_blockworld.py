import random
import sys
import Queue as Q
from copy import deepcopy

letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

class blockworld:

    def __init__(self,b,s):

        self.blocks =b
        self.stacks = s
        self.initial =[None] * b
        self.initial= [[] for x in range(0,self.blocks)]
        self.letters = letters[0:s]

        temp=-1
        for j in range(0,s):
            num = random.randint(0, self.blocks - 1)
            while temp == num:
                num = random.randint(0,self.blocks-1)
            self.initial[num].append(letters[j])
            temp = num


        # self.initial[0].append('B')
        #
        #
        # self.initial[1].append('C')
        # self.initial[1].append('E')
        #
        # self.initial[1].append('A')
        # self.initial[2].append('D')


        # self.initial[0].append('D')
        #
        # self.initial[1].append('E')
        # self.initial[1].append('F')
        # self.initial[1].append('I')
        # self.initial[1].append('J')
        #
        # self.initial[2].append('B')
        # self.initial[2].append('G')
        #
        # self.initial[3].append('C')
        # self.initial[3].append('H')
        #
        # self.initial[4].append('A')


        self.goal = [None] * b
        self.goal = [[] for x in range(0, self.blocks)]
        self.goal[0]= letters[0:s]


    def successors(self,s):
        state = s
        out=[]
        #print "STATE", state
        for i in range (0,len(state)):
            if len(state[i]) >0:
                temp= deepcopy(state)
                lastelement = temp[i].pop()
                for j in range(0,len(state)):
                    temp2 = deepcopy(temp)
                    if i != j:
                        temp2[j].append(lastelement)
                        out.append(temp2)
        return out

    def testgoal(self,s):
        fstack = s[0]
        found = False
        if len(fstack)==len(self.goal[0]):
            for i in range (0,len(self.goal[0])):
                gtemp = self.goal[0]
                if fstack[i]==gtemp[i]:
                    found = True
                else:
                    found =False
                    break
        else:
            found = False
        return found


    def heuristic_cost_h1(self, state):

        gn = 0
        mismatch = 0
        temp = state[0]
        for i in range(0, len(state[0])):
            if temp[i] == letters[i] and mismatch == 0:
                gn -= 1
            else:
                mismatch += 1
                gn += (gn + mismatch)

        y = len(state)
        x = 0
        for i in range(0, len(state)):
            x += len(state[i])
        finalletters = letters[0:x]

        # print y,x,final

        mat = [[0 for i in range(0, x)] for j in range(0, y)]

        for i in range(0, len(state)):
            for j in range(0, len(state[i])):
                t = state[i][j]
                mat[i][j] = t

        # print mat

        fn = 0
        for l in range(0, len(finalletters)):
            letter = finalletters[l]
            for i in range(0, x):
                for j in range(0, y):
                    if mat[j][i] == letter:
                        f = abs(j - 0) + abs(i - l)
                        # print l, letter, j, i, f
                        fn += f

        return gn + fn


    def heuristic_cost_h2(self,state):
         return self.height_neighbor_rule(state) #+ self.stochastic_rule(state)


    def height_neighbor_rule(self,state):

        penalty = 0

        for i in range(0, len(state)):

            temp = state[i]

            if len(temp) == 0:
                penalty -=1
            elif i==0 and len(temp) == 1 and temp[0] == letters[0]:
                penalty -= 2
            elif i==0 and len(temp) == 1 and temp[0] != letters[0]:
                penalty += 2
            elif i!=0 and len(temp) == 1 and temp[0] == letters[0]:
                penalty +=  0
            elif i != 0 and len(temp) == 1 and temp[0] != letters[0]:
                penalty -= 1
            else:
                if i ==0:
                    for k in range(0,len(temp)):
                        if temp[k]==letters[k]:
                            penalty -= 2

                for j in range(len(temp) - 1, -1, -1):
                    if j == 0:
                        continue
                    up = temp[j]
                    upind = letters.index(up)
                    down = temp[j - 1]
                    downind = letters.index(down)

                    diff = abs(upind - downind)

                    if upind > downind:
                        if i ==0:
                            penalty += 2 + diff
                        else:
                            penalty +=4 + diff

                    elif downind > upind:
                        if i == 0:
                            penalty += 4 + diff
                        else:
                            penalty += 2 + diff
        return penalty


def traceback(n):
    temp = []
    currentnode = n
    while currentnode != None:
        temp.append(currentnode.state)
        currentnode = currentnode.parent
    print "Goal Depth : ", len(temp)
    print "\nSOLUTION PATH is : \n"
    for i in range(len(temp)-1,-1,-1):
        state = temp[i]
        for j in range(0,len(state)):
            print j ,":", state[j]
        print "   "
    return len(temp)


def graph_search(game, frontier):

    newnode = Node(game.initial)
    newnode.cost = game.heuristic_cost_h2(newnode.state) + game.g_n(newnode.state)

    goal_test = 1

    if game.testgoal(newnode.state):
        return newnode

    frontier.put((newnode))
    explored = set()

    while True:

        if frontier.qsize() == 0:
            print "Failed"
            return 0

        current_node = frontier.get()
        print "Current Node is : ", current_node.state

        explored.add(current_node.id)

        for neighbor in game.successors(current_node.state):

            next_node = Node(neighbor,current_node)
            next_node.cost = game.heuristic_cost_h2(next_node.state)

            if next_node.id not in explored and next_node not in frontier.queue:

                goal_test += 1

                if game.testgoal(next_node.state):
                    print "Found Goal Node : ", next_node.id, next_node.cost, goal_test, frontier.qsize()
                    return next_node

                frontier.put((next_node))
                print "Child Node : ", next_node.id, next_node.cost, goal_test, frontier.qsize()

def dfs (game):
    return graph_search(game, Q.LifoQueue())

def bfs(game):
    return graph_search(game, Q.Queue())





def astar_search(game,frontier):

    newnode = Node(game.initial)

    if game.testgoal(newnode.state):
        print "\n Your initial state is a GOAL STATE -", newnode.state
        return newnode

    newnode.cost += game.heuristic_cost_h2(newnode.state)

    frontier.put((newnode.cost,newnode))

    explored = set()

    iteration =0

    while True:

        iteration += 1

        if frontier.qsize()==0:
            print "Failed"
            return 0

        cc, current_node = frontier.get()

        if game.testgoal(current_node.state):
            print "\nFOUND !! GOAL STATE -", current_node.state, ",", "Frontier size: ", frontier.qsize()
            return current_node

        print "Current iteration :", iteration, "  State :", current_node.id, "  Cost :" , current_node.cost, "  Frontier size :" , frontier.qsize()

        explored.add(current_node.id)

        for neighbor in game.successors(current_node.state):

            next_node = Node(neighbor,current_node)
            next_node.cost += game.heuristic_cost_h2(next_node.state)


            if next_node.id not in explored and (next_node.cost,next_node) not in frontier.queue:

                frontier.put((next_node.cost,next_node))
                #print "Child Node : ", next_node.id, ",", " node cost : " , next_node.cost

            else:
                for items in frontier.queue:
                    if items[1]==next_node and  items[1].cost > next_node.cost:
                        items[1].cost = next_node.cost



class Node:
    def __init__(self,s,p=None,a=None,c=None):
        self.state =s
        self.parent =p
        self.action=a
        self.cost= c

        self.id =''
        for i in range(0,len(s)):
            tblock = s[i]
            for j in range(0,len(tblock)):
                tstack = tblock[j]
                self.id += tstack
            self.id += '-'

        self.cost = self.g_n(s)

        if self.parent != None:
            self.cost -= abs(self.cost - self.g_n(self.parent.state))


    def g_n(self, state):
        gn = 0
        mismatch = 0
        temp = state[0]
        for i in range(0, len(state[0])):
            if temp[i] == letters[i] and mismatch == 0:
                gn -= 2
            else:
                mismatch += 1
                gn = 2 * mismatch
        return gn

#
# num = 0
# t2=[]
# while num<10:
#
#     num +=1
#     blocks = 10
#     stacks = 5
#
#
#     game = blockworld(stacks,blocks)
#     #print "Initial State : " , game.initial
#    # print game.goal
#
#
# # print "DFS-----------"
# # dfs_fs = dfs(game)
# # print "dfs",  dfs_fs.id
# # print "PATH-----------"
# # traceback(dfs_fs)
# #
#     #
#     # print "BFS-----------"
#     # bfs_fs = bfs(game)
#     # print "bfs", bfs_fs.id
#     # t1.append(traceback(bfs_fs))
#
#
#     #print "HS-----------"
#     hs_fs = astar_search(game,Q.PriorityQueue())
#     #print "heu", hs_fs.id
#     t2.append(traceback(hs_fs))
#
#
# # frontier = Q.Queue()
# # node = Node(game.initial)
# # frontier.put(node)
# # frontier.put(2)
# # frontier.put(3)
# #
# # if node not in frontier.queue:
# #     print "hi"
# #
# # while not frontier.empty():
# #     print "hi"
# #     frontier.get()
#
# print t2
#
# # #
# # #
# #




blocks = int(sys.argv[1])

stacks = int(sys.argv[2])



# blocks = 10#int(sys.argv[1])
#
# stacks = 5#int(sys.argv[2])
#


print "\nYou entered : " ,blocks , " blocks and ", stacks, " stacks \n"

game = blockworld(stacks,blocks)
print "\nInitial state of the game is - ", game.initial, "\n"
print "\nRunning a* search-----------\n"
hs_fs = astar_search(game,Q.PriorityQueue())
traceback(hs_fs)
print " \n  -- completed -- \n\n"

