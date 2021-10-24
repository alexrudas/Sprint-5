CREATE TABLE Usuarios (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre  CHAR (50),
    mail    CHAR (50),
    
    perfil  CHAR (15),
    usuario CHAR (20),
    passw   CHAR (20) 
);


CREATE TABLE Proveedores (
    id_proveedores INT AUTO_INCREMENT PRIMARY KEY,
    nombre         CHAR (30),
    categoria      CHAR (15),
    ciudad         CHAR (20),
    direccion      CHAR (50),
    telefono       VARCHAR (15) 
);


CREATE TABLE Productos (
    id_producto    INT AUTO_INCREMENT PRIMARY KEY,
    nombre         CHAR (30),
    marca          CHAR (20),
    descripcion    CHAR (50),
    categoria      CHAR (15),
    costo          DOUBLE,
    precio         DOUBLE,
    cantidad       DOUBLE,
    id_proveedores INT NOT NULL, FOREIGN KEY (id_proveedores) REFERENCES Proveedores (id_proveedores) 
                                
);