from django.shortcuts import render

# Create your views here.
## City

# class CityCreateView(generics.CreateAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin] # change to custom permission if needed

#     def perform_create(self, serializer):
#         serializer.save()

# class CityUpdateView(generics.UpdateAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

#     def perform_update(self, serializer):
#         serializer.save()

# class CityDestroyView(generics.DestroyAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [IsAdmin]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

# class CityListView(generics.ListAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return City.objects.all()

# class CityDetailView(generics.RetrieveAPIView):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]
#     lookup_field = 'id'
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()

# class CityViewSets(viewsets.ReadOnlyModelViewSet):
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]
#     lookup_url_kwarg = 'city_id'

#     def get_queryset(self):
#         return City.objects.all()
