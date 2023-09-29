# import simple_user as su
# import defs
import numpy as np
from matplotlib import pyplot as plt
import time

user_i = 4
analysis_dim = 5
iters_amnt = 365

user_name = chr(ord('A')+user_i)

# user_i_w = np.random.uniform(-2.05,2.05,size=analysis_dim)
# user_i_w = np.round(user_i_w,2)
user_i_w = np.array([1.76,-1.21,-0.12,1.5,-0.55])
user_i_w_string = np.array2string(user_i_w,precision=2,separator=',',sign=' ')

# plt.close('all')

t_list = np.loadtxt('one_user_output/{}_hist.csv'.format(user_name),delimiter=',')

# Make a plot of the history of the entropy for all users
entropy_fig, entropy_ax = plt.subplots()

entropy_ax.plot(t_list[:,1],label='Respuestas fijas')
entropy_ax.plot(t_list[:,3],label='Respuestas libres')

entropy_ax.set_title('Coeficiente de determinación')
entropy_ax.set_xlabel('Iteración')
entropy_ax.set_ylabel('$R^2$')
entropy_ax.legend()

entropy_fig.savefig('one_user_output/{}_r2.png'.format(user_name))
plt.close(entropy_fig)