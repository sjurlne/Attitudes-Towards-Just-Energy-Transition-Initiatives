"""Functions plotting results."""

import plotly.graph_objects as go


def plot_relative_differences(model, data_info, width=1.0, plot_title="Relative Differences Standardized"):

    order = data_info['order']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']

    att_levels = [att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    # Colors for each attribute group
    att_colors = ['red', 'blue', 'green', 'orange', 'purple']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model.params[f'att_{5-i}_{level}'] for level in levels]
        att_standard_errors = [model.bse[f'att_{5-i}_{level}'] for level in levels]

        relative_differences = [coeff - att_coefficients[-1] for coeff in att_coefficients]

        fig.add_trace(go.Scatter(
            x=relative_differences,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors[i], thickness=1.5),
            marker=dict(color='darkgray', size=10),
            orientation='h',
            showlegend = False,
        ))

        fig.add_shape(
            type="rect",
            x0=-width,  # Set a fixed value for x0, which is left side of the plot
            x1=width,  # Set the width of the shape to 1000 (right side of the plot)
            y0=total_levels - sum(len(l) for l in att_levels[i:]),  # Set y0 to the starting level index
            y1=total_levels - sum(len(l) for l in att_levels[i:]) + len(levels) - 1,  # Set y1 to the ending level index
            fillcolor=att_colors[i],
            opacity=0.1,  # Set the opacity for a light transparent effect
            layer="below",  # Place the rectangle below the scatter plot markers
        )

    # Add a vertical line at x=0 for reference
    fig.add_shape(type="line", x0=0, x1=0, y0=att_5_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))

    # Update the layout of the error bar plot
    fig.update_layout(
        title=plot_title,
        xaxis_title='',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_5_levels),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=80, r=30, b=40, t=80),
        height=600,  # Set the height of the plot to 600 pixels
        width=1000,
        title_x=0.62,
    )

    # Show the interactive error bar plot
    return fig
