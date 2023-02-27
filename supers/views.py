from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super



@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        supers = Super.objects.all()
        super_param = request.query_params.get('super_type')
        serializer = SuperSerializer(supers, many=True)
        if super_param:
            supers = supers.filter(super_type__type=super_param)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            heroes = supers.filter(super_type__type = "Hero")
            villains = supers.filter(super_type__type = "Villain")
            hero_serializer = SuperSerializer(heroes, many=True)
            villain_serializer = SuperSerializer(villains, many=True)
            custom_dictionary_response = {"Heroes":hero_serializer.data,"Villains":villain_serializer.data}
            return Response(custom_dictionary_response, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['Get', 'PUT', "DELETE"])
def supers_detail(request, pk): 
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(super)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        serializer = SuperSerializer(super)
        super.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    


# @api_view(['GET'])
# def heroes_and_villains(request):
#     supers = Super.objects.all()
#     super_types = Super.objects.all()
#     supers_serializer = SuperSerializer(supers, many=True)
#     super_types_serializer = SuperSerializer(super_types, many=True)

#     custom_response_dict = {
#         heroes = supers.filter(super_type__type = 'Hero')
#         heroes_serialized = SuperSerializer(heroes,many=True)
#         'supers': supers_serializer.data,
#         'super_types': super_types_serializer.data
#         }