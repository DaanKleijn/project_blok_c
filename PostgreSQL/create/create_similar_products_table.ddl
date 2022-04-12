CREATE TABLE similars (
    owner_product__id       VARCHAR,
    similar_product__id     VARCHAR,
    CONSTRAINT c_s_pk       PRIMARY KEY (owner_product__id,
                                         similar_product__id),
	CONSTRAINT c_b_fk_pid	FOREIGN KEY (owner_product__id)     REFERENCES products(product__id),
    CONSTRAINT c_b_fk_spid	FOREIGN KEY (similar_product__id) 	REFERENCES products(product__id)
);
