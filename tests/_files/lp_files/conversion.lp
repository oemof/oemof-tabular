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

c_e_BusBlock_balance(heat_0)_:
+1 flow(biomass_plant_heat_0)
= 0

c_e_BusBlock_balance(heat_1)_:
+1 flow(biomass_plant_heat_1)
= 0

c_e_BusBlock_balance(heat_2)_:
+1 flow(biomass_plant_heat_2)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_0)_:
+0.4 flow(biomass_biomass_plant_0)
-1 flow(biomass_plant_heat_0)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_1)_:
+0.4 flow(biomass_biomass_plant_1)
-1 flow(biomass_plant_heat_1)
= 0

c_e_TransformerBlock_relation(biomass_plant_biomass_heat_2)_:
+0.4 flow(biomass_biomass_plant_2)
-1 flow(biomass_plant_heat_2)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(biomass_biomass_plant_0) <= +inf
   0 <= flow(biomass_biomass_plant_1) <= +inf
   0 <= flow(biomass_biomass_plant_2) <= +inf
   0 <= flow(biomass_plant_heat_0) <= 100
   0 <= flow(biomass_plant_heat_1) <= 100
   0 <= flow(biomass_plant_heat_2) <= 100
end
