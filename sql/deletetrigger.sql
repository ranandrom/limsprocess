CREATE DEFINER=`root`@`localhost` TRIGGER `kmedic_tab`.`k_workflow_obj_AFTER_DELETE` AFTER DELETE ON `k_workflow_obj` FOR EACH ROW
BEGIN

DECLARE samplecode VARCHAR(50);-- 样本条码号
DECLARE samplestate int default 0;  -- 样本状态
DECLARE sampleprogress int default 0; -- 样本进度

-- 单个样本
select sample_code from cq_sample where id = old.obj_yw_id into samplecode;


if old.ppoint_id='aee64909-e51b-4beb-8c04-18f3e8b0f3c1' then
	set samplestate := 0;-- 收样审核
	set sampleprogress := 16;
end if;
if old.ppoint_id='d01478c9-5418-4ec8-98fd-646524ec684f' then
	set samplestate := 1;-- 信息录入
	set sampleprogress := 32;
end if;
if old.ppoint_id='024f86f2-3cc3-497a-99a3-68b580b298c2' then
	set samplestate := 2;-- 检测结果
	set sampleprogress := 48;
end if;
if old.ppoint_id='4d279527-23b2-49e3-b07e-05c7229ef6c9' then
	set samplestate := 3;-- 生成报告
	set sampleprogress := 64;
end if;

if old.ppoint_id='5e26ef42-e3e4-4a4d-bcc5-9cf13dbc6d0b' then
	set samplestate := 4;-- 报告发送
	set sampleprogress := 80;
end if;

if old.ppoint_id!='3575ef61-c4bf-43e3-9714-2d6338b2908c' and old.ppoint_id!='d6c32cbc-88c9-443b-bacf-ab94f479a32b' then
	update cq_sample set cq_sample.state = samplestate,cq_sample.progress=sampleprogress where cq_sample.sample_code = samplecode;
end if;


END