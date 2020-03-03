local=list(map(int,input().split()))
G=[[0 for i in range(local[0]+1)]for j in range(local[1]+1)]
G[0][0]=1
def comple(x,y):
    if (abs(x-local[2])+abs(y-local[3]))!=3 or (x==local[2]) or (y==local[3]):
        if 0<x<=local[0] and 0<y<=local[1] :
            G[x][y]=G[x-1][y]+G[x][y-1]
        if x==0 and y!=0:
            G[x][y]=G[x][y-1]
        if y==0 and x!=0:
            G[x][y] = G[x-1][y]
    else:
        G[x][y]=0
for i in range(local[1]+1):
    for j in range(local[0]+1):
        if i==local[3] and j==local[2]:
            continue
        comple(j,i)
print(G[local[0]][local[1]])


