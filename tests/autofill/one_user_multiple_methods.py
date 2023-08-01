import simple_user as su
import defs
import numpy as np
from matplotlib import pyplot as plt
import time

user_i = 3
analysis_dim = 5
iters_amnt = 365

user_name = chr(ord('A')+user_i)

user_i_w = np.random.uniform(-2.05,2.05,size=analysis_dim)
user_i_w = np.round(user_i_w,2)
user_i_w_string = np.array2string(user_i_w,precision=2,separator=',',sign=' ')

s_m1, wh_m1, entro_m1, rsq_m1 = su.one_user(savename = 'one_user_output/{}_m1'.format(user_name),
                    title = 'Evolución del peso del usuario {}: {}'.format(user_name,user_i_w_string),
                    iter_amnt=iters_amnt,
                    target_w=user_i_w,
                    # change=True,
                    # change_to=user_i_w_2,
                    # change_at=250,
                    # suv_init_kargs=dict(),
                    reduce_iters=True,
                    in_range_answer=True,
                    add_noise=True,
                    fit_answer=True,
                    get_entropy=True,
                    get_rsquared=True,
                    # target_move_func=defs.w_evolution,
                    dim=analysis_dim,
)

s_m2, wh_m2, entro_m2, rsq_m2 = su.one_user(savename = 'one_user_output/{}_m2'.format(user_name),
                    title = 'Evolución del peso del usuario {}: {}'.format(user_name,user_i_w_string),
                    iter_amnt=iters_amnt,
                    target_w=user_i_w,
                    # change=True,
                    # change_to=user_i_w_2,
                    # change_at=250,
                    # suv_init_kargs={'train_function':defs.custom_train_function},
                    reduce_iters=True,
                    in_range_answer=False,
                    add_noise=True,
                    fit_answer=False,
                    get_entropy=True,
                    get_rsquared=True,
                    # target_move_func=defs.w_evolution,
                    dim=analysis_dim,
)

# plt.close('all')

t_list = np.array([entro_m1,rsq_m1,entro_m2,rsq_m2]).transpose()

time.sleep(5)
plt.close('all')

# Save history
np.savetxt('one_user_output/{}_hist.csv'.format(user_name),t_list,delimiter=',')

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
