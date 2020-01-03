

CREATE TABLE Complex (
    id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    name VARCHAR (35) PRIMARY KEY
);

CREATE TABLE Tower (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR (2) NOT NULL,
    complex_id  INTEGER     NOT NULL,
    UNIQUE (name, complex_id),
    FOREIGN KEY (complex_id) REFERENCES Complex(id) ON DELETE CASCADE
);

CREATE TABLE Apartment (
    id         INTEGER     PRIMARY KEY AUTOINCREMENT,
    number     INTEGER     NOT NULL,
    tower_id   VARCHAR (2) NOT NULL,
    UNIQUE (number, tower_id),
    FOREIGN KEY (tower_id) REFERENCES Tower(id) ON DELETE CASCADE
);

CREATE TABLE Resident (
    cpf            VARCHAR (11) PRIMARY KEY,
    name           VARCHAR (50) NOT NULL,
    email          VARCHAR (50) NOT NULL,
    contact_number VARCHAR (13) NOT NULL,
    apt_id         INTEGER      NOT NULL,
    FOREIGN KEY (apt_id) REFERENCES Apartment(id) ON DELETE CASCADE
);

CREATE TABLE Role (
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    description VARCHAR (20) NOT NULL,
    UNIQUE (description)
);

CREATE TABLE Employee (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    cpf        VARCHAR (11) NOT NULL,
    name       VARCHAR (40) NOT NULL,
    age        INTEGER      NOT NULL,
    role       INTEGER      NOT NULL,
    complex_id INTEGER      NOT NULL,
    UNIQUE (cpf, role, complex_id),
    FOREIGN KEY (role)       REFERENCES Role(id) ON DELETE CASCADE,
    FOREIGN KEY (complex_id) REFERENCES Complex(id) ON DELETE CASCADE
);

CREATE TABLE Shop (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,
    type       VARCHAR (10) NOT NULL,
    complex_id INTEGER      NOT NULL,
    UNIQUE (type, complex_id),
    FOREIGN KEY (complex_id) REFERENCES Complex(id) ON DELETE CASCADE
);

CREATE TABLE Item (
    id            INTEGER        PRIMARY KEY AUTOINCREMENT,
    shop_id       INTEGER        NOT NULL,
    owner         INTEGER        NOT NULL,
    name          VARCHAR (20)   NOT NULL,
    price         DECIMAL (9)    NOT NULL,
    description   VARCHAR (500),
    images_folder VARCHAR (150),
    UNIQUE (images_folder),
    UNIQUE (shop_id, owner, name),
    FOREIGN KEY (owner)   REFERENCES Apartment(id) ON DELETE CASCADE,
    FOREIGN KEY (shop_id) REFERENCES Shop(id) ON DELETE CASCADE
);

CREATE TABLE Event (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    type       VARCHAR (20)  NOT NULL,
    title      VARCHAR (30)  NOT NULL,
    text       VARCHAR (200),
    complex_id INTEGER       NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id)
);

CREATE TABLE ComplexEvent (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    from_date   DATETIME NOT NULL,
    to_date     DATETIME NOT NULL,
    event_id    INTEGER  NOT NULL,
    employee_id INTEGER  NOT NULL,
    UNIQUE (from_date, to_date, event_id),
    FOREIGN KEY (event_id)    REFERENCES Event(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES Employee(id) ON DELETE CASCADE
);

CREATE TABLE ResidentEvent (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    from_date   DATETIME NOT NULL,
    to_date     DATETIME NOT NULL,
    event_id    INTEGER  NOT NULL,
    apt_id      INTEGER  NOT NULL,
    UNIQUE(from_date, to_date, event_id),
    FOREIGN KEY (event_id) REFERENCES Event(id) ON DELETE CASCADE,
    FOREIGN KEY (apt_id)   REFERENCES Apartment(id) ON DELETE CASCADE
);

CREATE TABLE Services(
    name    VARCHAR (50) PRIMARY KEY,
    company VARCHAR (30) NOT NULL,
    type    VARCHAR (30) NOT NULL,
    apt_id  INTEGER      NOT NULL,
    FOREIGN KEY (apt_id) REFERENCES Apartment(id) ON DELETE CASCADE
);

CREATE TABLE Weekday(
    week_day     INTEGER PRIMARY KEY,
    from_hour    TIME NOT NULL,
    to_hour      TIME
);

CREATE TABLE ServiceWeekday(
    service_name VARCHAR (50) NOT NULL,
    weekday_name INTEGER      NOT NULL,
    PRIMARY KEY (service_name, weekday_name),
    FOREIGN KEY (service_name) REFERENCES Services(name),
    FOREIGN KEY (weekday_name) REFERENCES Weekday(week_day)
);

CREATE TABLE Rule (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    text       VARCHAR (150) NOT NULL,
    complex_id INTEGER       NOT NULL,
    FOREIGN KEY (complex_id) REFERENCES Complex(id) ON DELETE CASCADE
);

CREATE TABLE Warning (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    type       INTEGER       NOT NULL,
    text       VARCHAR (150) NOT NULL,
    tower_id   INTEGER       NOT NULL,
    FOREIGN KEY (tower_id) REFERENCES Tower(id) ON DELETE CASCADE
);