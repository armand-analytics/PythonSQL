select x.Workspace_Region, sum(x.serv_bgt) as total_s_b
from (
select distinct pd.Workspace_Region, cast(REPLACE(sd.Services_Budget, '$', '') as decimal(10, 2)) as serv_bgt
from sales_data sd
left join Project_Data pd on pd.Opportunity_ID =sd.Opportunity_ID) x 
group by x.Workspace_Region 