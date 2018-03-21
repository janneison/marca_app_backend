from django.contrib.auth.models import Group
from rest_framework import serializers
from parametrizacion.models import (Pais, Region, Municipio, Empresa, Cargo, 
User, ContactoEmpresa, Persona, Estado, Tipo, Proyecto, ProyectoUsuario)
from asistencia.models import (Horario, Asistencia, Retraso)
from rest_framework.validators import UniqueValidator
import datetime
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PaisSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Pais
		fields=('id','nombre','validaRut')

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    pais_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Pais.objects.all())
    pais = PaisSerializer(read_only=True)
    class Meta:
        model = Region
        fields=('id','nombre','pais','pais_id')

class MunicipioSerializer(serializers.HyperlinkedModelSerializer):
    
    region_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Region.objects.all())
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Municipio
        fields=('id','nombre','region','region_id')

class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    proyectos = serializers.SerializerMethodField('_contadorProyecto',read_only=True)
    usuarios = serializers.SerializerMethodField('_proyectoUsuarios',read_only=True)
    puntualidad = serializers.SerializerMethodField('_puntualidad',read_only=True)
	#logo = serializers.ImageField(required=False)
    def _contadorProyecto(self,obj):
        usuarios = Proyecto.objects.filter(empresa_id=obj.id)
        cantidad = len(usuarios)
        return cantidad
    
    def _proyectoUsuarios(self,obj):
        usuarios = Proyecto.objects.filter(empresa_id=obj.id)
        cantidad = len(usuarios)
        return cantidad
    
    def _puntualidad(self,obj):
        horario = Horario.objects.filter(proyecto__empresa_id=obj.id).first()
        asistencias = Asistencia.objects.filter(proyecto__empresa_id=obj.id)
        cantidad = 0
        if horario:
            for item in asistencias:
                diferencia = item.horaEntrada.minute - horario.horaInicio.minute
                cantidad = diferencia
             
        return cantidad

    class Meta:
        model = Empresa
        fields=('url','id','nombre','rut','direccion','correoElectronico',
        'telefono','telefonoFijo','municipio','municipio_id','field','usuarios','proyectos',
        'numero','estado','fechaEstadoProyecto','puntualidad')

#Api rest para Cargo
class CargoSerializer(serializers.HyperlinkedModelSerializer):
    cliente = EmpresaSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    class Meta:
        model = Cargo
        fields=('id','nombre','cliente_id','cliente','nivel')

class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    class Meta:
        model = Persona
        fields=('url','id','nombre','primerApellido','segundoApellido','rut','genero','estadoCivil',
        'correoElectronico','telefono','telefono2','telefonoFijo','municipio','municipio_id','fechaNacimiento',
        'numero','nombreCalle','cargo','descripcionCargo','nacionalidad')

class EmpresaContactoSerializer(serializers.HyperlinkedModelSerializer):
    persona=PersonaSerializer(read_only=True)
    persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())
    empresa=EmpresaSerializer(read_only=True)
    empresa_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    class Meta:
        model = ContactoEmpresa
        fields=('id','persona','persona_id','empresa','empresa_id','cargo')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8,write_only=True)
    persona=PersonaSerializer(read_only=True)
    persona_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all())
    cargo=CargoSerializer(read_only=True)
    cargo_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Cargo.objects.all())
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'email', 'password','groups','username','id','persona','persona_id','cargo','cargo_id')
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        return user
    
class EstadoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Estado
        fields=('id', 'app', 'nombre', 'icono', 'color','orden')

class TipoSerializer(serializers.HyperlinkedModelSerializer):
    	
    class Meta:
        model = Tipo
        fields=( 'id','app', 'nombre' , 'icono' , 'color')

class ProyectoSerializer(serializers.HyperlinkedModelSerializer):
    municipio_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Municipio.objects.all())
    municipio = MunicipioSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Estado.objects.all(),allow_null=True)
    #estado = EstadoSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Tipo.objects.all(),allow_null=True)
    #tipo = EstadoSerializer(read_only=True)
    usuarios = serializers.SerializerMethodField('_contadorProyecto',read_only=True)
    supervisor = serializers.SerializerMethodField('_proyectoSupervisor',read_only=True)
    puntualidad = serializers.SerializerMethodField('_puntualidad',read_only=True)
    empresa=EmpresaSerializer(read_only=True)
    empresa_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
    contacto=PersonaSerializer(read_only=True)
    contacto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Persona.objects.all(),allow_null=True)

    def _contadorProyecto(self,obj):
        usuarios = ProyectoUsuario.objects.filter(proyecto_id=obj.id)
        cantidad = len(usuarios)
        return cantidad
    
    def _puntualidad(self,obj):
        horario = Horario.objects.filter(proyecto_id=obj.id).first()
        asistencias = Asistencia.objects.filter(proyecto_id=obj.id)
        cantidad = 0
        if horario:
            for item in asistencias:
                diferencia = item.horaEntrada.minute - horario.horaInicio.minute
                cantidad = diferencia
             
        return cantidad
    
    def _proyectoSupervisor(self,obj):
        usuarios = ProyectoUsuario.objects.filter(proyecto_id=obj.id)
        supervisor = ""
        if usuarios:
            if usuarios[0].usuario.persona:
                supervisor = usuarios[0].usuario.persona.nombre + " " + usuarios[0].usuario.persona.primerApellido

        return supervisor

    class Meta:
        model = Proyecto
        fields=('url','id','nombre','descripcion','valorAdjudicado','latitud','longitud','fechaInicio',
        'fechaFin','municipio','municipio_id','empresa','empresa_id','estado_id','tipo_id',
        'idProyecto','nombreCalle','numero','codigoPostal','ip','contacto','contacto_id','supervisor','usuarios','puntualidad')

class ProyectoUsuarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario=UserSerializer(read_only=True)
    usuario_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=User.objects.all())
    cargo=CargoSerializer(read_only=True)
    cargo_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Cargo.objects.all())
    proyecto=ProyectoSerializer(read_only=True)
    proyecto_id=serializers.PrimaryKeyRelatedField(write_only=True,queryset=Proyecto.objects.all())
    class Meta:
        model = ProyectoUsuario
        fields=('id','usuario','usuario_id','proyecto','proyecto_id','cargo','cargo_id','desde','hasta','horas')