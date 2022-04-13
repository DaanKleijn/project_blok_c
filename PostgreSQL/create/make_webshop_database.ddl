-- This file is dedicated to creating the SQL database. It creates five tables: products, profiles, buid, sessions and
-- event_products.

CREATE TABLE products (
	product__id 				VARCHAR 			CONSTRAINT c_prod_pk_id 			PRIMARY KEY,
	brand 						VARCHAR,
	category 					VARCHAR,
	color 						VARCHAR,
	flavor 						VARCHAR,
	gender 						VARCHAR,
	herhaalaankopen 			VARCHAR 			CONSTRAINT c_prod_bool_ha 			CHECK (herhaalaankopen 		IN ('true', 'false')),
	product_name 				VARCHAR				CONSTRAINT c_prod_nn_name 			NOT NULL,
	selling_price 				INT					CONSTRAINT c_prod_nn_price			NOT NULL,
	availability 				INT,
	discount 					VARCHAR,
	doelgroep 					VARCHAR,
	eenheid 					VARCHAR,
	factor 						VARCHAR,
	geschiktvoor 				VARCHAR,
	geursoort 					VARCHAR,
	huidconditie 				VARCHAR,
	huidtype 					VARCHAR,
	huidtypegezicht 			VARCHAR,
	klacht 						VARCHAR,
	kleur 						VARCHAR,
	leeftijd 					VARCHAR,
	soort 						VARCHAR,
	soorthaarverzorging 		VARCHAR,
	soortmondverzorging 		VARCHAR,
	sterkte 					VARCHAR,
	product_type 				VARCHAR,
	typehaarkleuring 			VARCHAR,
	typetandenbostel 			VARCHAR,
	variant 					VARCHAR,
	waterproof 					VARCHAR,
	recommendable				VARCHAR 			CONSTRAINT c_prod_bool_rec 			CHECK (recommendable 		IN ('true', 'false')),
	sub_category 				VARCHAR,
	sub_sub_category 			VARCHAR,
	sub_sub_sub_category 		VARCHAR
);

CREATE TABLE profiles(
	profile__id 	VARCHAR							CONSTRAINT c_prof_pk 				PRIMARY KEY,
	latest_activity TIMESTAMP WITH TIME ZONE,
	profile_type    VARCHAR
);

CREATE TABLE buids(
	buid			VARCHAR							CONSTRAINT c_buid_pk 				PRIMARY KEY,
	profile__id		VARCHAR,
	CONSTRAINT c_b_fk_pid							FOREIGN KEY (profile__id) 			REFERENCES profiles(profile__id)
);

CREATE TABLE sessions(
	session__id 		VARCHAR 					CONSTRAINT c_ses_pk 				PRIMARY KEY,
    profile__id         VARCHAR,
	session_end 		TIMESTAMP WITH TIME ZONE	CONSTRAINT c_ses_nn_se 				NOT NULL,
	CONSTRAINT c_ses_fk_prid 						FOREIGN KEY (profile__id)			REFERENCES profiles(profile__id)
);

CREATE TABLE event_products(
	session__id 		VARCHAR,
	product__id 		VARCHAR,
	event_type          VARCHAR (7)                     CONSTRAINT c_e_cat_et               CHECK (event_type IN ('ordered', 'viewed')),
	CONSTRAINT c_e_pk 									PRIMARY KEY (session__id, product__id),
	CONSTRAINT c_e_fk_sid 								FOREIGN KEY (session__id)			REFERENCES sessions(session__id),
    CONSTRAINT c_e_fk_pid                               FOREIGN KEY (product__id)           REFERENCES products(product__id)
);

-- trigger that skips all products with a null value for name or price.
CREATE FUNCTION trigger_nn_product()
   RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
BEGIN
	IF (NEW.selling_price IS NULL OR NEW.product_name IS NULL)
		THEN RETURN NULL;
	ELSE
		RETURN NEW;
END IF;
END;
$$;

CREATE TRIGGER products_nn_price
   BEFORE INSERT
   ON products
   FOR EACH ROW
       EXECUTE PROCEDURE trigger_nn_product();
