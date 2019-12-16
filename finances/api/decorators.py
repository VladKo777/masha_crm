# import json
# from rest_framework import status
# from rest_framework.response import Response
#
#
# def add_ability_to_create_many_objects(original_class):
#     def create(self, request, *args, **kwargs):
#         """
#         checks if post request data exists initializes serializer with many=True
#         else executes default CreateModelMixin.create method
#         """
#
#         json_string_data = request.data.get('data', False)
#         with open('MyLog.txt', 'a', encoding='utf-8') as file:
#             file.write('{}\n'.format(  json_string_data  ))
#
#         if not json_string_data:
#             return super(original_class, self).create(request, *args, **kwargs)
#         else:
#             json_data = json.loads(json_string_data)
#             serializer = self.get_serializer(data=json_data, many=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     original_class.create = create
#     return original_class
