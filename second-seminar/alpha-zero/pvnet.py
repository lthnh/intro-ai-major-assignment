import torch
import torch.nn as nn
import torch.nn.functional as F


class ResidualLayer(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super(ResidualLayer, self).__init__()

        self.conv_block_1 = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=3,
                stride=1,
            ),
            nn.BatchNorm2d(num_features=out_channels),
        )
        self.conv_block_2 = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=3,
                stride=1,
            ),
            nn.BatchNorm2d(num_features=out_channels),
        )

    def forward(self, x: torch.Tensor):
        x1 = F.relu(self.conv_block_1(x))
        x2 = F.relu(self.conv_block_2(x1) + x)
        return x2


class PolicyValueNetwork(nn.Module):
    def __init__(self, args):
        # game params

        # neural net
        super(PolicyValueNetwork, self).__init__()

        # the body
        self.body_block_conv = nn.Sequential(
            nn.Conv2d(in_channels=4, out_channels=256, kernel_size=3, stride=1),
            nn.BatchNorm2d(num_features=256),
        )
        self.body_block_residual = nn.Sequential()
        for i in range(3):
            self.body_block_residual.add_module(name=f'residual_layer_{i + 1}', module=ResidualLayer(256, 256))

        # the policy head
        self.policy_head_conv = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=2, kernel_size=1, stride=1),
            nn.BatchNorm2d(num_features=2),
        )
        self.policy_head_linear = nn.Linear(in_features=2, out_features=81)

        # the value head
        self.value_head_conv = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=1, kernel_size=1, stride=1),
            nn.BatchNorm2d(num_features=1),
        )
        self.value_head_hidden = nn.Linear(in_features=1, out_features=256)
        self.value_head_to_scalar = nn.Linear(in_features=256, out_features=1)

    def forward(self, x: torch.Tensor):
        x1 = F.relu(self.body_block_conv(x))
        x2 = self.body_block_residual(x1)

        x3 = F.relu(self.policy_head_conv(x2))
        p = self.policy_head_linear(x3)

        x4 = F.relu(self.value_head_conv(x2))
        x5 = F.relu(self.value_head_hidden(x4))
        v = F.tanh(self.value_head_to_scalar(x5))

        return p, v
