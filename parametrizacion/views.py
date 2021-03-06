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
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, User, 
Estado, Tipo, Persona, Proyecto,ContactoEmpresa,ProyectoUsuario)
from marcaAPP.resource import MessageNC, ResponseNC
from parametrizacion.serializers import (UserSerializer, GroupSerializer, PaisSerializer, TipoSerializer,
RegionSerializer, MunicipioSerializer, EmpresaSerializer, CargoSerializer, EstadoSerializer, PersonaSerializer,
ProyectoSerializer,EmpresaContactoSerializer, ProyectoUsuarioSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

@permission_classes((AllowAny,))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para usuarios creacion y edicion.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    model=User

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de usuarios puedes buscar por nombre o id_cargo
        '''
        try:
            queryset = super(UserViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_cargo = self.request.query_params.get('id_cargo', None)

            if dato or id_cargo:
                if dato:
                    qset = (Q(persona__nombre__icontains=dato))
                if id_cargo:
                    if dato:
                        qset=qset&(Q(cargo_id=id_cargo))
                    else:
                        qset=(Q(cargo_id=id_cargo))

                queryset = self.model.objects.filter(qset)
            #utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({ResponseNC.message:'','success':'ok',
                    ResponseNC.data:serializer.data})

            serializer = self.get_serializer(queryset,many=True)
            return Response({ResponseNC.message:'','success':'ok',ResponseNC.data:serializer.data})
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor',ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        """
	    Crear un usuario persona_id, cargo_id son solo lectura
	    """
        if request.method == 'POST':
            try:
                serializer = UserSerializer(data=request.data,context={'request': request})

                if serializer.is_valid():
                    serializer.save(persona_id=request.data['persona_id'],cargo_id=request.data['cargo_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos ' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API muestra los grupos 
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PaisViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de paises, puede utilizar el parametro (dato) por medio del cual, se podra buscar por todo o parte del nombre.
	"""
	model=Pais
	queryset = model.objects.all()
	serializer_class = PaisSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
		except Exception as e:
			return Response({ResponseNC.message:MessageNC['vacio'],'success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)


	def list(self, request, *args, **kwargs):
		try:
			queryset = super(PaisViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			if dato:
				qset = (Q(nombre__icontains=dato))
				queryset = self.model.objects.filter(qset)
			#utilizar la variable ignorePagination para quitar la paginacion
			ignorePagination= self.request.query_params.get('ignorePagination',None)
			if ignorePagination is None:
				page = self.paginate_queryset(queryset)
				if page is not None:
					serializer = self.get_serializer(page,many=True)	
					return self.get_paginated_response({ResponseNC.message:'','success':'ok',
					ResponseNC.data:serializer.data})
	
			serializer = self.get_serializer(queryset,many=True)
			return Response({ResponseNC.message:'','success':'ok',
					ResponseNC.data:serializer.data})			
		except Exception as e:
			return Response({ResponseNC.message:MessageNC['errorServidor'],ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			try:
				serializer = PaisSerializer(data=request.data,context={'request': request})

				if serializer.is_valid():
					serializer.save()
					return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
						ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({ResponseNC.message:serializer.errors,'success':'fail',
			 		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
			 	return Response({ResponseNC.message:'Se presentaron errores al procesar los datos ' + str(e),'success':'error',
			  		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = PaisSerializer(instance,data=request.data,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
						ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({ResponseNC.message:serializer.errors,'success':'fail',
			 		ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
			except Exception as e:
			 	return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
					ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

	def destroy(self,request,*args,**kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
			return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
				ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
			ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)	

class RegionViewSet(viewsets.ModelViewSet):
    """
	Retorna una lista de Regiones, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar las regiones que hacen parte de determinado pais.
    """
    model=Region
    queryset = model.objects.all()
    serializer_class = RegionSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
        except Exception as e:
            return Response({ResponseNC.message:'No se encontraron datos','success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(RegionViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_pais = self.request.query_params.get('id_pais', None)

            if dato or id_pais:
                if dato:
                    qset = (Q(nombre__icontains=dato))
                if id_pais:
                    if dato:
                        qset=qset&(Q(pais_id=id_pais))
                    else:
                        qset=(Q(pais_id=id_pais))

                queryset = self.model.objects.filter(qset)
            #utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({ResponseNC.message:'','success':'ok',
                    ResponseNC.data:serializer.data})

            serializer = self.get_serializer(queryset,many=True)
            return Response({ResponseNC.message:'','success':'ok',ResponseNC.data:serializer.data})
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor',ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                serializer = RegionSerializer(data=request.data,context={'request': request})

                if serializer.is_valid():
                    serializer.save(pais_id=request.data['pais_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = RegionSerializer(instance,data=request.data,context={'request': request},partial=partial)
                if serializer.is_valid():
                    serializer.save(pais_id=request.data['pais_id'])
                    return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
            ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
            ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

class MunicipioViewSet(viewsets.ModelViewSet):
    """
    Retorna una lista de Municipios, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar los municipios que hacen parte de determinada region.
    """
    model=Municipio
    queryset = model.objects.all()
    serializer_class = MunicipioSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({ResponseNC.message:'',ResponseNC.status:'success',ResponseNC.data:serializer.data})
        except Exception as e:
            return Response({ResponseNC.message:'No se encontraron datos','success':'fail',ResponseNC.data:''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(MunicipioViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_region= self.request.query_params.get('id_region', None)

            if dato or id_region:
                if dato:
                    qset = (Q(nombre__icontains=dato))
                if id_region:
                    if dato:
                        qset=qset&(Q(region_id=id_region))
                    else:
                        qset=(Q(region_id=id_region))

                queryset = self.model.objects.filter(qset)
            #utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({ResponseNC.message:'','success':'ok',
                    ResponseNC.data:serializer.data})

            serializer = self.get_serializer(queryset,many=True)
            return Response({ResponseNC.message:'','success':'ok',
            ResponseNC.data:serializer.data})
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor',ResponseNC.status:'error',ResponseNC.data:''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                serializer = MunicipioSerializer(data=request.data,context={'request': request})

                if serializer.is_valid():
                    serializer.save(region_id=request.data['region_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = MunicipioSerializer(instance,data=request.data,context={'request': request},partial=partial)
                if serializer.is_valid():
                    serializer.save(region_id=request.data['region_id'])
                    return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
            ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
            ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
#Fin api rest para municipio

class CargoViewSet(viewsets.ModelViewSet):
    """
    Retorna una lista de Cargos, puede utilizar el parametro (dato) a traver del cual, se podra buscar por todo o parte del nombre, tambien puede buscar por medio de la empresa de cual pertenece dicho cargo.
    """
    model= Cargo
	#model_log=Logs
	#model_acciones=Acciones
    nombre_modulo='parametrizacion.cargo'
    queryset = model.objects.all()
    serializer_class = CargoSerializer

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','status':'success','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            paginacion = self.request.query_params.get('sin_paginacion', None)

            queryset = super(CargoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            empresa_filtro=self.request.query_params.get('empresa_filtro', None)
            if empresa_filtro:
                empresa_id = empresa_filtro
                qset=(Q(cliente_id=empresa_id))
            else:
                if request.user.cargo:
                    empresa_id = request.user.cargo.cliente.id
                    qset=(Q(cliente_id=empresa_id))
                else:
                    return Response({ResponseNC.message:'El usuario actual no tiene un cargo y no se pueden definir sus permisos','success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
                
            if dato:
                qset = qset & (Q(nombre__icontains=dato))
                queryset = self.model.objects.filter(qset)

            if paginacion==None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok',
                    'data':serializer.data})

                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
            else:
                serializer = self.get_serializer(queryset,many=True)
                return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor' + str(e),'status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                serializer = CargoSerializer(data=request.data,context={'request': request})

                if serializer.is_valid():
                    serializer.save(cliente_id=request.data['cliente_id'])
                    return Response({ResponseNC.message:'El registro ha sido guardado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = CargoSerializer(instance,data=request.data,context={'request': request},partial=partial)
                if serializer.is_valid():
                    serializer.save(cliente_id=request.data['cliente_id'])
                    return Response({ResponseNC.message:'El registro ha sido actualizado exitosamente','success':'ok',
                    ResponseNC.data:serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({ResponseNC.message:serializer.errors,'success':'fail',
                    ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({ResponseNC.message:'Se presentaron errores al procesar los datos' + str(e),'success':'error',
                ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({ResponseNC.message:'El registro se ha eliminado correctamente','success':'ok',
            ResponseNC.data:''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({ResponseNC.message:'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error',
            ResponseNC.data:''},status=status.HTTP_400_BAD_REQUEST)

    

#Fin Api rest para Cargo
class EmpresaViewSet(viewsets.ModelViewSet):
    """
	Retorna una lista de empresas, puede utilizar el parametro <b>{dato=[texto a buscar]}</b>, a traves del cual, se podra buscar por todo o parte del nombre y nit.<br/>
    """
    model=Empresa
    queryset = model.objects.all()
    serializer_class = EmpresaSerializer
    paginate_by = 15
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(EmpresaViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_empresa = self.request.query_params.get('id_empresa', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if (dato):
                qset = (Q(nombre__icontains=dato)|Q(rut__icontains=dato))
                if id_empresa:
                    if dato:
                        qset=qset&(Q(empresa_id=id_empresa))
                    else:
                        qset=(Q(empresa_id=id_empresa))
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
        
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):

        if request.method == 'POST':				
            try:
                serializer = EmpresaSerializer(data=request.data,context={'request': request})
                empresa = Empresa.objects.filter(rut=request.data['rut'])

                if empresa:
                    return Response({'message':'Ya existe una empresa registrada con el rut digitado','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)
                
                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':serializer.data},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
    
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = EmpresaSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class EmpresaContactoViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT de Empresa contacto o la relación de una empresa y sus contactos.
    """
    model=ContactoEmpresa
    queryset = model.objects.all()
    serializer_class = EmpresaContactoSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un contacto
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de contatos, se puede buscar por empresa o por rut.
        '''
        try:
            queryset = super(EmpresaContactoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)

            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if (dato):
                qset = (Q(persona__nombre__icontains=dato)|Q(persona__rut__icontains=dato))
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
        
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea un nuevo contacto, requiere id_empresa e id_persona.
        '''
        if request.method == 'POST':				
            try:
                serializer = EmpresaContactoSerializer(data=request.data,context={'request': request})
                
                if serializer.is_valid():
                    serializer.save(empresa_id=request.data['empresa_id'],persona_id=request.data['persona_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza contacto, Envia el contacto con sus cambios.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = EmpresaContactoSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(empresa_id=request.data['empresa_id'],persona_id=request.data['persona_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina un contacto.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class EstadoViewSet(viewsets.ModelViewSet):
    """
		Retorna una lista de estados, puede utilizar el parametro <b>{dato=[texto a buscar]}</b>, a traves del cual, se podra buscar por todo o parte del nombre y aplicacion.<br/>
		Igualmente puede utilizar los siguientes parametros:<br/><br/>
		<b>{aplicacion=TEXTO}</b>: Retorna la lista de estados  con el nombre de la aplicacion del TEXTO escrito.<br/>
		Es posible utilizar los parametros combinados, por ejemplo: buscar en la lista de estados aquellos que contentan determinado texto en su nombre o aplicacion.
	"""
    model=Estado
    queryset = model.objects.all()
    serializer_class = EstadoSerializer
    parser_classes=(FormParser, MultiPartParser,)
    paginate_by = 10

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(EstadoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            aplicacion= self.request.query_params.get('aplicacion',None)
			
            if (dato or aplicacion):
                if dato:
                    qset = (Q(nombre__icontains=dato) | Q(app__icontains=dato))
                if aplicacion:
                    qset = (Q(app__exact=aplicacion))

                queryset = self.model.objects.filter(qset).order_by('orden')
			#utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
            serializer = self.get_serializer(queryset,many=True)
            return Response({'message':'','success':'ok','data':serializer.data})			
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class TipoViewSet(viewsets.ModelViewSet):
    """
		Retorna una lista de tipos, puede utilizar el parametro <b>{dato=[texto a buscar]}</b>, a traves del cual, se podra buscar por todo o parte del nombre y aplicacion.<br/>
		Igualmente puede utilizar los siguientes parametros:<br/><br/>
		<b>{aplicacion=TEXTO}</b>: Retorna la lista de estados  con el nombre de la aplicacion del TEXTO escrito.<br/>
		Es posible utilizar los parametros combinados, por ejemplo: buscar en la lista de estados aquellos que contentan determinado texto en su nombre o aplicacion.
	"""
    model=Tipo
    queryset = model.objects.all()
    serializer_class = TipoSerializer
    parser_classes=(FormParser, MultiPartParser,)
    paginate_by = 10

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(TipoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            aplicacion= self.request.query_params.get('aplicacion',None)
			
            if (dato or aplicacion):
                if dato:
                    qset = (Q(nombre__icontains=dato) | Q(app__icontains=dato))
                if aplicacion:
                    qset = (Q(app__exact=aplicacion))

                queryset = self.model.objects.filter(qset).order_by('orden')
			#utilizar la variable ignorePagination para quitar la paginacion
            ignorePagination= self.request.query_params.get('ignorePagination',None)
            if ignorePagination is None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page,many=True)	
                    return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})
            
            serializer = self.get_serializer(queryset,many=True)
            return Response({'message':'','success':'ok','data':serializer.data})			
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PersonaViewSet(viewsets.ModelViewSet):
    """
	Retorna una lista de personas, puede utilizar el parametro <b>{dato=[texto a buscar]}</b>, a traves del cual, se podra buscar por todo o parte del nombre y rut.<br/>
    """
    model=Persona
    queryset = model.objects.all()
    serializer_class = PersonaSerializer
    paginate_by = 15
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(PersonaViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)

            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if (dato):
                qset = (Q(nombre__icontains=dato)|Q(rut__icontains=dato))
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
        
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):

        if request.method == 'POST':				
            try:
                datos = request.data;
                serializer = PersonaSerializer(data=request.data,context={'request': request})
                persona = Persona.objects.filter(rut=request.data['rut'])

                if persona:
                    return Response({'message':'Ya existe una persona registrada con el rut digitado','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)
                
                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos (' + str(e) + ')','success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
    
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = PersonaSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class ProyectoViewSet(viewsets.ModelViewSet):
    """
	Retorna una lista de proyectos, puede utilizar el parametro <b>{dato=[texto a buscar]}</b>, a traves del cual, se podra buscar por todo o parte del nombre y descripcion.<br/>
    """
    model=Proyecto
    queryset = model.objects.all()
    serializer_class = ProyectoSerializer
    paginate_by = 25
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = super(ProyectoViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)

            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if (dato):
                qset = (Q(nombre__icontains=dato)|Q(descripcion__icontains=dato))
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
        
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):

        if request.method == 'POST':				
            try:
                serializer = ProyectoSerializer(data=request.data,context={'request': request})
                qset = (Q(nombre=request.data['nombre'])&Q(empresa_id=request.data['empresa_id']))
                proyecto = Proyecto.objects.filter(qset)
                
                if proyecto:
                    return Response({'message':'ya existe un proyecto con con el nombre ' + request.data['nombre'] + ' para la empresa escogida','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'],empresa_id=request.data['empresa_id'],contacto_id=request.data['contacto_id'],
                    tipo_id=request.data['tipo_id'],estado_id=request.data['estado_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as ei:
                return Response({'message':'ya existe un proyecto con con el nombre ' + request.data['nombre'] + ' para la empresa escogida','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
    
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = ProyectoSerializer(instance,data=request.data,context={'request': request},partial=partial)

                if serializer.is_valid():
                    serializer.save(municipio_id=request.data['municipio_id'],empresa_id=request.data['empresa_id'],
                    tipo_id=request.data['tipo_id'],estado_id=request.data['estado_id'],contacto_id=request.data['contacto_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as ei:
                return Response({'message':'ya existe un proyecto con con el nombre ' + request.data['nombre'] + ' para la empresa escogida','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

class ProyectoUsuarioViewSet(viewsets.ModelViewSet):
    """
	API ENDPOINT de Proyecto usuario o la relación de un proyecto y sus usuarios.
    """
    model=ProyectoUsuario
    queryset = model.objects.all()
    serializer_class = ProyectoUsuarioSerializer
    paginate_by = 20
    nombre_modulo=''

    def retrieve(self,request,*args, **kwargs):
        '''
        Devuelve un usuario de un proyecto
        '''
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({'message':'','success':'ok','data':serializer.data})
        except Exception as e:
            return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        '''
        Retorna una lista de usuarios asociados a proyectos, se puede buscar por usuario(id_usuario) o por nombre. la variable sin_paginacion indica que no paginaremos el resultado
        '''
        try:
            queryset = super(ProyectoUsuarioViewSet, self).get_queryset()
            dato = self.request.query_params.get('dato', None)
            id_usuario = self.request.query_params.get('id_usuario', None)
            sin_paginacion= self.request.query_params.get('sin_paginacion',None)

            if (dato or id_usuario):
                qset = (Q(persona__nombre__icontains=dato)|Q(user__username__icontains=dato))
                
                if id_usuario:
                    if dato:
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
        
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        '''
        Crea la relacion de usuario y proyecto, requiere proyecto_id , usuario_id, cargo_id.
        '''
        if request.method == 'POST':				
            try:
                serializer = ProyectoUsuarioSerializer(data=request.data,context={'request': request})
                qset = (Q(proyecto_id=request.data['proyecto_id'])&Q(usuario_id=request.data['usuario_id']))
                proyectoUsu = ProyectoUsuario.objects.filter(qset)
                
                if proyectoUsu:
                    return Response({'message':'El trabajador ya fue asignado a este proyecto','success':'fail',
                    'data':''},status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'],usuario_id=request.data['usuario_id'],
                    cargo_id=request.data['cargo_id'])
                    return Response({'message':'El registro ha sido guardado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            
            except Exception as e:
                return Response({'message':'Se presentaron errores al procesar los datos ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        '''
        Actualiza la relacion.
        '''
        if request.method == 'PUT':
            try:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer = ProyectoUsuarioSerializer(instance,data=request.data,context={'request': request},partial=partial)
				
                if serializer.is_valid():
                    serializer.save(proyecto_id=request.data['proyecto_id'],usuario_id=request.data['usuario_id'],
                    cargo_id=request.data['cargo_id'])
                    return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok','data':serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':serializer.errors,'success':'fail','data':''},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):
        '''
        Elimina un usuario de un proyecto.
        '''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message':'El registro se ha eliminado correctamente','success':'ok','data':''},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Se presentaron errores de comunicacion con el servidor ' + str(e),'success':'error','data':''},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def listaProyectosConUsuarios(request):
    '''
    Retorna una lista de proyectos del usuario
    '''
    try:
        #id_usuario = request.user.id
        ListPendientes = []
        #qset=(Q(usuario_id=id_usuario))
        ListProyectos = Proyecto.objects.all()
        for item in ListProyectos:
            qset=(Q(proyecto_id=item.id))
            usuarios = ProyectoUsuario.objects.filter(qset)
            cantidad = len(usuarios)
            supervisor = ""
            contacto = ""
            if usuarios:
                if usuarios[0].usuario.persona:
                    supervisor = usuarios[0].usuario.persona.nombre + " " + usuarios[0].usuario.persona.primerApellido

            lista={
                    "id": item.id,
                    "nombre": item.nombre,
                    "municipio": item.municipio.nombre,
                    "descripcion": item.descripcion,
                    "longitud": item.longitud,
                    "latitud": item.longitud,
                    "empresa": item.empresa.nombre,
                    "idProyecto": item.idProyecto,
                    "nombreCalle": item.nombreCalle,
                    "ip":item.ip,
                    "usuarios":cantidad,
                    "supervisor":supervisor
            }
            ListPendientes.append(lista)

        return Response({'message':'','success':'ok','data':ListPendientes})	
        
    except Exception as e:
        return Response({'message':'Se presentaron errores de comunicacion con el servidor (' + str(e) + ')','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

