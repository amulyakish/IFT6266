__author__ = 'Vincent Archambault-Bouffard'


import theano
print theano.config.device

train = """!obj:pylearn2.train.Train {
    dataset: &train !obj:pylearn2.datasets.mnist.MNIST {
        which_set: 'train',
        one_hot: 1,
        start: 0,
        stop: 50000
    },
    model: !obj:pylearn2.models.mlp.MLP {
        layers: [
                 !obj:pylearn2.models.mlp.SoftmaxPool {
                     layer_name: 'h0',
                     detector_layer_dim: 500,
                     pool_size: 1,
                     sparse_init: 15,
                 }, !obj:pylearn2.models.mlp.Softmax {
                     layer_name: 'y',
                     n_classes: 10,
                     irange: 0.
                 }
                ],
        nvis: 784,
    },
    algorithm: !obj:pylearn2.training_algorithms.bgd.BGD {
        batch_size: 10000,
        line_search_mode: 'exhaustive',
        conjugate: 1,
        updates_per_batch: 10,
        monitoring_dataset:
            {
                'train' : *train,
                'valid' : !obj:pylearn2.datasets.mnist.MNIST {
                              which_set: 'train',
                              one_hot: 1,
                              start: 50000,
                              stop:  60000
                          },
                'test'  : !obj:pylearn2.datasets.mnist.MNIST {
                              which_set: 'test',
                              one_hot: 1,
                          }
            },
        cost: !obj:pylearn2.costs.cost.MethodCost {
                method: 'cost_from_X',
                supervised: 1
        },
        termination_criterion: !obj:pylearn2.termination_criteria.MonitorBased {
            channel_name: "valid_y_misclass"
        }
    },
    extensions: [
        !obj:pylearn2.train_extensions.best_params.MonitorBasedSaveBest {
             channel_name: 'valid_y_misclass',
             save_path: "mlp_best.pkl"
        },
    ]
}"""