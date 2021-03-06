

from neural_nets.nn_models_getter import get_nn_model
from optimizers import get_optimizer
from utils_train import fit, test
from configs import configs_tim
from data_loader_creation import get_dataloader_objects
from classification_results import results_storer
from visualisations import plot_metrics_from_pkl

""" USER: SELECT THE CONFIGURATION YOU NEED """
myList = configs_tim.list_of_configs
#myList = configs_joaquin.list_of_configs
#myList = configs_ozhan.list_of_configs
 
for idx, my_cfg in enumerate(myList):
    print('++++ CONFIGURATION %2d, of %2d' % (idx, len(myList)))

    """ PREPARE DATALOADERS """
    # TODO: Write a method that checks if we have already stored the DL objects for this specific my_cfg -> LOAD THEM
    # TODO: If not -> STORE THEM (...We need a unique identifier for each DL object.. for example MD5 value)
    train_dl, val_dl, test_dl, input_dimension_, output_dimension_ = get_dataloader_objects(my_cfg)


    """CLASSIFICATION"""
    # Get the model
    model_untrained = get_nn_model(my_cfg.nn_list[my_cfg.nn_selection_idx], input_dimension=input_dimension_,
                                   output_dimension=output_dimension_, dropout=my_cfg.dropout_perc)

    # Get the optimizer
    optimizer = get_optimizer(my_cfg.optimizer_list[my_cfg.optimizer_selection_idx], my_cfg.learning_rate,
                              model_untrained.parameters(), my_cfg.momentum, my_cfg.weight_decay)


    # Train and show validation loss
    train_losses, train_accuracies, val_losses, val_accuracies, model_trained, time_spent_for_training_s =\
        fit(train_dl, val_dl, model_untrained, optimizer, my_cfg.loss_fn, my_cfg.num_of_epochs,
            scheduler=my_cfg.scheduler)

    # Test the net
    print('\n \n+++++++++++++++++++++++++++++++++++++++++')
    print('Performance on the test set:')
    test_loss, test_accuracy = test(model_trained, test_dl, my_cfg.loss_fn, print_loss=True)
    print('->test_loss: {:.4f}, test_accuracy: {:.4f}%'.format(test_loss, test_accuracy))


    # Store the results
    results_storer.store_results_for_plot(my_cfg,test_loss, test_accuracy, train_losses,
                                 train_accuracies, time_spent_for_training_s, val_losses, val_accuracies)

    results_storer.store_results(my_cfg, model_trained, optimizer, test_loss, test_accuracy, train_losses,
                                 train_accuracies, time_spent_for_training_s, val_losses, val_accuracies, test_dl)



