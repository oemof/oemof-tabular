\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+2.5 flow(ch4_import_ch4_0_0)
+2.5 flow(ch4_import_ch4_0_1)
+2.5 flow(ch4_import_ch4_0_2)
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

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(ch4_import_ch4_0_0) <= 1000
   0 <= flow(ch4_import_ch4_0_1) <= 1000
   0 <= flow(ch4_import_ch4_0_2) <= 1000
end
