import os
import time
from types import SimpleNamespace

import numpy as np
import numpy.typing as npt
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

from .pvnet import PolicyValueNetwork
from .utils import AverageMeter

args = SimpleNamespace(
    **{
        "lr": 0.001,
        "dropout": 0.3,
        "epochs": 10,
        "batch_size": 64,
        "cuda": torch.cuda.is_available(),
        "num_channels": 512,
    }
)


class UTTTNeuralNetwork:
    def __init__(self, state: torch.Tensor):
        self.nnet: nn.Module = PolicyValueNetwork(args)
        self.board_size: int = 9
        self.action_size: int = 81

        if args.cuda:
            self.nnet.cuda()

    def train(self, examples: list[tuple[npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]]):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        optimizer = optim.Adam(self.nnet.parameters())

        for epoch in range(args.epochs):
            print("EPOCH ::: " + str(epoch + 1))
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count: int = len(examples) // args.batchsize

            t = tqdm(range(batch_count), desc="training neural network")
            for _ in t:
                sample_ids = np.random.randint(len(examples), size=args.batchsize)
                states, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                states = torch.from_numpy(states)
                target_pis = torch.from_numpy(pis)
                target_vs = torch.from_numpy(vs)
                # predict
                if args.cuda:
                    states = states.contiguous().cuda()
                    target_pis = target_pis.contiguous().cuda()
                    target_vs = target_vs.contiguous().cuda()
                # compute output
                out_pi, out_v = self.nnet(states)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v
                # record loss
                pi_losses.update(l_pi.item(), states.size(0))
                v_losses.update(l_v.item(), states.size(0))
                t.set_postfix(loss_pi=pi_losses, loss_v=v_losses)
                # compute gradient and do stochastic gradient descent
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, state: npt.ArrayLike):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        state = torch.from_numpy(state)
        if args.cuda:
            state = state.contiguous().cuda()
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(state)

        print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save_checkpoint(self, folder="checkpoint", filename="checkpoint.pth.tar"):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print(
                "Checkpoint Directory does not exist! Making directory {}".format(
                    folder
                )
            )
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save(
            {
                "state_dict": self.nnet.state_dict(),
            },
            filepath,
        )

    def load_checkpoint(self, folder="checkpoint", filename="checkpoint.pth.tar"):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise Exception("No model in path {}".format(filepath))
        map_location = None if args.cuda else "cpu"
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint["state_dict"])
