# old_helper.py

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy, scipy.stats as st
import plotly.io as pio

instances = [1, 2, 3, 4, 5]

nvec = {
    'sp' : {
        1 : 7016, 2 : 12842, 3 : 17500, 4 : 22154, 5 : 25882
    },
    'ny' : {
        1 : 4265, 2 : 7789, 3 : 10799, 4 : 13622, 5 : 16454
    }
}

algs_order = [ 
    #'rfid_dd!250_nc!2', 'rfid_dd!250_nc!5', 'rfid_dd!1000_nc!2', 
    'rfid_dd!1000_nc!5', 'rfid', 'djahel_wc!start_el!high', 
    #'djahel_wc!start_el!medium', 'djahel_wc!start_el!low', 
    'fuzzy', 'kapusta2', 'petri_lc!False', 'tpn4', 'allgreen' ]

algs_names = {
    'petri_lc!False' : 'TPN',
    #'rfid_dd!1000_nc!2' : 'RFID-100-2', 'rfid_dd!250_nc!5' : 'RFID-25-5', 
    #'rfid_dd!1000_nc!5' : 'RFID-100-5', 
    'rfid_dd!1000_nc!5' : 'RFID', 
    #'rfid_dd!250_nc!2' : 'RFID-25-2',
    'rfid' : 'RFID',
    #'djahel_wc!start_el!high' : 'Fuzzy-H', 
    'djahel_wc!start_el!high' : 'Fuzzy', 
    #'djahel_wc!start_el!medium' : 'Fuzzy-M', 'djahel_wc!start_el!low' : 'Fuzzy-L',
    'fuzzy' : 'Fuzzy',
    'kapusta2' : 'Queue based',
    'tpn4' : 'New TPN',
    'allgreen' : 'All Green'
}

evs_name = {'veh11651' : 'EV',
            'veh4856' : 'EV',
            'vehev1' : 'EV'}   

y_axis_labels = {
    'imp' : 'Time-Loss Improvement (times)',
    'perc' : 'Time-Loss Improvement (%)',
    'tl' : 'Time-Loss (s)',
    'rt' : 'Runtime (s)',
    'tl-ttt' : 'Time-Loss/Actual Travel Time (%)'
}                   

def get_values(df_sce,metric,scenario):
    x_values = [ nvec[scenario][i] for i in instances ]
    count = dict([ (i,df_sce[df_sce['instance'] == i][metric].count()) for i in instances ])
    means = dict([ (i,df_sce[df_sce['instance'] == i][metric].mean()) for i in instances ])
    std_err = dict([ (i,st.sem(df_sce[df_sce['instance'] == i][metric])) for i in instances ])
    y_errors = [ means[i]-st.t.interval(0.95, count[i]-1, loc=means[i], scale=std_err[i])[0] for i in instances ]

    return x_values, [ means[i] for i in means ], y_errors

def make_line_graph(df,scenario):
    df_sce = df[ (df['scenario'] == scenario) & (df['teleported'] == False) ]

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    x_values, means, y_errors = get_values(df_sce,'tl',scenario)

    # Add traces
    fig.add_trace(
        go.Scatter(x=x_values, y=means, name="Time-Loss (s)",
            error_y=dict(
                type='data', # value of error bar given in data coordinates
                array=y_errors,
                visible=True)
            ),
        secondary_y=False,
    )

    df_sce_copy = df_sce.copy()

    df_sce_copy['tl-ttt'] = (df_sce_copy['tl']/df_sce_copy['ttt'])*100

    x_values, means, y_errors = get_values(df_sce_copy,'tl-ttt',scenario)

    fig.add_trace(
        go.Scatter(x=x_values, y=means, name="Time-Loss/Actual Travel Time (%)",
        error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=y_errors,
            visible=True)
        ),
        secondary_y=True,
    )    

    # Add figure title
    fig.update_layout(
        title_text="No Preemption Results - {}".format(scenario)
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Number of Vehicles")

    # Set y-axes titles
    fig.update_yaxes(title_text="Time-Loss (s)", secondary_y=False)
    fig.update_yaxes(title_text="Time-Loss/Actual Travel Time (%)", secondary_y=True, range=[0,100])

    fig.show()    

def make_bar_graph(df,scenario,alg):
    df_sce = df[ (df['scenario'] == scenario) & (df['perc'].notnull()) ]
    fig = go.Figure()
    petri_alg = df_sce[df_sce['alg'].str.contains(alg)]
    alg_names = petri_alg['alg'].unique()

    for aname in algs_order:
        if aname in alg_names:
            df_alg = df_sce[df_sce['alg'] == aname]

            x_values, means, y_errors = get_values(df_alg,'perc',scenario)

            fig.add_trace(go.Bar(
                name=algs_names[aname],
                x=x_values, y=means,
                error_y=dict(type='data', array=y_errors)
            ))

    petri_df = df_sce[df_sce['alg'].str.contains('petri_lc!False')]

    x_values, means, y_errors = get_values(petri_df,'perc',scenario)

    fig.add_trace(go.Bar(
        name='TPN',
        x=x_values, y=means,
        error_y=dict(type='data', array=y_errors)
    ))

    fig.update_layout(barmode='group')
    fig.show()    

def make_boxplot_grouped(df,metric,title_label,figname,scenario, width=600, height=480):
    df = df[(df['scenario'] == scenario) & (df[metric].notnull())]
    algs = df['alg'].unique().tolist()

    fig = go.Figure()

    for alg in [alg for alg in algs_order if alg in algs]:
        complete_values = []
        xlabels = []
        for i in instances:
            tmp_df = df[(df['alg'] == alg) & (df['instance'] == i)][metric]
            values = tmp_df.nlargest(tmp_df.size-1).tolist()
            xlabels += [nvec[scenario][i]]*len(values)
            complete_values += values

        fig.add_trace(go.Box(
            y=complete_values,
            x=xlabels,
            name=algs_names[alg]
        ))

    fig.update_layout(
        yaxis_title=y_axis_labels[metric],
        xaxis_title='Number of Vehicles',
        title=title_label,
        boxmode='group',
        font=dict(
            size=14
        )
    )
    fig.show()
    pio.write_image(fig, 'figs/{}.pdf'.format(figname), format='pdf', width=width, height=height) 

def make_boxplot(df,metric,title_label,figname,scenario, width=600, height=480):
    fig = go.Figure()

    df = df[df[metric].notnull()]

    for i in instances:
        tmp_df = df[(df['alg'] == 'no-preemption') & (df['instance'] == i) & (df['scenario'] == scenario)][metric]
        fig.add_trace(go.Box(y=tmp_df.nlargest(tmp_df.size-1).tolist(), name=nvec[scenario][i]))

    fig.update_layout(
        yaxis_title=y_axis_labels[metric],
        xaxis_title='Number of Vehicles',
        title=title_label,
        font=dict(
            size=14
        )        
    )        

    fig.show()
    pio.write_image(fig, 'figs/{}.pdf'.format(figname), format='pdf', width=width, height=height)         