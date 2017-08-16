CREATE DEFINER=`root`@`localhost` TRIGGER `kmedic_tab`.`cq_sample_AFTER_UPDATE` before UPDATE ON `cq_sample` FOR EACH ROW
BEGIN


if new.state = 5 then
	set new.progress := 90;
  set new.flag := '已分派';
end if;

if new.state = 6 then
    set new.progress := 100;
    set new.flag := '办结';
    set new.reported_time = CURRENT_DATE;
end if;


END