from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .models import Note
from .serializers import NoteSerializer
from loguru import logger
from .redisutil import RedisUtils

class NoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing note instances.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    redis = RedisUtils()

    def get_queryset(self):
        """
        Returns notes for the logged-in user with is_archive and is_trash as False.
        """
        return Note.objects.filter(user=self.request.user, is_archive=False, is_trash=False)

    def list(self, request, *args, **kwargs):
        """
        List all notes for the logged-in user that are not archived or trashed.
        """
        try:
            cache_key = f"user_{request.user.id}"
            cache_note = self.redis.get(cache_key)

            if cache_note:
                logger.info(f"Notes feteched from the cache for user {request.user.id}")
                return Response({"Message":"The list of cache notes of user","satus":"Sucess","data":cache_note},status=status.HTTP_200_OK)
                
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            self.redis.save(cache_key,serializer.data,ex=300)
            return Response({"Message":"The list of notes of user ","status":"Sucess","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving notes: {str(e)}")
            return Response({
                'error': 'An error occurred while retrieving notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Create a new note for the logged-in user.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            cache_key = f"user_{request.user.id}"
            cache_note = self.redis.get(cache_key)
            if cache_note is None:
                cache_note=[]
            cache_note.append(serializer.data)
            self.redis.save(cache_key,cache_note,ex=300)
            headers = self.get_success_headers(serializer.data)
            return Response({"Message":"The notes  is created of user ","satus":"Sucess","data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return Response({
                'error': 'An error occurred while creating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a specific note by its ID.
        """
        try:
            cache_key = f"user_{request.user.id}_note_{pk}"
            cache_note = self.redis.get(cache_key)
            if cache_note:
                logger.info(f"Notes are  fetched from the cache of user {cache_key}")
                return Response({"Message":"The data of the retrive note from cache","satus":"Sucess","data":cache_note},status=status.HTTP_200_OK)   
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            self.redis.save(cache_key, serializer.data, ex=300) 
            return Response({"Message":"The data of the retrive note","satus":"Sucess","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while retrieving the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update a specific note by its ID.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            note_cache_key = f"user_{request.user.id}_note_{pk}"
            self.redis.save(note_cache_key,serializer.data,ex=300)
            cache_key = f"user_{request.user.id}"
            queryset = self.get_queryset()
            self.redis.save(cache_key,self.get_serializer(queryset,many=True).data,ex=300)
            return Response({"Message":"The note is updated","satus":"Sucess","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error updating note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update a specific note by its ID.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            note_cache_key = f"user_{request.user.id}_note_{pk}"
            self.redis.save(note_cache_key,serializer.data,ex=300)
            cache_key =  f"user_{request.user.id}"
            queryset=self.get_queryset()
            self.redis.save(cache_key,self.get_serializer(queryset,many=True).data,ex=300)
            return Response({"Message":"The note is partial updated","satus":"Sucess","data":serializer.data},status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error partially updating note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while partially updating the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete a specific note by its ID.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            note_cache_key = f"user_{request.user.id}_note_{pk}"
            
            self.redis.delete(note_cache_key)
            cache_key = f"user_{request.user.id}"
            queryset = self.get_queryset()
            self.redis.save(cache_key,self.get_serializer(queryset,many=True).data,ex=300)
            
            return Response({"Message":"The note is deleted","satus":"Sucess"},status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error deleting note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while deleting the note.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='toggle_archive', permission_classes=[IsAuthenticated])
    def toggle_archive(self, request, pk=None):
        """
        Toggle the archive status of a note.
        """
        try:
            note = Note.objects.get(id=pk,user=request.user)
        
            note.is_archive = not note.is_archive
            note.save()
            
            note_cache_key = f"user_{request.user.id}"
            
            note_cache_data = self.redis.get(note_cache_key)

            if note_cache_data:
                for cache_note in note_cache_data:
                    if cache_note['id'] == pk:           
                        cache_note['is_archive'] = note.is_archive
                self.redis.save(note_cache_key,note_cache_data,ex=300)
                logger.info(f"Note {pk} archive status toggled in cache bjjlfor user {request.user.id}")

            
            return Response({
                'message': 'Note archive status toggled successfully.',
                'data': NoteSerializer(note).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error toggling archive status for note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while toggling the archive status.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='archived_notes', permission_classes=[IsAuthenticated])
    def archived_notes(self, request):
        """
        List all archived notes for the logged-in user.
        """
        try:
            note_cache_key = f"user_{request.user.id}_archived_notes"
            note_cache_data = self.redis.get(note_cache_key)
            if note_cache_data:
                logger.info(f"Archived Notes feteched from the cache for user {request.user.id}")
                
        
                return Response({"Message":"Archived notes retrived from cache","satus":"Sucess","data":note_cache_data},status=status.HTTP_200_OK)   
                            
            queryset = Note.objects.filter(user=request.user, is_archive=True)
            serializer = NoteSerializer(queryset, many=True)
            self.redis.save(note_cache_key,serializer.data,ex=300)
            return Response({
                'message': 'Archived notes retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving archived notes: {str(e)}")
            return Response({
                'error': 'An error occurred while retrieving archived notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='toggle_trash', permission_classes=[IsAuthenticated])
    def toggle_trash(self, request, pk=None):
        
        """
        Toggle the trash status of a note.
        """
        try:
            note = Note.objects.get(id=pk,user=request.user)
            note.is_trash = not note.is_trash
            note.save()
            
            note_cache_key = f"user_{request.user.id}"
            note_cache_data = self.redis.get(note_cache_key)
            if note_cache_data:
                for cache_note in note_cache_data:
                    if cache_note['id'] == pk:
                        cache_note['is_trash'] = note.is_trash
                self.redis.save(note_cache_key,note_cache_data,ex=300)
            return Response({
                'message': 'Note trash status toggled successfully.',
                'data': NoteSerializer(note).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error toggling trash status for note with ID {pk}: {str(e)}")
            return Response({
                'error': 'An error occurred while toggling the trash status.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='trashed_notes', permission_classes=[IsAuthenticated])
    def trashed_notes(self, request):
        """
        List all trashed notes for the logged-in user.
        """
        try:
            note_cache_key = f"user_{request.user.id}"
            note_cache_data = self.redis.get(note_cache_key)
            if note_cache_data:
                logger.info(f"Trash note of user {request.user.id}")
                return Response({
                'message': 'Trashed notes retrieved from cache successfully.',
                'data': note_cache_data
            }, status=status.HTTP_200_OK)
                

            
            queryset = Note.objects.filter(user=request.user, is_trash=True)
            serializer = NoteSerializer(queryset, many=True)
            self.redis.save(note_cache_key,serializer.data,ex=300)
            return Response({
                'message': 'Trashed notes retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving trashed notes: {str(e)}")
            return Response({
                'error': 'An error occurred while retrieving trashed notes.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
