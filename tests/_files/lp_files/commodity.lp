\* Source Pyomo model name=Model *\

min
objective:
+10 flow(biomass_commodity_biomass_0)
+10 flow(biomass_commodity_biomass_1)
+10 flow(biomass_commodity_biomass_2)

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

c_u_SimpleFlowBlock_full_load_time_max_constr(biomass_commodity_biomass)_:
+1 flow(biomass_commodity_biomass_0)
+1 flow(biomass_commodity_biomass_1)
+1 flow(biomass_commodity_biomass_2)
<= 1000

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(biomass_commodity_biomass_0) <= 900
   0 <= flow(biomass_commodity_biomass_1) <= 500
   0 <= flow(biomass_commodity_biomass_2) <= 400
end
