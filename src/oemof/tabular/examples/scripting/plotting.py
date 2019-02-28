import os

import plotly.offline as offline

from oemof.tabular.tools.plots import hourly_plot, stacked_plot
# plot results with plotly

name = "dispatch"

# results path for output
results_path = os.path.join(
    os.path.expanduser('~'),
    "oemof-results",
    name,
    "output")

offline.plot(
    hourly_plot(
        name,
        'DE',
        os.path.join(
            os.path.expanduser('~'),
            "oemof-results")
        ),
    filename=os.path.join(results_path, 'hourly-plot.html'))


# plot results with plotly
# offline.plot(
#     stacked_plot(
#         name,
#         os.path.join(
#             os.path.expanduser('~'),
#             "oemof-results")
#         ),
#     filename=os.path.join(results_path, 'stacked-plot.html'))
