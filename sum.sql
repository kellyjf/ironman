.head on
.mode tabs
.out sum.txt
select strftime("%W",logtime) as Week ,
	sum(case when sport='Swim' then minutes end)/60. as 'SwimTime' ,
	sum(case when sport='Bike' then minutes end)/60. as 'BikeTime' ,
	sum(case when sport='Run' then minutes end)/60. as 'RunTime'  ,
	sum(case when sport='Swim' then distance end) as 'Swim' ,
	sum(case when sport='Bike' then distance end) as 'Bike' ,
	sum(case when sport='Run' then distance end) as 'Run'  
from workouts group by 1;
