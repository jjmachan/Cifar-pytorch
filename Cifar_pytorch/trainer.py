# AUTOGENERATED! DO NOT EDIT! File to edit: 02_trainer.ipynb (unless otherwise specified).

__all__ = ['eval_model_accuracy', 'train']

# Cell
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

from Cifar_pytorch import dataloader

# Cell
def eval_model_accuracy(model, loader, device):
    '''
    Evaluate the model and print accuracy with the test data

    Args:
        model: torch model
        loader (DataLoader): The dataloader that loads up the training data
        device: torch.device object
    '''

    with torch.no_grad():
        total = 0
        correct = 0
        for images, labels in loader:
            outputs = model(images.to(device))
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels.to(device)).sum().item()
        print('[TEST ACCURACY]: %.3f%'%(correct * 100/total))

# Cell
def train(model, trainloader, testloader, optimizer, criterion, device, epochs):
    '''
    Trains the model with the parameters passed.

    Args:
        model : Torch model
        trainloader (DataLoader): DataLoader that is defined using the dataset we require.
        testloader (Dataloader): DataLoader for test set
        optimizer: torch.optim object with the params for the model
        criterion: the loss function that is used
        device: torch.device object that tell whether to use cuda or cpu
        epochs (int): Number of epochs to train.
    '''

    for epoch in range(epochs):
        print('[EPOCH: %3d/%3d]'%(epoch, epochs))
        running_loss = 0.0
        for  i, data in enumerate(trainloader, 0):
            image, target = data
            image = image.to(device)
            target = target.to(device)

            optimizer.zero_grad()

            output = model(image)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 500 == 499:
                running_loss /= 3000
                print('loss: %.3f'%(running_loss))
                running_loss = 0.0

        # Evaluate the model accuracy with the test set after every epoch
        eval_model_accuracy(model=model, loader=testloader, device=device)