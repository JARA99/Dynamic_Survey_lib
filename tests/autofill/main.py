import simple_user as su
import defs
import numpy as np
from matplotlib import pyplot as plt
import time
from pydyn_surv import funcs

user_amt = 6
analysis_dim = 5
iters_amnt = 730

analysis_data = dict()

for user_i in range(user_amt):
    user_name = chr(ord('A')+user_i)
    print('Executing user {}'.format(user_name))

    user_i_w = np.random.uniform(-2.05,2.05,size=analysis_dim)
    user_i_w = np.round(user_i_w,2)
    user_i_w_2 = np.random.uniform(-2.05,2.05,size=analysis_dim)
    user_i_w_2 = np.round(user_i_w_2,2)
    # user_i_w_string = np.array2string(user_i_w,precision=2,separator=',',sign=' ')
    user_i_w_1_string = np.array2string(user_i_w,precision=2,separator=',',sign=' ')
    user_i_w_2_string = np.array2string(user_i_w_2,precision=2,separator=',',sign=' ')
    user_i_w_string = '{}->{}'.format(user_i_w_1_string,user_i_w_2_string)
    
    s_cf, wh_cf, entro_cf, rsq_cf = su.one_user(savename = 'output/current_run/w_histo/{}_cf'.format(user_name),
                        title = 'Evolución del peso del usuario {}: {}'.format(user_name,user_i_w_string),
                        iter_amnt=iters_amnt,
                        target_w=user_i_w,
                        change=True,
                        change_to=user_i_w_2,
                        change_at=200,
                        # suv_init_kargs={'train_function':defs.custom_train_function},
                        reduce_iters=True,
                        in_range_answer=True,
                        add_noise=True,
                        fit_answer=True,
                        get_entropy=True,
                        get_rsquared=True,
                        # target_move_func=defs.w_evolution,
                        dim=analysis_dim,
    )

    s_df, wh_df, entro_df, rsq_df = s_cf, wh_cf, entro_cf, rsq_cf
    
    # s_df, wh_df, entro_df, rsq_df = su.one_user(savename = 'output/current_run/w_histo/{}_df'.format(user_name),
    #                     title = 'Evolución del peso del usuario {}: {}'.format(user_name,user_i_w_string),
    #                     iter_amnt=iters_amnt,
    #                     target_w=user_i_w,
    #                     # change=True,
    #                     # change_to=user_i_w_2,
    #                     # change_at=250,
    #                     suv_init_kargs=dict(),
    #                     reduce_iters=True,
    #                     in_range_answer=True,
    #                     add_noise=True,
    #                     fit_answer=True,
    #                     get_entropy=True,
    #                     get_rsquared=True,
    #                     # target_move_func=defs.w_evolution,
    #                     dim=analysis_dim,
    # )

    
    # plt.close('all')

    t_list = np.array([entro_df,rsq_df,entro_cf,rsq_cf]).transpose()

    # analysis_data[user_name] = pd.DataFrame(t_list,columns=['cf entropy','cf rsquared','df entropy','df rsquared'])

    wh_cf = np.array(wh_cf)
    # Ocurrences of -1,0 and 1 are in each column of wh_cf
    wh_cf_count = np.apply_along_axis(lambda x: np.bincount(x.astype(int)+1,minlength=3),0,wh_cf)
    wh_df = np.array(wh_df)
    # Ocurrences of -1,0 and 1 are in each column of wh_df
    wh_df_count = np.apply_along_axis(lambda x: np.bincount(x.astype(int)+1,minlength=3),0,wh_df)

    # print(t_list)
    # print(wh_cf)
    # print(wh_cf_count)
    # print(wh_df)
    # print(wh_df_count)

    defs.plot_bars(user_name,wh_cf_count,'_cf',': {}'.format(user_i_w_string),'output/current_run/count_bars/')
    defs.plot_bars(user_name,wh_df_count,'_df',': {}'.format(user_i_w_string),'output/current_run/count_bars/')

    time.sleep(5)
    plt.close('all')

    # Save the data to the analysis_data dict:
    analysis_data[user_name] = {'history':t_list,'count_cf':wh_cf_count,'count_df':wh_df_count}


# print(analysis_data)
# Save history
for user_name, stored in analysis_data.items():
    np.savetxt('output/current_run/csv_data/{}_hist.csv'.format(user_name),stored['history'],delimiter=',')
    np.savetxt('output/current_run/csv_data/{}_count_cf.csv'.format(user_name),stored['count_cf'],delimiter=',')
    np.savetxt('output/current_run/csv_data/{}_count_df.csv'.format(user_name),stored['count_df'],delimiter=',')

# Make a plot of the history of the entropy for all users
entropy_fig, entropy_ax = plt.subplots()

for user_name, stored in analysis_data.items():
    entropy_ax.plot(stored['history'][:,0],label='Usuario {}'.format(user_name))

entropy_ax.set_title('Entropía del cuestionario por usuario')
entropy_ax.set_xlabel('Iteración')
entropy_ax.set_ylabel('Entropía')
entropy_ax.legend()

entropy_fig.savefig('output/current_run/all_users/entropy_df.png')
plt.close(entropy_fig)

# Make a plot of the history of the rsquared for all users
rsquared_fig, rsquared_ax = plt.subplots()

for user_name, stored in analysis_data.items():
    rsquared_ax.plot(stored['history'][:,1],label='Usuario {}'.format(user_name))

rsquared_ax.set_title('Coeficiente de determinación del cuestionario por usuario')
rsquared_ax.set_xlabel('Iteración')
rsquared_ax.set_ylabel('Coeficiente de determinación')
rsquared_ax.legend()

rsquared_fig.savefig('output/current_run/all_users/rsquared_df.png')
plt.close(rsquared_fig)



    


# print(*('{} -> {}\n'.format(x,y) for x,y in tsurv.training_dataset),sep='')

# tds = tsurv.training_dataset
# w0 = np.array([0,0,0,0,0])
# eta = 0.01
# iter = 2000

# method1 = ml.gradient_descent(ml.squared_loss,ml.squared_loss_derivative,tds,eta,iter,False,w0)
# print('method1:',method1)

