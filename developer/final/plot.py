"""Functions plotting results."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def attribute_support(df, attribute):
    df = df.copy()

    df = df[[attribute, 'support']]
    df['support'] = df['support'].astype(int)

    categories = df[attribute].unique()

    support = {"Attribute Level": [], "Value": [], "CI_lower": [], "CI_upper": []}
    
    for cat in categories[::-1]:
        group = df[df[attribute] == cat]
        mean = group['support'].mean()
        std_dev = group['support'].std()
        n = len(group)
        confidence_interval = 1.96 * (std_dev / (n**0.5))  # 95% confidence interval

        support["Attribute Level"].append(cat.replace('&', '<br>'))
        support["Value"].append(mean.round(2))
        support["CI_lower"].append((mean - confidence_interval).round(2))
        support["CI_upper"].append((mean + confidence_interval).round(2))

    df = pd.DataFrame(support)

    color_scale = ["rgb(173, 221, 142)", "rgb(127, 188, 65)", "rgb(78, 139, 37)", "rgb(45, 82, 21)"]

    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Attribute Level"]],
            y=[row["Value"]],
            error_y=dict(
                type='data',
                array=[row["CI_upper"] - row["Value"]],
                arrayminus=[row["Value"] - row["CI_lower"]],
                visible=True
            ),
            marker_color=color_scale[i],
            name=row["Attribute Level"]
        ))

    # Set y-axis range from 0 to 1
    fig.update_layout(yaxis_range=[0, 1], width=600, height=500)

    # Add a horizontal line at y=0.5
    fig.add_hline(y=0.5, line_dash="dash")


    fig.update_layout(barmode="group", bargap=0.6, bargroupgap=0.1)
    fig.update_layout(
        title={
            'text': "Fig 1: Support of the different phase-out strategies",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        margin=dict(l=20, r=20, t=45, b=5),
        paper_bgcolor="#EADDCA",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  # Show legend for different Attribute Levels
        xaxis_showticklabels=True,
        xaxis_title=None,
    )

    return fig


def plot_amce(model, data_info, width=1.0, plot_title="Fig 2: AMCE on support for policy attributes"):

    order = data_info['order']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']
    att_6_levels = order['att_6']

    att_levels = [att_6_levels, att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors = data_info['colors']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model.params[f'att_{6-i}_{level}'] for level in levels]
        att_standard_errors = [model.bse[f'att_{6-i}_{level}'] for level in levels]

        relative_differences = [coeff - att_coefficients[-1] for coeff in att_coefficients]

        fig.add_trace(go.Scatter(
            x=relative_differences,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors[i], thickness=1.5),
            marker=dict(color='#36454F', size=10),
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
    fig.add_shape(type="line", x0=0, x1=0, y0=att_6_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))

    # Update the layout of the error bar plot
    fig.update_layout(
        title={
            'text': plot_title,
            'x': 0.0,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        xaxis_title='AMCE on support (0-1)',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_6_levels),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[-0.5,1.0]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=80, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=1000,
        title_x=0.50,
        paper_bgcolor="#EADDCA",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig

def plot_relative_differences_grouped(model_control, model_treated, data_info, width=1.0, plot_title="Marginal Means Treated / Control"):

    order = data_info['order']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']
    att_6_levels = order['att_6']

    att_levels = [att_6_levels, att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors_control = data_info['colors_control']
    att_colors_treated = data_info['colors_treated']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data for 'control' to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model_control.params[f'att_{6-i}_{level}'] for level in levels]
        att_standard_errors = [model_control.bse[f'att_{6-i}_{level}'] for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_control[i], thickness=1.5),
            marker=dict(color='darkgray', size=10),
            orientation='h',
            showlegend=False,
            name='Control',  # Add a legend name for the control group
        ))

    # Loop through each attribute group and add the data for 'treated' to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model_treated.params[f'att_{6-i}_{level}'] for level in levels]
        att_standard_errors = [model_treated.bse[f'att_{6-i}_{level}'] for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_treated[i], thickness=1.5),
            marker=dict(color=att_colors_treated[i], size=10),  # Use different colors for treated group
            orientation='h',
            showlegend=False,
            name='Treated',  # Add a legend name for the treated group
        ))

        fig.add_shape(
            type="rect",
            x0=-1.5,  # Set a fixed value for x0, which is left side of the plot
            x1=1.5,  # Set the width of the shape to 1000 (right side of the plot)
            y0=total_levels - sum(len(l) for l in att_levels[i:]),  # Set y0 to the starting level index
            y1=total_levels - sum(len(l) for l in att_levels[i:]) + len(levels) - 1,  # Set y1 to the ending level index
            fillcolor=att_colors_treated[i],
            opacity=0.1,  # Set the opacity for a light transparent effect
            layer="below",  # Place the rectangle below the scatter plot markers
        )

    # Add a vertical line at x=0 for reference
    fig.add_shape(type="line", x0=0, x1=0, y0=att_6_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))

    # Update the layout of the error bar plot
    fig.update_layout(
        title=plot_title,
        xaxis_title='',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_6_levels),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=80, r=30, b=40, t=80),
        height=600,  # Set the height of the plot to 600 pixels
        width=1000,
        title_x=0.62,
    )

    # Show the interactive error bar plot
    return fig
