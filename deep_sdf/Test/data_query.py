import numpy as np

def test():
    normalization_param_file_path = './output/sdf/normalization_param.npz'
    test_file_path = './output/sdf/test.npz'

    normalization_param = np.load(normalization_param_file_path, allow_pickle=True)
    test = np.load(test_file_path, allow_pickle=True)

    print(normalization_param)
    print(test)
    return True
