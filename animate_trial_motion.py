import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter




def animate(i):
    tmp = st_tracking.iloc[:i,:]
    tmp_q = st_tracking.iloc[i-1:i,:]
    ax.clear()
    ax.set_xlabel('X position', fontsize=10)
    ax.set_ylabel('Z position', fontsize=10)
    ax.set_title('Trial Motion')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    scat = ax.scatter(tmp['position_x'], tmp['position_z'], c=tmp['timestamp'])
    quiv = ax.quiver(tmp_q['position_x'],tmp_q['position_z'],
                      tmp_q['normdir_x'],tmp_q['normdir_z'],
                      color=(247/255,231/255,81/255),headwidth=4,headlength=4,headaxislength=3,scale=30)
    
    return scat,quiv

data = pd.read_csv('data/0000.csv')
data_tracking = pd.read_csv('data/0000_tracking.csv')
data_tracking['norm_vector'] = np.sqrt(1/(data_tracking['forward_x']**2+data_tracking['forward_z']**2))
data_tracking['normdir_x'] = data_tracking['forward_x']*data_tracking['norm_vector']
data_tracking['normdir_z'] = data_tracking['forward_z']*data_tracking['norm_vector']
for trial_num in data_tracking['sequenceNumber'].unique(): 
    st_tracking = data_tracking[data_tracking['sequenceNumber']==trial_num]
    single_trial = data[data['sequenceNumber']==trial_num].squeeze().to_dict() 
    t_start = single_trial['timeAtStartEncodingDistance']
    t_end = single_trial['timeAtEndProductionDistance']
    st_tracking = st_tracking[st_tracking['timestamp'].between(t_start,t_end)]
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    scat = ax.scatter([], [], [])
    quiv = ax.quiver([],[],[],[])
    anim = FuncAnimation(fig, animate, frames=2000, interval=100, repeat=False)
    plt.show()
    #anim.save(f'3_{trial_num}.gif', writer=PillowWriter(fps=10))
    print(t_start,t_end)
    print(st_tracking)

