\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+2.5 flow(ch4_import_ch4_0_0)
+2.5 flow(ch4_import_ch4_0_1)
+2.5 flow(ch4_import_ch4_0_2)
+2.5 flow(ch4_import_ch4_1_3)
+2.5 flow(ch4_import_ch4_1_4)
+2.5 flow(ch4_import_ch4_1_5)
+2.5 flow(ch4_import_ch4_2_6)
+2.5 flow(ch4_import_ch4_2_7)
+2.5 flow(ch4_import_ch4_2_8)
<= 1000

c_e_BusBlock_balance(ch4_0_0)_:
+1 flow(ch4_import_ch4_0_0)
= 0

c_e_BusBlock_balance(ch4_0_1)_:
+1 flow(ch4_import_ch4_0_1)
= 0

c_e_BusBlock_balance(ch4_0_2)_:
+1 flow(ch4_import_ch4_0_2)
= 0

c_e_BusBlock_balance(ch4_1_3)_:
+1 flow(ch4_import_ch4_1_3)
= 0

c_e_BusBlock_balance(ch4_1_4)_:
+1 flow(ch4_import_ch4_1_4)
= 0

c_e_BusBlock_balance(ch4_1_5)_:
+1 flow(ch4_import_ch4_1_5)
= 0

c_e_BusBlock_balance(ch4_2_6)_:
+1 flow(ch4_import_ch4_2_6)
= 0

c_e_BusBlock_balance(ch4_2_7)_:
+1 flow(ch4_import_ch4_2_7)
= 0

c_e_BusBlock_balance(ch4_2_8)_:
+1 flow(ch4_import_ch4_2_8)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(ch4_import_ch4_0_0) <= 1000
   0 <= flow(ch4_import_ch4_0_1) <= 1000
   0 <= flow(ch4_import_ch4_0_2) <= 1000
   0 <= flow(ch4_import_ch4_1_3) <= 1000
   0 <= flow(ch4_import_ch4_1_4) <= 1000
   0 <= flow(ch4_import_ch4_1_5) <= 1000
   0 <= flow(ch4_import_ch4_2_6) <= 1000
   0 <= flow(ch4_import_ch4_2_7) <= 1000
   0 <= flow(ch4_import_ch4_2_8) <= 1000
end
