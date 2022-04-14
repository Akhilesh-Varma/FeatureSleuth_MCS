from lib2to3.pytree import Base
import Models.model
import torch
from DataLoader import Loader
import hydra
from hydra.core.config_store  import ConfigStore
from Models.model import BaseModel, BaseModelWithSigmoid,ThreeLayerModel
from Optimization.TLoopWithExtraction import TLoopWithExtraction
from Optimization.TrainingLoop import TrainLoop
from Conf import DataConfig
from Conf.DataConfig import MNISTConfig
from Research.DataAnalysis import LoadData

cs = ConfigStore.instance()
cs.store(name="mnsit_config", node=MNISTConfig)

# This file is used to check accelerated learing process in MNIST dataset
#This file first train same model with whole dataset around 50,000 training data using simple tring in batches method
#after that training it runs the new model object on same Dataset using caching techniques
#for caching logic check file TLoopWithExtraction with method Tloop_Extraction

@hydra.main(config_path="Conf", config_name="DataConfig")
def main(cfg: MNISTConfig) -> None:
    # Load Train and Test Loader
    train_loader = Loader.Train_Loader.load_train_dataset(cfg.params.train_data_path, cfg.params.train_labels_path,
                                                          cfg.hyperparams.batch_size)
    test_loader = Loader.Test_Loader.load_test_dataset(cfg.params.test_data_path, cfg.params.test_labels_path,
                                                       cfg.hyperparams.batch_size)

    # creating model
    model = BaseModel()

    #calling Training Loop
    TrainLoop.Tloop(model,cfg.hyperparams.epochs,cfg.hyperparams.optimizer,cfg.hyperparams.learning_rate,train_loader,test_loader)
    del model

    model_new = BaseModel()
    firstlayername = "conv1"
    TLoopWithExtraction.Tloop_Extraction(model_new,15,firstlayername,cfg.hyperparams.epochs,cfg.hyperparams.optimizer,cfg.hyperparams.learning_rate,train_loader,test_loader)
    del model_new

    # # Saving model trained weights
    # path = cfg.params.pretrain_model_path
    # torch.save(model.state_dict(), path + model.__class__.__name__)
    # print('Trained model : {} saved at {path}'.format(model.__class__.__name__, path=path))


if __name__ == "__main__":
    main()
