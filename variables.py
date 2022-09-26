##########
#STYLES
##########

style_data_table={
    'color': 'black',
    'backgroundColor': 'white',
    'font-size': '12px',
    'textAlign': 'left',
    'whiteSpace': 'normal',
    'height': 'auto',
    }

style_data_cond_table=[{
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
    }]

style_header_table={
    'backgroundColor': '#116789',
    'color': 'white',
    'fontWeight': 'bold',
    'textAlign': 'left',
    'font-size': '15px',
    'whiteSpace': 'normal',
    'height': 'auto',
    }

#Colorblind-safe palette 
#(inspired by Fig.1 in https://personal.sron.nl/~pault/)
color_dict = {
    'blue' : 'rgba(68,119,170,1)',
    'light_blue' : 'rgba(68,119,170,0.6)',
    'cyan' : 'rgba(102,204,238,1)',
    'light_cyan' : 'rgba(102,204,238,0.6)',
    'green' : 'rgba(34,136,51,1)',
    'light_green' : 'rgba(34,136,51,0.6)',
    'yellow' : 'rgba(204,187,68,1)',
    'light_yellow' : 'rgba(204,187,68,0.6)',
    'red' : 'rgba(238,102,119,1)',
    'light_red' : 'rgba(238,102,119,0.6)',
    'purple' : 'rgba(170,51,119,1)',
    'light_purple' : 'rgba(170,51,119,0.6)',
    'grey' : 'rgba(187,187,187,1)',
    'light_grey' : 'rgba(187,187,187,0.6)',
    'black' : 'rgba(0,0,0,1)',
    'light_black' : 'rgba(0,0,0,0.5)',
    }

##########
#STORAGE PROCESSING
##########

##########
#DASHBOARD VARIABLES
##########




stylesheet_cytoscape = [
            {
            'selector': '.selected',
            'style': {
                'background-color': color_dict['light_blue'],
                'border-width': 4,
                'border-color': color_dict['blue'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.selected_unique_sample',
            'style': {
                'background-color': color_dict['light_blue'],
                'border-width': 4,
                'border-color': color_dict['purple'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.selected_unique_group',
            'style': {
                'background-color': color_dict['light_blue'],
                'border-width': 4,
                'border-color': color_dict['black'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.sample',
            'style': {
                'background-color': color_dict['light_red'],
                'border-width': 4,
                'border-color': color_dict['red'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.sample_unique_sample',
            'style': {
                'background-color': color_dict['light_red'],
                'border-width': 4,
                'border-color': color_dict['purple'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.sample_unique_group',
            'style': {
                'background-color': color_dict['light_red'],
                'border-width': 4,
                'border-color': color_dict['black'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.default',
            'style': {
                'background-color': color_dict['light_grey'],
                'border-width': 4,
                'border-color': color_dict['grey'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.default_unique_sample',
            'style': {
                'background-color': color_dict['light_grey'],
                'border-width': 4,
                'border-color': color_dict['purple'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '.default_unique_group',
            'style': {
                'background-color': color_dict['light_grey'],
                'border-width': 4,
                'border-color': color_dict['black'],
                'label': 'data(label)',
                }
        },
            {
            'selector': '[weight > 0.8]',
            'style': {
                'width': 2,
                }
        },
            {
            'selector': '[weight > 0.85]',
            'style': {
                'width': 3,
                }
        },
            {
            'selector': '[weight > 0.90]',
            'style': {
                'width': 5,
                }
        },
            {
            'selector': '[weight > 0.95]',
            'style': {
                'width': 7,
                }
        },
    ]



