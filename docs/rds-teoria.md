# RDS en AWS

## Ventajas de usar RDS

RDS permite utilizar bases de datos gestionadas por AWS sin tener que instalar PostgreSQL manualmente en una EC2.

Principales ventajas:
- Actualizaciones automáticas.
- Backups automáticos.
- Replicación de datos.
- Alta disponibilidad.
- Mayor seguridad y mantenimiento más simple.

Con RDS, AWS administra gran parte de la infraestructura y el mantenimiento de la base de datos.

---

# Configuracion aplicada en el proyecto

La base de datos del proyecto se desplego como una instancia Amazon RDS PostgreSQL.

Configuracion:

- Motor: PostgreSQL 15.
- Tipo de instancia: `db.t3.micro`.
- Acceso publico: desactivado.
- Subred: privada, dentro de `asir-vpc`.
- Security Group: `sg-rds`.
- Puerto: `5432`.

El endpoint, usuario y contrasena de RDS no se documentan en claro porque son datos sensibles. Se guardan en el archivo `.env` directamente en la instancia EC2.

Ejemplo de variable:

```env
DATABASE_URL=postgresql://<usuario>:<password>@<endpoint-rds>:5432/<nombre-bd>
```

---

# Seguridad de red en RDS

El grupo de seguridad `sg-rds` solo permite conexiones PostgreSQL desde el grupo de seguridad de la EC2:

```txt
Origen: sg-ec2-web
Puerto: 5432
Protocolo: TCP
```

Esto impide que la base de datos sea accesible directamente desde Internet. Aunque alguien conozca el endpoint de RDS, no podra conectarse si no esta dentro del flujo permitido por los Security Groups.

---

# Validacion desde EC2

Desde la instancia EC2 se instalo el cliente PostgreSQL:

```bash
sudo apt-get install -y postgresql-client
```

Conexion:

```bash
psql -h <endpoint-rds> -U <usuario> -d <nombre-bd>
```

Comprobaciones:

```sql
\dt
select count(*) from inventario;
select count(*) from logs_ips;
```

La aplicacion FastAPI crea las tablas si no existen y consume los datos desde RDS mediante SQLAlchemy.

---

# Migracion y uso por la aplicacion

Los datos generados durante las fases anteriores se migraron a RDS y el stack se reinicio para tomar la nueva configuracion:

```bash
docker compose down
docker compose up -d
```

Despues del reinicio, los endpoints `/inventario` y `/logs` leen los datos desde PostgreSQL gestionado por RDS.
