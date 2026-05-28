# IAM y Seguridad en AWS

## Principio de mínimo privilegio

El principio de mínimo privilegio consiste en dar a cada usuario o servicio únicamente los permisos necesarios para realizar su función y nada más.

Esto mejora la seguridad porque:
- Reduce errores accidentales.
- Evita accesos innecesarios.
- Limita daños si una cuenta es comprometida.

Por ejemplo, un usuario que solo necesita leer archivos S3 no debería poder borrar buckets o crear instancias EC2.

---

# Tipos de políticas IAM

## Identity-based policy

Son políticas que se asignan a:
- Usuarios
- Grupos
- Roles

Sirven para definir qué acciones puede hacer una identidad dentro de AWS.

Ejemplo:
- Permitir que un usuario pueda leer buckets S3.

## Resource-based policy

Son políticas que se asignan directamente a un recurso.

Ejemplos:
- Bucket policy en S3
- Políticas de SNS

Sirven para definir quién puede acceder a ese recurso.

---

# Roles IAM

Un rol IAM es una identidad temporal que puede asumir un usuario, servicio o instancia EC2 para obtener permisos.

La diferencia principal entre usuario y rol es:
- El usuario tiene credenciales permanentes.
- El rol utiliza credenciales temporales.

Las instancias EC2 usan roles porque es más seguro que guardar Access Keys dentro de la máquina virtual.

---

# Usuario de solo lectura

Se creó un usuario llamado:

```txt
asir-readonly
```

Este usuario tiene asociada la politica administrada `ReadOnlyAccess`. Su objetivo es poder inspeccionar recursos sin modificar la infraestructura.

Validacion realizada:

```bash
aws s3 ls --profile asir-readonly
aws s3 mb s3://prueba-asir-readonly --profile asir-readonly
```

El primer comando permite comprobar que el usuario puede listar recursos. El segundo debe fallar con `AccessDenied`, porque un usuario de solo lectura no debe crear buckets ni modificar recursos.

---

# Usuarios, MFA y credenciales

## Cuenta root

La cuenta root no se usa para operaciones diarias. Solo debe utilizarse para tareas de gestion de la cuenta, facturacion, recuperacion de acceso o cambios criticos que no pueda hacer un usuario IAM.

La cuenta root tiene MFA activado. Esto reduce el riesgo de que una contrasena comprometida permita tomar control total de la cuenta.

## Usuario administrador

Se creo el usuario IAM:

```txt
asir-admin
```

Este usuario tiene:

- Politica `AdministratorAccess`.
- MFA activado.
- Credenciales programaticas para AWS CLI.

La AWS CLI se configuro con este usuario y se valido con:

```bash
aws sts get-caller-identity
```

La respuesta esperada debe mostrar un ARN de este tipo:

```txt
arn:aws:iam::<id-cuenta>:user/asir-admin
```

Las Access Keys y Secret Access Keys no se guardan en Git ni en el repositorio.

## Rol para EC2 y S3

Para que la instancia EC2 pueda acceder a S3 no se guardan credenciales manuales dentro del servidor. En su lugar se usa el rol:

```txt
rol-ec2-s3
```

Este rol se asocia a la instancia EC2 y entrega credenciales temporales automaticamente mediante el metadata service de AWS.

La politica minima aplicada permite solo:

- `s3:PutObject`
- `s3:GetObject`

Y solo sobre:

```txt
arn:aws:s3:::asir-backups-<tu-nombre>/*
```

Esto respeta el principio de minimo privilegio: la EC2 puede subir y leer backups, pero no administrar todo S3 ni acceder a buckets ajenos.
