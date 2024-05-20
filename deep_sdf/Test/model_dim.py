import torch
from tqdm import trange

from deep_sdf.Model.decoder import Decoder

def test():
    decoder = Decoder(256, [512, 512, 512, 512, 512, 512, 512, 512], [0,1,2,3,4,5,6,7],0.2,[0,1,2,3,4,5,6,7],[4]).cuda()

    for i in trange(256):
        for i in range(256):
            test = torch.rand([256, 256 + 3]).cuda()
            result = decoder(test)
    print(result.shape)
    return True
