import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

import random
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

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

class Smooth:
    # 对输入的数据进行滑动平均
    def __init__(self, windowsize=100):
        self.window_size = windowsize
        self.data = np.zeros((self.window_size, 1), dtype=np.float32)
        self.index = 0
    
    def __iadd__(self, x):
        if self.index == 0:
            self.data[:] = x
        self.data[self.index % self.window_size] = x
        self.index += 1
        return self
    
    def __float__(self):
        return float(self.data.mean())
    
    def __format__(self, f):
        return self.__float__().__format__(f)

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

def imshow(tensor, title=None):
    image = recover_image(tensor)
    print(image.shape)
    plt.imshow(image)
    if title is not None:
        plt.title(title)

def mean_std(features):
    mean_std_features = []
    for x in features:
        x = x.view(*x.shape[:2], -1)
        x = torch.cat([x.mean(-1), torch.sqrt(x.var(-1) + epsilon)], dim=-1)
        n = x.shape[0]
        x2 = x.view(n, 2, -1).transpose(2, 1).contiguous().view(n, -1) # 【mean, ..., std, ...] to [mean, std, ...]
        mean_std_features.append(x2)
    mean_std_features = torch.cat(mean_std_features, dim=-1)
    return mean_std_features

def gram_matrix(y):
    (b, ch, h, w) = y.size()
    features = y.view(b, ch, w * h)
    features_t = features.transpose(1, 2)
    gram = features.bmm(features_t) / (ch * h * w)
    return gram

def tensor_to_array(tensor):
    x = tensor.cpu().detach().numpy()
    x = (x*255).clip(0, 255).transpose(0, 2, 3, 1).astype(np.uint8)
    return x

style_path = "../style/jiangnan.png"
style_name = "jn"
style_img = read_image(style_path).to(device)
# print('style_img ', style_img)

#vgg16 = models.vgg16(pretrained=True)
#vgg16 = VGG(vgg16.features[:23]).to(device).eval()
# print('vgg16', vgg16)

batch_size = 4
width = 480
model_base = 48
verbose_batch = 1024
style_weight = 1.2e5
content_weight = 1
tv_weight = 1e-6
optimizer_step = 1e-3

def save_debug_image(style_images, content_images, transformed_images, filename):
    #style_image = Image.fromarray(recover_image(style_images))
    #content_images = [recover_image(x) for x in content_images]
    #transformed_images = [recover_image(x) for x in transformed_images]
    t = transforms.Compose([
        transforms.Resize(width), 
        transforms.CenterCrop(width)
    ])
    style_image = Image.open(style_images)
    content_images = [t(Image.open(x)) for x in content_images]
    transformed_images = [t(Image.open(x)) for x in transformed_images]
    
    new_im = Image.new('RGB', (style_image.size[0] + (width + 5) * 4, max(style_image.size[1], width*2 + 5)))
    new_im.paste(style_image, (0,0))
    
    x = style_image.size[0] + 5
    for i, (a, b) in enumerate(zip(content_images, transformed_images)):
        new_im.paste(a, (x + (width + 5) * i, 0))
        new_im.paste(b, (x + (width + 5) * i, width + 5))
    
    new_im.save(filename)

those = ["1.jpg","3.jpg","6.jpg","7.jpg"]
save_debug_image(style_path, 
    ["../test/input/"+x for x in those], 
    ["../test/output/"+x for x in those],
    "../bis.jpg")
exit(0)

data_transform = transforms.Compose([
    transforms.Resize(width), 
    transforms.CenterCrop(width), 
    transforms.ToTensor(), 
    tensor_normalizer, 
])

dataset = torchvision.datasets.ImageFolder('../dataset/', transform=data_transform)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)
print('Dataset: ',dataset)

style_features = vgg16(style_img)
style_grams = [gram_matrix(x).detach() for x in style_features]
print('Gram: ',[x.shape for x in style_grams])

transform_net = TransformNet(model_base).to(device)
print('Transform_net: ', transform_net)

# optimizer = optim.Adam(transform_net.parameters(), optimizer_step)
optimizer = optim.Adam(transform_net.parameters(), lr=optimizer_step, eps=epsilon, amsgrad=True)
transform_net.train(True)

n_batch = len(data_loader)

for epoch in range(10):
    print('Epoch: {}'.format(epoch+1))
    smooth_content_loss = Smooth()
    smooth_style_loss = Smooth()
    smooth_tv_loss = Smooth()
    smooth_loss = Smooth()
    with tqdm(enumerate(data_loader), total=n_batch, mininterval=3) as pbar:
        for batch, (content_images, _) in pbar:
            optimizer.zero_grad()

            # 使用风格模型预测风格迁移图像
            content_images = content_images.to(device)
            transformed_images = transform_net(content_images)
            transformed_images = transformed_images.clamp(-3, 3)

            # 使用 vgg16 计算特征
            content_features = vgg16(content_images)
            transformed_features = vgg16(transformed_images)

            # content loss
            content_loss = content_weight * F.mse_loss(transformed_features[1], content_features[1])
            
            # total variation loss
            y = transformed_images
            tv_loss = tv_weight * (torch.sum(torch.abs(y[:, :, :, :-1] - y[:, :, :, 1:])) + 
            torch.sum(torch.abs(y[:, :, :-1, :] - y[:, :, 1:, :])))

            # style loss
            style_loss = 0.
            transformed_grams = [gram_matrix(x) for x in transformed_features]
            for transformed_gram, style_gram in zip(transformed_grams, style_grams):
                style_loss += style_weight * F.mse_loss(transformed_gram, 
                                                        style_gram.expand_as(transformed_gram))

            loss = style_loss + content_loss + tv_loss
            loss.backward()
            optimizer.step()

            #old_smooth_loss = float(smooth_loss)

            smooth_content_loss += content_loss.item()
            smooth_style_loss += style_loss.item()
            smooth_tv_loss += tv_loss.item()
            smooth_loss += loss.item()

            #if float(smooth_loss) > old_smooth_loss + 1:
            #    print('Loss increase found: ',old_smooth_loss,' -> ',float(smooth_loss))
            #    print("Imgs:",dataset.imgs[batch*4:batch*4+4])
            
            s = f'Content: {smooth_content_loss:.2f} '
            s += f'Style: {smooth_style_loss:.2f} '
            s += f'TV: {smooth_tv_loss:.4f} '
            s += f'Loss: {smooth_loss:.2f}'
            if batch % verbose_batch == 0:
                s = '\n' + s
                save_debug_image(style_img, content_images, transformed_images, 
                                 f"../debug/s_{epoch}_{batch}.jpg")
            pbar.set_description(s)
    torch.save(transform_net, f'model_{style_name}_epoch{epoch}_{width}x{width}_base{model_base}_step{optimizer_step}_{smooth_loss:.2f}.pth')
    