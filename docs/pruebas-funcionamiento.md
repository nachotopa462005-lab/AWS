# Pruebas de funcionamiento

Este documento recoge las pruebas realizadas para validar el despliegue. No se incluyen secretos, claves, contrasenas, IPs personales completas ni endpoints privados sensibles.

## 1. Identidad AWS CLI

Objetivo: comprobar que la CLI esta configurada con el usuario IAM administrador, no con la cuenta root.

Comando:

```bash
aws sts get-caller-identity
```

Resultado esperado:

```json
{
  "UserId": "<id-usuario>",
  "Account": "<id-cuenta>",
  "Arn": "arn:aws:iam::<id-cuenta>:user/asir-admin"
}
```

Estado: validado.

## 2. Usuario de solo lectura

Objetivo: comprobar que `asir-readonly` puede consultar recursos, pero no crear ni borrar.

Comandos:

```bash
aws s3 ls --profile asir-readonly
aws s3 mb s3://prueba-asir-readonly --profile asir-readonly
```

Resultado esperado:

- `aws s3 ls`: lista los buckets visibles.
- `aws s3 mb`: devuelve `AccessDenied`.

Estado: validado.

## 3. Estado de la instancia EC2

Objetivo: comprobar que la instancia de aplicacion esta arrancada.

Comando:

```bash
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=asir-ec2" \
  --query "Reservations[].Instances[].{Estado:State.Name,Tipo:InstanceType,PublicIp:PublicIpAddress}"
```

Resultado esperado:

```json
[
  {
    "Estado": "running",
    "Tipo": "t2.micro",
    "PublicIp": "<ip-publica-o-elastic-ip>"
  }
]
```

Estado: validado.

## 4. Stack Docker en EC2

Objetivo: comprobar que NGINX y el backend estan ejecutandose.

Comando:

```bash
docker compose ps
```

Resultado esperado:

```text
NAME      SERVICE   STATUS
backend   backend   Up
nginx     nginx     Up
```

Estado: validado.

## 5. Acceso HTTP al backend

Objetivo: comprobar que NGINX reenvia correctamente al backend FastAPI.

Comandos:

```bash
curl -i http://<elastic-ip>/
curl -i http://<elastic-ip>/docs
```

Resultado esperado:

- `/` devuelve HTTP 200 y un JSON con `status: ok`.
- `/docs` devuelve HTTP 200 y muestra Swagger UI de FastAPI.

Estado: validado.

## 6. Logs del backend

Objetivo: comprobar que el backend arranca sin errores y recibe peticiones.

Comando:

```bash
docker compose logs -f backend
```

Resultado esperado:

- No aparecen errores de conexion a base de datos.
- Se registran peticiones HTTP a los endpoints.

Estado: validado.

## 7. Conexion a RDS desde EC2

Objetivo: comprobar que RDS solo es accesible desde la EC2 y que la subred privada funciona correctamente.

Comando:

```bash
psql -h <endpoint-rds> -U <usuario> -d <nombre-bd>
```

Comprobacion SQL:

```sql
\dt
select count(*) from inventario;
select count(*) from logs_ips;
```

Resultado esperado:

- Conexion correcta desde la EC2.
- Las tablas `inventario` y `logs_ips` existen.
- Los endpoints de FastAPI pueden leer datos desde RDS.

Estado: validado.

## 8. Prueba de fallo del backend

Objetivo: comprobar el comportamiento de NGINX si el backend se detiene.

Comandos:

```bash
docker stop backend
curl -i http://<elastic-ip>/
docker compose up -d backend
curl -i http://<elastic-ip>/
```

Resultado esperado:

- Con `backend` detenido, NGINX devuelve HTTP 502 Bad Gateway.
- Tras reiniciar `backend`, la aplicacion vuelve a responder HTTP 200.

Estado: validado.

## 9. Acceso a S3 mediante rol de EC2

Objetivo: comprobar que la instancia usa el rol `rol-ec2-s3` y no credenciales manuales.

Comandos:

```bash
aws s3 ls s3://asir-backups-<tu-nombre>
aws s3 cp /tmp/backup-prueba.tar.gz s3://asir-backups-<tu-nombre>/backups/prueba/
```

Resultado esperado:

- La EC2 puede listar o subir objetos permitidos por la politica.
- No hay credenciales AWS guardadas dentro del repositorio ni en `.env`.

Estado: validado.

## 10. Alta disponibilidad y HTTPS

Objetivo: comprobar la capa frontal con balanceador, certificado y DNS.

Comprobaciones:

```bash
aws elbv2 describe-load-balancers
aws acm list-certificates
aws route53 list-hosted-zones
```

Resultado esperado:

- Existe un Application Load Balancer asociado a las subredes publicas.
- Existe un certificado ACM emitido o validado.
- Route 53 apunta el dominio al balanceador mediante registro Alias.
- La aplicacion responde por HTTPS.

Estado: validado si se usa dominio personalizado; si el acceso final se hace solo por Elastic IP, queda como mejora opcional.
