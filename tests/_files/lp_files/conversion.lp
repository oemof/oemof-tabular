\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(heat_0_0)_:
+1 flow(biomass_plant_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
+1 flow(biomass_plant_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
+1 flow(biomass_plant_heat_0_2)
= 0

c_e_BusBlock_balance(biomass_0_0)_:
+1 flow(biomass_biomass_plant_0_0)
= 0

c_e_BusBlock_balance(biomass_0_1)_:
+1 flow(biomass_biomass_plant_0_1)
= 0

c_e_BusBlock_balance(biomass_0_2)_:
+1 flow(biomass_biomass_plant_0_2)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_0_0)_:
-1 flow(biomass_plant_heat_0_0)
+0.4 flow(biomass_biomass_plant_0_0)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_0_1)_:
-1 flow(biomass_plant_heat_0_1)
+0.4 flow(biomass_biomass_plant_0_1)
= 0

c_e_ConverterBlock_relation(biomass_plant_biomass_heat_0_2)_:
-1 flow(biomass_plant_heat_0_2)
+0.4 flow(biomass_biomass_plant_0_2)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(biomass_plant_heat_0_0) <= 100
   0 <= flow(biomass_plant_heat_0_1) <= 100
   0 <= flow(biomass_plant_heat_0_2) <= 100
   0 <= flow(biomass_biomass_plant_0_0) <= +inf
   0 <= flow(biomass_biomass_plant_0_1) <= +inf
   0 <= flow(biomass_biomass_plant_0_2) <= +inf
end
