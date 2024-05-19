#availabletimetable
select distinct
User_ID, 
monthNameY,
sum(realNetAvailableTimeweek),sum(admintime),sum(billableTime), sum(efectiveTime), sum(ptoTime),
sum(billableTime)/sum(realNetAvailableTimeweek) as 'Billable Utilization %' ,
sum(efectiveTime)/sum(realNetAvailableTimeweek) as 'Effective Utilization %'
from(
select distinct 
User_ID
,weekYear
,numdaysofweek
,availableTime as SimpleAvTime
,realTimeperweekyear
,ptoTime
,availableTime-ptoTime as AvailableTime
,realTimeperweekyear-ptoTime as realNetAvailableTimeweek
,admintime
,billableTime
,efectiveTime
,monthNameY
from (
select distinct
yy.User_ID,
yy.llave, td.llave as llave2
,sum(yy.adminHrs) as admintime
,sum(yy.billableHrs) as billableTime
,sum(yy.efectiveHrs) as efectiveTime
,yy.weekYear
,sum(yy.ptoHrs) as ptoTime
,td.availableweekHours as availableTime
,td.numdaysofweek*8 as realTimeperweekyear
,td.numdaysofweek, yy.monthNameY
from (
select distinct
User_ID,
sum(adminHrs) as adminHrs,
SUM(efectiveHrs) as efectiveHrs,
sum(billableHrs) as billableHrs
,weekYear
,ptoHrs
,concat(User_ID, weekYear) as llave
,monthNameY
from (
select distinct
t.User_ID
,weekofyear(STR_TO_DATE(Timecard_Date, '%d/%m/%Y')) as weekYear
,concat(monthname(STR_TO_DATE(Timecard_Date, '%d/%m/%Y')), '-', year(STR_TO_DATE(t.Timecard_Date, '%d/%m/%Y'))) as monthNameY
,p.Project_Type
,case when Project_Type='PTO' then sum(Hours_Logged) else 0 end as ptoHrs
,case when Project_Type='Billable' then sum(Hours_Logged) else 0 end as billableHrs
,case when Project_Type='Other Admin' then sum(Hours_Logged) else 0 end as adminHrs
,case when Project_Type in ('Billable','Discretionary', 'Non-Discretionary' ) then sum(Hours_Logged) else 0 end as efectiveHrs
from timecard_data t left join project_data p on p.Workspace_ID=t.Workspace_ID
-- where  t.User_ID in ('9805405', '9862085')   -- and weekofyear(STR_TO_DATE(t.Timecard_Date, '%d/%m/%Y'))='41'
-- year(STR_TO_DATE(t.Timecard_Date, '%d/%m/%Y'))='2020'
-- and month(STR_TO_DATE(t.Timecard_Date, '%d/%m/%Y'))='10'
group by 
t.User_ID,
User_ID||weekYear,
p.Project_Type, 
t.Timecard_Date
order by weekofyear(STR_TO_DATE(t.Timecard_Date, '%d/%m/%Y')) asc) x group by User_ID, weekYear, ptoHrs, monthNameY
) yy inner join (select distinct	
						User_ID
                        ,concat(User_ID, weekofyear(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))) as llave                        
						,count(distinct dayname((STR_TO_DATE(Timecard_Date, '%d/%m/%Y')))) as numdaysofweek
						,40 as availableweekHours 
                        from timecard_data
						-- where User_ID in ('9805405', '9862085')-- and 
                        -- year(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))='2020'
						-- and month(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))='10'
						-- and weekofyear(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))='40'
						group by User_ID, concat(User_ID, weekofyear(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))) ) td on yy.llave=td.llave
group by 
yy.User_ID, yy.weekYear, yy.monthNameY, td.numdaysofweek) z) zz group by User_ID, monthNameY
order by User_ID, monthNameY 