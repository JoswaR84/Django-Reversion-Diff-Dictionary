import json
from django.contrib.auth.models import User
from reversion.models import Version, Revision

# Only for Shell #
##################
from calib_inv.models import Gauge
obj = Gauge.objects.get(pk=6)
##################

# Need to pass in the gauge to 'vers'
vers = Version.objects.get_for_object(obj)
dicts = []
# Builds dictionary for each version
for ver in vers:
    revision_id = ver.revision_id
    revision = Revision.objects.get(pk=revision_id)
    date = revision.date_created
    date = date.strftime('%m/%d/%y %H:%M%p')
    user_id = revision.user_id
    if not user_id:
        user = 'initial'
    if user_id:
        user = User.objects.get(pk=user_id)
        user = user.username
    load_data = json.loads(ver.serialized_data)
    data = load_data[0]['fields']
    temp_dict = {
            'revision id': revision_id, 
            'user': user, 
            'date': date, 
            'data': data
        }
    # Appends dictionary to 'dicts' list
    dicts.append(temp_dict)

diffs = []
# Newest first, compares 'dicts' list, 
# 'data' field and rebuilds dictionary.
for i in range(len(dicts)):
    if i + 1 < len(dicts):        
        dif = dict((dicts[i]['data'].items() 
            - dicts[i + 1]['data'].items()))
        temp_dict = {
            'revision id': dicts[i]['revision id'], 
            'user': dicts[i]['user'], 
            'date': dicts[i]['date'],
            'data': dif
        }
        # Appends dictionary to 'diffs' list
        diffs.append(temp_dict)
    else: 
        temp_dict = {
            'revision id': dicts[i]['revision id'], 
            'user': dicts[i]['user'], 
            'date': dicts[i]['date'],
        }
        # Appends initial dictionary to 'diffs' list
        diffs.append(temp_dict)

print(diffs)
