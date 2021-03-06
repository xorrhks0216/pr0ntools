#!/usr/bin/env python

# http://wiki.inkscape.org/wiki/index.php/PythonEffectTutorial
# http://lxml.de/tutorial.html

import sys

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *
import Image
import StringIO
import base64
from pr0ntools.image import liner
import re
import os
import time

def set_dbg(yes):
    global pdbg
    pdbg = yes

pdbg = 0
logf = None
logf = open('ink-liner.log', 'w')
def dbg(s):
    s = 'pr0nliner-ink: %s' % str(s)
    if pdbg:
        print s
    if logf:
        logf.write('%s\n' % str(s))
    
class PathifyEffect(inkex.Effect):
    def __init__(self):
        """
        Constructor.
        Defines the "--what" option of a script.
        """
        # Call the base class constructor.
        inkex.Effect.__init__(self)
        self.layer_prefix = 'active'
        #self.layer_prefix = 'contact'

    def create_output_layer(self):
        '''
        <g
           inkscape:groupmode="layer"
           id="layer2"
           inkscape:label="ref"
           style="display:inline">
           ...
        </g>
        '''
        svg = self.document.getroot()
        # Create a new layer
        l = inkex.etree.SubElement(svg, 'g')
        l.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        # let ID get auto-generated by inkscape
        l.set(inkex.addNS('label', 'inkscape'), 'output')
        # Visible by default
        l.set(inkex.addNS('style'), 'display:inline')
        self.output_layer = l

    def effect(self):
        start = time.time()
        self.create_output_layer()
        if 0:
            polygon = [(62.857143,71.428571), (114.285717,0), (0,312.857139), (-114.285717,0)]
            self.add_polygon(polygon)
        #self.show_image()
        i = self.get_image()
        fn = '/tmp/ink-pr0nliner.jpg'
        i.save(fn)
        for line in self.get_lines():
            dbg('Checking line (%ux, %uy)-(%ux, %uy)' % (line[0][0], line[0][1], line[1][0], line[1][1]))
            self.check_poly(line)
            self.check_poly(self.get_ref_polygon())
            l = liner.liner(fn, self.svg2cvpoly(line), self.svg2cvpoly(self.get_ref_polygon()), show=0)
            self.add_polygon(l)
        end = time.time()
        dbg('Plugin delta: %0.3f sec' % (end - start,))
        if pdbg:
            print 'Debug break'
            sys.exit(1)
    
    def check_poly(self, polygon):
        '''Throw exception if polygon goes out of bounds'''
        for (x, y) in polygon:
            if x < 0 or x >= self.width():
                dbg('')
                dbg('Polygon check failure')
                dbg('Polygon: %s' % polygon)
                dbg('Bad coords: (%f, %f)' % (x, y))
                dbg('Width: %d' % self.width())
                raise Exception('X out of bounds')
            if y < 0 or y >= self.height():
                dbg('')
                dbg('Polygon check failure')
                dbg('Polygon: %s' % polygon)
                dbg('Bad coords: (%f, %f)' % (x, y))
                dbg('Height: %d' % self.height())
                raise Exception('Y out of bounds')
    
    def width(self):
        svg = self.document.getroot()
        return inkex.unittouu(svg.get('width'))

    def height(self):
        svg = self.document.getroot()
        return inkex.unittouu(svg.attrib['height'])
        
    def svg2cvpoly(self, ink_poly):
        '''Convert Inkscape coordinate system to OpenCV coordinate system polygon'''
        '''
        OpenCV has UL origin but Inkscape has LL
        ...or maybe not
        The coordinates in the GUI don't match coordinates in the file?
        '''
        return ink_poly
        ret = []
        for (x, y) in ink_poly:
            ret.append((x, self.height() - y))
        return ret
    
    def get_layer(self, layername):
        '''Return the single layer matching layer name or throw an exception'''
        root = self.document.getroot()
        ret = []
        for e in root.findall('{%s}g' % root.nsmap['svg']):
            l = '{%s}label' % e.nsmap['inkscape']
            # Just because its a group doesn't mean its a layer
            if not l in e.attrib:
                continue
            name = e.attrib[l]
            if name != layername:
                continue
            ret.append(e)
        if len(ret) != 1:
            raise Exception("Wanted 1 layer named %s but got %d" % (layername, len(ret)))
        return ret[0]
    
    def inkns(self, elem):
        svg = self.document.getroot()
        return '{%s}%s' % (svg.nsmap['inkscape'], elem)

    def svgns(self, elem):
        svg = self.document.getroot()
        return '{%s}%s' % (svg.nsmap['svg'], elem)

    def xlinkns(self, elem):
        svg = self.document.getroot()
        return '{%s}%s' % (svg.nsmap['xlink'], elem)

    def get_ref_polygon(self):
        '''
        Eventually support more than one
        For now reject if not exactly one
        '''
        '''
        <g
           inkscape:groupmode="layer"
           id="layer6"
           inkscape:label="active-ref"
           style="display:inline">
          <rect
             style="fill:none;stroke:#ff0000;stroke-width:1.24627745;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;display:inline"
             id="rect3878"
             width="56.25"
             height="128.625"
             x="96.875"
             y="149.5" />
        </g>
        '''
        l = self.get_layer('%s-ref' % self.layer_prefix)
        
        ret = None
        rectes = l.findall(self.svgns('rect'))
        if len(rectes) != 1:
            raise Exception('Expected exactly one reference but got %d' % len(rectes))
        recte = rectes[0]
        width = float(recte.get('width'))
        height = float(recte.get('height'))
        x = float(recte.get('x'))
        y = float(recte.get('y'))
        
        return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        

    def get_lines(self):
        '''Return list of (point0, point1) where point is (x, y) tuple in input layer'''
        '''
        <path
           style="fill:#0000ff;fill-opacity:1;stroke:#ff0000;stroke-opacity:1"
           d="m 103.46821,304.91329 24.85549,0"
           id="path3843"
           inkscape:connector-curvature="0"
           transform="translate(167.57144,304.50507)" />
        '''
        l = self.get_layer('%s-in' % self.layer_prefix)
        
        # TODO: need to append this?
        # transform="translate(-167.57144,-304.50507)"
        transforme = l.get('transform')
        transforml = None
        if transforme:
            transforml = map(float, re.match('^translate\((.*),(.*)\)$', transforme).group(1, 2))
            dbg('Transform (layer): (%fx, %fy)' % (transforml[0], transforml[1]))
        
        ret = []
        for pathe in l.findall(self.svgns('path')):
            transformp = None
            transformpe = pathe.get('transform')
            if transformpe:
                transformp = map(float, re.match('^translate\((.*),(.*)\)$', transformpe).group(1, 2))
                dbg('Transform (path): (%fx, %fy)' % (transformp[0], transformp[1]))
            
            m = re.match('^m (.*),(.*) (.*),(.*)$', pathe.get('d'))
            path = map(float, map(float, m.group(*range(1, 5))))
            # Transform into list of coordinates
            path = [path[0:2], path[2:4]]
            if transforml:
                path[0] = (path[0][0] + transforml[0], path[0][1] + transforml[1])
            if transformp:
                path[0] = (path[0][0] + transformp[0], path[0][1] + transformp[1])
            # Since relative need to accumulate
            for i in xrange(1, len(path)):
                path[i] = (path[i - 1][0] + path[i][0], path[i - 1][1] + path[i][1])
            # (source, dest)
            ret.append(path)
        return ret

    def get_image(self):
        '''Return PIL image object to the source image'''
        l = self.get_layer('img')
        
        imagees = l.findall(self.svgns('image'))
        if len(imagees) != 1:
            raise Exception('Wanted layer to have exactly 1 image but got %u' % len(imagees))
        imagee = imagees[0]
        href = imagee.get(self.xlinkns('href'))
        if not href.startswith('data:image/jpeg;base64,'):
            raise Exception('not embedded jpeg')
        
        img64 = href[len('data:image/jpeg;base64,'):]
        d = base64.decodestring(img64)
        i = Image.open(StringIO.StringIO(d))
        return i

    def show_image(self):
        i = self.get_image()
        i.show()
        
    def validate_polygon(self, polygon):
        svg = self.document.getroot()
        canw = inkex.unittouu(svg.get('width'))
        canh = inkex.unittouu(svg.attrib['height'])
        if pdbg > 2:
            dbg("Canvas (%dx, %dy)" % (canw, canh))
            for (x, y) in polygon:
                dbg('  (%dx, %dy)' % (x, y))
        #os._exit(1)
        
    def add_polygon(self, polygon):
        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        self.validate_polygon(polygon)
        
        '''
        Inkscape represents paths as a special transform element + a relative path
        Why not make all absolute?
        Makes differences easier?
        wait...
            <g
            transform="translate(-167.57144,-304.50507)"
            ...
            <path
               transform="translate(167.57144,304.50507)"
       they cancel out
       
        <g
           inkscape:groupmode="layer"
           id="layer2"
           inkscape:label="ref"
           style="display:inline">
              <path
                 style="fill:#0000ff;fill-opacity:1;stroke:none;display:inline;stroke-opacity:1"
                 d="m 62.857143,71.428571 114.285717,0 0,312.857139 -114.285717,0 z"
                 id="path3013"
                 inkscape:connector-curvature="0" />
        </g>
        '''
        # TODO: rotate colors to make easier to read
        style = { 'fill':'#00ff00', 'fill-opacity':1,
                    'stroke':'none', 'stroke-opacity':1,
                    'display':'inline' }
        ms = ' '.join(['%s, %s' % (pair[0], pair[1]) for pair in polygon])
        poly_attributes = {'style':formatStyle(style),
                        'd':'M ' + ms + ' z'}
        # Above didn't put it in the svg namespace, does it matter?
        inkex.etree.SubElement(self.output_layer, inkex.addNS('path','svg'), poly_attributes )


# Create effect instance and apply it.
effect = PathifyEffect()
effect.affect()

