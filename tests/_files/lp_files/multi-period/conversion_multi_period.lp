\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(biomass_0_0)_:
+1 flow(biomass_biomass_plant_0_0)
= 0

c_e_BusBlock_balance(biomass_0_1)_:
+1 flow(biomass_biomass_plant_0_1)
= 0

c_e_BusBlock_balance(biomass_0_2)_:
+1 flow(biomass_biomass_plant_0_2)
= 0

c_e_BusBlock_balance(biomass_1_3)_:
+1 flow(biomass_biomass_plant_1_3)
= 0

c_e_BusBlock_balance(biomass_1_4)_:
+1 flow(biomass_biomass_plant_1_4)
= 0

c_e_BusBlock_balance(biomass_1_5)_:
+1 flow(biomass_biomass_plant_1_5)
= 0

c_e_BusBlock_balance(biomass_2_6)_:
+1 flow(biomass_biomass_plant_2_6)
= 0

c_e_BusBlock_balance(biomass_2_7)_:
+1 flow(biomass_biomass_plant_2_7)
= 0

c_e_BusBlock_balance(biomass_2_8)_:
+1 flow(biomass_biomass_plant_2_8)
= 0

c_e_BusBlock_balance(heat_0_0)_:
+1 flow(biomass_plant_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
+1 flow(biomass_plant_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
+1 flow(biomass_plant_heat_0_2)
= 0

c_e_BusBlock_balance(heat_1_3)_:
+1 flow(biomass_plant_heat_1_3)
= 0

c_e_BusBlock_balance(heat_1_4)_:
+1 flow(biomass_plant_heat_1_4)
= 0

c_e_BusBlock_balance(heat_1_5)_:
+1 flow(biomass_plant_heat_1_5)
= 0

c_e_BusBlock_balance(heat_2_6)_:
+1 flow(biomass_plant_heat_2_6)
= 0

c_e_BusBlock_balance(heat_2_7)_:
+1 flow(biomass_plant_heat_2_7)
= 0

c_e_BusBlock_balance(heat_2_8)_:
+1 flow(biomass_plant_heat_2_8)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_0_0)_:
+0.4 flow(biomass_biomass_plant_0_0)
-1 flow(biomass_plant_heat_0_0)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_0_1)_:
+0.4 flow(biomass_biomass_plant_0_1)
-1 flow(biomass_plant_heat_0_1)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_0_2)_:
+0.4 flow(biomass_biomass_plant_0_2)
-1 flow(biomass_plant_heat_0_2)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_1_3)_:
+0.4 flow(biomass_biomass_plant_1_3)
-1 flow(biomass_plant_heat_1_3)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_1_4)_:
+0.4 flow(biomass_biomass_plant_1_4)
-1 flow(biomass_plant_heat_1_4)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_1_5)_:
+0.4 flow(biomass_biomass_plant_1_5)
-1 flow(biomass_plant_heat_1_5)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_2_6)_:
+0.4 flow(biomass_biomass_plant_2_6)
-1 flow(biomass_plant_heat_2_6)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_2_7)_:
+0.4 flow(biomass_biomass_plant_2_7)
-1 flow(biomass_plant_heat_2_7)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_2_8)_:
+0.4 flow(biomass_biomass_plant_2_8)
-1 flow(biomass_plant_heat_2_8)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(biomass_biomass_plant_0_0) <= +inf
   0 <= flow(biomass_biomass_plant_0_1) <= +inf
   0 <= flow(biomass_biomass_plant_0_2) <= +inf
   0 <= flow(biomass_biomass_plant_1_3) <= +inf
   0 <= flow(biomass_biomass_plant_1_4) <= +inf
   0 <= flow(biomass_biomass_plant_1_5) <= +inf
   0 <= flow(biomass_biomass_plant_2_6) <= +inf
   0 <= flow(biomass_biomass_plant_2_7) <= +inf
   0 <= flow(biomass_biomass_plant_2_8) <= +inf
   0 <= flow(biomass_plant_heat_0_0) <= 100
   0 <= flow(biomass_plant_heat_0_1) <= 100
   0 <= flow(biomass_plant_heat_0_2) <= 100
   0 <= flow(biomass_plant_heat_1_3) <= 100
   0 <= flow(biomass_plant_heat_1_4) <= 100
   0 <= flow(biomass_plant_heat_1_5) <= 100
   0 <= flow(biomass_plant_heat_2_6) <= 100
   0 <= flow(biomass_plant_heat_2_7) <= 100
   0 <= flow(biomass_plant_heat_2_8) <= 100
end
