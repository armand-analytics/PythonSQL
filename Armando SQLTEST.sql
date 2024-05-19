Select
z.User_ID
,z.User_Role
,z.User_Geography
,z.User_Team
,z.User_End_Date
,z.User_Start_Date
from (select *, 
IFNULL((STR_TO_DATE(User_End_Date, '%d/%m/%Y')) - (STR_TO_DATE(User_Start_Date, '%d/%m/%Y')), 'Active')  as IsActive
from dba1.user_data
where IFNULL((STR_TO_DATE(User_End_Date, '%d/%m/%Y')) - (STR_TO_DATE(User_Start_Date, '%d/%m/%Y')), 'Active') ='Active') z
inner join (
select User_ID from (
select distinct User_ID, 
case when Hours_Logged=0 and month(STR_TO_DATE(Timecard_Date, '%d/%m/%Y'))=12 then 'notlogDec' else '0' end as flag1,
month(STR_TO_DATE(Timecard_Date, '%d/%m/%Y')) as month
#year(STR_TO_DATE(Timecard_Date, '%d/%m/%y')) as year
from dba1.timecard_data) x
where x.flag1 = 'notlogDec') y on y.User_ID=z.User_ID ;