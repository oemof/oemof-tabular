\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+2.5 flow(ch4_import_ch4_0)
+2.5 flow(ch4_import_ch4_1)
+2.5 flow(ch4_import_ch4_2)
<= 1000

c_e_Bus_balance(ch4_0)_:
+1 flow(ch4_import_ch4_0)
= 0

c_e_Bus_balance(ch4_1)_:
+1 flow(ch4_import_ch4_1)
= 0

c_e_Bus_balance(ch4_2)_:
+1 flow(ch4_import_ch4_2)
= 0

bounds
   0 <= flow(ch4_import_ch4_0) <= +inf
   0 <= flow(ch4_import_ch4_1) <= +inf
   0 <= flow(ch4_import_ch4_2) <= +inf
end
