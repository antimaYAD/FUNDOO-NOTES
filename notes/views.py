from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from .models import Note
from .serializers import NoteSerializer
from loguru import logger

class NoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing note instances.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
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
            return Response(serializer.data)
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
            return Response(serializer.data)
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
            return Response(status=status.HTTP_204_NO_CONTENT)
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
            queryset = Note.objects.filter(user=request.user, is_archive=True)
            serializer = NoteSerializer(queryset, many=True)
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
            print(note)
            note.is_trash = not note.is_trash
            note.save()
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
            queryset = Note.objects.filter(user=request.user, is_trash=True)
            serializer = NoteSerializer(queryset, many=True)
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
