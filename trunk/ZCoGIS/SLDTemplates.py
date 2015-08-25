# NEW SLD TEMPLATES FOR NEW SYSTEM

# Style for a layer consists of a rule, filter, symbolizer and textsymbolizer


# for use to add named layers to this
baseSLDTemplate = """<StyledLayerDescriptor version="1.0.0">
%s
</StyledLayerDescriptor>
"""

namedLayer = """<NamedLayer>
        <Name>%s</Name>
        <UserStyle>
            <Title>LayerStyle</Title>
            <FeatureTypeStyle>                
                %s                
            </FeatureTypeStyle>
        </UserStyle>
</NamedLayer>
"""


locationNamedLayer = """<NamedLayer>
        <Name>Location</Name>
        <UserStyle>
            <Title>StyleLocation</Title>
            <FeatureTypeStyle>                
                %s                
            </FeatureTypeStyle>
        </UserStyle>
</NamedLayer>
"""

textSymbolizer = """<TextSymbolizer>
    <Geometry>
        <PropertyName>the_geom</PropertyName>
    </Geometry>
    <Label>%s</Label>
    <Font>
        <CssParameter name="font-family">times</CssParameter>
        <CssParameter name="font-style">italic</CssParameter>
        <CssParameter name="font-weight">bold</CssParameter>
        <CssParameter name="font-size">5</CssParameter>
    </Font>
    <Fill>
        <CssParameter name="fill">#FF0000</CssParameter>
    </Fill>
    <LabelPlacement>
        <PointPlacement>
            <AnchorPoint>
                <AnchorPointX>0.5</AnchorPointX>
                <AnchorPointY>0.5</AnchorPointY>
            </AnchorPoint>
            <Displacement>
                <DisplacementX>4</DisplacementX>
                <DisplacementY>4</DisplacementY>
            </Displacement>
            <Rotation>6</Rotation>
        </PointPlacement>
    </LabelPlacement>
</TextSymbolizer>
"""

pointSymbolizer = """<PointSymbolizer>
    <Geometry>
        <PropertyName>the_geom</PropertyName>
    </Geometry>
    <Graphic>
        <Mark>
            <WellKnownName>%s</WellKnownName>
            <Fill>
                <CssParameter name="fill">%s</CssParameter>                                
            </Fill>
        </Mark>
        <Size>%s</Size>
    </Graphic>
</PointSymbolizer>
"""

polygonSymbolizer = """<PolygonSymbolizer>
    <Geometry>
        <PropertyName>the_geom</PropertyName>
    </Geometry>
    <Fill>
        <CssParameter name="fill">%s</CssParameter>
    </Fill>
    <Stroke>
        <CssParameter name="stroke">%s</CssParameter>
        <CssParameter name="stroke-width">%s</CssParameter>
    </Stroke>
</PolygonSymbolizer>   
"""

# OPERATORS
equalTo = """<PropertyIsEqualTo>
    <PropertyName>%s</PropertyName>
    <Literal>%s</Literal>
</PropertyIsEqualTo>
"""

greaterThan = """<PropertyIsGreaterThan>
        <PropertyName>%s</PropertyName>
        <Literal>%s</Literal>
</PropertyIsGreaterThan>
"""

lessThan = """<PropertyIsLessThan>
        <PropertyName>%s</PropertyName>
        <Literal>%s</Literal>
</PropertyIsLessThan>
"""

notEqualTo = """<PropertyIsNotEqualTo>
    <PropertyName>%s</PropertyName>
    <Literal>%s</Literal>
</PropertyIsNotEqualTo>
"""

like = """<PropertyIsLike wildcard='*' singleChar='.' escape='!'>
    <PropertyName>%s</PropertyName>
    <Literal>%s</Literal>
</PropertyIsLike>
"""

between = """<PropertyIsBetween>
    <PropertyName>%s</PropertyName>
    <LowerBoundary>%s</LowerBoundary>
    <UpperBoundary>%s</UpperBoundary>
</PropertyIsBetween>
"""


sldPointGreaterThanTemplate = '''
<StyledLayerDescriptor version="1.0.0">    
    <NamedLayer>
        <Name>Location</Name>
        <UserStyle>
            <Title>StyleLocation</Title>
            <FeatureTypeStyle>
                <Rule>
                    <Filter>
                        <AND>
                            <PropertyIsEqualTo>
                                <PropertyName>unit</PropertyName>
                                <Literal>%s</Literal>
                            </PropertyIsEqualTo>
                            <PropertyIsGreaterThan>
                                    <PropertyName>timestamp</PropertyName>
                                    <Literal>%s</Literal>
                            </PropertyIsGreaterThan>
                        </AND>
                    </Filter>
                    <PointSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FF0000</CssParameter>                                
                                </Fill>
                            </Mark>
                            <Size>8.0</Size>
                        </Graphic>
                    </PointSymbolizer>
                    <TextSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Label>timestamp</Label>
                        <Font>
                            <CssParameter name="font-family">times</CssParameter>
                            <CssParameter name="font-style">italic</CssParameter>
                            <CssParameter name="font-weight">bold</CssParameter>
                            <CssParameter name="font-size">5</CssParameter>
                        </Font>
                        <Fill>
                            <CssParameter name="fill">#FF0000</CssParameter>
                        </Fill>
                        <LabelPlacement>
                            <PointPlacement>
                                <AnchorPoint>
                                    <AnchorPointX>0.5</AnchorPointX>
                                    <AnchorPointY>0.5</AnchorPointY>
                                </AnchorPoint>
                                <Displacement>
                                    <DisplacementX>4</DisplacementX>
                                    <DisplacementY>4</DisplacementY>
                                </Displacement>
                                <Rotation>6</Rotation>
                            </PointPlacement>
                        </LabelPlacement>
                    </TextSymbolizer>
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
    %s
</StyledLayerDescriptor>
'''


sldPointBetweenTemplate = '''
<StyledLayerDescriptor version="1.0.0">    
    <NamedLayer>
        <Name>Location</Name>
        <UserStyle>
            <Title>StyleLocation</Title>
            <FeatureTypeStyle>
                <Rule>
                    <Filter>
                        <AND>
                            <PropertyIsEqualTo>
                                <PropertyName>unit</PropertyName>
                                <Literal>%s</Literal>
                            </PropertyIsEqualTo>
                            <PropertyIsGreaterThan>
                                    <PropertyName>timestamp</PropertyName>
                                    <Literal>%s</Literal>
                            </PropertyIsGreaterThan>
                            <PropertyIsLessThan>
                                    <PropertyName>timestamp</PropertyName>
                                    <Literal>%s</Literal>
                            </PropertyIsLessThan>
                        </AND>
                    </Filter>
                    <PointSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FF0000</CssParameter>                                
                                </Fill>
                            </Mark>
                            <Size>8.0</Size>
                        </Graphic>
                    </PointSymbolizer>
                    <TextSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Label>timestamp</Label>
                        <Font>
                            <CssParameter name="font-family">times</CssParameter>
                            <CssParameter name="font-style">italic</CssParameter>
                            <CssParameter name="font-weight">bold</CssParameter>
                            <CssParameter name="font-size">5</CssParameter>
                        </Font>
                        <Fill>
                            <CssParameter name="fill">#FF0000</CssParameter>
                        </Fill>
                        <LabelPlacement>
                            <PointPlacement>
                                <AnchorPoint>
                                    <AnchorPointX>0.5</AnchorPointX>
                                    <AnchorPointY>0.5</AnchorPointY>
                                </AnchorPoint>
                                <Displacement>
                                    <DisplacementX>4</DisplacementX>
                                    <DisplacementY>4</DisplacementY>
                                </Displacement>
                                <Rotation>6</Rotation>
                            </PointPlacement>
                        </LabelPlacement>
                    </TextSymbolizer>
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
    %s
</StyledLayerDescriptor>
'''





sldLocationDisable = '''
<StyledLayerDescriptor version="1.0.0">    
    <NamedLayer>
        <Name>Location</Name>
        <UserStyle>
            <Title>StyleLocation</Title>
            <FeatureTypeStyle>
                <Rule>
                    <Filter>                       
                        <PropertyIsEqualTo>
                            <PropertyName>oid</PropertyName>
                            <Literal>-99</Literal>
                        </PropertyIsEqualTo> 
                    </Filter>
                    <PointSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FF0000</CssParameter>                                
                                </Fill>
                            </Mark>
                            <Size>8.0</Size>
                        </Graphic>
                    </PointSymbolizer>                    
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
    
    <NamedLayer>
        <Name>Zones</Name>
        <UserStyle>
            <Title>StyleGeoFence</Title>
            <FeatureTypeStyle>
                <Rule>
                    <Filter>                        
                        <PropertyIsNotEqualTo>
                            <PropertyName>oid</PropertyName>
                            <Literal>-99</Literal>
                        </PropertyIsNotEqualTo>
                    </Filter>
                    <PolygonSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Fill>
                            <CssParameter name="fill">#ff0000</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#0000ff</CssParameter>
                            <CssParameter name="stroke-width">2.0</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>                    
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>    
    
</StyledLayerDescriptor>
'''

geoFenceNamedLayer = '''
<NamedLayer>
        <Name>Zones</Name>
        <UserStyle>
            <Title>StyleZones</Title>
            <FeatureTypeStyle>
                <Rule>
                    <Filter>                        
                        <PropertyIsEqualTo>
                            <PropertyName>unit</PropertyName>
                            <Literal>%s</Literal>
                        </PropertyIsEqualTo>
                    </Filter>
                    <PolygonSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Fill>
                            <CssParameter name="fill">#ff0000</CssParameter>
                        </Fill>
                        <Stroke>
                            <CssParameter name="stroke">#0000ff</CssParameter>
                            <CssParameter name="stroke-width">2.0</CssParameter>
                        </Stroke>
                    </PolygonSymbolizer>
                    <TextSymbolizer>
                        <Geometry>
                            <PropertyName>the_geom</PropertyName>
                        </Geometry>
                        <Label>fence_name</Label>
                        <Font>
                            <CssParameter name="font-family">times</CssParameter>
                            <CssParameter name="font-style">italic</CssParameter>
                            <CssParameter name="font-weight">bold</CssParameter>
                            <CssParameter name="font-size">5</CssParameter>
                        </Font>
                        <Fill>
                            <CssParameter name="fill">#FF0000</CssParameter>
                        </Fill>
                        <LabelPlacement>
                            <PointPlacement>
                                <AnchorPoint>
                                    <AnchorPointX>0.5</AnchorPointX>
                                    <AnchorPointY>0.5</AnchorPointY>
                                </AnchorPoint>
                                <Displacement>
                                    <DisplacementX>4</DisplacementX>
                                    <DisplacementY>4</DisplacementY>
                                </Displacement>
                                <Rotation>6</Rotation>
                            </PointPlacement>
                        </LabelPlacement>
                    </TextSymbolizer>
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
'''



dummySLD = """<StyledLayerDescriptor version="1.0.0"> <NamedLayer> <Name>WorldGen_Outline</Name> <UserStyle> <Title>xxx</Title> <FeatureTypeStyle> <Rule> <Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>Africa</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#0000ff</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule> <Rule> <Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>Antarctic</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#ff0000</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule> <Rule> <Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>Australia</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#00ff00</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule><Rule><Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>Europe</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#ffff00</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule><Rule><Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>North America</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#ff00ff</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule><Rule><Filter><PropertyIsEqualTo><PropertyName>NA3DESC</PropertyName><Literal>Asia</Literal></PropertyIsEqualTo></Filter> <LineSymbolizer> <Geometry> <PropertyName>center-line</PropertyName> </Geometry> <Stroke> <CssParameter name="stroke">#CC0000</CssParameter> <CssParameter name="stroke-width">2.0</CssParameter> </Stroke> </LineSymbolizer> </Rule> </FeatureTypeStyle> </UserStyle> </NamedLayer> </StyledLayerDescriptor>"""