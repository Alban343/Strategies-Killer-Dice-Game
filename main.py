import pandas as pd
import numpy as np

# Visualisation des strategies de jeu +

list = [6,6,5]
i = [5, 5]

extend = (np.sum([np.sum(list) , np.sum(i)]))/(len(list) + len(i))

print(extend)