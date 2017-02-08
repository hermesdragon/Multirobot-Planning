import math, sys, pygame, random
from math import *
from pygame import *

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
sensingrange = 70
delta = 10.0
GOAL_RADIUS = 10
NUMNODES = 500000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,180,105
yellow=255,240,14
orange=255,103,14

count = 0
rectObs = []

def dist(p1,p2):    
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def step_from_to(p1,p2):
    if dist(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + delta*cos(theta), p1[1] + delta*sin(theta)

def collides(p):    
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            return True
    return False


def get_random_clear():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        noCollision = collides(p)
        if noCollision == False:
            return p


def init_obstacles():  
    global rectObs
    rectObs = []
    rectObs.append(pygame.Rect((XDIM / 2.0 + 200, YDIM / 2.0 - 180),(50,50)))
    rectObs.append(pygame.Rect((370,100),(50,50)))
    rectObs.append(pygame.Rect((400,300),(50,50)))
    rectObs.append(pygame.Rect((250,180),(50,50)))
    rectObs.append(pygame.Rect((100,100),(50,50)))
    rectObs.append(pygame.Rect((100,400),(50,50)))
    for rect in rectObs:
        pygame.draw.rect(screen, white, rect)


def reset():
    global count
    screen.fill(black)
    init_obstacles()
    count = 0

def main():
    global count
    
    

    initPoseSet = True
    initialPoint = Node((23,475), None)
    goalPoseSet = True
    goalPoint = Node((694, 104), None)
    currentState = 'buildTree'
    l = []
    nodes = []
    reset()
    nodes.append(initialPoint)
    pygame.draw.circle(screen, yellow, initialPoint.point, GOAL_RADIUS)
    pygame.draw.circle(screen, yellow, goalPoint.point, GOAL_RADIUS)
    while True:
        if currentState == 'goalFound':
            currNode = goalNode.parent
            pygame.display.set_caption('Goal-1 Reached')

            while currNode.parent != None:
                pygame.draw.line(screen,yellow,currNode.point,currNode.parent.point,5)
                currNode = currNode.parent
                l.append(currNode)
            break
        else:
            count = count+1
            pygame.display.set_caption('Performing RRT For Goal-1')
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point,rand) <= dist(parentNode.point,rand):
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True

                newnode = step_from_to(parentNode.point,rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen,red,parentNode.point,newnode)

                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    currentState = 'goalFound'

                    goalNode = nodes[len(nodes)-1]
                    l.append(goalNode)
    
            else:
                print("Ran out of nodes... :(")
                return;

        pygame.display.update()
        fpsClock.tick(10000)
    
    

    
    initPoseSet = True
    initialPoint = Node((23,415), None)
    goalPoseSet = True
    goalPoint = Node((694, 164), None)
    currentState = 'buildTree'
    nodes = []
    s1 = goalNode
    nodes.append(initialPoint)
    
    pygame.draw.circle(screen, blue, initialPoint.point, GOAL_RADIUS)
    pygame.draw.circle(screen, blue, goalPoint.point, GOAL_RADIUS)
    

    while True:
        if currentState == 'goalFound':
            currNode = goalNode.parent
            pygame.display.set_caption('Goal-2 Reached')
            

            while currNode.parent != None:
                pygame.draw.line(screen,blue,currNode.point,currNode.parent.point,5)
                currNode = currNode.parent
        else:
            count = count+1
            pygame.display.set_caption('Performing RRT For Goal-2')
            if count < NUMNODES:
                foundNext = False
                widin = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if dist(p.point,rand) <= dist(parentNode.point,rand):
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True


                                

                newnode = step_from_to(parentNode.point,rand)
                cn = s1
                while cn.parent != None:
                    if dist(newnode, cn.point) <= sensingrange:
                        widin = True
                    cn = cn.parent
                if widin == True:
                    nodes.append(Node(newnode, parentNode))
                    pygame.draw.line(screen,green,parentNode.point,newnode)

                    if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                        currentState = 'goalFound'

                        goalNode = nodes[len(nodes)-1]

                
            else:
                print("Ran out of nodes... :(")
                return;

        
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Exiting")

        pygame.display.update()
        fpsClock.tick(10000)



if __name__ == '__main__':
    main()