"""Original scalar reverse-mode engine. Run with Python 3; no dependencies."""
import math


class Value:
    def __init__(self, data, parents=()):
        self.data = float(data)
        self.grad = 0.0
        self.parents = parents
        self._backward = lambda: None

    @staticmethod
    def wrap(x):
        return x if isinstance(x, Value) else Value(x)

    def __add__(self, other):
        other = self.wrap(other)
        out = Value(self.data + other.data, (self, other))

        def backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = backward
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = self.wrap(other)
        out = Value(self.data * other.data, (self, other))

        def backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = backward
        return out

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-self.wrap(other))

    def __pow__(self, power):
        if not isinstance(power, (int, float)):
            raise TypeError("This engine supports constant numeric exponents.")
        out = Value(self.data ** power, (self,))

        def backward():
            self.grad += power * self.data ** (power - 1) * out.grad

        out._backward = backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,))

        def backward():
            self.grad += (1 - t * t) * out.grad

        out._backward = backward
        return out

    def backward(self):
        order, seen = [], set()

        def visit(node):
            if node in seen:
                return
            seen.add(node)
            for parent in node.parents:
                visit(parent)
            order.append(node)

        visit(self)
        for node in order:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(order):
            node._backward()


def checks():
    for point in [-2.0, -0.3, 0.7, 2.0]:
        x = Value(point)
        loss = (x * x + 3 * x).tanh()
        loss.backward()
        h = 1e-6
        f = lambda z: math.tanh(z * z + 3 * z)
        numerical = (f(point + h) - f(point - h)) / (2 * h)
        assert math.isclose(x.grad, numerical, abs_tol=1e-8)
    x = Value(2)
    loss = x * x + x
    loss.backward()
    assert x.grad == 5
    loss.backward()
    assert x.grad == 5
    w = Value(-1)
    initial = (w.data - 3) ** 2
    for _ in range(80):
        loss = (w - 3) ** 2
        loss.backward()
        w.data -= 0.1 * w.grad
    final = (w.data - 3) ** 2
    assert final < 1e-12
    return {"gradient_checks": 6, "initial_loss": initial,
            "final_loss": final, "learned_parameter": w.data}


if __name__ == "__main__":
    print(checks())
