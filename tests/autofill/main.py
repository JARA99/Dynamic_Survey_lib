import simple_user as su
import defs
from pydyn_surv import ml
import numpy as np

if False:

    iters_amnt = 365

    su.one_user('one_user_tests/base','Evolución del peso\n',
                iter_amnt=iters_amnt,in_range_answer=True)

    # su.one_user('one_user_tests/t02','Respuestas sin acotar, sin cambio de peso',
    #             iter_amnt=iters_amnt,in_range_answer=False)

    su.one_user('one_user_tests/new_train','Evolución del peso\nFunción de entrenamiento redefinida',
                iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function})


    iters_amnt = 730

    # def ct(*args,**kwargs):
    #     return defs.custom_train_function(*args,tds_len=50,**kwargs)


    su.one_user('one_user_tests/wchange_new_train','Evolución del peso\nCambio de peso esperado\nFunción de entrenamiento redefinida',
                iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
                change=True,change_at=365,change_to=[-2,0.5,0,1,2])

    su.one_user('one_user_tests/wchange','Evolución del peso\nCambio de peso esperado',
                iter_amnt=iters_amnt,in_range_answer=True,
                change=True,change_at=365,change_to=[-2,0.5,0,1,2])


    iters_amnt = 365

    su.one_user('one_user_tests/base_2','Evolución del peso\n',
                iter_amnt=iters_amnt,in_range_answer=True,
                target_w=[0,0.5,1,1.5,2])
    
    su.one_user('one_user_tests/new_train_2','Evolución del peso\nFunción de entrenamiento redefinida',
                iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
                target_w=[2,0,1,0,0],fit_answer=False)

iters_amnt = 365

tsurv = su.one_user('one_user_tests/new_train_2','Evolución del peso con ruido agregado\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-1.234,1.423,0.523,0.21,-0.3],fit_answer=False,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_2','Evolución del peso con ruido agregado',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-1.234,1.423,0.523,0.21,-0.3],fit_answer=False,add_noise=True)

tsurv = su.one_user('one_user_tests/new_train_3','Evolución del peso con ruido agregado\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-0.234,0.0423,0.523,0.21,-0.3],fit_answer=False,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_3','Evolución del peso con ruido agregado',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-0.234,0.0423,0.523,0.21,-0.3],fit_answer=False,add_noise=True)

tsurv = su.one_user('one_user_tests/new_train_1','Evolución del peso con ruido agregado\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-2,-1,0,1,2],fit_answer=False,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_1','Evolución del peso con ruido agregado',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-2,-1,0,1,2],fit_answer=False,add_noise=True)


tsurv = su.one_user('one_user_tests/new_train_2_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-1.234,1.423,0.523,0.21,-0.3],fit_answer=True,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_2_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-1.234,1.423,0.523,0.21,-0.3],fit_answer=True,add_noise=True)

tsurv = su.one_user('one_user_tests/new_train_3_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-0.234,0.0423,0.523,0.21,-0.3],fit_answer=True,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_3_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-0.234,0.0423,0.523,0.21,-0.3],fit_answer=True,add_noise=True)

tsurv = su.one_user('one_user_tests/new_train_1_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas\nFunción de entrenamiento redefinida',
            iter_amnt=iters_amnt,in_range_answer=True,suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-2,-1,0,1,2],fit_answer=True,add_noise=True)

tsurv = su.one_user('one_user_tests/basic_1_fit','Evolución del peso con ruido agregado\nRespuestas discretizadas',
            iter_amnt=iters_amnt,in_range_answer=True,#suv_init_kargs={'train_function':defs.custom_train_function},
            target_w=[-2,-1,0,1,2],fit_answer=True,add_noise=True)

# print(*('{} -> {}\n'.format(x,y) for x,y in tsurv.training_dataset),sep='')

# tds = tsurv.training_dataset
# w0 = np.array([0,0,0,0,0])
# eta = 0.01
# iter = 2000

# method1 = ml.gradient_descent(ml.squared_loss,ml.squared_loss_derivative,tds,eta,iter,False,w0)
# print('method1:',method1)

