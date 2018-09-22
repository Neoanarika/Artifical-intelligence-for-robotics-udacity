import numpy as np 
def filter(x, P):
    for n in range(len(measurements)):
        
        # prediction
        x = (F @ x) + u
        P = F @ P @ F.T
        
        # measurement update
        Z = np.array([measurements[n]])
        y = Z.T - (H @ x)
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + (K @ y)
        P = (I - (K @ H)) @ P
    
    print('x= ',x)
    print('P= ',P)

measurements = np.array([[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]])
initial_xy = np.array([4., 12.])

# measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
# initial_xy = [-4., 8.]

# measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
# initial_xy = [1., 19.]

dt = 0.1

x = np.array([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
u = np.array([[0.], [0.], [0.], [0.]]) # external motion

#### DO NOT MODIFY ANYTHING ABOVE HERE ####
#### fill this in, remember to use the matrix() function!: ####

P =  np.array([[0,0,0,0],[0,0,0,0],[0,0,1000,0],[0,0,0,1000]]) # initial uncertainty: 0 for positions x and y, 1000 for the two velocities
F =  np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1]]) # next state function: generalize the 2d version to 4d
H =  np.array([[1,0,0,0],[0,1,0,0]])# measurement function: reflect the fact that we observe x and y but not the two velocities
R =  np.array([[0.1,0.],[0,0.1]])# measurement uncertainty: use 2x2 matrix with 0.1 as main diagonal
I =  np.eye(4) # 4d identity matrix

###### DO NOT MODIFY ANYTHING HERE #######

filter(x, P)
