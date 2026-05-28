# Operaciones realizadas con AWS CLI

Este documento resume los comandos usados o equivalentes para dejar trazabilidad del trabajo realizado desde la EC2 y desde la maquina local. Los valores sensibles se sustituyen por marcadores.

## Configuracion inicial de AWS CLI

```bash
aws configure
```

Valores usados:

- Access Key ID: credencial del usuario `asir-admin`.
- Secret Access Key: guardada fuera del repositorio.
- Region: `eu-west-1`.
- Output: `json`.

Validacion:

```bash
aws sts get-caller-identity
```

La salida debe contener:

```text
arn:aws:iam::<id-cuenta>:user/asir-admin
```

## IAM

Usuarios creados:

- `asir-admin`, con `AdministratorAccess` y MFA.
- `asir-readonly`, con `ReadOnlyAccess`.

Rol para EC2:

- `rol-ec2-s3`.
- Politica minima: `s3:PutObject` y `s3:GetObject` sobre el bucket `asir-backups-<tu-nombre>`.

Politica minima usada:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::asir-backups-<tu-nombre>/*"
    }
  ]
}
```

## VPC

Recursos creados:

- VPC: `asir-vpc`, CIDR `10.0.0.0/16`.
- Subred publica: `asir-public`, CIDR `10.0.1.0/24`.
- Subred privada: `asir-private`, CIDR `10.0.2.0/24`.
- Internet Gateway asociado a la VPC.
- Tabla de rutas publica con `0.0.0.0/0` hacia el Internet Gateway.

Comandos de comprobacion:

```bash
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=asir-vpc"
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>"
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc-id>"
```

## EC2

Configuracion:

- AMI: Ubuntu Server 22.04 LTS.
- Tipo: `t2.micro`.
- Subred: `asir-public`.
- Key pair: `asir-keypair`.
- Security Group: `sg-ec2-web`.

Reglas de entrada:

- SSH 22 desde `<tu-ip-publica>/32`.
- HTTP 80 desde `0.0.0.0/0`.
- HTTPS 443 desde `0.0.0.0/0`.

Instalacion de Docker en la EC2:

```bash
sudo apt-get update
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
```

## Despliegue de aplicacion en EC2

```bash
git clone <url-repositorio>
cd <directorio-repositorio>
nano .env
docker compose up --build -d
docker compose ps
docker compose logs -f backend
```

El archivo `.env` se crea directamente en el servidor y no se sube a Git.

## S3

Bucket:

```text
asir-backups-<tu-nombre>
```

Configuracion aplicada:

- Bloqueo de acceso publico activado.
- Permisos mediante rol IAM de EC2.
- Regla de ciclo de vida para mover `backups/` a Glacier Instant Retrieval tras 30 dias.

Comprobacion desde EC2:

```bash
aws s3 ls s3://asir-backups-<tu-nombre>
```

## Cron de backups

Script:

```text
/app/scripts/s3_backup.sh
```

Entrada de cron:

```cron
0 2 * * * /app/scripts/s3_backup.sh >> /var/log/asir-s3-backup.log 2>&1
```

## RDS

Configuracion:

- Motor: PostgreSQL 15.
- Tipo: `db.t3.micro`.
- Subred: `asir-private`.
- Acceso publico: desactivado.
- Security Group: `sg-rds`.
- Puerto: `5432`.

Regla de seguridad:

- Entrada PostgreSQL 5432 solo desde `sg-ec2-web`.

Conexion desde EC2:

```bash
sudo apt-get install -y postgresql-client
psql -h <endpoint-rds> -U <usuario> -d <nombre-bd>
```

## Alta disponibilidad, HTTPS y dominio

Componentes configurados:

- Application Load Balancer delante de EC2.
- Certificado SSL/TLS en AWS Certificate Manager.
- Route 53 apuntando el dominio personalizado al balanceador.

Comprobaciones:

```bash
aws elbv2 describe-load-balancers
aws acm list-certificates
aws route53 list-hosted-zones
```
