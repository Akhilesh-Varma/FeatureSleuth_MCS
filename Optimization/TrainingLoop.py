from asyncore import loop
import torch
import torch.nn as nn
from ModelEvaluation.Evaluation import Evaluation
from Visualization.LossCurve import LossCurve
from tqdm import tqdm

class TrainLoop():
    def __init__(self):
        self

    def Tloop(model, epochs, optimizer, learning_rate, train_loader, test_loader, cloned_model=None,
              get_final_accuracy=True):
        # loss criteria
        loss_criterion = nn.NLLLoss()

        # selectinf type of optimizer
        if optimizer == 'ADAM':
            optimizer = torch.optim.Adam(model.parameters(), learning_rate)
        elif optimizer == 'SGD':
            optimizer = torch.optim.SGD(model.parameters(), learning_rate)

        loss_values = []
        for epoch in range(epochs):
            running_loss = 0
            batch_counter = 0
            loop = tqdm(enumerate(train_loader), total = len(train_loader), leave=True)
            for batch_idx,(images, labels) in loop:
                model.train()
                # batch_counter += 1
                # print(batch_counter)
                # forward pass
                outputs = model(images)
                # finding loss
                loss = loss_criterion(outputs, labels)
                # backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                # evaluation of model on test data
                accuracy = 0
                if (cloned_model == None):
                    accuracy = Evaluation.Eval(model, epoch, test_loader)
                else:
                    cloned_model.load_state_dict(
                        model.state_dict())  # this is recquired so that new weights are tranfered for testing
                    accuracy = Evaluation.Eval(cloned_model, epoch, test_loader)
                loop.set_description(f"Epoch[{epoch+1}/{epochs}]")
                loop.set_postfix(loss = loss.item(),accuracy=accuracy,running_loss = running_loss)
            loss_values.append(running_loss / len(train_loader))

        if(epoch+1 == epochs and get_final_accuracy):
            if (cloned_model == None):
                print("Accuracy on train set:")
                Evaluation.Eval(model, epoch, train_loader)
                print("Accuracy on test set:")
                Evaluation.Eval(model, epoch, test_loader)
            else:
                cloned_model.load_state_dict(
                    model.state_dict())  # this is recquired so that new weights are tranfered for testing
                print("Accuracy on train set:")
                Evaluation.Eval(cloned_model, epoch, train_loader)
                print("Accuracy on test set:")
                Evaluation.Eval(cloned_model, epoch, test_loader)
        # Plotting Loss Curve
        LossCurve.PlotCurve(loss_values, epochs)
