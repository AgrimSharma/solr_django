from django.http import HttpResponse
from django.shortcuts import render
import http.client
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_document(request):
    if request.method == "POST":
        import pdb;pdb.set_trace()
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
                    response = json.dumps(response)
            except Exception:
                response = dict(status="Try Again later")
            return HttpResponse(response)
    else:
        # cores = ['techproducts', 'births', "doctor"]
        return render(request, "search_document.html")
