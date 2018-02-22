import os
import argparse
import numpy as np

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

DEFAULT_DATATYPE = np.float32

def read_config_file(file):
    config = configparser.ConfigParser()
    config.read(file)
    section = config.sections()
    fileParams = {}

    fileParams['data_url'] = eval(config.get(section[0],'data_url'))
    fileParams['train_data'] = eval(config.get(section[0],'train_data'))
    fileParams['test_data'] = eval(config.get(section[0],'test_data'))
    fileParams['model_name'] = eval(config.get(section[0],'model_name'))
    fileParams['conv'] = eval(config.get(section[0],'conv'))
    fileParams['dense'] = eval(config.get(section[0],'dense'))
    fileParams['activation'] = eval(config.get(section[0],'activation'))
    fileParams['out_act'] = eval(config.get(section[0],'out_act'))
    fileParams['loss'] = eval(config.get(section[0],'loss'))
    fileParams['optimizer'] = eval(config.get(section[0],'optimizer'))
    fileParams['metrics'] = eval(config.get(section[0],'metrics'))
    fileParams['epochs'] = eval(config.get(section[0],'epochs'))
    fileParams['batch_size'] = eval(config.get(section[0],'batch_size'))
    fileParams['learning_rate'] = eval(config.get(section[0], 'learning_rate'))
    fileParams['drop'] = eval(config.get(section[0],'drop'))
    fileParams['classes'] = eval(config.get(section[0],'classes'))
    fileParams['pool'] = eval(config.get(section[0],'pool'))
    fileParams['save'] = eval(config.get(section[0], 'save'))

    # parse the remaining values
    for k,v in config.items(section[0]):
        if not k in fileParams:
            fileParams[k] = eval(v)

    return fileParams


def common_parser(parser, file_path=None):
    if file_path is None:
        file_path = os.path.dirname(os.path.realpath(__file__))

    parser.add_argument("--config_file", dest='config_file', type=str,
                        default=os.path.join(file_path, 'nt3_default_model.txt'),
                        help="specify model configuration file")
        
    return parser



def args_overwrite_config(args, config):

    params = config
    args_dict = vars(args)


    for key in args_dict.keys():
        params[key] = args_dict[key]

    if 'datatype' not in params:
        params['datatype'] = DEFAULT_DATATYPE
    else:
        if params['datatype'] in set(['f16', 'f32', 'f64']):
            params['datatype'] = get_choice(params['datatype'])

    return params


def get_nt3_parser():
    #parser = argparse.ArgumentParser(prog='nt3_baseline',
    #    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    #    description='Train Autoencoder - Pilot 1 Benchmark NT3')
    parser = argparse.ArgumentParser()
    
    return common_parser(parser)


def initialize_parameters():
    # Get command-line parameters
    parser = get_nt3_parser()
    args = parser.parse_args()
    #print('Args:', args)
    # Get parameters from configuration file
    fileParameters = read_config_file(args.config_file)
    #print ('Params:', fileParameters)
    # Consolidate parameter set. Command-line parameters overwrite file configuration
    gParameters = p1_common.args_overwrite_config(args, fileParameters)
    return gParameters

