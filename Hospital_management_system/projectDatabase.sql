CREATE DATABASE phase1;
USE phase1;

CREATE TABLE USERS (
    id INT NOT NULL,
    user VARCHAR(40) NOT NULL,
    PRIMARY KEY(id, user),
    password VARCHAR(40) NOT NULL,
    isadmin BOOL NOT NULL
);

INSERT INTO USERS VALUES(1, 'ameer', 'ameer', false);
INSERT INTO USERS VALUES(2, 'admin', 'admin', true);

CREATE TABLE HOSPITAL (
    Hospital_ID INT NOT NULL,
    Phone_No VARCHAR(100),
    Hospital_Name VARCHAR(40) NOT NULL,
    Hospital_Address VARCHAR(100) NOT NULL,
    PRIMARY KEY (Hospital_ID)
);

INSERT INTO HOSPITAL VALUES(1, '011511', 'mostashfa el mostashfa', 'johayna square');

CREATE TABLE DEPARTMENT (
    dep_name VARCHAR(40) NOT NULL,
    dep_id INT NOT NULL,
    PRIMARY KEY (dep_id),
    head VARCHAR(40) NOT NULL,
    staff_no INT NOT NULL
);

INSERT INTO DEPARTMENT VALUES('surgery', 1, 'Dr Ameer', 9);

CREATE TABLE DOCTOR (
    Gender BOOL NOT NULL, #True for male False for female
    Age INT NOT NULL,
    Doctor_ID INT NOT NULL,
    Name VARCHAR(40) NOT NULL,
    Position VARCHAR(40) NOT NULL,
    Phone_Number VARCHAR(40) NOT NULL,
    Hospital_ID INT,
    dep_id INT,
    PRIMARY KEY (Doctor_ID, Hospital_ID, dep_id),
    FOREIGN KEY (Hospital_ID) REFERENCES HOSPITAL(Hospital_ID),
    FOREIGN KEY (dep_id) REFERENCES DEPARTMENT(dep_id)
);

INSERT INTO DOCTOR VALUES(true, 23, 1, 'Ameer', 'Head', '011511', 1, 1);
INSERT INTO DOCTOR VALUES(true, 25, 2, 'Omar', 'Head', '011531', 1, 1);

CREATE TABLE NURSE (
    Name VARCHAR(40) NOT NULL,
    Gender BOOL NOT NULL,
    Age INT NOT NULL,
    Nurse_ID INT NOT NULL,
    Hospital_ID INT,
    PRIMARY KEY (Nurse_ID),
    FOREIGN KEY (Hospital_ID) REFERENCES HOSPITAL(Hospital_ID)
);

INSERT INTO NURSE VALUES('Zahra', false, 23, 1, 1);

CREATE TABLE ROOM (
    room_no INT NOT NULL,
    PRIMARY KEY (room_no),
    room_type VARCHAR(20) NOT NULL,
    room_status BOOL NOT NULL #True for occupied false for non occupied
);

INSERT INTO ROOM VALUES(1, '3enaya', false);

CREATE TABLE PATIENT (
    patient_id INT NOT NULL,
    PRIMARY KEY (patient_id),
    FOREIGN KEY (patient_id) REFERENCES USERS(id),
    patient_name VARCHAR(40),
    patient_age INT,
    patient_gender BOOL,
    patient_address VARCHAR(100),
    patient_phone VARCHAR(20)
    #room_no INT, #IF ITS NULL HES NOT STAYING IN HOSPITAL
    #FOREIGN KEY (room_no) REFERENCES ROOM(room_no)
);

INSERT INTO PATIENT VALUES(1, 'ameer', 20, true, '6 october', '011551123');
#INSERT INTO PATIENT VALUES(2, 'Sama', 20, true, '6 october', '011551123');

CREATE TABLE OUTPATIENT (
    patient_id INT NOT NULL,
    checkback_date DATE,
    PRIMARY KEY (patient_id),
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id)
);

INSERT INTO OUTPATIENT (patient_id, checkback_date) VALUES(1, '2023-01-09');

CREATE TABLE INPATIENT (
    patient_id INT NOT NULL,
    PRIMARY KEY (patient_id),
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
    date_admission DATE NOT NULL,
    date_discharge DATE NOT NULL,
    room_no INT NOT NULL,
    FOREIGN KEY (room_no) REFERENCES ROOM(room_no)
);
#INSERT INTO INPATIENT VALUES(2, '2023-01-10', '2023-01-20', 1);

CREATE TABLE APPOINTMENT (
    app_id INT NOT NULL,
    app_dr_id INT,
    FOREIGN KEY(app_dr_id) REFERENCES DOCTOR(Doctor_ID),
    app_date DATE NOT NULL, #format YYYY-MM-DD
    patient_id INT NOT NULL,
    app_time INT NOT NULL, #should be an hour from 9 am to 11 pm
    notes VARCHAR(200),
    PRIMARY KEY (app_id, app_dr_id),
    FOREIGN KEY(patient_id) REFERENCES PATIENT(patient_id)
);

INSERT INTO APPOINTMENT (app_id, app_dr_id, app_date, patient_id, app_time, notes) VALUES(1, 1, '2023-01-08', 1, 11, NULL);
INSERT INTO APPOINTMENT (app_id, app_dr_id, app_date, patient_id, app_time, notes) VALUES(2, 1, '2023-01-08', 1, 13, NULL);

CREATE TABLE MEDICATION (
    med_id INT NOT NULL,
    PRIMARY KEY (med_id),
    name VARCHAR(40) NOT NULL,
    brand VARCHAR(40) NOT NULL,
    quantity INT NOT NULL,
    price INT NOT NULL,
    patient_id INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id)
);

INSERT INTO MEDICATION (med_id, name, brand, quantity, price, patient_id) VALUES(1, 'paracetamol', 'panadol', 5, 20, 1);