import itertools

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import scipy.ndimage
from skimage.transform import downscale_local_mean
import plotly.express as px


def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0 / (pl_entries - 1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k * h)[:3]) * 255))
        pl_colorscale.append([k * h, 'rgb' + str((C[0], C[1], C[2]))])

    return pl_colorscale

def plotly_surface_plot_from_above(gray, colorname):
    xyz = gray.shape

    terrain_cmap = plt.cm.get_cmap(colorname)

    terrain = matplotlib_to_plotly(terrain_cmap, 255)

    fig = go.Figure(data=[go.Surface(showscale=False,colorscale=terrain, z=gray)])

    scene = dict(camera=dict(up=dict(x=0., y=1, z=0), eye=dict(x=0., y=0., z=1.8)),
                 # the default values are 1.25, 1.25, 1.25
                 xaxis=dict(showgrid=False, visible=False),
                 yaxis=dict(showgrid=False, visible=False),
                 zaxis=dict(showgrid=False, visible=False),
                 aspectmode='manual',  # this string can be 'data', 'cube', 'auto', 'manual'
                 # a custom aspectratio is defined as follows:
                 aspectratio=dict(x=xyz[1] / max(xyz[0], xyz[1]), y=xyz[0] / max(xyz[0], xyz[1]), z=np.max(gray))
                 )

    fig.update_layout(scene=scene)
    fig.update_traces(contours_z=dict(show=False, usecolormap=True,
                                      highlightcolor="limegreen", project_z=True))

    fig.update_scenes(yaxis_autorange="reversed")

    return fig


def plotly_surface_plot_isometric(gray, colorname):
    xyz = gray.shape

    terrain_cmap = plt.cm.get_cmap(colorname)

    terrain = matplotlib_to_plotly(terrain_cmap, 255)

    fig = go.Figure(data=[go.Surface(colorscale=terrain, z=gray, showscale=False)])

    scene = dict(
                 # the default values are 1.25, 1.25, 1.25
                 xaxis=dict(showgrid=False, visible=False),
                 yaxis=dict(showgrid=False, visible=False),
                 zaxis=dict(showgrid=False, visible=False),
                 aspectmode='manual',  # this string can be 'data', 'cube', 'auto', 'manual'
                 # a custom aspectratio is defined as follows:
                 aspectratio=dict(x=xyz[1] / max(xyz[0], xyz[1]), y=xyz[0] / max(xyz[0], xyz[1]), z=np.max(gray))
                 )

    fig.update_layout(scene=scene)
    fig.update_traces(contours_z=dict(show=False, usecolormap=True,
                                      highlightcolor="limegreen", project_z=True))

    fig.update_scenes(xaxis_autorange="reversed")

    return fig

def plotly_contour_lines(gray, colorname):
    terrain_cmap = plt.cm.get_cmap(colorname)

    terrain = matplotlib_to_plotly(terrain_cmap, 255)

    layout = go.Layout(xaxis=dict(showgrid=False, visible=False, constrain="domain"),
                       yaxis=dict(showgrid=False, visible=False, scaleanchor="x", scaleratio=1))

    fig = go.Figure(data=
    go.Contour(
        z=gray,
        colorscale=terrain,
        showscale=False,
        # contours=dict(start=0,end=1,size=0.1,),
    ), layout=layout)

    fig.update_yaxes(autorange="reversed")

    return fig


def plotly_whole_process(gray, colorname, sigma=8):
    xyz = gray.shape

    terrain_cmap = plt.cm.get_cmap(colorname)

    terrain = matplotlib_to_plotly(terrain_cmap, 255)

    gray_cmap = plt.cm.get_cmap('gray')

    gray_color = matplotlib_to_plotly(gray_cmap, 255)

    surf1 = dict(type='surface',  # the initial surface,
                 z=np.zeros_like(gray),
                 surfacecolor=gray,
                 showscale=False,
                 colorscale=gray_color)

    # Black values become 1 and white ones 0
    gray = 1 - gray

    surf2 = dict(type='surface',  # the initial surface,
                 z=np.zeros_like(gray) + 1,
                 surfacecolor=gray,
                 showscale=False,
                 colorscale=gray_color)

    gray = scipy.ndimage.filters.gaussian_filter(gray, sigma)

    surf3 = dict(type='surface',  # the initial surface,
                 z=np.zeros_like(gray) + 2,
                 surfacecolor=gray,
                 showscale=False,
                 colorscale=gray_color)

    cmin, cmax = np.min(0.001*gray + 3), np.max(0.001*gray + 3)
    step = (cmax - cmin) / 15
    surfcolor = np.array([[int((y - cmin) / step) * step + cmin for y in x] for x in (0.001*gray + 3)])

    surf4 = dict(type='surface',  # the initial surface,
                 contours={
                     "z": {"show": True, "width": 1, "color": 'black', "start": cmin, "end": cmax, "size": step}
                 },
                 z=0.001*gray + 3,
                 surfacecolor=surfcolor,
                 showscale=False,
                 colorscale=terrain)

    surf5 = dict(type='surface',  # the initial surface,
                 z=gray + 4,
                 colorscale=terrain,
                 showscale=False)

    scene = dict(
        # the default values are 1.25, 1.25, 1.25
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        zaxis=dict(showgrid=False, visible=False),
        aspectmode='manual',  # this string can be 'data', 'cube', 'auto', 'manual'
        # a custom aspectratio is defined as follows:
        aspectratio=dict(x=xyz[1] / max(xyz[0], xyz[1]), y=xyz[0] / max(xyz[0], xyz[1]), z=1)
    )

    fig = go.Figure(data=[surf1, surf2, surf3, surf4, surf5])

    fig.update_layout(scene=scene)

    fig.update_scenes(xaxis_autorange="reversed")

    return fig


def plotly_imshow_plain_figure_gray(img):
    fig = px.imshow(img, color_continuous_scale=px.colors.sequential.gray)
    fig.update(layout_coloraxis_showscale=False)
    scene = dict(
        xaxis=dict(showgrid=False, visible=False, zeroline= False),
        yaxis=dict(showgrid=False, visible=False, zeroline= False),
    )
    fig.update_layout(scene=scene)
    return fig


def plotly_imshow_plain_figure(img):
    if len(img.shape) == 3:
        img = rgb2gray(img)

    if np.max(img) > 1:
        img = img / 255

    fig = px.imshow(img, color_continuous_scale=px.colors.sequential.gray)
    fig.update(layout_coloraxis_showscale=False)
    fig.update(layout_scene_xaxis_visible=False)
    scene = dict(
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
    )
    fig.update_layout(scene=scene)
    return fig

def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def generate_process(img):
    if len(img.shape) == 3:
        gray = rgb2gray(img)
    elif len(img.shape) == 2:
        gray = img

    if np.max(img) > 1:
        gray = gray / 255

    gray = 1 - gray
    resolution_x = max(gray.shape[0] // 400, 1)
    resolution_y = max(gray.shape[1] // 400, 1)
    gray = downscale_local_mean(gray, (resolution_x, resolution_y))
    gray = scipy.ndimage.filters.gaussian_filter(gray, 3)
    return gray