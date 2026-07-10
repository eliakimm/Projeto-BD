ALTER table usuario
ALTER COLUMN senha type varchar(255);

ALTER TABLE material_apoio
ADD COLUMN arquivo BYTEA NOT NULL;

ALTER TABLE material_apoio
ADD COLUMN id_user INT;

ALTER TABLE material_apoio
ADD CONSTRAINT fk_material_usuario
FOREIGN KEY (id_user)
REFERENCES usuario(id_user);