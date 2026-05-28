![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-RDS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

# Proyecto AWS ASIR

## Descripcion

Aplicacion **FastAPI** desplegada con **Docker Compose** y **NGINX**, conectada a **PostgreSQL en Amazon RDS**.  
El proyecto incluye documentacion teorica y tecnica sobre AWS, IAM, VPC, EC2, S3, RDS, backups, pruebas de funcionamiento e infraestructura como codigo con CloudFormation.

---

## Despliegues

| Entorno | URL |
| --- | --- |
| Local | `http://localhost` |
| Swagger local | `http://localhost/docs` |
| AWS EC2 | `http://<elastic-ip>` |
| Swagger AWS | `http://<elastic-ip>/docs` |

> No se suben IPs reales, endpoints privados, claves, `.env`, passwords ni archivos `.pem`.

---

## Tecnologias

| Tecnologia | Uso |
| --- | --- |
| FastAPI | API backend |
| SQLAlchemy | Acceso a base de datos |
| PostgreSQL / RDS | Base de datos gestionada |
| Docker Compose | Ejecucion del stack |
| NGINX | Proxy inverso |
| EC2 | Servidor cloud |
| S3 | Backups |
| IAM | Usuarios, roles y permisos |
| VPC | Red privada en AWS |
| CloudFormation | Infraestructura como codigo |

---

## Arquitectura AWS

```text
Usuario
  |
  v
Elastic IP / ALB
  |
  v
VPC asir-vpc 10.0.0.0/16
  |
  +-- Subred publica asir-public 10.0.1.0/24
  |     +-- EC2 Ubuntu 22.04 t2.micro
  |           +-- NGINX
  |           +-- FastAPI
  |
  +-- Subred privada asir-private 10.0.2.0/24
        +-- RDS PostgreSQL 15

S3 asir-backups-<tu-nombre> <- rol IAM rol-ec2-s3
```

---

## Endpoints

| Metodo | Ruta | Uso |
| --- | --- | --- |
| GET | `/` | Estado de la API |
| GET | `/docs` | Swagger |
| GET | `/inventario` | Listar inventario |
| POST | `/inventario` | Crear item |
| GET | `/logs` | Listar logs |
| POST | `/logs` | Registrar IP |

---

## Estructura

```text
AWS/
+-- main.py
+-- docker-compose.yml
+-- nginx/default.conf
+-- scripts/s3_backup.sh
+-- infra/cloudformation/asir-stack.yml
+-- docs/
    +-- aws-teoria.md
    +-- iam-seguridad.md
    +-- aws-red.md
    +-- rds-teoria.md
    +-- operaciones-aws-cli.md
    +-- pruebas-funcionamiento.md
    +-- informe-final.md
```

---

## Ejecutar en local

```bash
git clone <url-del-repositorio>
cd AWS
```

Crear `.env`:

```env
DATABASE_URL=postgresql://<usuario>:<password>@<host>:5432/<nombre-bd>
```

Levantar el stack:

```bash
docker compose up --build -d
docker compose ps
```

Abrir:

```text
http://localhost
http://localhost/docs
```

---

## Despliegue en AWS

En EC2:

```bash
sudo apt-get update
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com | sh
git clone <url-del-repositorio>
cd AWS
nano .env
docker compose up --build -d
```

Validaciones:

```bash
aws sts get-caller-identity
docker compose ps
curl -i http://<elastic-ip>/
curl -i http://<elastic-ip>/docs
docker compose logs -f backend
```

---

## Backups e infraestructura

Script de backup:

```bash
BACKUP_BUCKET=asir-backups-<tu-nombre> ./scripts/s3_backup.sh
```

Cron diario a las 2:00:

```cron
0 2 * * * /app/scripts/s3_backup.sh >> /var/log/asir-s3-backup.log 2>&1
```

Plantilla CloudFormation:

```text
infra/cloudformation/asir-stack.yml
```

---

## Documentacion

| Archivo | Contenido |
| --- | --- |
| `docs/aws-teoria.md` | Cloud, modelos IaaS/PaaS/SaaS, Free Tier, Glacier |
| `docs/iam-seguridad.md` | IAM, minimo privilegio, MFA, roles |
| `docs/aws-red.md` | VPC, subredes, Elastic IP, ALB, red |
| `docs/rds-teoria.md` | RDS PostgreSQL y seguridad |
| `docs/operaciones-aws-cli.md` | Comandos usados en AWS CLI |
| `docs/pruebas-funcionamiento.md` | Evidencias y validaciones |
| `docs/informe-final.md` | Informe tecnico final |

---

## Seguridad

- No usar la cuenta root para operaciones diarias.
- Activar MFA en root y usuarios IAM.
- Usar `asir-admin` para administracion y `asir-readonly` para lectura.
- No subir `.env`, Access Keys, passwords ni claves `.pem`.
- Usar roles IAM en EC2 para acceder a S3.
- Mantener RDS en subred privada y permitir PostgreSQL solo desde `sg-ec2-web`.

---

## Autor

Practica de despliegue cloud en AWS para ASIR.
