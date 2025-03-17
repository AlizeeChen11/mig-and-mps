# Configure and use MIG on Azure VM with Nvidia GPU
This document walkthrough the steps to enable MIG on Nvidia GPU and how to use them to run different workloads.

## Prerequisites
MIG is only available on high end GPU type. You will nede to chosoe a VM SKU at least with A100.

## Configuration
### Create Azure resource:
Provision an Azure VM with Azure marketplace HPC image:
```
az vm create --resource-group RGNAME --name VMNAME --image microsoft-dsvm:ubuntu-hpc:2204:latest --public-ip-sku Standard --admin-username azureuser --admin-password xxx --size Standard_NC40ads_H100_v5  --location LOCATION --security-type Standard
Note: microsoft-dsvm:ubuntu-hpc:2204:latest will use the latest available marketplace Ubuntu-HPC image. If you would like to use a specifc version of image, you can run "az vm image list --publisher "Microsoft-DSVM" --offer "Ubuntu-HPC" -o table --all" to list all available image version.

```
### Enable MIG:
```
nvidia-smi -L
sudo nvidia-smi -pm ENABLED
sudo nvidia-smi -mig 1
nvidia-smi -i 0 --query-gpu=pci.bus_id,mig.mode.current --format=csv
```

List available MIG configuration users can choose:
```
nvidia-smi mig -lgip
```
You will get result similar as below:
```
+-----------------------------------------------------------------------------+
| GPU instance profiles:                                                      |
| GPU   Name             ID    Instances   Memory     P2P    SM    DEC   ENC  |
|                              Free/Total   GiB              CE    JPEG  OFA  |
|=============================================================================|
|   0  MIG 1g.12gb       19     7/7        10.75      No     16     1     0   |
|                                                             1     1     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.12gb+me    20     1/1        10.75      No     16     1     0   |
|                                                             1     1     1   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.24gb       15     4/4        21.62      No     26     1     0   |
|                                                             1     1     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 2g.24gb       14     3/3        21.62      No     32     2     0   |
|                                                             2     2     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 3g.47gb        9     2/2        46.38      No     60     3     0   |
|                                                             3     3     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 4g.47gb        5     1/1        46.38      No     64     4     0   |
|                                                             4     4     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 7g.94gb        0     1/1        93.12      No     132    7     0   |
|                                                             8     7     1   |
+-----------------------------------------------------------------------------+
```
List possible placements available:
```
nvidia-smi mig -lgipp
```
You will see resutl similar as below:
```
GPU  0 Profile ID 19 Placements: {0,1,2,3,4,5,6}:1
GPU  0 Profile ID 20 Placements: {0,1,2,3,4,5,6}:1
GPU  0 Profile ID 15 Placements: {0,2,4,6}:2
GPU  0 Profile ID 14 Placements: {0,2,4}:2
GPU  0 Profile ID  9 Placements: {0,4}:4
GPU  0 Profile ID  5 Placement : {0}:4
GPU  0 Profile ID  0 Placement : {0}:8
```
Run the following command to divide the H100 GPU Instance into 3 slices by using 3 different profiles
```
sudo nvidia-smi mig -cgi 9,15,19 -C
```
Verify the MIG configuration:
```
sudo nvidia-smi mig -lgi
nvidia-smi -L
nvidia-smi

+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.03              Driver Version: 560.35.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 NVL                On  |   00000001:00:00.0 Off |                   On |
| N/A   31C    P0             62W /  400W |      64MiB /  95830MiB |     N/A      Default |
|                                         |                        |              Enabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| MIG devices:                                                                            |
+------------------+----------------------------------+-----------+-----------------------+
| GPU  GI  CI  MIG |                     Memory-Usage |        Vol|        Shared         |
|      ID  ID  Dev |                       BAR1-Usage | SM     Unc| CE ENC  DEC  OFA  JPG |
|                  |                                  |        ECC|                       |
|==================+==================================+===========+=======================|
|  0    1   0   0  |              38MiB / 47488MiB    | 60      0 |  3   0    3    0    3 |
|                  |                 0MiB / 65535MiB  |           |                       |
+------------------+----------------------------------+-----------+-----------------------+
|  0    5   0   1  |              13MiB / 22144MiB    | 26      0 |  1   0    1    0    1 |
|                  |                 0MiB / 32767MiB  |           |                       |
+------------------+----------------------------------+-----------+-----------------------+
|  0   13   0   2  |              13MiB / 11008MiB    | 16      0 |  1   0    1    0    1 |
|                  |                 0MiB / 16383MiB  |           |                       |
+------------------+----------------------------------+-----------+-----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

Test to run workload by specifying the MIG devices:


To disbale MIG, you can run:
```
nvidia-smi -mig 0
```


