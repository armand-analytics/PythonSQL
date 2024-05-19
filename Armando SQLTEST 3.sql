select zz.User_ID, zz.cw as '#Workspace_Region' from (select distinct
count(Workspace_ID) cw
,User_ID
from (select distinct
	Workspace_ID
	,User_ID
	from timecard_data td
	where year(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))='2021' and Hours_Logged>0) z
group by User_ID)zz  where zz.cw>1 order by cw asc;

/*--------------------to ansure is what we need:
-- select distinct
-- Workspace_ID
-- ,User_ID
-- from timecard_data td
-- where year(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))='2021' and Hours_Logged>0 and User_ID='11706435' */