from plotly.graph_objs import Scatter, Layout
import plotly
import plotly.offline as py
import numpy as np
import plotly.graph_objs as go

import plotly.graph_objects as go

postal = [2, 3, 4]
population = [4, 5, 6]
state = [6, 7, 8]
size = [100, 200, 300]
fig = go.Figure(data=go.Scatter(
    x=postal,
    y=population,
    mode='markers+lines',
    marker=dict(size=size,
                color=population,
showscale=True,
                ),
    text=state,
))

fig.show()
