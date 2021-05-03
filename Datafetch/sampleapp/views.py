import json
from statistics import mode
from operator import itemgetter
import pandas as pd

from django.shortcuts import render
from itertools import groupby
from django.views.decorators.csrf import csrf_exempt

import requests

# Create your views here.

@csrf_exempt
def index(request):
        link = "https://www.mocky.io/v2/5d403d913300003a209d2ad3"
        f = requests.get(link)
        test_tr = (f.text)
        test_tr = str(test_tr)[1:-1]
        ab = test_tr.split(",")
        person = {}
        for x in ab:
            x = x.split(":")
            if x[0].strip() in person.keys():
                person[x[0].strip()].append(x[1])
            else:
                person[x[0].strip()] = [x[1]]

        array_len = []
        array_name = []
        frequent = []

        for per, value in person.items():
            array_name.append(per)
            array_len.append(len(value))
            frequent.append(mode(value))

        a = [list(x) for x in zip(array_name, array_len,frequent )]
        b = sorted(a, key=itemgetter(1), reverse=True)[:5]

        name = []
        freq= []
        msg=[]
        for i in b:
            count = 0
            for j in i:
                count = count + 1
                if count == 1:
                    name.append(j)
                if count == 2:
                    freq.append(j)
                if count == 3:
                    msg.append(j)

        para = {"name": name, "freq":freq, "msg":msg }
        df = pd.DataFrame(para)
        json_records = df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        context = {'d': data}
        return render(request, 'sampleapp/home.html', context)