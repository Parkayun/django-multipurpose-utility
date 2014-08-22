# -*- coding:utf -8-
import json

from django.shortcuts import HttpResponse


def json_response(data, acao=False):
    try: 
        data = json.dumps(data)
    except Exception, e:
        data = json.dumps({'error': 'json dumps error'})
    finally:
        response = HttpResponse(data, content_type='application/json')
        if acao:
            response['Access-Control-Allow-Origin'] = '*'
        return response


def get_hand_type_fields(model):
    result = ''
    for field in model._meta.fields:
        if not field.has_default() and (not field.blank and not field.null):
            field_type = field.get_internal_type()
            if 'IntegerField' in field_type or 'SmallIntegerField' in field_type:
                result += field.name+"=1, "
            elif 'ForeignKey' in field_type or 'OneToOneField' in field_type:
                result += field.name+"='key', "
            else:
                result += field.name+"='', "


class AutoCreator(object):
    def __init__(self):
        self.key_counter = {}

    def run(self, model):
        field_query = ''
        for field in model._meta.fields:
            if not field.has_default() and (not field.blank and not field.null):
                field_type = field.get_internal_type()

                if field_type in ['IntegerField', 'SmallIntegerField']:
                    field_query += field.name+"=1,"

                elif field_type in ['ForeignKey', 'OneToOneField']:
                    parent_model = field.rel.to
                    self.run(parent_model)

                    counter_key = model.__name__+'_'+field.rel.to.__name__
                    if not self.key_counter.has_key(counter_key):
                        self.key_counter[counter_key] = -1
                    self.key_counter[counter_key] += 1

                    idx = self.key_counter[counter_key]
                    key_field = parent_model.__name__ + '.objects.all()['+str(idx)+']'
                    field_query += field.name+"="+key_field+", "

                    exec 'from '+parent_model.__module__+' import '+parent_model.__name__

                elif field_type in ['DateField', 'DateTimeField'] and (not field.auto_now and not field.auto_now_add):
                    if 'start' in field.name or 'begin' in field.name:
                        field_query += field.name+"='2014-01-01', "
                    elif 'end' in field.name:
                        field_query += field.name+"='2014-12-31', "
                    else:
                        field_query += field.name+"='2014-06-06', "

                else:
                    max_length = 10
                    if field.max_length and max_length > field.max_length:
                        max_length = field.max_length

                    import random
                    value = ''.join([chr(random.randint(97, 122)) for _ in xrange(max_length)])

                    field_query += field.name+"='"+value+"', "

        exec 'from '+model.__module__+' import '+model.__name__

        query = model._meta.object_name+'.objects.create('+field_query+')'
        eval(query)