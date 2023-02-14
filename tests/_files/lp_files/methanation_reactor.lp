\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(ch4_0)_:
+1 flow(m_reactor_storage_products_ch4_0)
= 0

c_e_Bus_balance(ch4_1)_:
+1 flow(m_reactor_storage_products_ch4_1)
= 0

c_e_Bus_balance(ch4_2)_:
+1 flow(m_reactor_storage_products_ch4_2)
= 0

c_e_Bus_balance(h2_0)_:
+1 flow(h2_m_reactor_combine_educts_0)
= 0

c_e_Bus_balance(h2_1)_:
+1 flow(h2_m_reactor_combine_educts_1)
= 0

c_e_Bus_balance(h2_2)_:
+1 flow(h2_m_reactor_combine_educts_2)
= 0

c_e_Transformer_relation(m_reactor_m_reactor_storage_educts_m_reactor_storage_products_0)_:
-1 flow(m_reactor_m_reactor_storage_products_0)
+0.93000000000000005 flow(m_reactor_storage_educts_m_reactor_0)
= 0

c_e_Transformer_relation(m_reactor_m_reactor_storage_educts_m_reactor_storage_products_1)_:
-1 flow(m_reactor_m_reactor_storage_products_1)
+0.93000000000000005 flow(m_reactor_storage_educts_m_reactor_1)
= 0

c_e_Transformer_relation(m_reactor_m_reactor_storage_educts_m_reactor_storage_products_2)_:
-1 flow(m_reactor_m_reactor_storage_products_2)
+0.93000000000000005 flow(m_reactor_storage_educts_m_reactor_2)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_co2_m_reactor_storage_educts_0)_:
+1 flow(co2_m_reactor_combine_educts_0)
-0.20000000000000001 flow(m_reactor_combine_educts_m_reactor_storage_educts_0)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_co2_m_reactor_storage_educts_1)_:
+1 flow(co2_m_reactor_combine_educts_1)
-0.20000000000000001 flow(m_reactor_combine_educts_m_reactor_storage_educts_1)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_co2_m_reactor_storage_educts_2)_:
+1 flow(co2_m_reactor_combine_educts_2)
-0.20000000000000001 flow(m_reactor_combine_educts_m_reactor_storage_educts_2)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_h2_m_reactor_storage_educts_0)_:
+1 flow(h2_m_reactor_combine_educts_0)
-0.80000000000000004 flow(m_reactor_combine_educts_m_reactor_storage_educts_0)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_h2_m_reactor_storage_educts_1)_:
+1 flow(h2_m_reactor_combine_educts_1)
-0.80000000000000004 flow(m_reactor_combine_educts_m_reactor_storage_educts_1)
= 0

c_e_Transformer_relation(m_reactor_combine_educts_h2_m_reactor_storage_educts_2)_:
+1 flow(h2_m_reactor_combine_educts_2)
-0.80000000000000004 flow(m_reactor_combine_educts_m_reactor_storage_educts_2)
= 0

c_e_GenericStorageBlock_balance_first(m_reactor_storage_educts)_:
-1 GenericStorageBlock_init_content(m_reactor_storage_educts)
+1 GenericStorageBlock_storage_content(m_reactor_storage_educts_0)
-1 flow(m_reactor_combine_educts_m_reactor_storage_educts_0)
+1 flow(m_reactor_storage_educts_m_reactor_0)
= 0

c_e_GenericStorageBlock_balance_first(m_reactor_storage_products)_:
-1 GenericStorageBlock_init_content(m_reactor_storage_products)
+1 GenericStorageBlock_storage_content(m_reactor_storage_products_0)
-1 flow(m_reactor_m_reactor_storage_products_0)
+1 flow(m_reactor_storage_products_ch4_0)
= 0

c_e_GenericStorageBlock_balance(m_reactor_storage_educts_1)_:
-1 GenericStorageBlock_storage_content(m_reactor_storage_educts_0)
+1 GenericStorageBlock_storage_content(m_reactor_storage_educts_1)
-1 flow(m_reactor_combine_educts_m_reactor_storage_educts_1)
+1 flow(m_reactor_storage_educts_m_reactor_1)
= 0

c_e_GenericStorageBlock_balance(m_reactor_storage_educts_2)_:
-1 GenericStorageBlock_storage_content(m_reactor_storage_educts_1)
+1 GenericStorageBlock_storage_content(m_reactor_storage_educts_2)
-1 flow(m_reactor_combine_educts_m_reactor_storage_educts_2)
+1 flow(m_reactor_storage_educts_m_reactor_2)
= 0

c_e_GenericStorageBlock_balance(m_reactor_storage_products_1)_:
-1 GenericStorageBlock_storage_content(m_reactor_storage_products_0)
+1 GenericStorageBlock_storage_content(m_reactor_storage_products_1)
-1 flow(m_reactor_m_reactor_storage_products_1)
+1 flow(m_reactor_storage_products_ch4_1)
= 0

c_e_GenericStorageBlock_balance(m_reactor_storage_products_2)_:
-1 GenericStorageBlock_storage_content(m_reactor_storage_products_1)
+1 GenericStorageBlock_storage_content(m_reactor_storage_products_2)
-1 flow(m_reactor_m_reactor_storage_products_2)
+1 flow(m_reactor_storage_products_ch4_2)
= 0

c_e_GenericStorageBlock_balanced_cstr(m_reactor_storage_educts)_:
-1 GenericStorageBlock_init_content(m_reactor_storage_educts)
+1 GenericStorageBlock_storage_content(m_reactor_storage_educts_2)
= 0

c_e_GenericStorageBlock_balanced_cstr(m_reactor_storage_products)_:
-1 GenericStorageBlock_init_content(m_reactor_storage_products)
+1 GenericStorageBlock_storage_content(m_reactor_storage_products_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(co2_m_reactor_combine_educts_0) <= +inf
   0 <= flow(co2_m_reactor_combine_educts_1) <= +inf
   0 <= flow(co2_m_reactor_combine_educts_2) <= +inf
   0 <= flow(h2_m_reactor_combine_educts_0) <= +inf
   0 <= flow(h2_m_reactor_combine_educts_1) <= +inf
   0 <= flow(h2_m_reactor_combine_educts_2) <= +inf
   0 <= flow(m_reactor_m_reactor_storage_products_0) <= 5
   0 <= flow(m_reactor_m_reactor_storage_products_1) <= 5
   0 <= flow(m_reactor_m_reactor_storage_products_2) <= 5
   0 <= flow(m_reactor_combine_educts_m_reactor_storage_educts_0) <= 50
   0 <= flow(m_reactor_combine_educts_m_reactor_storage_educts_1) <= 50
   0 <= flow(m_reactor_combine_educts_m_reactor_storage_educts_2) <= 50
   0 <= flow(m_reactor_storage_educts_m_reactor_0) <= +inf
   0 <= flow(m_reactor_storage_educts_m_reactor_1) <= +inf
   0 <= flow(m_reactor_storage_educts_m_reactor_2) <= +inf
   0 <= flow(m_reactor_storage_products_ch4_0) <= 50
   0 <= flow(m_reactor_storage_products_ch4_1) <= 50
   0 <= flow(m_reactor_storage_products_ch4_2) <= 50
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_educts_0) <= 100
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_educts_1) <= 100
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_educts_2) <= 100
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_products_0) <= 1000
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_products_1) <= 1000
   0 <= GenericStorageBlock_storage_content(m_reactor_storage_products_2) <= 1000
   0 <= GenericStorageBlock_init_content(m_reactor_storage_educts) <= 100
   0 <= GenericStorageBlock_init_content(m_reactor_storage_products) <= 1000
end
