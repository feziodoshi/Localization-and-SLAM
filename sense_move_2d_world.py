import math
import numpy as np
import time
world = [['R','G', 'G', 'R','R'],
          ['R', 'R','G','R','R'],
          ['R','R','G', 'G','R'],
          ['R','R','R','R','R']]
# p=[[0.05,0.05,0.05,0.05,0.05],[0.05,0.05,0.05,0.05,0.05],[0.05,0.05,0.05,0.05,0.05],[0.05,0.05,0.05,0.05,0.05]]
# p=[[1,0,0],[0,1,0],[0,0,1]]
p=[]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
sensorRight = 0.7
sensorWrong=1-sensorRight
pMove = 0.8  ##probablity to move exactly(lets just say that there is no undershoot and overshoot)
pNotMove=1-pMove

def gaussian(pos,mean,variance):
	num=((math.pow(pos-mean,2))/variance)/2
	num=math.exp(-1*num)
	num=num/(math.sqrt(2*math.pi*variance))
	return(num)


def norm(p):
	total=0
	for i in p:
		for j in i:
			total+=j
	for i in range(len(p)):
		for j in range(len(p[i])):
			p[i][j]=p[i][j]/float(total)
	return p

def sense(p,Z):
	for i in range(len(p)):
		for j in range(len(p[i])):
			if(world[i][j]==Z):
				# print("yayy")
				p[i][j]*=sensorRight
			else:
				# print("no")
				p[i][j]*=sensorWrong
	p=norm(p)
	return p

def take_vectors_and_convolute(p,U):
	q=[]
	for vec in p:
		q_=[]
		for i in range(len(vec)):
			# print(vec[(i-U)%len(vec)])
			x=vec[(i-U)%len(vec)]*pMove
			y=vec[(i)%len(vec)]*pNotMove
			q_.append(x+y)
		q.append(q_)
	return(q)

def take_transpose(p):
	q=np.transpose(p)
	q=list(q)
	return(q) 


def move(p,move):
	if(move==[0,0]):
		##do not move
		q=p
	elif(move==[1,0]):
		##move down
		p=take_transpose(p)
		q=take_vectors_and_convolute(p,1)
		q=take_transpose(q)
	elif(move==[-1,0]):
		##move up
		p=take_transpose(p)
		q=take_vectors_and_convolute(p,-1)
		q=take_transpose(q)
	elif(move==[0,1]):
		##move right
		q=take_vectors_and_convolute(p,1)
	elif(move==[0,-1]):
		##move left
		q=take_vectors_and_convolute(p,-1)
	return(q)

def create_uniform():
	q=[]
	tot_len=len(world[0])*len(world)
	uniform=float(1)/tot_len
	for i in world:
		to_be_append=[]
		for j in i:
			to_be_append.append(uniform)
		q.append(to_be_append)
	return(q)

def localize(measurements,motions):
	p=create_uniform()
	assert len(measurements)==len(motions),"Invalid localization"
	for i in range(len(measurements)):
		p=move(p,motions[i])
		p=sense(p,measurements[i])
		print(p)
		time.sleep(1)
	return(p)

# p = localize(measurements,motions)
# print(p)
print(gaussian(8,10,4))

##first move and then sense and get a new belief
