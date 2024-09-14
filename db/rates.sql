-- rates.sql

CREATE TABLE rates (
    id SERIAL PRIMARY KEY,
    day DATE NOT NULL,
    orig_code VARCHAR(10),
    dest_code VARCHAR(10),
    price NUMERIC,
    count INTEGER
);

INSERT INTO rates (day, orig_code, dest_code, price, count) VALUES 
('2021-01-31', 'CNGGZ', 'EETLL', 1154.33, 3),
('2021-01-30', 'CNGGZ', 'EETLL', 1154.33, 3),
('2021-01-29', 'CNGGZ', 'EETLL', 1154.33, 3);
