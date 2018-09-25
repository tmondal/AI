import numpy as np
import matplotlib.pyplot as pl

X=4;Y=16    # shape of grid
grid=np.ones([4,16])  
T=np.zeros([42,42])  #transition matrix
empty_sq=[]  # empty locations in the grid
epsilon=0.00
O=np.zeros([42,42]) # emission matrix

# find empty squares in the grid
def init_empty_sq():
    for x in range(0,4):
        for y in range(0,16):
            if(grid[x][y]==1):
                empty_sq.append((x,y))

#calculate transition model 
def trans_model():
    for i in range(0,42):
        (x ,y)=empty_sq[i]
        Neigh=Neighbour(x,y)
        Ns=len(Neigh)
        for j in range(0,Ns):
            index=empty_sq.index(Neigh[j])
            T[i][index]=1/Ns

#calculate sensor model at time t            
# (x,y) is true location of the robot at time t
def sensor_model(x,y):
    R=sensor_reading(x,y)
    for i in range(0,42):
        (a,b)=empty_sq[i]
        A=sensor_reading(a,b)
        dit=error(A,R)
        t=np.power(1-epsilon,4-dit)*np.power(epsilon,dit)
        O[i][i]=t;
            
# find all possible neighbour of a current location
def Neighbour(x,y):
    a_list=[]
    if x-1>=0 and grid[x-1][y]==1:
        a_list.append((x-1,y))    
    if x+1<X and grid[x+1][y]==1:
        a_list.append((x+1,y)) 
    if y+1<Y and grid[x][y+1]==1:
        a_list.append((x,y+1)) 
    if y-1>=0 and grid[x][y-1]==1:
        a_list.append((x,y-1))
    return a_list    

#find sensor reading given a location 
def sensor_reading(x,y):
    reading=list("1111")    
    if x-1<0 or grid[x-1][y]==0:
        reading[0]="0"    
    if x+1>=X or grid[x+1][y]==0:
        reading[1]="0"
    if y+1>=Y or grid[x][y+1]==0:
        reading[2]="0"
    if y-1<0 or grid[x][y-1]==0:
        reading[3]="0"    
    return reading

# error is discrepancy between true value of a square and sensor reading
def error(A,R):
    cnt=0;
    for i in range(0,4):
        if A[i]!= R[i]:
            cnt=cnt+1        
    return cnt

#filtering
def filtering(f):
    f=np.matmul(O,np.matmul(np.transpose(T),f))
    return f
#create the grid    
def initialize_grid():
    grid[0][4]=0;grid[0][10]=0;grid[0][14]=0;grid[1][0]=0
    grid[1][1]=0;grid[1][4]=0;grid[1][6]=0;grid[1][7]=0
    grid[1][9]=0;grid[1][11]=0;grid[1][13]=0;grid[1][14]=0
    grid[1][15]=0;grid[2][0]=0;grid[2][4]=0;grid[2][6]=0
    grid[2][7]=0;grid[2][13]=0;grid[2][14]=0;grid[3][2]=0
    grid[3][6]=0;grid[3][11]=0
    for i in range(0,4):
        for j in range(0,16):
            print("("+str(i)+","+str(j)+")="+str(int(grid[i][j]))),
        print("")    
    
def HMM():
    start=1
    f=np.full([42,1],1/42) #prior
    arr_err=[]
    e_path=[]
    a_path=[]
    for i in range(0,2):
        if start==1:
           print("Choose state to start:")
           start=0
        else:
           print("Choose state to move:")  
        a=int(input("Enter x:"))
        b=int(input("Enter y:"))
        if(a<0 or a>4 or b<0 or b>15 or grid[a][b]==0):
            continue
        sensor_model(a,b)           # calculate O matrix 
        f=filtering(f)              #find posterior
        size=len(f)
        #print(O)
        #print(f)
        ind=np.argmax(f)
        #print("ind="+str(ind))
        print("HMM says:"+str(empty_sq[ind]))
        x,y=empty_sq[ind]
        arr_err.append(abs(a-x)+abs(b-y));
        z=viterbi_algo()
        e_path.append(empty_sq[z])
        a_path.append((a,b))
    acc=path_acc(e_path,a_path)
    print("accuracy="+str(acc))

def path_acc(e_path,a_path):
    cnt=0;
    for i in range(0,len(e_path)):
         if e_path[i]==a_path[i]:
             cnt=cnt+1;
    return cnt/len(e_path)
    

#viterbi algorithm to find most likely path
def viterbi_algo():
    m=np.full([42,1],1/42)
    g=np.multiply(np.transpose(T),np.transpose(m))
    #print(np.transpose(T))
    #print(np.transpose(m))
    t=np.amax(g,axis=1)
    #print(t)
    m=np.matmul(O,t)
    max_ind=np.argmax(m)
    return max_ind
    
    
if __name__ == '__main__':
    initialize_grid()
    init_empty_sq()
    trans_model()
    #print(T)
    HMM()             
