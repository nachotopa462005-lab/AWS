# Informe final del despliegue en AWS

## Resumen del proyecto

El proyecto despliega una aplicacion FastAPI en una instancia EC2 dentro de una VPC propia. La aplicacion se publica mediante NGINX como proxy inverso y usa una base de datos PostgreSQL gestionada en Amazon RDS. Para almacenamiento de copias de seguridad se utiliza Amazon S3 con una politica de ciclo de vida hacia Glacier Instant Retrieval.

El repositorio contiene la documentacion tecnica, el stack Docker de la aplicacion, la configuracion de NGINX, un script de backup a S3 y una plantilla CloudFormation de referencia para recrear la infraestructura principal.

## Servicios utilizados

- IAM: usuarios administrativos, usuario de solo lectura, MFA y roles para EC2.
- VPC: red privada `asir-vpc` con subred publica y subred privada.
- EC2: instancia Ubuntu 22.04 LTS `t2.micro` para ejecutar Docker, NGINX y FastAPI.
- Elastic IP: direccion publica fija asociada a la instancia EC2.
- S3: bucket privado `asir-backups-<tu-nombre>` para backups.
- RDS: PostgreSQL 15 en subred privada, sin acceso publico.
- Security Groups: control de acceso a EC2 y RDS.
- Application Load Balancer, ACM y Route 53: capa opcional de alta disponibilidad, HTTPS y dominio personalizado.

## Arquitectura

```text
Usuario
  |
  v
DNS / Route 53
  |
  v
Application Load Balancer o Elastic IP
  |
  v
Internet Gateway
  |
  v
VPC asir-vpc 10.0.0.0/16
  |
  +-- Subred publica asir-public 10.0.1.0/24
  |     |
  |     +-- EC2 Ubuntu 22.04 t2.micro
  |           |
  |           +-- NGINX puerto 80/443
  |           +-- FastAPI backend
  |
  +-- Subred privada asir-private 10.0.2.0/24
        |
        +-- RDS PostgreSQL 15 db.t3.micro

S3 asir-backups-<tu-nombre>
  ^
  |
Rol IAM rol-ec2-s3 asociado a EC2
```

## Red y seguridad

La VPC separa la parte publica de la parte privada. La EC2 se ubica en la subred publica porque debe recibir trafico HTTP/HTTPS desde Internet. RDS se ubica en la subred privada y no tiene IP publica.

El grupo de seguridad `sg-ec2-web` permite:

- SSH, puerto 22, solo desde la IP publica del administrador.
- HTTP, puerto 80, desde cualquier origen.
- HTTPS, puerto 443, desde cualquier origen.

El grupo de seguridad `sg-rds` permite:

- PostgreSQL, puerto 5432, solo desde `sg-ec2-web`.

Con esta configuracion, la base de datos no queda expuesta a Internet y solo acepta conexiones iniciadas desde la instancia EC2.

## Despliegue de aplicacion

En la EC2 se instalaron Docker y Docker Compose. El repositorio se copio al servidor y se creo un archivo `.env` directamente en la instancia, sin subirlo a Git.

Comandos usados en la EC2:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f backend
```

El archivo `.env` debe contener al menos:

```env
DATABASE_URL=postgresql://<usuario>:<password>@<endpoint-rds>:5432/<nombre-bd>
```

## Pruebas realizadas

Las pruebas funcionales estan documentadas en `docs/pruebas-funcionamiento.md`.

Resumen:

- La AWS CLI queda configurada con el usuario IAM `asir-admin`.
- `aws sts get-caller-identity` devuelve el ARN del usuario `asir-admin`.
- La instancia EC2 queda en estado `running`.
- El backend FastAPI responde a traves de NGINX.
- La ruta `/docs` de FastAPI es accesible.
- La aplicacion se conecta a RDS PostgreSQL desde la EC2.
- Los endpoints `/inventario` y `/logs` consumen datos desde RDS.
- Al detener el contenedor `backend`, NGINX devuelve un error 502.
- Al reiniciar el servicio, la aplicacion vuelve a responder.
- El rol `rol-ec2-s3` permite subir y leer objetos del bucket S3 sin guardar credenciales en la instancia.

## Infraestructura como codigo

La carpeta `infra/cloudformation/` contiene una plantilla CloudFormation de referencia:

```text
infra/cloudformation/asir-stack.yml
```

La plantilla define la VPC, subredes, Internet Gateway, tablas de rutas, Security Groups, rol IAM para S3, bucket de backups con ciclo de vida a Glacier Instant Retrieval, instancia EC2, Elastic IP y una instancia RDS PostgreSQL.

Ejemplo de despliegue:

```bash
aws cloudformation deploy \
  --template-file infra/cloudformation/asir-stack.yml \
  --stack-name asir-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    KeyName=asir-keypair \
    AdminCidr=<tu-ip-publica>/32 \
    BackupBucketName=asir-backups-<tu-nombre> \
    DbUsername=<usuario-rds> \
    DbPassword=<password-segura>
```

## Conclusiones

El proyecto cumple el objetivo principal: desplegar una aplicacion backend en AWS usando una arquitectura separada por capas, con red propia, instancia EC2 publica, base de datos RDS privada, backups en S3 y controles de seguridad mediante IAM y Security Groups.

La mejora natural para produccion seria dejar todo el aprovisionamiento gestionado exclusivamente con CloudFormation o Terraform, usar HTTPS con ALB y ACM como punto de entrada unico, y mantener las evidencias de pruebas actualizadas tras cada despliegue.
