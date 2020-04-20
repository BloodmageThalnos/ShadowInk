import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

import numpy as np
from collections import defaultdict
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from os import listdir
from os.path import isfile, join
import time
import sys
import argparse

from queue import Queue # put, get, qsize


class VGG(nn.Module):
    def __init__(self, features):
        super(VGG, self).__init__()
        self.features = features
        self.layer_name_mapping = {
            '3': "relu1_2",
            '8': "relu2_2",
            '15': "relu3_3",
            '22': "relu4_3"
        }
        for p in self.parameters():
            p.requires_grad = False
    def forward(self, x):
        outs = []
        for name, module in self.features._modules.items():
            x = module(x)
            if name in self.layer_name_mapping:
                outs.append(x)
        return outs

class MyConv2D(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1):
        super(MyConv2D, self).__init__()
        self.weight = torch.zeros((out_channels, in_channels, kernel_size, kernel_size)).to(device)
        self.bias = torch.zeros(out_channels).to(device)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = (kernel_size, kernel_size)
        self.stride = (stride, stride)
    def forward(self, x):
        return F.conv2d(x, self.weight, self.bias, self.stride)
    def extra_repr(self):
        s = ('{in_channels}, {out_channels}, kernel_size={kernel_size}'
             ', stride={stride}')
        return s.format(**self.__dict__)

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv = nn.Sequential(
            *ConvLayer(channels, channels, kernel_size=3, stride=1), 
            *ConvLayer(channels, channels, kernel_size=3, stride=1, relu=False)
        )
    def forward(self, x):
        return self.conv(x) + x

def ConvLayer(in_channels, out_channels, kernel_size=3, stride=1, 
    upsample=None, instance_norm=True, relu=True, trainable=False):
    layers = []
    if upsample:
        layers.append(nn.Upsample(mode='nearest', scale_factor=upsample))
    layers.append(nn.ReflectionPad2d(kernel_size // 2))
    layers.append(nn.Conv2d(in_channels, out_channels, kernel_size, stride))
    if instance_norm:
        layers.append(nn.InstanceNorm2d(out_channels))
    if relu:
        layers.append(nn.ReLU())
    return layers

class TransformNet(nn.Module):
    def __init__(self, base=32):
        super(TransformNet, self).__init__()
        self.downsampling = nn.Sequential(
            *ConvLayer(3, base, kernel_size=9), 
            *ConvLayer(base, base*2, kernel_size=3, stride=2), 
            *ConvLayer(base*2, base*4, kernel_size=3, stride=2), 
        )
        self.residuals = nn.Sequential(*[ResidualBlock(base*4) for i in range(5)])
        self.upsampling = nn.Sequential(
            *ConvLayer(base*4, base*2, kernel_size=3, upsample=2),
            *ConvLayer(base*2, base, kernel_size=3, upsample=2),
            *ConvLayer(base, 3, kernel_size=9, instance_norm=False, relu=False),
        )
    
    def forward(self, X):
        y = self.downsampling(X)
        y = self.residuals(y)
        y = self.upsampling(y)
        return y

cnn_normalization_mean = [0.485, 0.456, 0.406]
cnn_normalization_std = [0.229, 0.224, 0.225]
tensor_normalizer = transforms.Normalize(mean=cnn_normalization_mean, std=cnn_normalization_std)
epsilon = 1e-5

def preprocess_image(image, target_width=None):
    if target_width:
        t = transforms.Compose([
            transforms.Resize(target_width), 
            transforms.CenterCrop(target_width), 
            transforms.ToTensor(), 
            tensor_normalizer, 
        ])
    else:
        t = transforms.Compose([
            transforms.ToTensor(), 
            tensor_normalizer, 
        ])
    return t(image).unsqueeze(0)

def read_image(path, target_width=None):
    image = Image.open(path)
    return preprocess_image(image, target_width)

def recover_image(tensor):
    image = tensor.detach().cpu().numpy()
    image = image * np.array(cnn_normalization_std).reshape((1, 3, 1, 1)) + \
    np.array(cnn_normalization_mean).reshape((1, 3, 1, 1))
    return (image.transpose(0, 2, 3, 1) * 255.).clip(0, 255).astype(np.uint8)[0]

def recover_tensor(tensor):
    m = torch.tensor(cnn_normalization_mean).view(1, 3, 1, 1).to(tensor.device)
    s = torch.tensor(cnn_normalization_std).view(1, 3, 1, 1).to(tensor.device)
    tensor = tensor * s + m
    return tensor.clamp(0, 1)

width = 256
model_base = 32

input_path = '../test/input/'
output_path = '../test/output/'

parser = argparse.ArgumentParser()
parser.add_argument('model_name')
parser.add_argument('mode', default='once', choices=['once','continued'])
parser.add_argument('input_path', nargs='?', default=input_path)
parser.add_argument('output_path', nargs='?', default=output_path)
args = parser.parse_args()
model_name = args.model_name
mode = args.mode
input_path = args.input_path
output_path = args.output_path

start_time = time.time()
if 'net' in model_name: # using state_dict
    transform_net = TransformNet(model_base).to("cpu")
    transform_net.load_state_dict(torch.load(model_name))
else: # using model
    transform_net = torch.load(model_name)
transform_net.train(False)
print('Net load ok, cost %s seconds.' % (time.time() - start_time))

if mode=='continued':
    done_files = set()
    wait_queue = Queue()
    while True:
        for f in listdir(input_path):
            if isfile(join(input_path, f)) and f not in done_files:
                done_files.add(f)
                wait_queue.put(f)
        while not wait_queue.empty():
            file = wait_queue.get()
            try:
                input_img = preprocess_image(Image.open(input_path+file), width)
            except Exception as e:
                print(f'Image.open("{file}") failed: {e}')
                continue
            output = transform_net(input_img)
            print(f'Transform {file} ok.')
            try:
                output_img = Image.fromarray(recover_image(output.detach()), 'RGB')
                output_img.save(output_path+file, quality=100)
            except Exception as e:
                print(f'Failed when saving {file}')
                continue
        time.sleep(0.2)
else:
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    if not files:
        print('Found no file in',input_path,'. Please check.')
        exit(0)
    start_time = time.time()
    for file in files:
        input_img = preprocess_image(Image.open(input_path+file), width)
        output = transform_net(input_img)
        print(f'Transform {file} ok.')

        output_img = Image.fromarray(recover_image(output.detach()), 'RGB')
        output_img.save(output_path+file, quality=100)
    print("Successful done %d files, cost %s seconds." % (len(files), time.time() - start_time))

