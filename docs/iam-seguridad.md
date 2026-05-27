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