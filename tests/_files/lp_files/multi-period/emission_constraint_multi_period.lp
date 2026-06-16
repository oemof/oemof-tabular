\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_upper_limit_:
+2.5 flow(ch4_import_ch4_0)
+2.5 flow(ch4_import_ch4_1)
+2.5 flow(ch4_import_ch4_2)
+2.5 flow(ch4_import_ch4_3)
+2.5 flow(ch4_import_ch4_4)
+2.5 flow(ch4_import_ch4_5)
+2.5 flow(ch4_import_ch4_6)
+2.5 flow(ch4_import_ch4_7)
+2.5 flow(ch4_import_ch4_8)
<= 1000

c_e_BusBlock_balance(ch4_0)_:
+1 flow(ch4_import_ch4_0)
= 0

c_e_BusBlock_balance(ch4_1)_:
+1 flow(ch4_import_ch4_1)
= 0

c_e_BusBlock_balance(ch4_2)_:
+1 flow(ch4_import_ch4_2)
= 0

c_e_BusBlock_balance(ch4_3)_:
+1 flow(ch4_import_ch4_3)
= 0

c_e_BusBlock_balance(ch4_4)_:
+1 flow(ch4_import_ch4_4)
= 0

c_e_BusBlock_balance(ch4_5)_:
+1 flow(ch4_import_ch4_5)
= 0

c_e_BusBlock_balance(ch4_6)_:
+1 flow(ch4_import_ch4_6)
= 0

c_e_BusBlock_balance(ch4_7)_:
+1 flow(ch4_import_ch4_7)
= 0

c_e_BusBlock_balance(ch4_8)_:
+1 flow(ch4_import_ch4_8)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(ch4_import_ch4_0) <= 1000
   0 <= flow(ch4_import_ch4_1) <= 1000
   0 <= flow(ch4_import_ch4_2) <= 1000
   0 <= flow(ch4_import_ch4_3) <= 1000
   0 <= flow(ch4_import_ch4_4) <= 1000
   0 <= flow(ch4_import_ch4_5) <= 1000
   0 <= flow(ch4_import_ch4_6) <= 1000
   0 <= flow(ch4_import_ch4_7) <= 1000
   0 <= flow(ch4_import_ch4_8) <= 1000
end
