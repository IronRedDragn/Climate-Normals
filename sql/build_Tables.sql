DROP TABLE STATES;
CREATE TABLE STATES(
    StateLong CHAR(50) NOT NULL,
    StateAbbr CHAR(2) PRIMARY KEY NOT NULL);

COPY STATES FROM '/home/acruz/Coding/Climate-Normals/txt_files/states.csv' DELIMITER ',' CSV HEADER;