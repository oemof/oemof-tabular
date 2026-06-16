\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(biomass_commodity_biomass_0)
+10 flow(biomass_commodity_biomass_1)
+10 flow(biomass_commodity_biomass_2)
+8.203482998751552 flow(biomass_commodity_biomass_3)
+8.203482998751552 flow(biomass_commodity_biomass_4)
+8.203482998751552 flow(biomass_commodity_biomass_5)
+6.729713331080575 flow(biomass_commodity_biomass_6)
+6.729713331080575 flow(biomass_commodity_biomass_7)
+6.729713331080575 flow(biomass_commodity_biomass_8)

s.t.

c_e_BusBlock_balance(biomass_0)_:
+1 flow(biomass_commodity_biomass_0)
= 0

c_e_BusBlock_balance(biomass_1)_:
+1 flow(biomass_commodity_biomass_1)
= 0

c_e_BusBlock_balance(biomass_2)_:
+1 flow(biomass_commodity_biomass_2)
= 0

c_e_BusBlock_balance(biomass_3)_:
+1 flow(biomass_commodity_biomass_3)
= 0

c_e_BusBlock_balance(biomass_4)_:
+1 flow(biomass_commodity_biomass_4)
= 0

c_e_BusBlock_balance(biomass_5)_:
+1 flow(biomass_commodity_biomass_5)
= 0

c_e_BusBlock_balance(biomass_6)_:
+1 flow(biomass_commodity_biomass_6)
= 0

c_e_BusBlock_balance(biomass_7)_:
+1 flow(biomass_commodity_biomass_7)
= 0

c_e_BusBlock_balance(biomass_8)_:
+1 flow(biomass_commodity_biomass_8)
= 0

c_u_SimpleFlowBlock_full_load_time_max_constr(biomass_commodity_biomass)_:
+1 flow(biomass_commodity_biomass_0)
+1 flow(biomass_commodity_biomass_1)
+1 flow(biomass_commodity_biomass_2)
+1 flow(biomass_commodity_biomass_3)
+1 flow(biomass_commodity_biomass_4)
+1 flow(biomass_commodity_biomass_5)
+1 flow(biomass_commodity_biomass_6)
+1 flow(biomass_commodity_biomass_7)
+1 flow(biomass_commodity_biomass_8)
<= 1000

bounds
   0 <= flow(biomass_commodity_biomass_0) <= 900.0
   0 <= flow(biomass_commodity_biomass_1) <= 500.0
   0 <= flow(biomass_commodity_biomass_2) <= 400.0
   0 <= flow(biomass_commodity_biomass_3) <= 900.0
   0 <= flow(biomass_commodity_biomass_4) <= 500.0
   0 <= flow(biomass_commodity_biomass_5) <= 400.0
   0 <= flow(biomass_commodity_biomass_6) <= 900.0
   0 <= flow(biomass_commodity_biomass_7) <= 500.0
   0 <= flow(biomass_commodity_biomass_8) <= 400.0
end
