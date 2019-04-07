import android, time

droid = android.Android()
droid.eventClearBuffer()
droid.startLocating()
time.sleep(3)
loc = droid.readLocation().result
if loc == {}:
    loc = droid.getLastKnownLocation().result
    print("getLastKnownLocation()")
if loc != {}:
    try:
        n = loc['gps']
        print("loc['gps']")
    except KeyError:
        n = loc['network']
        print("loc['network']")
    la = n['latitude']
    lo = n['longitude']
    address = droid.geocode(la, lo).result
    print(address)
    #mapShow = "http://api.map.baidu.com/marker?location=%s,%s&title=我的位置&content=我在这里&output=html" % (la, lo)
    mapShow ="https://restapi.amap.com/v3/staticmap?location=%s,%s&zoom=10&size=750*300&markers=mid,,A:%s,%s&key=%s"%(
        lo,la,lo,la,"3975f37408a3ab4904502e3630639014")
    droid.setClipboard(mapShow)
    markers="https://restapi.amap.com/v3/staticmap?markers=mid,0xFF0000,开:%s,%s;%s,%s|mid,0x008000,标:%s,%s;%s,%s&key=%s"%(
        lo,la,lo+0.1,la+0.1,lo+0.02,la,lo,la+0.01,"3975f37408a3ab4904502e3630639014")
    droid.setClipboard(markers)
    print(mapShow,markers)


"""
while 1:
    droid.eventClearBuffer()
    event = droid.eventWaitFor('location', 3000)
    print(event)
    try:
        provider = event.result['data']['gps']['provider']
        if provider == 'gps':
            lat = str(event['data']['gps']['latitude'])
            lng = str(event['data']['gps']['longitude'])
            latlng = 'lat: ' + lat + ' lng: ' + lng
            print(latlng)
            mapShow = "http://api.map.baidu.com/marker?location=%s,%s&title=我的位置&content=我在这里&output=html" % (lat, lng)
            print(mapShow)
            droid.setClipboard(mapShow)
            break
        else:
            continue
    except KeyError:
        continue
"""
droid.stopLocating()