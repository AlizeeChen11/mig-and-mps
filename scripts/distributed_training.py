import os
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP

# Simple model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 128)

    def forward(self, x):
        return self.fc(x)

def setup(rank, world_size):
    dist.init_process_group(
        backend='nccl',          # Use 'nccl' for GPUs
        init_method='env://',    # Read setup from environment variables
        world_size=world_size,
        rank=rank
    )

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size):
    print(f"Running DDP training on rank {rank}.")
    setup(rank, world_size)

    # Set the GPU for this rank
    device = torch.device(f'cuda:{rank}')

    model = SimpleModel().to(device)
    ddp_model = DDP(model, device_ids=[rank])

    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for epoch in range(1000):
        inputs = torch.randn(10000, 10).to(device)
        targets = torch.randn(10000, 1).to(device)

        optimizer.zero_grad()
        outputs = ddp_model(inputs)
        loss = loss_fn(outputs, targets)
        loss.backward()
        optimizer.step()
              print(f"Rank {rank}, Epoch {epoch}, Loss: {loss.item()}")

    cleanup()

if __name__ == "__main__":
    world_size = torch.cuda.device_count()
    if world_size < 1:
        raise RuntimeError("No GPUs found!")

    # For multiprocessing
    import torch.multiprocessing as mp
    mp.spawn(train,
             args=(world_size,),
             nprocs=world_size,
             join=True)
