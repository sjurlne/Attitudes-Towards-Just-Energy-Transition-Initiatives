"""Functions plotting results."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

import plotly.graph_objs as go

# Fig 1 (Paper)
def attribute_support(df, attribute):
    df = df.copy()

    df = df[[attribute, 'support']]
    df['support'] = df['support'].astype(int)

    categories = ['Reduce2030', 'Eliminate2050', 'Eliminate2070']

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

    color_scale = ['#BF40BF', '#9F2B68', '#702963']  

    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Attribute Level"]],
            y=[row["Value"]],
            error_y=dict(
                type='data',
                array=[row["CI_upper"] - row["Value"]],
                arrayminus=[row["Value"] - row["CI_lower"]],
                visible=True
            ),
                marker=dict(
            color=color_scale[i],  # Set marker color
            size=8  # Adjust marker size if needed
            ),
            line=dict(
                color='black',  # Set line color
                width=2  # Adjust line width if needed
            ),
            name=row["Attribute Level"],
            mode='markers'  # Show lines and markers
        ))
        next_row_index = i + 1
        if next_row_index < len(df):
            next_row = df.iloc[next_row_index]
            fig.add_trace(go.Scatter(
                x=[row["Attribute Level"], next_row["Attribute Level"]],  # Provide a list of x-values
                y=[row["Value"], next_row["Value"]],  # Provide a list of y-values
                mode='lines',  # Use 'lines' mode for the line trace
                line=dict(
                    color='black',  # Set line color
                    width=0.5  # Adjust line width if needed
                ),
                showlegend=False  # Hide this trace from the legend
        ))

    # Set y-axis range from 0 to 1
    fig.update_layout(yaxis_range=[0.45, 0.8], xaxis_range=[-.25,2.25], width=600, height=500)
    fig.update_yaxes(ticksuffix = "   ")
    fig.update_xaxes(tickprefix = "<br>")
    

    # Add a horizontal line at y=0.5
    fig.add_hline(y=0.5, line_dash="dash", line=dict(color='#AFE1AF',  width=3))

    fig.add_vline(x=-0.25)

    fig.update_layout(
        title={
            'text': "  ",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        margin=dict(l=70, r=50, t=45, b=60),
        paper_bgcolor="#FFFFFF",
         xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.2)'  # Change the x-axis gridline color (black with some transparency)
        ),
        yaxis=dict(
            title={
                'text' : "% respondents supporting the policy",
                'font': {'family': 'Computer Modern'},
                },
            titlefont=dict(
            size=18  # Adjust the font size as needed
            ),
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.2)'  # Change the y-axis gridline color (black with some transparency)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  # Show legend for different Attribute Levels
        xaxis_showticklabels=True,
        xaxis_title=None,
    )

    return fig


# Fig 2 (paper)
def plot_regression(model, data_info, width=1.0, plot_title="Fig 2: on support for policy attributes"):

    order = data_info['order_reg']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']

    att_levels = [att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors = data_info['colors']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels) +  5

    # Loop through each attribute group and add the data to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model.params[f'att_{5-i}_{level}'] for level in levels] + [0] 
        att_standard_errors = [model.bse[f'att_{5-i}_{level}']*1.97 for level in levels] + [0]

        reference = ['Eliminate2070', 'NothingSoc', 'NothingEco', 'GovAlone', 'NoInterference']

        levels = levels + [reference[5-i-1]] 

        fig.add_trace(go.Scatter(
            x=att_coefficients,
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
            y0=total_levels - sum(len(l) + 1 for l in att_levels[i:]),  # Set y0 to the starting level index
            y1=total_levels - sum(len(l) + 1 for l in att_levels[i:]) + len(levels) -1,  # Set y1 to the ending level index
            fillcolor=att_colors[i],
            opacity=0.1,  # Set the opacity for a light transparent effect
            layer="below",  # Place the rectangle below the scatter plot markers
        )
    
    att_1_levels = att_1_levels + [reference[0]]
    att_2_levels = att_2_levels + [reference[1]]
    att_3_levels = att_3_levels + [reference[2]] 
    att_4_levels = att_4_levels + [reference[3]] 
    att_5_levels = att_5_levels + [reference[4]]

    # Add a vertical line at x=0 for reference
    fig.add_shape(type="line", x0=0, x1=0, y0=att_5_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))
    fig.add_vline(x=-0.05)

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
        yaxis=dict(categoryorder='array', categoryarray=att_5_levels, tickfont=dict(size=16)),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[-0.05,0.15]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=90, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=550,
        title_x=0.50,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig

# Fig 3 (Paper)
def plot_MM(MM_data, data_info, width=1.0, plot_title="Fig 3: Marginal Means on support for policy attributes"):

    order = data_info['order_mm']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']

    att_levels = [att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors = data_info['colors']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [MM_data.iloc[0][f'att_{5-i}_{level}_MM'] for level in levels]
        att_standard_errors = [MM_data.iloc[1][f'att_{5-i}_{level}_MM']*1.97 for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
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
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=att_5_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))
    fig.add_vline(x=0.4)

    # Update the layout of the error bar plot
    fig.update_layout(
        title={
            'text': plot_title,
            'x': 0.0,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        xaxis_title='MM on support (0-1)',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_5_levels, tickfont=dict(size=16)),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[0.4,0.8]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=90, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=550,
        title_x=0.50,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig

# Fig 4.1 / 5.1
# Group AMCE

def plot_AMCE_group(model_control, model_treated, data_info, group1, group2, width=1.0, plot_title="Marginal Means Treated / Control"):


    nobs_light = model_control.nobs /12
    nobs_dark = model_treated.nobs /12

    order = data_info['order_reg']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']

    att_levels = [att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors_control = data_info['colors_control']
    att_colors_treated = data_info['colors_treated']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels) +  5

    # Loop through each attribute group and add the data for 'control' to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model_control.params[f'att_{5-i}_{level}'] for level in levels] + [0] 
        att_standard_errors = [model_control.bse[f'att_{5-i}_{level}']*1.97 for level in levels] + [0]

        reference = ['Eliminate2070', 'NothingSoc', 'NothingEco', 'GovAlone', 'NoInterference']

        levels = levels + [reference[5-i-1]] 

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_control[i], thickness=1.5),
            marker=dict(color=att_colors_control[i], size=8),
            orientation='h',
            showlegend = False,
        ))
        

     # Loop through each attribute group and add the data to the plot
    for i, levels in enumerate(att_levels):
        att_coefficients = [model_treated.params[f'att_{5-i}_{level}'] for level in levels] + [0] 
        att_standard_errors = [model_treated.bse[f'att_{5-i}_{level}']*1.97 for level in levels] + [0]

        reference = ['Eliminate2070', 'NothingSoc', 'NothingEco', 'GovAlone', 'NoInterference']

        levels = levels + [reference[5-i-1]] 

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_treated[i], thickness=1.5),
            marker=dict(color=att_colors_treated[i], size=8),
            orientation='h',
            showlegend = False,
        ))

        fig.add_shape(
            type="rect",
            x0=-width,  # Set a fixed value for x0, which is left side of the plot
            x1=width,  # Set the width of the shape to 1000 (right side of the plot)
            y0=total_levels - sum(len(l) + 1 for l in att_levels[i:]),  # Set y0 to the starting level index
            y1=total_levels - sum(len(l) + 1 for l in att_levels[i:]) + len(levels) -1,  # Set y1 to the ending level index
            fillcolor=att_colors_treated[i],
            opacity=0.1,  # Set the opacity for a light transparent effect
            layer="below",  # Place the rectangle below the scatter plot markers
        )

    # Add a vertical line at x=0 for reference
    fig.add_shape(type="line", x0=0, x1=0, y0=att_5_levels[0], y1='Eliminate2070', line=dict(color="gray", width=1))
    fig.add_vline(x=-0.05)

    fig.add_annotation(
                x=0.05,  # X-coordinate for the annotation (adjust as needed)
                y=21.0,  # Y-coordinate for the annotation (above the plot)
                text=f"{group1} (lighter): n={int(nobs_light)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )
    fig.add_annotation(
                x=0.05,  # X-coordinate for the annotation (adjust as needed)
                y=22.0,  # Y-coordinate for the annotation (above the plot)
                text=f"{group2} (darker): n={int(nobs_dark)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )

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
        yaxis=dict(categoryorder='array', categoryarray=att_5_levels, tickfont=dict(size=16)),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[-0.05,0.20]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=90, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=550,
        title_x=0.50,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig

# Fig 4.2 / 5.2

def plot_MM_group(model_control, model_treated, data_info, group1, group2, width=1.0, plot_title="Marginal Means Treated / Control"):


    nobs_light = model_control.iloc[2,1] 
    nobs_dark = model_treated.iloc[2,1] 

    order = data_info['order_mm']
    att_1_levels = order['att_1']
    att_2_levels = order['att_2']
    att_3_levels = order['att_3']
    att_4_levels = order['att_4']
    att_5_levels = order['att_5']

    att_levels = [att_5_levels, att_4_levels, att_3_levels, att_2_levels, att_1_levels]

    att_colors_control = data_info['colors_control']
    att_colors_treated = data_info['colors_treated']

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data for 'control' to the plot
    for i, levels in enumerate(att_levels):

        att_coefficients = [model_control.iloc[0][f'att_{5-i}_{level}_MM'] for level in levels]
        att_standard_errors = [model_control.iloc[1][f'att_{5-i}_{level}_MM']*1.97  for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_control[i], thickness=1.5),
            marker=dict(color=att_colors_control[i], size=10),
            orientation='h',
            showlegend=False,
            name='Control',  # Add a legend name for the control group
        ))
        

    # Loop through each attribute group and add the data for 'treated' to the plot
    for i, levels in enumerate(att_levels):

        att_coefficients = [model_treated.iloc[0][f'att_{5-i}_{level}_MM'] for level in levels]
        att_standard_errors = [model_treated.iloc[1][f'att_{5-i}_{level}_MM']*1.97 for level in levels]

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
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=att_5_levels[0], y1=att_1_levels[-1], line=dict(color="gray", width=1, dash='dash'))
    fig.add_vline(x=0.4)

    fig.add_annotation(
                x=0.6,  # X-coordinate for the annotation (adjust as needed)
                y=22.0,  # Y-coordinate for the annotation (above the plot)
                text=f"{group1} (lighter): n={int(nobs_light)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )
    fig.add_annotation(
                x=0.6,  # X-coordinate for the annotation (adjust as needed)
                y=21.0,  # Y-coordinate for the annotation (above the plot)
                text=f"{group2} (darker): n={int(nobs_dark)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )

    # Update the layout of the error bar plot
    fig.update_layout(
        title={
            'text': plot_title,
            'x': 0.0,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        xaxis_title='MM on support (0-1)',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_5_levels, tickfont=dict(size=16)),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[0.4,0.85]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=90, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=550,
        title_x=0.50,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig



def spatial_justice_coal_state(model_control, model_treated, data_info, group1, group2, width=1.0, plot_title="Marginal Means Treated / Control"):
    

    nobs_light = model_control.iloc[2,1] 
    nobs_dark = model_treated.iloc[2,1] 

    order = data_info['order_mm']
    att_3_levels = order['att_3']

    att_levels = [att_3_levels]

    att_colors_control = '#c27e9a'
    att_colors_treated = '#a33c67'

    fig = go.Figure()

    total_levels = sum(len(levels) for levels in att_levels)

    # Loop through each attribute group and add the data for 'control' to the plot
    for i, levels in enumerate(att_levels):

        att_coefficients = [model_control.iloc[0][f'att_{3-i}_{level}_MM'] for level in levels]
        att_standard_errors = [model_control.iloc[1][f'att_{3-i}_{level}_MM']*1.97  for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_control, thickness=1.5),
            marker=dict(color=att_colors_control, size=10),
            orientation='h',
            showlegend=False,
            name='Control',  # Add a legend name for the control group
        ))
        

    # Loop through each attribute group and add the data for 'treated' to the plot
    for i, levels in enumerate(att_levels):

        att_coefficients = [model_treated.iloc[0][f'att_{3-i}_{level}_MM'] for level in levels]
        att_standard_errors = [model_treated.iloc[1][f'att_{3-i}_{level}_MM']*1.97 for level in levels]

        fig.add_trace(go.Scatter(
            x=att_coefficients,
            y=levels,
            mode='markers',
            error_x=dict(type='data', array=att_standard_errors, color=att_colors_treated, thickness=1.5),
            marker=dict(color=att_colors_treated, size=10),  # Use different colors for treated group
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
            fillcolor=att_colors_treated,
            opacity=0.1,  # Set the opacity for a light transparent effect
            layer="below",  # Place the rectangle below the scatter plot markers
        )

    # Add a vertical line at x=0 for reference
    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=att_3_levels[0], y1=att_3_levels[-1], line=dict(color="gray", width=1, dash='dash'))
    fig.add_vline(x=0.4)

    fig.add_annotation(
                x=0.6,  # X-coordinate for the annotation (adjust as needed)
                y=4.0,  # Y-coordinate for the annotation (above the plot)
                text=f"{group1} (lighter): n={int(nobs_light)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )
    fig.add_annotation(
                x=0.6,  # X-coordinate for the annotation (adjust as needed)
                y=3.5,  # Y-coordinate for the annotation (above the plot)
                text=f"{group2} (darker): n={int(nobs_dark)}",
                showarrow=False,
                font=dict(
                    family='Computer Modern',
                    size=13,
                    ),
            )

    # Update the layout of the error bar plot
    fig.update_layout(
        title={
            'text': plot_title,
            'x': 0.0,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        xaxis_title='MM on support (0-1)',
        yaxis_title='Attribute Levels',
        yaxis=dict(categoryorder='array', categoryarray=att_3_levels, tickfont=dict(size=16)),  # Set the categoryorder for y-axis based on att_1_levels
        xaxis=dict(tickformat='.2f', zeroline=False, range=[0.4,0.85]),  # Remove x-axis zeroline
        showlegend=True,  # Show legend with attribute names
        margin=dict(l=90, r=30, b=40, t=80),
        height=800,  # Set the height of the plot to 600 pixels
        width=550,
        title_x=0.50,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor='rgba(0,0,0,0)',
    ) 

    # Show the interactive error bar plot
    return fig


def attribute_support_coal_state(df, attribute):
    df = df.copy()

    df = df[[attribute, 'support']]
    df['support'] = df['support'].astype(int)

    categories = ['Reduce2030', 'Eliminate2050', 'Eliminate2070']

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

    color_scale = ['#BF40BF', '#9F2B68', '#702963']  

    fig = go.Figure()

    for i, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Attribute Level"]],
            y=[row["Value"]],
            error_y=dict(
                type='data',
                array=[row["CI_upper"] - row["Value"]],
                arrayminus=[row["Value"] - row["CI_lower"]],
                visible=True
            ),
                marker=dict(
            color=color_scale[i],  # Set marker color
            size=8  # Adjust marker size if needed
            ),
            line=dict(
                color='black',  # Set line color
                width=2  # Adjust line width if needed
            ),
            name=row["Attribute Level"],
            mode='markers'  # Show lines and markers
        ))
        next_row_index = i + 1
        if next_row_index < len(df):
            next_row = df.iloc[next_row_index]
            fig.add_trace(go.Scatter(
                x=[row["Attribute Level"], next_row["Attribute Level"]],  # Provide a list of x-values
                y=[row["Value"], next_row["Value"]],  # Provide a list of y-values
                mode='lines',  # Use 'lines' mode for the line trace
                line=dict(
                    color='black',  # Set line color
                    width=0.5  # Adjust line width if needed
                ),
                showlegend=False  # Hide this trace from the legend
        ))

    # Set y-axis range from 0 to 1
    fig.update_layout(yaxis_range=[0.45, 0.8], xaxis_range=[-.25,2.25], width=600, height=500)
    fig.update_yaxes(ticksuffix = "   ")
    fig.update_xaxes(tickprefix = "<br>")
    

    # Add a horizontal line at y=0.5
    fig.add_hline(y=0.5, line_dash="dash", line=dict(color='#AFE1AF',  width=3))

    fig.add_vline(x=-0.25)

    fig.update_layout(
        title={
            'text': "  ",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'family': 'Computer Modern'}
        },
        margin=dict(l=70, r=50, t=45, b=60),
        paper_bgcolor="#FFFFFF",
         xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.2)'  # Change the x-axis gridline color (black with some transparency)
        ),
        yaxis=dict(
            title={
                'text' : "% respondents supporting the policy",
                'font': {'family': 'Computer Modern'},
                },
            titlefont=dict(
            size=18  # Adjust the font size as needed
            ),
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.2)'  # Change the y-axis gridline color (black with some transparency)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  # Show legend for different Attribute Levels
        xaxis_showticklabels=True,
        xaxis_title=None,
    )

    return fig