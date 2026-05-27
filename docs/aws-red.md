# VPC y arquitectura de red en AWS

## ¿Qué es una VPC?

Una VPC (Virtual Private Cloud) es una red virtual privada dentro de AWS donde se crean y organizan los recursos cloud.

La VPC permite:
- Definir rangos de IP privadas.
- Crear subredes.
- Configurar rutas y acceso a Internet.
- Aislar recursos de otras redes de AWS.

Todos los recursos deben estar dentro de una VPC porque AWS necesita una red donde conectar instancias, bases de datos y servicios.

La VPC aísla:
- Tráfico de red
- Direcciones IP
- Recursos internos

---

# Subred pública y privada

## Subred pública

Una subred pública tiene acceso directo a Internet mediante un Internet Gateway.

Normalmente se utilizan para:
- Instancias EC2
- Servidores web
- Bastion hosts

## Subred privada

Una subred privada no tiene acceso directo a Internet.

Se utiliza para:
- Bases de datos RDS
- Servicios internos
- Recursos sensibles

Esto mejora la seguridad porque los recursos no quedan expuestos públicamente.

---

# Configuración realizada

## VPC creada

```txt
asir-vpc
```
---

# Diagrama de arquitectura de red

```text
                         INTERNET
                              |
                              v
                     +----------------+
                     | Internet Gateway|
                     +----------------+
                              |
                              v
========================================================
|                    VPC: asir-vpc                     |
|                  CIDR: 10.0.0.0/16                  |
|                                                      |
|  +-----------------------------------------------+   |
|  | Subred pública: asir-public                  |   |
|  | CIDR: 10.0.1.0/24                            |   |
|  | Availability Zone: eu-west-1a                |   |
|  |                                               |   |
|  | Recursos:                                     |   |
|  | - EC2 pública                                 |   |
|  +-----------------------------------------------+   |
|                                                      |
|                                                      |
|  +-----------------------------------------------+   |
|  | Subred privada: asir-private                 |   |
|  | CIDR: 10.0.2.0/24                            |   |
|  | Availability Zone: eu-west-1b                |   |
|  |                                               |   |
|  | Recursos:                                     |   |
|  | - Base de datos RDS                           |   |
|  +-----------------------------------------------+   |
|                                                      |
========================================================

```
# TABLA DE RUTAS

## SUBRED PUBLICA

Destino: 0.0.0.0/0
Target: Internet Gateway

La subred publica tiene acceso a internet.

## SUBRED PRIVADA 

Sin ruta directa hacia Internet

La subred privada permanece aislada por seguridad.

# Documentación AWS: Direccionamiento IP en EC2

En el despliegue de infraestructura en Amazon Web Services (AWS), es fundamental comprender cómo gestionar el direccionamiento IP de las instancias EC2 para garantizar la disponibilidad y continuidad de los servicios.

## IP Pública Dinámica vs. Elastic IP (IP Estática)

A continuación se detallan las diferencias clave entre ambos tipos de direcciones IP:

| Característica | IP Pública Dinámica | Elastic IP (IP Elástica) |
| :--- | :--- | :--- |
| **Persistencia** | Se libera cuando la instancia se detiene (Stop) o se termina (Terminate). Al volver a iniciar la instancia, se asigna una nueva IP. | Permanece asociada a tu cuenta de AWS y a la instancia hasta que decidas liberarla manualmente, sin importar los reinicios o detenciones. |
| **Costo** | Es gratuita mientras la instancia esté asociada y en ejecución. | Es gratuita mientras esté asociada a una instancia *en ejecución*. AWS cobra una tarifa si la Elastic IP está reservada pero no está asociada a ninguna máquina (o si la máquina está apagada). |
| **Uso Principal** | Entornos de desarrollo, pruebas temporales o instancias detrás de un balanceador de carga (Load Balancer). | Servidores de producción, servidores web directos, servidores DNS y servicios que requieren endpoints fijos. |

## ¿Cuándo es necesaria una Elastic IP?

Una **Elastic IP** es indispensable en los siguientes escenarios:

1. **Servidores Web Directos sin Balanceador:** Si apagas una instancia para hacer un mantenimiento (por ejemplo, cambiar el tipo de instancia a una más potente) y dependes de una IP dinámica, al encenderla tu IP cambiará. Esto rompería la configuración de tus dominios (registros DNS tipo A) y tus usuarios no podrían acceder hasta que actualices los DNS (lo cual puede tardar horas en propagarse).
2. **Políticas de Seguridad y Listas Blancas (Whitelisting):** Si tu servidor EC2 necesita comunicarse con una API externa de un cliente o un proveedor que requiere "filtrar por IP" para darte acceso, necesitas una IP fija. Si tu IP cambia en cada reinicio, te bloquearán el acceso.
3. **Servidores de Correo (SMTP) y VPNs:** Los servicios de pasarelas VPN (como túneles IPSec) o servidores de correo electrónico corporativo requieren una IP estática confiable que no cambie y que pueda configurarse con registros PTR (DNS Inverso) para evitar caer en carpetas de SPAM.
4. **Recuperación Rápida ante Fallos (Failover):** Si tu servidor principal falla, puedes reasignar rápidamente tu Elastic IP a una instancia de respaldo en cuestión de segundos. Para el mundo exterior, la IP sigue siendo la misma, minimizando el tiempo de inactividad.