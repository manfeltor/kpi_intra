from django.db import models

# Create your models here.

from django.db import models

class bdoms(models.Model):

    pedido = models.CharField(max_length=50, null=True)
    flujo = models.CharField(max_length=2, null=True)
    seller = models.CharField(max_length=50, null=True)
    sucCodigo = models.CharField(max_length=100, null=True)
    # sucursal = models.CharField(max_length=50, null=True)
    estadoPedido = models.CharField(max_length=30, null=True)
    fechaCreacion = models.DateTimeField(null=True)
    # fechaPactada = models.DateTimeField(null=True)
    # franjaHoraria1 = models.CharField(max_length=10, null=True)
    # franjaHoraria2 = models.CharField(max_length=10, null=True)
    # fechaConfirmacion = models.DateTimeField(null=True)
    # fechaColecta = models.DateTimeField(null=True)
    fechaRecepcion = models.DateTimeField(null=True)
    fechaDespacho = models.DateTimeField(null=True)
    fechaEntrega = models.DateTimeField(null=True)
    # diffMmConfirmacionCreacion = models.CharField(max_length=20, null=True)
    # diffMmConfirmacionColecta = models.CharField(max_length=20, null=True)
    # diffMmColectaEntrega = models.CharField(max_length=20, null=True)
    # diffMmCreacionEntrega = models.CharField(max_length=20, null=True)
    # remito = models.CharField(max_length=50, null=True)
    # ruta = models.CharField(max_length=50, null=True)
    # orden = models.CharField(max_length=5, null=True)
    lpn = models.CharField(max_length=100, primary_key=True)
    estadoLpn = models.CharField(max_length=50, null=True)
    # sku = models.CharField(max_length=100, null=True)
    # skuDescripcion = models.CharField(max_length=200, null=True)
    # unidades = models.IntegerField(null=True)
    # bulto = models.IntegerField(null=True)
    # bultosPedido = models.IntegerField(null=True)
    # alto = models.FloatField(null=True)
    # ancho = models.FloatField(null=True)
    # largo = models.FloatField(null=True)
    # peso = models.FloatField(null=True)
    # valorDeclarado = models.CharField(max_length=10, null=True)
    # almacen = models.CharField(max_length=50, null=True)
    # ubicacion = models.CharField(max_length=20, null=True)
    # fechaGuardado = models.DateTimeField(null=True)
    # nombre = models.CharField(max_length=50, null=True)
    # documento = models.CharField(max_length=20, null=True)
    # direccion = models.CharField(max_length=200, null=True)
    # calle = models.CharField(max_length=50, null=True)
    # numero = models.CharField(max_length=50, null=True)
    # telefono = models.CharField(max_length=50, null=True)
    # provincia = models.CharField(max_length=50, null=True)
    # localidad = models.CharField(max_length=50, null=True)
    # zona = models.CharField(max_length=10, null=True)
    # transporte = models.CharField(max_length=50, null=True)
    # observaciones = models.CharField(max_length=200, null=True)
    # trackingColecta = models.CharField(max_length=50, null=True)
    trackingDistribucion = models.CharField(max_length=50, null=True)
    trackingTransporte = models.CharField(max_length=50, null=True)
    # rutaAnterior = models.CharField(max_length=10, null=True)
    # ordenAnterior = models.CharField(max_length=4, null=True)
    # rutaColecta = models.CharField(max_length=50, null=True)
    # ordenColecta = models.CharField(max_length=50, null=True)
    # pallet = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=6, null=True)
    # dock = models.CharField(max_length=50, null=True)
    # latitud = models.CharField(max_length=50, null=True)
    # longitud = models.CharField(max_length=50, null=True)
    # m3 = models.FloatField(null=True)
    # mail = models.EmailField(max_length=50, null=True)
    codigoPostal = models.CharField(max_length=5, null=True)
    tte = models.CharField(max_length=50, null=True)
    # tteDireccion = models.CharField(max_length=200, null=True)
    # tteProvincia = models.CharField(max_length=20, null=True)
    # tteLocalidad = models.CharField(max_length=20, null=True)
    # tteNotas = models.CharField(max_length=200, null=True)
    # tteFranjaHoraria1 = models.CharField(max_length=10, null=True)
    # tteFranjaHoraria2 = models.CharField(max_length=10, null=True)
    # metodoEnvio = models.CharField(max_length=50, null=True)
    # proveedor = models.CharField(max_length=50, null=True)
    # costo = models.FloatField(null=True)
    # precioVenta = models.CharField(max_length=7, null=True)
    tteSucursalDistribucion = models.CharField(max_length=3, null=True)
    tiendaEntrega = models.CharField(max_length=50, null=True)
    # distancia = models.CharField(max_length=7, null=True)
    # excedente = models.CharField(max_length=7, null=True)
    # pesoAforado = models.CharField(max_length=7, null=True)
    # express = models.CharField(max_length=50, null=True)
    # repartidor = models.CharField(max_length=50, null=True)