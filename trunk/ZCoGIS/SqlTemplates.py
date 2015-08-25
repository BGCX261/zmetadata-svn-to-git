##municipalityPositionTemplate = '''
##select local_municipalities.mn_name
##from location,  local_municipalities
##where location.device_id = '%s' and  (location.the_geom @ local_municipalities.the_geom) and (location.tmstamp = '%s')
##'''

municipalityPositionTemplate = '''
select local_municipalities.mn_name
from incident, incident_point, local_municipalities
where incident.id = incident_point.oid and incident.unit = %s and  (incident_point.the_geom @ local_municipalities.the_geom) and
 (incident.timestamp = '%s')'''

##suburbPositionTemplate = '''
##select suburbs.suburb
##from location,  suburbs
##where location.device_id = '%s' and  (location.the_geom @ suburbs.the_geom) and (location.tmstamp = '%s')
##'''

suburbPositionTemplate = '''
select suburbs.suburb
from incident, incident_point, suburbs
where incident.id = incident_point.oid and incident.unit = %s and
  (incident_point.the_geom @ suburbs.the_geom) and
 (incident.timestamp = '%s')
'''

##provincePositionTemplate = '''
##select provinces.name
##from location,  provinces
##where location.device_id = '%s' and  (location.the_geom @ provinces.the_geom) and (location.tmstamp = '%s')
##'''

provincePositionTemplate = '''
select provinces.name
from incident, incident_point , provinces
where incident.id = incident_point.oid and incident.unit = %s and 
(incident_point.the_geom @ provinces.the_geom) and (incident.timestamp = '%s')
'''


##roadPositionTemplate = '''
##SELECT name
##FROM roads
##WHERE 
##Distance(the_geom, (select location.the_geom from location where location.device_id = '%s' and location.tmstamp='%s' limit 1)) < 0.0005
##and roads.name <> ''
##'''

roadPositionTemplate = '''
SELECT name
FROM roads
WHERE 
Distance(the_geom, (select incident_point.the_geom from incident, incident_point where incident.id = incident_point.oid and incident.unit = %s and incident.timestamp='%s' limit 1)) < 0.0005
and roads.name <> ''
'''

locationExtentTemplate = '''
select box2d(the_geom)
from location
where device_id = '%s' and tmstamp = '%s'
'''

extentOfPointsBeforeTmStampTemplate = '''
select extent(the_geom) from location
where device_id = '%s' and tmstamp > '%s' 
'''

extentBetweenTimes = '''
select extent(the_geom) from location
where device_id = '%s' and tmstamp > '%s' and tmstamp < '%s' 
'''

getExtentForMunicAndSuburb = '''
select extent(suburbs.the_geom) 
from local_municipalities, suburbs
where local_municipalities.mn_name = '%s' and suburbs.suburb = '%s'
'''


suburbNamesForMunicName = '''
select suburbs.suburb
from suburbs, local_municipalities
where local_municipalities.mn_name = '%s' and suburbs.the_geom @ local_municipalities.the_geom
'''

allMunicNames = '''
select distinct local_municipalities.mn_name
from local_municipalities , suburbs
where suburbs.the_geom @ local_municipalities.the_geom order by local_municipalities.mn_name
'''

GeoFenceHasName = '''
select fence_name from geofence where fence_name = '%s'
'''

insertGeofenceFromSuburb = '''
insert into geofence (device_id, fence_class, from_time, to_time, fence_name, the_geom)
values ('%s',%s,'%s','%s','%s',(select the_geom from suburbs where suburb = '%s'))
'''

GetFenceNamesForDefice = '''
select fence_name from geofence where fence_name = '%s' order by fence_name
'''

getFenceNamesForDevice = '''
select fence_name 
from geofence
where device_id = '%s'
'''

getGeoFenceExtentForNameAndDeviceId = '''
select extent(the_geom) 
from geofence
where device_id = '%s' and fence_name = '%s'
'''

deleteGeoFenceWithNameAndId = '''
delete from geofence 
where device_id = '%s' and fence_name = '%s'
'''

##select local_municipalities.mn_name
##from location,  local_municipalities
##where location.device_id = '1' and 
## (location.the_geom @ local_municipalities.the_geom)
## and (location.tmstamp = '2006-10-04 11:22:06')


##select roads.name
##from location,  roads
##where location.device_id = '1' and  Overlaps(Buffer(location.the_geom,10), roads.the_geom)
##and (location.tmstamp = '2006-10-04 11:22:58')  