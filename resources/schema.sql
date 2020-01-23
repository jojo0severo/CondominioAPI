CREATE TABLE Address (
  id                 INTEGER       PRIMARY KEY,
  street_name        VARCHAR (150) NOT NULL,
  neighbourhood_name VARCHAR (150) NOT NULL,
  state_name         VARCHAR (60)  NOT NULL,
  country_name       VARCHAR (40)  NOT NULL,
  UNIQUE (street_name, neighbourhood_name, state_name, country_name)
);

CREATE TABLE Condominium (
  id               INTEGER      PRIMARY KEY AUTO_INCREMENT,
  condominium_name VARCHAR (60) NOT NULL,
  street_number    INTEGER      NOT NULL,
  address_id       INTEGER      REFERENCES Address(id),
  UNIQUE(condominium_name, address_id)
);

CREATE TABLE Tower (
  id             INTEGER      PRIMARY KEY,
  tower_name     VARCHAR (10) NOT NULL,
  condominium_id INTEGER      REFERENCES Condominium(id),
  UNIQUE (tower_name, condominium_id)
);

CREATE TABLE Apartment (
  id         INTEGER PRIMARY KEY,
  apt_number INTEGER NOT NULL,
  tower_id   INTEGER REFERENCES Tower(id),
  UNIQUE(apt_number, tower_id)
);

CREATE TABLE Resident (
  id            INTEGER      PRIMARY KEY,
  cpf           VARCHAR (11) NOT NULL,
  name          VARCHAR (50) NOT NULL,
  birthday      DATE         NOT NULL,
  photo_address VARCHAR (200),
  apartment_id  INTEGER      REFERENCES Apartment(id),
  UNIQUE(cpf, apartment_id),
  UNIQUE(photo_address)
);

CREATE TABLE ResidentUser (
  username    VARCHAR (25) PRIMARY KEY,
  password    VARCHAR (25) NOT NULL,
  resident_id INTEGER      REFERENCES Resident(id),
  UNIQUE(username, password)
);

CREATE TABLE Employee (
  id             INTEGER      PRIMARY KEY,
  cpf            VARCHAR (11) NOT NULL,
  name           VARCHAR (50) NOT NULL,
  birthday       DATE         NOT NULL,
  photo_address  VARCHAR (200),
  role           VARCHAR (50) NOT NULL,
  condominium_id INTEGER      REFERENCES Condominium(id),
  UNIQUE(cpf, role, condominium_id),
  UNIQUE(photo_address)
);

CREATE TABLE EmployeeUser (
  username    VARCHAR (25) PRIMARY KEY,
  password    VARCHAR (25) NOT NULL,
  employee_id INTEGER      REFERENCES Employee(id),
  UNIQUE(username, password)
);

CREATE TABLE Rules (
  id             INTEGER       PRIMARY KEY,
  text           VARCHAR (500) NOT NULL,
  condominium_id INTEGER       REFERENCES Condominium(id)
);

CREATE TABLE Notification (
  id             INTEGER       PRIMARY KEY,
  type           INTEGER       NOT NULL,
  title          VARCHAR (25)  NOT NULL,
  text           VARCHAR (300) NOT NULL,
  finish         DATETIME      NOT NULL,
  condominium_id INTEGER       REFERENCES Condominium(id)
);

CREATE TABLE EventType (
  id             INTEGER      PRIMARY KEY AUTO_INCREMENT,
  name           VARCHAR (30) NOT NULL,
  condominium_id INTEGER      REFERENCES Condominium(id),
  UNIQUE(name, condominium_id)
);

CREATE TABLE Event (
  id            INTEGER  PRIMARY KEY,
  start         DATETIME NOT NULL,
  finish        DATETIME NOT NULL,
  event_type_id INTEGER  REFERENCES EventType(id),
  apartment_id  INTEGER  REFERENCES Apartment(id),
  UNIQUE(event_type_id, start, finish)
);

CREATE TABLE Service (
  id            INTEGER      PRIMARY KEY,
  service_name  VARCHAR (30) NOT NULL,
  employee_name VARCHAR (50),
  arrival       DATETIME,
  apartment_id  INTEGER      REFERENCES Apartment(id)
);

CREATE TABLE Guest (
  id           INTEGER      PRIMARY KEY,
  guest_name   VARCHAR (50) NOT NULL,
  arrival      DATETIME,
  apartment_id INTEGER      REFERENCES Apartment(id)
);
