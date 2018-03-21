from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from asistencia.models import (Horario, Asistencia, Retraso, Permiso)
from marcaAPP.resource import MessageNC, ResponseNC
from asistencia.serializers import (AsistenciaSerializer, RetrasoSerializer, HorarioSerializer, PermisoSerializer)
from parametrizacion.models import (ProyectoUsuario)
from parametrizacion.serializers import (ProyectoUsuarioSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import date

class AsistenciaViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT para registrar la asistencia.
    """
    model=Asistencia
    queryset = model.objects.all()
    serializer_class = AsistenciaSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un regsitro de asistencia
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de datos de asistencia ya sea por usuario(id_usuario) o proyacto(id_proyecto)
        '''
        try:
            queryset = super(AsistenciaViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_usuario = self.request.query_params.get('id_usuario', None)
            id_proyecto = self.request.query_params.get('id_proyecto', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if id_proyecto or id_usuario:
                if id_proyecto:
                    qset = (Q(proyecto__id=id_proyecto))
                if id_usuario:
                    if id_proyecto:
                        qset=qset&(Q(usuario_id=id_usuario))
                    else:
                        qset=(Q(usuario_id=id_usuario))

                queryset = self.model.objects.filter(qset)

            page = self.paginate_queryset(queryset)

            if sin_paginacion is None: 
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})	
        
        except:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea el registro de una asistencia a un proyecto, requiere proyecto_id , usuario_id.
        '''
        if request.method == 'POST':				
            try:
                serializer = AsistenciaSerializer(data=request.data,context={'request': request})
                
                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'],usuario_id=request.data['usuario_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza la assitencia a un proyecto.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = AsistenciaSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'],usuario_id=request.data['usuario_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina una asistencia.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message':'Se presentaron errores al procesar la solicitud','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class PermisoViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT para registrar la permisos.
    """
    model=Permiso
    queryset = model.objects.all()
    serializer_class = PermisoSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un regsitro de permisos
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de datos de asistencia ya sea por usuario(id_usuario) o proyacto(id_proyecto)
        '''
        try:
            queryset = super(PermisoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_autorizado = self.request.query_params.get('id_autorizado', None)
            id_estado = self.request.query_params.get('id_estado', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if id_autorizado or id_estado:
                if id_autorizado:
                    qset = (Q(autorizado__persona_id=id_autorizado))
                if id_estado:
                    if id_autorizado:
                        qset=qset&(Q(estado_id=id_estado))
                    else:
                        qset=(Q(estado_id=id_estado))

                queryset = self.model.objects.filter(qset)

            page = self.paginate_queryset(queryset)

            if sin_paginacion is None: 
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})	
        
        except:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea el registro de un permiso, requiere autorizado_id , estado_id.
        '''
        if request.method == 'POST':				
            try:
                serializer = PermisoSerializer(data=request.data,context={'request': request})
                
                if serializer.is_valid():
                    serializer.save(autorizado_id=request.data['autorizado_id'],estado_id=request.data['estado_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza la assitencia a un proyecto.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = PermisoSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    erializer.save(autorizado_id=request.data['autorizado_id'],estado_id=request.data['estado_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina una asistencia.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message':'Se presentaron errores al procesar la solicitud','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)


class HorarioViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT para registrar los horarios en el proyecto.
    """
    model=Horario
    queryset = model.objects.all()
    serializer_class = HorarioSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un regsitro de horario
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de datos de horaios puedes filtrar por proyecto(id_proyecto)
        '''
        try:
            queryset = super(HorarioViewSet, self).get_queryset()
            id_proyecto = self.request.query_params.get('id_proyecto', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if id_proyecto:
                qset = (Q(proyecto__id=id_proyecto))
                queryset = self.model.objects.filter(qset)

            page = self.paginate_queryset(queryset)

            if sin_paginacion is None: 
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})	
        
        except:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea el registro de horarios a un proyecto, requiere proyecto_id.
        '''
        if request.method == 'POST':				
            try:
                serializer = HorarioSerializer(data=request.data,context={'request': request})
                
                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza un horario.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = HorarioSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina una asistencia.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message':'Se presentaron errores al procesar la solicitud','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class RetrasoViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT para registrar retrasos.
    """
    model=Retraso
    queryset = model.objects.all()
    serializer_class = RetrasoSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un regsitro de retraso
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de datos de retrasos ya sea por usuario(id_usuario) o proyacto(id_proyecto)
        '''
        try:
            queryset = super(RetrasoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_usuario = self.request.query_params.get('id_usuario', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if id_usuario:
                qset=(Q(usuario_id=id_usuario))
                
                queryset = self.model.objects.filter(qset)

            page = self.paginate_queryset(queryset)

            if sin_paginacion is None: 
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})	
        
        except:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea un retraso de un usuario en un proyecto, requiere proyecto_id , usuario_id
        '''
        if request.method == 'POST':				
            try:
                serializer = RetrasoSerializer(data=request.data,context={'request': request})
                
                if serializer.is_valid():
                    serializer.save(usuario_id=request.data['usuario_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos (' + str(e) + ')','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza la retraso a un proyecto.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = RetrasoSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(usuario_id=request.data['usuario_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos (' + str(e) + ')','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina un retraso.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message':'Se presentaron errores al procesar la solicitud','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listaProyectos(request):
    '''
    Retorna una lista de proyectos del usuario
    '''
    try:
        id_usuario = request.user.id
        ListPendientes = []
        qset=(Q(usuario_id=id_usuario))
        ListProyectos = ProyectoUsuario.objects.filter(qset)

        for item in ListProyectos:
            lista={
                    "id": item.proyecto.id,
                    "nombre": item.proyecto.nombre,
                    "latitud": item.proyecto.latitud,
                    "longitud": item.proyecto.longitud,
                    "hora_entrada": '9:00',
                    "hora_salida":'19:00'
            }
            ListPendientes.append(lista)

        return Response({'message':'','success':'ok','data':ListPendientes})	
        
    except Exception as e:
        return Response({'message':'Se presentaron errores de comunicacion con el servidor (' + str(e) + ')','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def ultimasAsistencias(request):
    '''
    Retorna una lista de proyectos del usuario
    '''
    try:
        id_usuario = request.user.id
        ListPendientes = []
        today = date.today()
        qset=(Q(usuario_id=id_usuario))
        qset=qset&(Q(entrada=today))
        listAsistencias = Asistencia.objects.filter(qset).reverse()[:5]

        for item in listAsistencias:
            lista={
                "id": item.id,
                "nombre_proyecto": item.proyecto.nombre,
                "hora_marcacion": item.horaEntrada.strftime("%H:%M:%S"),
                "fecha_marcación":item.entrada
            }
            ListPendientes.append(lista)

        return Response({'message':'','success':'ok','data':ListPendientes})	
        
    except Exception as e:
        return Response({'message':'Se presentaron errores de comunicacion con el servidor (' + str(e) + ')','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def listaDeNovedades(request):
    '''
    Retorna una lista de novedades en proyecto
    '''
    try:
        id_usuario = request.user.id
        ListPendientes = []

        today = date.today()
        qset=(Q(entrada=today))
        ListProyectos = Asistencia.objects.filter(qset)

        for item in ListProyectos:
            if item.usuario.cargo:
                cargo = item.usuario.cargo.nombre
            else:
                cargo = ""
            
            if item.usuario.persona:
                usuario = item.usuario.persona.nombre + ' ' + item.usuario.persona.primerApellido
            else:
                usuario = ''
            
            lista={
                    "id": item.id,
                    "gerencia":'Prueba',
                    "supervisor": "Janneison",
                    "proyecto": item.proyecto.nombre,
                    "trabajador":usuario ,
                    "cargo": cargo,
                    "hora_ingreso": item.horaEntrada.strftime("%H:%M:%S"),
                    "marca_ingreso": item.horaEntrada.strftime("%H:%M:%S"),
                    "envia_aviso":'',
                    "llegada_estimada":'',
                    "envia_ausencia":"",
                    "sf":0
            }
            ListPendientes.append(lista)

        return Response({'message':'','success':'ok','data':ListPendientes})	
        
    except Exception as e:
        return Response({'message':'Se presentaron errores de comunicacion con el servidor (' + str(e) + ')','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		