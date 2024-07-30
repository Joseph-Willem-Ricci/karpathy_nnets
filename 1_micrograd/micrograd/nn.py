import random
from .engine import Value

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []
    
class Neuron(Module):
    def __init__(self, num_inputs, nonlin=True):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(num_inputs)]
        # self.b = Value(0)
        self.b = Value(random.uniform(-1, 1))
        self.nonlin = nonlin

    def __call__(self, x):
        activation = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        out = activation.tanh()
        return out
        # return activation.relu() if self.nonlin else activation
    
    def parameters(self):
        return self.w + [self.b]
    
    def __repr__(self):
        return f"{'ReLU' if self.nonlin else 'Linear'}Neuron({len(self.w)})"
    
class Layer(Module):
    def __init__(self, num_inputs, num_outputs, **kwargs):
        self.neurons = [Neuron(num_inputs, **kwargs) for _ in range(num_outputs)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out
    
    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]
    
    def __repr__(self):
        return f"Layer of [{', '.join(str(n) for n in self.neurons)}]"

class MLP(Module):
    """Multilayer Perceptron"""
    def __init__(self, num_inputs, num_outputs):
        sz = [num_inputs] + num_outputs
        self.layers = [Layer(sz[i], sz[i+1], nonlin=1!=len(num_outputs)-1)
                       for i in range(len(num_outputs))]
    
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
    
    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"
    

# x = [2.0, 3.0, -1.0]
# n = MLP(3, [4, 4, 1])

# xs = [
#     [2.0, 3.0, -1.0],
#     [3.0, -1.0, .5],
#     [.5, 1.0, 1.0],
#     [1.0, 1.0, -1.0],
# ]
# ys = [1.0, -1.0, -1.0, 1.0]  # desired targets

# # TRAINING LOOP
# for k in range(20):

#     # forward pass
#     ypred = [n(x) for x in xs]
#     MSE = sum((yout - ygt)**2 for yout, ygt in zip(ypred, ys))
#     loss = MSE

#     # zero all gradients
#     n.zero_grad()

#     # backward pass
#     loss.backward()

#     # update
#     for p in n.parameters():
#         p.data -= p.grad * 0.05

#     print(k, loss.data)
#     # print(ypred)