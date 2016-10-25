#!/usr/bin/env python

from poly_decomp import poly_decomp

line1 = [[0, 0],[5, 5]]
line2 = [[5, 0],[0, 5]]
line3 = [[-1, -1],[-5, -5]]
poly = [[0, 0], [5, 0], [5, 5], [2.5, 2.5], [0, 5]]

class TestPoly_Decomp:
    def test_line_intersection(self):
        assert poly_decomp.lineInt(line1, line2) == [2.5, 2.5]

    def test_no_line_intersection(self):
        assert poly_decomp.lineInt(line1, line3) == [0, 0]

    def test_line_segments_intersect(self):
        assert poly_decomp.lineSegmentsIntersect(line1[0], line1[1], line2[0], line2[1]) == True

    def test_no_line_segments_intersect(self):
        assert poly_decomp.lineSegmentsIntersect(line1[0], line1[1], line3[0], line3[1]) == False

    def test_collinear(self):
        assert poly_decomp.collinear([0, 0], [5, 0], [10, 0]) == True

    def test_not_collinear(self):
        assert poly_decomp.collinear([0, 0], [5, 1], [10, 0]) == False

    def test_polygonAt(self):
        index = 2
        assert poly_decomp.polygonAt(poly, index) == [5, 5]

    def test_polygonAt_negative_index(self):
        index = -2
        assert poly_decomp.polygonAt(poly, index) == [2.5, 2.5]

    def test_polygonClear(self):
        poly_decomp.polygonClear(poly)
        assert len(poly) == 0

    def test_polygonAppend(self):
        source = [[0, 5], [2.5, 2.5], [5, 5], [5, 0], [0, 0]]
        poly_decomp.polygonAppend(poly, source, 0, 5)
        assert poly == source

    def test_polygonMakeCCW(self):
        poly_decomp.polygonMakeCCW(poly)
        assert poly == [[0, 0], [5, 0], [5, 5], [2.5, 2.5], [0, 5]]

    def test_polygonIsReflex(self):
        assert poly_decomp.polygonIsReflex(poly, 3) == True

    def test_not_polygonIsReflex(self):
        assert poly_decomp.polygonIsReflex(poly, 4) == False

    def test_polygonCanSee(self):
        assert poly_decomp.polygonCanSee(poly, 0, 4) == True

    def test_not_polygonCanSee(self):
        assert poly_decomp.polygonCanSee(poly, 3, 4) == False

    def test_polygonCopy(self):
        assert poly_decomp.polygonCopy(poly, 2, 3) == [[5, 5], [2.5, 2.5]]

    def test_polygonCutEdges(self):
        assert poly_decomp.polygonGetCutEdges(poly) == [[[2.5, 2.5], [0, 0]]]

    def test_polygonDecomp(self):
        assert poly_decomp.polygonDecomp(poly) == [[[0, 0], [2.5, 2.5], [0, 5]], [[0, 0], [5, 0], [5, 5], [2.5, 2.5]]]

    def test_not_polygonIsSimple(self):
        nonsimple_poly = [[0, 0], [5, 0], [0, 5], [5, 5]]
        assert poly_decomp.polygonIsSimple(nonsimple_poly) == False

    def test_polygonIsSimple(self):
        assert poly_decomp.polygonIsSimple(poly) == True

    def test_getIntersectionPoint(self):
        assert poly_decomp.getIntersectionPoint(line1[0], line1[1], line2[0], line2[1]) == [2.5, 2.5]

    def test_polygonQuickDecomp(self):
        assert poly_decomp.polygonQuickDecomp(poly) == [[[5, 0], [5, 5], [2.5, 2.5]], [[2.5, 2.5], [0, 5], [0, 0], [5, 0]]]

    def test_polygonRemoveCollinearPoints(self):
        collinear_poly = [[0, 0], [5, 0], [10, 0], [5, 5]]
        poly_decomp.polygonRemoveCollinearPoints(collinear_poly)
        assert collinear_poly == [[0, 0], [10, 0], [5, 5]]
