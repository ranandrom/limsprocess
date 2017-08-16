CREATE DEFINER=`root`@`localhost` TRIGGER `kmedic_tab`.`k_workflow_obj_AFTER_UPDATE` AFTER UPDATE ON `k_workflow_obj` FOR EACH ROW
BEGIN
DECLARE samplecode VARCHAR(50);-- 样本条码号
DECLARE ispl VARCHAR(50); -- 是否批量
DECLARE samplestate int default 0;  -- 样本状态
DECLARE sampleflag VARCHAR(50);     -- 状态完结情况
DECLARE sampleprogress int default 0; -- 样本进度
DECLARE project_state_max int default 0; -- 项目状态
DECLARE project_state_min int default 0; -- 项目状态
DECLARE accountid VARCHAR(50);       -- 项目id in lims
DECLARE project_progress int default 0; -- 项目进度
-- 单个样本
select sample_code from cq_sample where id = new.obj_yw_id into samplecode;
select account_id from cq_sample where id = new.obj_yw_id into accountid;
set sampleflag := new.obj_flag;
-- 批量样本  收样阶段
if samplecode is null or samplecode = '''' then
	set accountid := new.obj_yw_id;
end if;





-- 获取是否批量标记
select is_pl from cq_sample where cq_sample.sample_code = samplecode into ispl;
-- PILIANG
if new.ppoint_id=''3575ef61-c4bf-43e3-9714-2d6338b2908c'' then
	BLOCK1: begin
		DECLARE done INT DEFAULT 0;
        DECLARE c1 VARCHAR(50);
		DECLARE cur1 CURSOR FOR SELECT id FROM cq_sample where cq_sample.account_id = new.obj_yw_id;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur1;
		read_loop: LOOP
			FETCH cur1 INTO c1;
			update cq_sample set cq_sample.flag=new.obj_flag where cq_sample.id = c1;
			IF done THEN
				LEAVE read_loop;
			END IF;
		END LOOP;
		CLOSE cur1;
    end BLOCK1;
	update project_info set project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;
-- 批量收样审核
if new.ppoint_id=''d6c32cbc-88c9-443b-bacf-ab94f479a32b'' then
	BLOCK2: begin
		DECLARE done INT DEFAULT 0;
        DECLARE c2 VARCHAR(50);
		DECLARE cur2 CURSOR FOR SELECT id FROM cq_sample where cq_sample.account_id = new.obj_yw_id;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur2;
		read_loop: LOOP
			FETCH cur2 INTO c2;
			update cq_sample set cq_sample.flag=new.obj_flag where cq_sample.id = c2;
			IF done THEN
				LEAVE read_loop;
			END IF;
		END LOOP;
		CLOSE cur2;
    end BLOCK2;
	update project_info set project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;
if new.ppoint_id!=''3575ef61-c4bf-43e3-9714-2d6338b2908c'' and new.ppoint_id!=''d6c32cbc-88c9-443b-bacf-ab94f479a32b'' then
	update cq_sample set cq_sample.flag=new.obj_flag where cq_sample.sample_code = samplecode;
end if;
if ispl=''是'' then
	update project_info set project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;

if new.ppoint_id=''5e26ef42-e3e4-4a4d-bcc5-9cf13dbc6d0b'' then
	set samplestate := 5;-- 报告发送
	set sampleprogress := 95;
	if new.obj_flag=''办结'' then
		set samplestate := 6;-- 结束
		set sampleprogress := 100;
	end if;
    update cq_sample set cq_sample.state = samplestate,cq_sample.progress=sampleprogress,cq_sample.flag=new.obj_flag where cq_sample.id = new.obj_yw_id;
 end if;



END