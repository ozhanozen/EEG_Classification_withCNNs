# Here we define our network classes
import torch
import torch.nn as nn
import neural_nets.fully_connected as fc
import neural_nets.recurrent as rc
import neural_nets.convolutional as conv


# Model selection
def get_nn_model(model_name, input_dimension, output_dimension):
    if model_name == 'SimpleFC':
        model = fc.Simple(input_dimension, output_dimension)
    elif model_name == 'DeepFC':
        model = fc.Deep(input_dimension, output_dimension)
    else:
        raise Exception('Mismatch between nn_list in config and available names in get_nn_model')

    # Transfer model to gpu if possible
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    print(device, "Will be used for training of this model.")
    if (device == torch.device("cuda")) and (torch.cuda.device_count() > 1):
        print("You have", torch.cuda.device_count(), "GPUs for training!")
        model = nn.DataParallel(model)
    model = model.to(device)

    return model