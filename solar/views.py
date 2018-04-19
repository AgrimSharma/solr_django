from django.http import HttpResponse
from django.shortcuts import render
import http.client
import json

from django.views.decorators.csrf import csrf_exempt


def fetch_data(url):
    connection = http.client.HTTPConnection("localhost", 8983)

    connection.request('GET', url)
    headers = {'Content-type': 'application/json'}

    response = connection.getresponse()
    response = response.read().decode()
    response = json.loads(response)['response']
    if response['numFound'] > 0:
        return response


@csrf_exempt
def add_document(request):
    if request.method == "POST":
        ids = request.POST.get('id','')
        title = request.POST.get("title", "")
        if not ids or not title:
            return HttpResponse(json.dumps(dict(status=400)))
        else:
            connection = http.client.HTTPConnection("localhost", 8983)

            headers = {'Content-type': 'application/json'}

            foo = {'add': {'doc': {'id': ids, 'title': title}, 'boost': 1, 'overwrite': True,
                           'commitWithin': 1000}}
            json_foo = json.dumps(foo)

            connection.request('POST', '/solr/core/update?wt=json', json_foo, headers)

            response = connection.getresponse()
            response = json.loads(response.read().decode())
            response['status'] = "success"
            return HttpResponse(json.dumps(response))

    else:
        return render(request, "add_document.html")


@csrf_exempt
def search_document(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        fields = request.POST.get("fields", "")
        # core = request.POST.get("core", "")

        if not query:
            url = "/solr/core/select?wt=json&indent=true&q=*:*"
            connection = http.client.HTTPConnection("localhost", 8983)

            headers = {'Content-type': 'application/json'}
            connection.request('GET', url)

            response = connection.getresponse()
            response = response.read().decode()
            response = json.loads(response)['response']
            if response['numFound'] > 0:
                response = json.dumps(response)
            return HttpResponse(response)

        else:
            if fields:
                url = "/solr/core/select?wt=json&indent=true&q={query}&fl={fields}".format(query=query,
                                                                                           fields=fields)
            else:
                url = "/solr/core/select?wt=json&indent=true&q={query}".format(query=query)
            connection = http.client.HTTPConnection("localhost", 8983)

            headers = {'Content-type': 'application/json'}

            try:
                connection.request('GET', url)

                response = connection.getresponse()
                response = response.read().decode()
                response = json.loads(response)['response']
                if response['numFound'] > 0:
                    response = response
            except Exception:
                response = dict(status="Try Again later")
            return HttpResponse(json.dumps(response))
    else:
        return render(request, "search_document.html")


@csrf_exempt
def search_city_document(request):
    if request.method == "POST":
        city = request.POST.get('city', '')

        if not city:
            return HttpResponse(json.dumps(dict(status=400)))

        else:
            university = fetch_data("/solr/university/select?wt=json&indent=true&q=city:{}*&fl=name,city".format(city[:3]))
            propertys = fetch_data("/solr/property/select?wt=json&indent=true&q=city:{}*&fl=Address,city".format(city[:3]))

            return HttpResponse(
                json.dumps(
                    dict(
                        city=city,
                        university=[dict(name=u['name'][0], city=u['city'][0]) for u in university['docs']],
                        property=[dict(address=u['Address'][0], city=u['city'][0]) for u in propertys['docs']])))
    else:
        return render(request, "search_city_document.html")



