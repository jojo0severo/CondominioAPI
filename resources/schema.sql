

CREATE TABLE Complex (
    id   INTEGER      PRIMARY KEY,
    name VARCHAR (25) NOT NULL
)

CREATE TABLE Bloc (
    id         VARCHAR (2) PRIMARY KEY,
    complex_id INTEGER     NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
)

CREATE TABLE Tower (
    id      VARCHAR (2) PRIMARY KEY,
    bloc_id VARCHAR (2) NOT NULL,
    FOREIGN KEY (bloc_id) REFERENCES Bloc(id)
)

CREATE TABLE Apartment (
    id       INTEGER     PRIMARY KEY,
    tower_id VARCHAR (2) NOT NULL,
    FOREIGN KEY (tower_id) REFERENCES Tower(id)
)

CREATE TABLE Employees (
    cpf        VARCHAR (11) PRIMARY KEY,
    role       INTEGER      NOT NULL,
    name       VARCHAR (40) NOT NULL,
    complex_id INTEGER      NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(complex_id)
)

CREATE TABLE Shop (
    type       VARCHAR (10) PRIMARY KEY,
    complex_id INTEGER      NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
)

CREATE TABLE Item (
    id            INTEGER       PRIMARY KEY AUTOINCREMENT,
    shop_id       VARCHAR (10)  NOT NULL,
    owner         INTEGER       NOT NULL,
    name          VARCHAR (15)  NOT NULL,
    price         DECIMAL (6)   NOT NULL,
    description   VARCHAR (150),
    images_folder VARCHAR (150),
    UNIQUE(owner, name),
    FOREIGN KEY (owner)   REFERENCES Apartment(id),
    FOREIGN KEY (shop_id) REFERENCES Shop(type)
)

CREATE TABLE Event (
    id          INTEGER       PRIMARY KEY AUTOINCREMENT,
    type        VARCHAR (10)  NOT NULL,
    title       VARCHAR (30)  NOT NULL,
    description VARCHAR (250),
    from_date   TIMESTAMP,
    to_date     TIMESTAMP,
    complex_id  INTEGER       NOT NULL,
    UNIQUE(type, title, from_date, to_date),
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
)

CREATE TABLE Rule (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    text       VARCHAR (150) NOT NULL,
    complex_id INTEGER       NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
)

CREATE TABLE Warning (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    type       INTEGER       NOT NULL,
    text       VARCHAR (150) NOT NULL,
    complex_id INTEGER       NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
)