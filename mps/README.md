# Configure and use GPU in MPS mode
This document walks though the steps to configure and use Nvidia GPU in Multi-Process Service mode

## Prerequisites
- An active Azure subscription
- Nvidia GPU VM SKU quota available
- Proper GPU driver installed

### Detailed steps
```
az vm create --resource-group RG --name VMNAME --image  microsoft-dsvm:ubuntu-hpc:2204:latest  --public-ip-sku Standard --admin-username azureuser --admin-password  --size Standard_NC4as_T4_v3  --location LOCATION
sudo nvidia-smi -pm 1
nvidia-cuda-mps-control -d
export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log
#  limit the GPU compute usage per process
export CUDA_MPS_ACTIVE_THREAD_PERCENTAGE=50

```

Run test: python3 ./scripts/distributed_training.py
Monitor result:

<img width="852" height="450" alt="image" src="https://github.com/user-attachments/assets/52319fec-30cf-4916-bf5b-48149c606e0d" />
