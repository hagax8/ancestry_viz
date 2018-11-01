import altair as alt
from altair.expr import datum, substring
from vega_datasets import data
from sys import argv
import pandas as pd
df = pd.read_csv(argv[1])

df = df.dropna(subset=['longitude', 'latitude'])

countries = alt.topo_feature(data.world_110m.url, 'countries')

selection = alt.selection_multi(fields=['population'])


brush = alt.selection_interval()
hover = selection
color = alt.condition(selection,
                      alt.Color('population:N', legend=None),
                      alt.value('#EEEEEE'))

chart = alt.Chart(countries).mark_geoshape(
    fill='#CCCCCC',
    stroke='white',
    opacity=0.4
).properties(
    width=850,
    height=850
)

chart += alt.Chart().mark_circle(size=300, stroke="black", strokeWidth=0.3).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    color=color,
    tooltip=['population', '1000G population code',
             '1000G superpopulation code']
).project(type="orthographic").transform_filter(brush).add_selection(hover)

chart_GTM = alt.Chart().mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("GTM axis 1", scale=alt.Scale(domain=[-1.0, 1.0]), axis=alt.Axis(
        ticks=False, labels=False, grid=False,
    )),
    y=alt.Y("GTM axis 2", scale=alt.Scale(domain=[-1.0, 1.0]), axis=alt.Axis(
        ticks=False, labels=False, grid=False,
    )),
    color=color,
    tooltip=['id', 'population', '1000G population code',
             '1000G superpopulation code'],
).properties(
    width=250,
    height=250,
).add_selection(brush)


minsne1 = df["t-SNE axis 1"].min()
minsne2 = df["t-SNE axis 2"].min()
maxsne1 = df["t-SNE axis 1"].max()
maxsne2 = df["t-SNE axis 2"].max()
minpca1 = df["Principal component 1"].min()
minpca2 = df["Principal component 2"].min()
maxpca1 = df["Principal component 1"].max()
maxpca2 = df["Principal component 2"].max()
chart_tSNE = alt.Chart().mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("t-SNE axis 1",
            scale=alt.Scale(domain=[minsne1, maxsne1]),
            axis=alt.Axis(ticks=False, labels=False, grid=False)),
    y=alt.Y("t-SNE axis 2",
            scale=alt.Scale(domain=[minsne2, maxsne2]),
            axis=alt.Axis(ticks=False, labels=False, grid=False)),
    color=color,
    tooltip=['id', 'population', '1000G population code',
             '1000G superpopulation code']
).properties(
    width=250,
    height=250,
).add_selection(brush)

chart_PCA = alt.Chart().mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("Principal component 1",
            scale=alt.Scale(domain=[minpca1, maxpca1]),
            axis=alt.Axis(
                ticks=False, labels=False, grid=False)),
    y=alt.Y("Principal component 2",
            scale=alt.Scale(domain=[minpca2, maxpca2]),
            axis=alt.Axis(
                ticks=False, labels=False, grid=False)),
    color=color,
    tooltip=['id', 'population', '1000G population code',
             '1000G superpopulation code']
).properties(
    width=250,
    height=250,
).add_selection(brush)

legend = alt.Chart().mark_rect().encode(
    y=alt.Y('population:N', axis=alt.Axis(orient='left', title="Populations")),
    color=color
).add_selection(
    selection
).transform_filter(brush)

hcharts = alt.hconcat(chart_GTM, chart_tSNE, chart_PCA, data=df)
chart = alt.hconcat(legend, chart, data=df)
vcharts = alt.vconcat(hcharts, chart, data=df)

vcharts.save(argv[2]+'.html')
