#!/usr/bin/env python

"""
This is a heavily modified version of the matplotlib's example poly_editor.py
which can be found here: http://matplotlib.org/examples/event_handling/poly_editor.html.
This example visually demonstrates the poly_decomp library.

#TODO Fix the i, d, and t commands
#TODO Blue polygon has left over lines and vertices after decomposing and moving
#TODO Enable dragging of entire polygon instead of just vertices

"""
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment
import poly_decomp as pd


class PolygonInteractor(object):
    """
    An polygon editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them

      'd' delete the vertex under point

      'i' insert a vertex at point.  You must be within epsilon of the
          line connecting two existing vertices

      'b' decompose currently selected polygon

    """

    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, ax, polys):
        self.polys = []
        self.lines = []
        self.ax = ax
        self._ind = None
        self._polyind = None

        # register all polygons
        for poly in polys:
            self.register_new_polygon(poly)

    def register_new_polygon(self, poly):
            self.ax.add_patch(poly)
            if poly.figure is None:
                raise RuntimeError('You must first add the polygon to a figure or canvas before defining the interactor')
            canvas = poly.figure.canvas
            x, y = zip(*poly.xy)
            line = Line2D(x, y, marker='o', markerfacecolor='r', animated=True)
            self.lines.append(line)
            self.ax.add_line(line)
            #self._update_line(poly)

            cid = poly.add_callback(self.poly_changed)

            canvas.mpl_connect('draw_event', self.draw_callback)
            canvas.mpl_connect('button_press_event', self.button_press_callback)
            canvas.mpl_connect('key_press_event', self.key_press_callback)
            canvas.mpl_connect('button_release_event', self.button_release_callback)
            canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
            self.canvas = canvas

            self.polys.append(poly)

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        for poly in self.polys:
            self.ax.draw_artist(poly)
        for line in self.lines:
            self.ax.draw_artist(line)
        self.canvas.blit(self.ax.bbox)

    def poly_changed(self, poly):
        'this method is called whenever the polygon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        Artist.update_from(self.line, poly)
        self.line.set_visible(vis)  # don't use the poly visibility state

    def get_ind_under_point(self, event):
        'get the index of the polygon and vertex under point if within epsilon tolerance'

        # display coords
        for index, poly in enumerate(self.polys):
            xy = np.asarray(poly.xy)
            xyt = poly.get_transform().transform(xy)
            xt, yt = xyt[:, 0], xyt[:, 1]
            d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
            indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
            ind = indseq[0]
            polyind = index

            if d[ind] >= self.epsilon:
                ind = None
            else:
                break

        return polyind, ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._polyind, self._ind = self.get_ind_under_point(event)
        print "selected polygon #%s, vertex #%s" % (self._polyind, self._ind)

        self.press_location = event

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts:
            return
        if event.button != 1:
            return
        #self._ind = None

    def key_press_callback(self, event):
        'whenever a key is pressed'
        if not event.inaxes:
            return
        if event.key == 't':
            self.showverts = not self.showverts
            self.line.set_visible(self.showverts)
            if not self.showverts:
                self._ind = None
        elif event.key == 'd':
            polyind, ind = self.get_ind_under_point(event)
            if ind is not None:
                self.poly.xy = [tup for i, tup in enumerate(self.poly.xy) if i != ind]
                self.line.set_data(zip(*self.poly.xy))
        elif event.key == 'i':
            xys = self.poly.get_transform().transform(self.poly.xy)
            p = event.x, event.y  # display coords
            for i in range(len(xys) - 1):
                s0 = xys[i]
                s1 = xys[i + 1]
                d = dist_point_to_segment(p, s0, s1)
                if d <= self.epsilon:
                    self.poly.xy = np.array(
                        list(self.poly.xy[:i]) +
                        [(event.xdata, event.ydata)] +
                        list(self.poly.xy[i:]))
                    self.line.set_data(zip(*self.poly.xy))
                    break
        elif event.key == 'b':
            if self._polyind is None or self._ind is None:
                return 

            print "Decomposing polygon # %s" % self._polyind

            decomposed = pd.polygonDecomp(self.polys[self._polyind].xy.tolist())
            for poly in decomposed:
                # import pdb
                # pdb.set_trace()
                self.register_new_polygon(Polygon(poly, color=self.polys[self._polyind].get_fc()))

            #self.polys[self._polyind].remove()
            self.ax.clear()
            del self.polys[self._polyind]
            del self.lines[self._ind]

        self.canvas.draw()

    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts:
            return
        if self._polyind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        # move poly itself
        if self._ind is None:
            self.polys[self._polyind].get_transform().transform()
            delta = (event.xdata - self.press_location.x, event.ydata - self.press_location.y)
            self.polys[self._polyind].xy += np.array(delta)

        # move vertex of poly
        else:
            x, y = event.xdata, event.ydata
            self.polys[self._polyind].xy[self._ind] = x, y
            if self._ind == 0:
                self.polys[self._polyind].xy[-1] = x, y
            elif self._ind == len(self.polys[self._polyind].xy) - 1:
                self.polys[self._polyind].xy[0] = x, y

        self.lines[self._polyind].set_data(zip(*self.polys[self._polyind].xy))
        self.canvas.restore_region(self.background)
        for i in xrange(0, len(self.polys)):
            self.ax.draw_artist(self.polys[i])
            self.ax.draw_artist(self.lines[i])
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    polys = []

    xs = [0, 5, 5, 2.5, 0]
    ys = [0, 0, 5, 2.5, 5]
    poly = Polygon(list(zip(xs, ys)), animated=True, color='blue')
    polys.append(poly)

    xs = [0, -5, -5, -2.5, 0]
    ys = [0, 0, -5, -2.5, -5]
    poly = Polygon(list(zip(xs, ys)), animated=True, color='red')
    polys.append(poly)

    fig, ax = plt.subplots()
    p = PolygonInteractor(ax, polys)

    #ax.add_line(p.line)
    ax.set_title('Click and drag a point to move it')
    ax.set_xlim((-10, 10))
    ax.set_ylim((-10, 10))
    plt.show()
