import plotly.express as px

def line_chart(df):
    fig = px.line(df)
    return fig

def bar_chart(df):
    fig = px.bar(df)
    return fig

def pie_chart(df):
    fig = px.pie(df)
    return fig