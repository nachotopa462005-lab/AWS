# AWS - Teoría

## ¿Qué es la computación en la nube?

La computación en la nube consiste en usar servidores, almacenamiento y otros recursos por Internet sin tener que comprar hardware físico. Esto permite acceder a servicios de forma rápida, flexible y pagando solo por lo que se utiliza.

---

# Modelos de servicios cloud

## IaaS

Infrastructure as a Service.  
El proveedor ofrece la infraestructura (servidores, red, almacenamiento) y el usuario administra el sistema operativo y las aplicaciones.

Ejemplo:
- AWS EC2

## PaaS

Platform as a Service.  
El proveedor también administra el sistema operativo y la plataforma. El usuario solo desarrolla y despliega aplicaciones.

Ejemplo:
- AWS Elastic Beanstalk

## SaaS

Software as a Service.  
El usuario utiliza directamente una aplicación desde Internet sin administrar nada.

Ejemplo:
- Gmail
- Netflix

## ¿Qué modelo usa EC2?

AWS EC2 pertenece al modelo **IaaS**.

---

# Modelo de responsabilidad compartida

AWS utiliza un modelo donde tanto AWS como el cliente tienen responsabilidades.

## AWS se encarga de:
- Hardware
- Centros de datos
- Red física
- Infraestructura cloud

## El usuario se encarga de:
- Configuración de EC2
- Usuarios y permisos
- Seguridad del sistema
- Datos y aplicaciones

---

# Conceptos importantes

## Región (Region)

Ubicación geográfica donde AWS tiene centros de datos.

## Availability Zone

Centro de datos dentro de una región. Sirve para mejorar disponibilidad y redundancia.

## VPC

Red virtual privada dentro de AWS.

## Subnet

División de una VPC.

## Security Group

Firewall virtual que controla el tráfico de entrada y salida.

## AMI

Plantilla utilizada para crear instancias EC2.

## Instancia EC2

Máquina virtual dentro de AWS.

---

# AWS Free Tier

El Free Tier permite usar algunos servicios gratis durante 12 meses.

## EC2
- 750 horas mensuales de t2.micro/t3.micro
- 1 vCPU y 1 GB RAM

## S3
- 5 GB de almacenamiento
- 20.000 solicitudes GET

## RDS
- 750 horas mensuales db.t2.micro
- 20 GB de almacenamiento

---

# Conclusión

AWS permite trabajar con infraestructura en la nube de forma flexible y escalable. EC2 es un servicio IaaS que ofrece máquinas virtuales, mientras que el Free Tier facilita aprender AWS gratuitamente durante el primer año.


## Seguridad de la cuenta root

La cuenta root tiene acceso total a todos los recursos de AWS.  
Por seguridad, no debe utilizarse para tareas diarias, ya que un error o robo de credenciales podría comprometer toda la cuenta.

Lo recomendable es usar usuarios IAM con permisos específicos y dejar la cuenta root solo para tareas críticas de administración.

# Amazon S3 Glacier

Amazon S3 Glacier es un servicio de almacenamiento de bajo coste diseñado para backups y archivos que no necesitan acceso frecuente.

Permite guardar datos a largo plazo pagando menos que en almacenamiento estándar.

Tiene sentido usar Glacier para:
- copias de seguridad,
- archivos históricos,
- recuperación ante desastres,
- o datos que se consultan pocas veces.

# Flujo de una Petición HTTP en el Stack ASIR

El camino que recorre una petición desde que el usuario interactúa con la aplicación hasta que se consultan los datos se compone de los siguientes eslabones:

1. **Navegador (Cliente):** El usuario introduce la URL o realiza una acción en la interfaz web (ej. consultar el inventario).
2. **DNS:** El sistema de nombres de dominio traduce el dominio amigable (si lo hubiera) en la dirección IP pública correspondiente.
3. **Elastic IP:** La petición llega a la IP estática y pública asociada a nuestra instancia EC2 en AWS, atravesando el Internet Gateway y los Security Groups correspondientes.
4. **NGINX (Proxy Inverso):** Recibe la petición en el puerto 80/443 de la EC2. Evalúa las reglas de configuración y redirige el tráfico internamente hacia el contenedor del backend a través de la red interna de Docker. (Si el backend está caído, aquí es donde NGINX intercepta la desconexión y responde con un error 502).
5. **FastAPI (Backend):** El framework procesa la solicitud HTTP entrante, ejecuta la lógica de negocio del endpoint solicitado y traduce la petición en una consulta SQL mediante la variable `DATABASE_URL`.
6. **RDS PostgreSQL (Base de Datos):** La consulta viaja de forma segura por la subred privada `asir-private` (restringida por el grupo de seguridad `sg-rds`) hasta la instancia de base de datos administrada, la cual procesa la consulta y devuelve los registros solicitados al backend para hacer el camino de vuelta hacia el navegador del usuario.