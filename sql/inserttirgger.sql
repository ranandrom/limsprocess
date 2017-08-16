CREATE DEFINER=`root`@`localhost` TRIGGER `kmedic_tab`.`k_workflow_obj_AFTER_INSERT` AFTER INSERT ON `k_workflow_obj` FOR EACH ROW
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
if samplecode is null or samplecode = '' then
	-- select sample_code from cq_sample where account_id = new.obj_yw_id into samplecode;
	set accountid := new.obj_yw_id;
	set project_progress := 20;-- 收样中
    -- update project_info set project_info.manager_name = '未命名项目',project_info.manager_state = project_state,project_info.manager_progress=project_progress,project_info.flag=flag where  project_info.sample_id = accountid;
end if;
-- 获取是否批量标记
select is_pl from cq_sample where cq_sample.sample_code = samplecode into ispl;
if new.ppoint_id='5b0fe078-c120-4ec6-b464-d03e7c89abd1' then
	set samplestate := 0;-- 收样登记
	set sampleprogress := 16;
end if;
if new.ppoint_id='aee64909-e51b-4beb-8c04-18f3e8b0f3c1' then
	set samplestate := 1;-- 收样审核
	set sampleprogress := 32;
end if;
if new.ppoint_id='d01478c9-5418-4ec8-98fd-646524ec684f' then
	set samplestate := 2;-- 信息录入 
	set sampleprogress := 48;
-- 	if ispl='是' then
-- 		set project_state_max := 1;-- 实验中
-- 		set project_progress := 40;
-- 	end if;
end if;
if new.ppoint_id='024f86f2-3cc3-497a-99a3-68b580b298c2' then
	set samplestate := 3;-- 检测结果 
	set sampleprogress := 64;
-- 	if ispl='是' then
-- 		set project_state := 2;-- 分析检测中
-- 		set project_progress := 60;
-- 	end if;
end if;
if new.ppoint_id='4d279527-23b2-49e3-b07e-05c7229ef6c9' then
	set samplestate := 4;-- 生成报告 
	set sampleprogress := 80;
-- 	if ispl='是' then
-- 		set project_state := 3;-- 报告中
-- 		set project_progress := 80;
-- 	end if;
end if;

if new.ppoint_id='5e26ef42-e3e4-4a4d-bcc5-9cf13dbc6d0b' then
	set samplestate := 5;-- 报告发送
	set sampleprogress := 95;
	if new.obj_flag='办结' then
		set samplestate := 6;-- 结束
		set sampleprogress := 100;
	end if;
end if;
 
if new.ppoint_id='3575ef61-c4bf-43e3-9714-2d6338b2908c' then
	set samplestate := -1;-- 批量收样登记 
    set sampleprogress := 16;
    -- update project_info set project_info.manager_name = '未命名项目2',project_info.manager_state = project_state,project_info.manager_progress=project_progress,project_info.flag=flag where  project_info.sample_id = accountid;
	BLOCK1: begin
		DECLARE done INT DEFAULT 0;
        DECLARE c1 VARCHAR(50);
		DECLARE cur1 CURSOR FOR SELECT id FROM cq_sample where cq_sample.account_id = new.obj_yw_id;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur1;
		read_loop: LOOP
			FETCH cur1 INTO c1;
			update cq_sample set cq_sample.state = samplestate,cq_sample.progress=sampleprogress,cq_sample.flag=new.obj_flag where cq_sample.id = c1;
			IF done THEN
				LEAVE read_loop;
			END IF;
		END LOOP; 
		CLOSE cur1;
    end BLOCK1;
    BLOCK4: begin
		DECLARE project_sample_count int default 0; -- 项目所有样本
		DECLARE all_progress int default 0;
		DECLARE done INT DEFAULT 0;
		DECLARE c3 int default 0;
        DECLARE sid VARCHAR(50);  
		DECLARE cur CURSOR FOR SELECT id,progress FROM cq_sample where cq_sample.account_id = accountid;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur;
		read_loop: LOOP
			FETCH cur INTO sid,c3;
            IF done THEN
				LEAVE read_loop;
			END IF;
			set all_progress := all_progress + c3;
			set project_sample_count := project_sample_count + 1;            
		END LOOP; 
        set project_progress := (all_progress / project_sample_count) ;
		CLOSE cur;
		
	end BLOCK4;
    select max(state) from cq_sample where account_id = accountid into project_state_max;
    select min(state) from cq_sample where account_id = accountid into project_state_min;
    if project_progress=100 then
		set project_state_max := 6;-- 结束 
        set project_state_min := 6;-- 结束 
	end if;
	update project_info set project_info.manager_state_max = project_state_max,project_info.manager_state_min = project_state_min,project_info.manager_progress=project_progress,project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;
if new.ppoint_id='d6c32cbc-88c9-443b-bacf-ab94f479a32b' then
	set samplestate := -2;-- 批量收样审核
    set sampleprogress := 32;
	BLOCK2: begin
		DECLARE done INT DEFAULT 0;
        DECLARE c2 VARCHAR(50);
		DECLARE cur2 CURSOR FOR SELECT id FROM cq_sample where cq_sample.account_id = new.obj_yw_id;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur2;
		read_loop: LOOP
			FETCH cur2 INTO c2;
			update cq_sample set cq_sample.state = samplestate,cq_sample.progress=sampleprogress,cq_sample.flag=new.obj_flag where cq_sample.id = c2;
			IF done THEN
				LEAVE read_loop;
			END IF;
		END LOOP; 
		CLOSE cur2;
    end BLOCK2;
    BLOCK5: begin
		DECLARE project_sample_count int default 0; -- 项目所有样本
		DECLARE all_progress int default 0;
		DECLARE done INT DEFAULT 0;
		DECLARE c3 int default 0;
        DECLARE sid VARCHAR(50);  
		DECLARE cur CURSOR FOR SELECT id,progress FROM cq_sample where cq_sample.account_id = accountid;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur;
		read_loop: LOOP
			FETCH cur INTO sid,c3;
            IF done THEN
				LEAVE read_loop;
			END IF;
			set all_progress := all_progress + c3;
			set project_sample_count := project_sample_count + 1;            
		END LOOP; 
        set project_progress := (all_progress / project_sample_count) ;
		CLOSE cur;
		
	end BLOCK5;
    select max(state) from cq_sample where account_id = accountid into project_state_max;
    select min(state) from cq_sample where account_id = accountid into project_state_min;
    if project_progress=100 then
		set project_state_max := 6;-- 结束 
        set project_state_min := 6;-- 结束 
	end if;
	update project_info set project_info.manager_state_max = project_state_max,project_info.manager_state_min = project_state_min,project_info.manager_progress=project_progress,project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;
if new.ppoint_id!='3575ef61-c4bf-43e3-9714-2d6338b2908c' and new.ppoint_id!='d6c32cbc-88c9-443b-bacf-ab94f479a32b' then
	update cq_sample set cq_sample.state = samplestate,cq_sample.progress=sampleprogress,cq_sample.flag=new.obj_flag where cq_sample.sample_code = samplecode;
end if;
if ispl='是' then
	BLOCK3: begin
		DECLARE project_sample_count int default 0; -- 项目所有样本
		DECLARE all_progress int default 0;
		DECLARE done INT DEFAULT 0;
		DECLARE c3 int default 0;
        DECLARE sid VARCHAR(50);  
		DECLARE cur CURSOR FOR SELECT id,progress FROM cq_sample where cq_sample.account_id = accountid;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
		OPEN cur;
		read_loop: LOOP
			FETCH cur INTO sid,c3;
            IF done THEN
				LEAVE read_loop;
			END IF;
			set all_progress := all_progress + c3;
			set project_sample_count := project_sample_count + 1;            
		END LOOP; 
        set project_progress := (all_progress / project_sample_count) ;
		CLOSE cur;
		
	end BLOCK3;
    select max(state) from cq_sample where account_id = accountid into project_state_max;
    select min(state) from cq_sample where account_id = accountid into project_state_min;
    if project_progress=100 then
		set project_state_max := 6;-- 结束 
        set project_state_min := 6;-- 结束 
	end if;
	update project_info set project_info.manager_state_max = project_state_max,project_info.manager_state_min = project_state_min,project_info.manager_progress=project_progress,project_info.manager_flag=new.obj_flag where project_info.sample_id = accountid;
end if;
END