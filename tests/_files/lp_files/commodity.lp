\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(biomass_commodity_biomass_0_0)
+10 flow(biomass_commodity_biomass_0_1)
+10 flow(biomass_commodity_biomass_0_2)

s.t.

c_e_BusBlock_balance(biomass_0_0)_:
+1 flow(biomass_commodity_biomass_0_0)
= 0

c_e_BusBlock_balance(biomass_0_1)_:
+1 flow(biomass_commodity_biomass_0_1)
= 0

c_e_BusBlock_balance(biomass_0_2)_:
+1 flow(biomass_commodity_biomass_0_2)
= 0

c_u_SimpleFlowBlock_full_load_time_max_constr(biomass_commodity_biomass)_:
+1 flow(biomass_commodity_biomass_0_0)
+1 flow(biomass_commodity_biomass_0_1)
+1 flow(biomass_commodity_biomass_0_2)
<= 1000

bounds
   0 <= flow(biomass_commodity_biomass_0_0) <= 900.0
   0 <= flow(biomass_commodity_biomass_0_1) <= 500.0
   0 <= flow(biomass_commodity_biomass_0_2) <= 400.0
end
