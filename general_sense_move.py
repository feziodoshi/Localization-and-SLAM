import math

world=['red','red','green','red','red']
measurement=['green']
pHit=4
pMiss=1
pUndershoot=0.1
pExact=0.7
pOvershoot=0.3
initialBelief=[0.2,0.2,0.2,0.2,0.2]

def norm(p):
	##normalizes an input vector
    s=sum(p)
    for i in range(len(p)):
        p[i]=p[i]/float(s)
    return p


def add_vec(set_vec,probablity):
	q=[]
	len_every_vec=len(set_vec[0])
	for i in range(len(probablity)):
		for j in range(len_every_vec):
			set_vec[i][j]*=probablity[i]
	for i in range(len_every_vec):
		x=0
		for j in range(len(set_vec)):
			x+=set_vec[j][i]
		q.append(x)

	return q



def cal_entropy(p):
	##if this value is decreasing it is gaining more information
    s=0
    for i in p:
        s+=(i*math.log(i))
    s=s*-1
    return s

def sense(p,Z):
	##here p is the belief and Z are the set of measurements it needs to do
	for sensing_col in Z:
		# print("Currently Sensing colour",sensing_col)
		for i in range(len(p)):
			if(world[i]==sensing_col):
				# print("found at",i)
				p[i]=p[i]*pHit
			else:
				# print("not found",i)
				p[i]=p[i]*pMiss
	norm(p)
	##there is a big catch in entropy gain, now consider you have kept a bot for sensing infinitely and it does so, lets say it is choo
	return(p)

def move_inexact(p,U,probablity):
	under=[]
	exact=[]
	over=[]
	for i in range(len(p)):
		under.append(p[(i-U-1)%len(p)])
		exact.append(p[(i-U)%len(p)])
		over.append(p[(i-U+1)%len(p)])
	q=add_vec([under,exact,over],probablity)
	return(q)



# print(add_vec([[0,0,1],[1,0,0],[0,1,0]],[0.1,0.7,0.2]))
# initial_belief=sense(initial_belief,measurement)
# print(initial_belief)
for i in range(100):
	initialBelief=sense(initialBelief,measurement)
	print(initialBelief)
	print((cal_entropy(initialBelief))*100)
# initial_belief=sense(initial_belief,measurement)
# initial_belief=sense(initial_belief,measurement)
# print(initial_belief)
print(move_inexact(initialBelief,2,[0.1,0.8,0.1]))