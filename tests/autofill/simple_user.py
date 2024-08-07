from pydyn_surv.survey import survey
from matplotlib import pyplot as plt
from defs import *

TOTAL_ITERATIONS = 5

# Basic example: No added randomness, fitted answers
# Create a survey with dim=5
def one_user(savename = 'one_user',
             title = 'Ejemplo básico',
             iter_amnt = TOTAL_ITERATIONS,
             target_w = [-2,-1,0,1,2],
             change = False,
             change_at = 365,
             change_to = [-1,-2,-1,1,2],
             suv_init_kargs = dict(),
             reduce_iters = True,
             in_range_answer = True,
             add_noise = False,
             fit_answer = True,
             get_entropy = False,
             get_rsquared = False,
             target_move_func = lambda x: x,
             dim = 5,
             ):

    d5_items_dicts = create_items_dicts(dim=dim)
    cats = ['C{}'.format(i) for i in range(1,dim+1)]
    s1 = survey(d5_items_dicts, 'S1 - Basic example: No added randomness, fitted answers',categories=cats,**suv_init_kargs)
    # s1.print_info()

    # Create a user with target_w 
    u1 = user(target_w = np.array(target_w))

    # Create a list for storing the item evolution history
    item_evolution_history = []
    entropy_evolution_history = []
    rsquared_evolution_history = []
    real_w_history = []

    for n_iteration in range(iter_amnt):
        # Get an item from the survey, add it to the history
        n_item, *_ = s1.launch_random()
        item_evolution_history.append(n_item.category_vector)

        # Set a re-train iteration number
        if reduce_iters:
            re_train_iters = int(2000/(n_iteration+1))
            if re_train_iters < 50:
                re_train_iters = 50
        else:
            re_train_iters = 2000

        # Change if needed
        if change and n_iteration == change_at:
            u1.target_w = np.array(change_to)
            print('{}) Target weight vector changed to: {}'.format(n_iteration,u1.target_w))

        # Answer the item
        real_w_history.append(u1.target_w)
        u1.answer_item(n_item, fit_answer = fit_answer, add_noise = add_noise,kargs={'iter_':re_train_iters},in_range_answer=in_range_answer)

        # Update target
        u1.target_w = target_move_func(u1.target_w)

        # Get entropy
        if get_entropy:
            entro = get_survey_entropy(s1)
            entropy_evolution_history.append(entro)
        
        if get_rsquared:
            rsq = get_survey_rsquared(s1)
            rsquared_evolution_history.append(rsq)

        # Print weight vector
        print('{}) Weight vector: {}'.format(n_iteration,s1.get_weight()))
    
    real_w_history = np.array(real_w_history)

    # Get the weight evolution history
    s1_w_evolution = np.array(s1.get_weight_history())

    # Set scale factor
    # s1_w_evolution = s1_w_evolution * 1.5

    # Plot the weight vector evolution: for each dimension plot a line with the evolution of the weight
    # Create a figure
    fig, ax = plt.subplots()

    # Plot the target weight vector

    # if change:
    #     # First block
    #     ax.hlines(target_w[0], 0, change_at, label='C1 esperado',colors='C1',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[1], 0, change_at, label='C2 esperado',colors='C2',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[2], 0, change_at, label='C3 esperado',colors='C3',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[3], 0, change_at, label='C4 esperado',colors='C4',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[4], 0, change_at, label='C5 esperado',colors='C5',linestyles='dotted',linewidth=1.2)
    #     # Second block
    #     ax.hlines(change_to[0], change_at, iter_amnt,colors='C1',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(change_to[1], change_at, iter_amnt,colors='C2',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(change_to[2], change_at, iter_amnt,colors='C3',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(change_to[3], change_at, iter_amnt,colors='C4',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(change_to[4], change_at, iter_amnt,colors='C5',linestyles='dotted',linewidth=1.2)
    # else:
    #     ax.hlines(target_w[0], 0, iter_amnt, label='C1 esperado',colors='C1',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[1], 0, iter_amnt, label='C2 esperado',colors='C2',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[2], 0, iter_amnt, label='C3 esperado',colors='C3',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[3], 0, iter_amnt, label='C4 esperado',colors='C4',linestyles='dotted',linewidth=1.2)
    #     ax.hlines(target_w[4], 0, iter_amnt, label='C5 esperado',colors='C5',linestyles='dotted',linewidth=1.2)

    # Plot the evolution of the target weights
    for n_cat in range(len(cats)):
        ax.plot(real_w_history[:,n_cat], label='{} esperado'.format(cats[n_cat]), color=cats[n_cat], linestyle='dotted',linewidth=1.2)
    # ax.plot(real_w_history[:,0], label='C1 esperado', color='C1', linestyle='dotted',linewidth=1.2)
    # ax.plot(real_w_history[:,1], label='C2 esperado', color='C2', linestyle='dotted',linewidth=1.2)
    # ax.plot(real_w_history[:,2], label='C3 esperado', color='C3', linestyle='dotted',linewidth=1.2)
    # ax.plot(real_w_history[:,3], label='C4 esperado', color='C4', linestyle='dotted',linewidth=1.2)
    # ax.plot(real_w_history[:,4], label='C5 esperado', color='C5', linestyle='dotted',linewidth=1.2)

    # Plot the evolution of the weights
    for n_cat in range(len(cats)):
        ax.plot(s1_w_evolution[:,n_cat], label='{} entrenado'.format(cats[n_cat]), color=cats[n_cat])
    # ax.plot(s1_w_evolution[:,0], label='C1', color='C1')
    # ax.plot(s1_w_evolution[:,1], label='C2', color='C2')
    # ax.plot(s1_w_evolution[:,2], label='C3', color='C3')
    # ax.plot(s1_w_evolution[:,3], label='C4', color='C4')
    # ax.plot(s1_w_evolution[:,4], label='C5', color='C5')

    # Add vertical line on weight change
    # if change:
    #     ax.vlines(change_at, -2, 2, colors='gray', linestyles='dotted',linewidth=0.5)

    # Add legend, title and labels
    ax.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax.set_title(title)
    ax.set_xlabel('Numero de iteracion')
    ax.set_ylabel('Valor del peso')

    # Save the figure to output
    fig.savefig('{}.png'.format(savename),bbox_inches='tight')
    # plt.close(fig)

    return s1, item_evolution_history, entropy_evolution_history, rsquared_evolution_history

