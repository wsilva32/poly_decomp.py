poly_decomp.py: Decompose 2D polygons into convex pieces
=========================

.. image:: https://img.shields.io/pypi/v/poly_decomp.svg
    :target: https://pypi.python.org/pypi/poly_decomp

Installation
------------

.. code-block:: bash

    $ pip install poly_decomp

Usage
------------

.. code-block:: python

    import poly_decomp as pd
    
    polygon = [[0, 0], [5, 0], [5, 5], [2.5, 2.5], [0, 5]]
    #           |\    /| 
    #           | \  / |
    #           |  \/  |
    #           |      |
    #           |------|

    print pd.polygonDecomp(polygon)
    # --> [[[0, 0], [2.5, 2.5], [0, 5]], [[0, 0], [5, 0], [5, 5], [2.5, 2.5]]]
    #           |\   /| 
    #           | \ / |
    #           |  /  |
    #           | /   |
    #           |/----|

    print pd.polygonQuickDecomp(polygon)
    # --> [[[5, 0], [5, 5], [2.5, 2.5]], [[2.5, 2.5], [0, 5], [0, 0], [5, 0]]]
    #           |\   /| 
    #           | \ / |
    #           |  \  |
    #           |   \ |
    #           |----\|

About
-----------------

Implementation based on `Schteppe's <http://steffe.se>`_ `poly-decomp.js <https://github.com/schteppe/poly-decomp.js>`_.

Algorithms based on `Mark Bayazit's <http://mpen.ca>`_ `Poly Decomp <https://mpen.ca/406/bayazit>`_.
