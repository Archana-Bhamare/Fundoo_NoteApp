import logging

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Notes
from Fundoo_Note.serializers import CreateNoteSerializer, DisplayNoteSerializer, RestoreNoteSerializer

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename="C:\\Users\\KatK\\django_projects\\FundooNote_Project\\static\\Notetest.log",
                    level=logging.INFO, format=LOG_FORMAT, filemode='w')
logger = logging.getLogger()

@method_decorator(login_required(login_url='/login/'), name="dispatch")
class createNoteList(GenericAPIView):

    queryset = Notes.objects.all()
    serializer_class = CreateNoteSerializer

    def get(self, request):
        queryset = Notes.objects.filter(user_id=self.request.user.id)
        serializer = CreateNoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            logger.info("Note Successfully Created")
            return Response("Note Created", status=status.HTTP_201_CREATED)
        logger.error("Something went Wrong")
        return Response("Note not Created", status=status.HTTP_406_NOT_ACCEPTABLE)


@method_decorator(login_required(login_url='/login/'), name="dispatch")
class UpdateNoteList(GenericAPIView):

    queryset = Notes.objects.all()
    serializer_class = DisplayNoteSerializer

    def get(self, request, pk):
        try:
            note = Notes.objects.get(id=pk, user_id=self.request.user.id)
            serializer = DisplayNoteSerializer(note)
            return Response(serializer.data)

        except Notes.DoesNotExist:
            logger.error("Note Does not Exist")
            return Response("this note does not exist", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            note = Notes.objects.get(id=pk, user_id=self.request.user.id)
            serializer = DisplayNoteSerializer(note, data=request.data)

            if serializer.is_valid():
                serializer.save()
                logger.info("Note SuccessFully Updated")
                return Response('Note updated', status=status.HTTP_202_ACCEPTED)

        except Notes.DoesNotExist:
            logger.error("Note Does not Exist")
            return Response("this note does not exist", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            note = Notes.objects.get(id=pk)
            print(note)
            note.delete()
            logger.info("Note Deleted Successfully")
            return Response("Note deleted", status=status.HTTP_202_ACCEPTED)

        except Notes.DoesNotExist:
            logger.error("Note Not Found")
            return Response("Not found", status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required(login_url='/login/'), name="dispatch")
class ArchiveNoteList(GenericAPIView):

    queryset = Notes.objects.all()

    def get(self, request):
        note = Notes.objects.filter(is_archive=True, user_id=self.request.user.id)
        serializer = DisplayNoteSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required(login_url='/login/'), name="dispatch")
class PinNoteList(GenericAPIView):

    queryset = Notes.objects.all()

    def get(self, request):
        note = Notes.objects.filter(is_pin=True, user_id=self.request.user.id)
        serializer = DisplayNoteSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required(login_url='/login/'), name="dispatch")
class TrashNoteList(GenericAPIView):

    queryset = Notes.objects.all()

    def get(self, request):
        note = Notes.objects.filter(is_trash=True, user_id=self.request.user.id)
        serializer = DisplayNoteSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required(login_url='/login/'), name="dispatch")
class RestoreNoteList(GenericAPIView):

    serializer_class = RestoreNoteSerializer
    queryset = Notes.objects.all()

    def get(self, request, pk):
        try:
            note = Notes.objects.get(
                id=pk, is_trash=True, user_id=self.request.user.id)
            serializer = DisplayNoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Notes.DoesNotExist:
            logger.error("This note does not exist")
            return Response("this note does not exist", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            note = Notes.objects.get(
                id=pk, is_trash=True, user_id=self.request.user.id)
            serializer = RestoreNoteSerializer(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Note Restored Successfully")
                return Response('Restore from trash', status=status.HTTP_202_ACCEPTED)

        except Notes.DoesNotExist:
            logger.error("This note not found in Trash")
            return Response("this note not found in trash", status=status.HTTP_404_NOT_FOUND)