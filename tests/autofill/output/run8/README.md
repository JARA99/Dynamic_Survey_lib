This run I make a movile target weight xD. Using:

```python
def w_evolution(w:np.ndarray):
    r_w = w.copy()
    for i in range(len(r_w)):
        if i%2 == 0:
            r_w[i] += np.random.normal(-0.0005,0.001,1)[0]
        else:
            r_w[i] += np.random.normal(0.0005,0.001,1)[0]
    return r_w
```
