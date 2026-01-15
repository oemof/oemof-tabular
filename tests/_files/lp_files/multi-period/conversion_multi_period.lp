\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(biomass_0)_:
+1 flow(biomass_biomass_plant_0)
= 0

c_e_BusBlock_balance(biomass_1)_:
+1 flow(biomass_biomass_plant_1)
= 0

c_e_BusBlock_balance(biomass_2)_:
+1 flow(biomass_biomass_plant_2)
= 0

c_e_BusBlock_balance(biomass_3)_:
+1 flow(biomass_biomass_plant_3)
= 0

c_e_BusBlock_balance(biomass_4)_:
+1 flow(biomass_biomass_plant_4)
= 0

c_e_BusBlock_balance(biomass_5)_:
+1 flow(biomass_biomass_plant_5)
= 0

c_e_BusBlock_balance(biomass_6)_:
+1 flow(biomass_biomass_plant_6)
= 0

c_e_BusBlock_balance(biomass_7)_:
+1 flow(biomass_biomass_plant_7)
= 0

c_e_BusBlock_balance(biomass_8)_:
+1 flow(biomass_biomass_plant_8)
= 0

c_e_BusBlock_balance(heat_0)_:
+1 flow(biomass_plant_heat_0)
= 0

c_e_BusBlock_balance(heat_1)_:
+1 flow(biomass_plant_heat_1)
= 0

c_e_BusBlock_balance(heat_2)_:
+1 flow(biomass_plant_heat_2)
= 0

c_e_BusBlock_balance(heat_3)_:
+1 flow(biomass_plant_heat_3)
= 0

c_e_BusBlock_balance(heat_4)_:
+1 flow(biomass_plant_heat_4)
= 0

c_e_BusBlock_balance(heat_5)_:
+1 flow(biomass_plant_heat_5)
= 0

c_e_BusBlock_balance(heat_6)_:
+1 flow(biomass_plant_heat_6)
= 0

c_e_BusBlock_balance(heat_7)_:
+1 flow(biomass_plant_heat_7)
= 0

c_e_BusBlock_balance(heat_8)_:
+1 flow(biomass_plant_heat_8)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_0)_:
+0.4 flow(biomass_biomass_plant_0)
-1 flow(biomass_plant_heat_0)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_1)_:
+0.4 flow(biomass_biomass_plant_1)
-1 flow(biomass_plant_heat_1)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_2)_:
+0.4 flow(biomass_biomass_plant_2)
-1 flow(biomass_plant_heat_2)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_3)_:
+0.4 flow(biomass_biomass_plant_3)
-1 flow(biomass_plant_heat_3)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_4)_:
+0.4 flow(biomass_biomass_plant_4)
-1 flow(biomass_plant_heat_4)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_5)_:
+0.4 flow(biomass_biomass_plant_5)
-1 flow(biomass_plant_heat_5)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_6)_:
+0.4 flow(biomass_biomass_plant_6)
-1 flow(biomass_plant_heat_6)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_7)_:
+0.4 flow(biomass_biomass_plant_7)
-1 flow(biomass_plant_heat_7)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_8)_:
+0.4 flow(biomass_biomass_plant_8)
-1 flow(biomass_plant_heat_8)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(biomass_biomass_plant_0) <= +inf
   0 <= flow(biomass_biomass_plant_1) <= +inf
   0 <= flow(biomass_biomass_plant_2) <= +inf
   0 <= flow(biomass_biomass_plant_3) <= +inf
   0 <= flow(biomass_biomass_plant_4) <= +inf
   0 <= flow(biomass_biomass_plant_5) <= +inf
   0 <= flow(biomass_biomass_plant_6) <= +inf
   0 <= flow(biomass_biomass_plant_7) <= +inf
   0 <= flow(biomass_biomass_plant_8) <= +inf
   0 <= flow(biomass_plant_heat_0) <= 100
   0 <= flow(biomass_plant_heat_1) <= 100
   0 <= flow(biomass_plant_heat_2) <= 100
   0 <= flow(biomass_plant_heat_3) <= 100
   0 <= flow(biomass_plant_heat_4) <= 100
   0 <= flow(biomass_plant_heat_5) <= 100
   0 <= flow(biomass_plant_heat_6) <= 100
   0 <= flow(biomass_plant_heat_7) <= 100
   0 <= flow(biomass_plant_heat_8) <= 100
end
