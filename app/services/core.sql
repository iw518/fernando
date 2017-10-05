/*sql 文件开始
sql语句块按下列格式书写，便于read_sql函数解析:
--start func_name
  ......
  sql语句
  ......
--end func_name

*/

--start find_sections
/*查询剖面数据*/
SELECT
  pouatt.PouNo,
  pholeatt.holeno,
  pmhole.distance
FROM pmhole
  INNER JOIN pouatt ON pmhole.pnumber = pouatt.pnumber
  INNER JOIN pholeatt ON pmhole.hnumber = pholeatt.hnumber
  INNER JOIN base ON pmhole.project_count = base.project_count
                     AND base.project_count = pholeatt.project_count
WHERE base.project_name = '{}'
ORDER BY pmhole.tid
--end find_sections


--start find_holes_with_BG
/*查询带标贯试验点的勘探孔
返回holeName, bgPoint, testDep, N635, clayContent, soilType
*/
SELECT
  soilhole.soil_holeNo,
  pmbg.bgpoint,
  (pmbg.startpos + pmbg.endpos) / 2,
  pmbg.n635,
  grain.k_0005,
  grain.k025_0074
FROM ((pmbg
  INNER JOIN base ON pmbg.project_count = base.project_count)
  INNER JOIN soilhole
    ON (pmbg.hnumber = soilhole.hnumber) AND (base.project_count = soilhole.project_count))
  INNER JOIN (grain
    RIGHT JOIN main ON grain.tnumber = main.tnumber)
    ON (pmbg.startpos = main.stardep) AND (soilhole.soil_hnumber = main.soil_hnumber)
WHERE (base.project_name) = '{}'
ORDER BY LEN(soilhole.soil_holeNo), soilhole.soil_holeNo,
  Len(pmbg.bgpoint), pmbg.bgpoint
--end find_holes_with_BG

--start find_holes_with_layer
/*
查询勘探孔分层
必须按照norder排序,不能按照zp93.anumber排序
*/
SELECT
  pholeatt.holeno,
  zp93.dep,
  zp93.norder
FROM (zp93
  INNER JOIN base
    ON zp93.project_count = base.project_count)
  INNER JOIN pholeatt ON zp93.hnumber = pholeatt.hnumber
WHERE base.project_name = '{0}' AND pholeatt.attribute > {1} AND pholeatt.attribute <{2}
ORDER BY pholeatt.attribute, zp93.norder, LEN(pholeatt.holeno),
pholeatt.holeno
--end find_holes_with_layer


--start find_holes_with_info
/*
查询所有勘探孔标高、孔深、水位及勘探孔类型
查找每个项目所含钻孔及其孔深，返回list[hole,....],
hole主要组成为hole.holeName,hole.Dep
*/
SELECT
  pholeatt.holeno,
  pholeatt.height,
  pholeatt.depth,
  pholeatt.waterlevel,
  pholeatt.attribute
FROM pholeatt
  INNER JOIN base
    ON pholeatt.project_count = base.project_count
WHERE base.project_name = '{0}' AND pholeatt.attribute >{1} AND pholeatt.attribute <{2}
ORDER BY pholeatt.attribute, pholeatt.hole_order,
LEN(pholeatt.holeno), pholeatt.holeno
--end find_holes_with_info

--start find_holes_with_dep
/*
查询所有取土孔，及对应终孔土样深度
*/
SELECT
  soilhole.soil_holeNo,
  Max(main.enddep)
FROM (soilhole
  INNER JOIN main ON
                    soilhole.soil_hnumber = main.soil_hnumber)
  INNER JOIN base ON soilhole.project_count = base.project_count
GROUP BY
  soilhole.hole_order, soilhole.soil_holeNo, base.project_name
HAVING base.project_name = '{}'
ORDER BY
  len(soilhole.soil_holeNo),
  soilhole.soil_holeNo,
  soilhole.hole_order
--end find_holes_with_dep

--start find_CPT
/*
查询所有静力触探孔及对应Ps数据
*/
SELECT
  pholeatt.holeno,
  tpfs.qc_fs
FROM (tpfs
  INNER JOIN base
    ON tpfs.project_count = base.project_count)
  INNER JOIN pholeatt
    ON base.project_count = pholeatt.project_count
WHERE base.project_name = '{}'
      AND (pholeatt.hnumber = tpfs.hnumber)
      AND (pholeatt.attribute = 2)
ORDER BY LEN(pholeatt.holeno), pholeatt.holeno,
  pholeatt.hnumber
--end find_CPT


--start find_layers
/*
查找项目分层信息
此处采用right join，为了防止部分地层地质时代为空
*/
SELECT
  pmlayer.layerno,
  pmlayer.layername,
  geologic_age.geologic_age
FROM geologic_age
  RIGHT JOIN (pmlayer
    INNER JOIN base ON
                      pmlayer.project_count = base.project_count)
    ON geologic_age.anumber = pmlayer.anumber
WHERE base.project_name = '{}'
ORDER BY pmlayer.layerorder
--end find_layers

--start retrieve_common_index
SELECT
  Count(p0),
  Count(wl),
  Count(c),
  Count(a01_02)
FROM rules
  INNER JOIN base
    ON rules.project_count = base.project_count
WHERE base.project_name = '{}' AND rules.CQ_flag = 0

--end retrieve_common_index

--start retrieve_grain_index
/*(k_2,k2_05,k05_025,k025_0074,k0074_005,k005_001,k001_0005,k_0002)*/
SELECT Count(grain.project_count)
FROM grain
  INNER JOIN base
    ON grain.project_count = base.project_count
WHERE base.project_name = '{}'
--end retrieve_grain_index

--start retrieve_penetration_index
SELECT Count(kv)
FROM rules
  INNER JOIN base
    ON rules.project_count = base.project_count
WHERE base.project_name = '{}' AND rules.CQ_flag = 0
--end retrieve_penetration_index

--start retrieve_special_index
SELECT
  Count(cu),
  Count(ccu),
  Count(qu),
  Count(k0),
  Count(nn)
FROM trial
  INNER JOIN base
    ON trial.project_count = base.project_count
WHERE base.project_name = '{}'
--end retrieve_special_index

--start retrieve_slow_shearing_index
SELECT Count(c)
FROM rules
  INNER JOIN base
    ON rules.project_count = base.project_count
WHERE base.project_name = '{}' AND rules.CQ_flag = 32
--end retrieve_slow_shearing_index

--start retrieve_quick_shearing_index
SELECT Count(c)
FROM rules
  INNER JOIN base
    ON rules.project_count = base.project_count
WHERE base.project_name = '{}' AND rules.CQ_flag = 16

--end retrieve_quick_shearing_index

--start retrieve_spt_index
SELECT Count(*)
FROM pmbg
  INNER JOIN base
    ON pmbg.project_count = base.project_count
WHERE base.project_name = '{}'
--end retrieve_spt_index

--start retrieve_indexes.enterprise
SELECT
  pmlayer.layerno,
  pmlayer.layername,
    'PS1' = Sum(CASE titemdata.itemCode
                WHEN 'PS1'
                  THEN titemdata.iavg
                ELSE 0 END),
    'DENSITY' = Sum(CASE titemdata.itemCode
                    WHEN 'DENSITY'
                      THEN titemdata.iavg
                    ELSE 0 END),
    'CON_C' = Sum(CASE titemdata.itemCode
                  WHEN 'CON_C'
                    THEN titemdata.iavg
                  ELSE 0 END),
    'CON_F' = Sum(CASE titemdata.itemCode
                  WHEN 'CON_F'
                    THEN titemdata.iavg
                  ELSE 0 END),
    'QUICK_C' = Sum(CASE titemdata.itemCode
                    WHEN 'QUICK_C'
                      THEN titemdata.iavg
                    ELSE 0 END),
    'QUICK_F' = Sum(CASE titemdata.itemCode
                    WHEN 'QUICK_F'
                      THEN titemdata.iavg
                    ELSE 0 END),
    'SLOW_C' = Sum(CASE titemdata.itemCode
                   WHEN 'SLOW_C'
                     THEN titemdata.iavg
                   ELSE 0 END),
    'SLOW_F' = Sum(CASE titemdata.itemCode
                   WHEN 'SLOW_F'
                     THEN titemdata.iavg
                   ELSE 0 END),
    'CCU' = Sum(CASE titemdata.itemCode
                WHEN 'CCU'
                  THEN titemdata.iavg
                ELSE 0 END),
    'FCU' = Sum(CASE titemdata.itemCode
                WHEN 'FCU'
                  THEN titemdata.iavg
                ELSE 0 END),
    'CU' = Sum(CASE titemdata.itemCode
               WHEN 'CU'
                 THEN titemdata.iavg
               ELSE 0 END),
    'FU' = Sum(CASE titemdata.itemCode
               WHEN 'FU'
                 THEN titemdata.iavg
               ELSE 0 END),
    'KH' = Sum(CASE titemdata.itemCode
               WHEN 'KH'
                 THEN titemdata.iavg
               ELSE 0 END),
    'KV' = Sum(CASE titemdata.itemCode
               WHEN 'KV'
                 THEN titemdata.iavg
               ELSE 0 END),
    'K0' = Sum(CASE titemdata.itemCode
               WHEN 'K0'
                 THEN titemdata.iavg
               ELSE 0 END)
FROM titemdata
  INNER JOIN pmlayer ON titemdata.anumber = pmlayer.anumber
  INNER JOIN base
    ON titemdata.project_count = base.project_count
WHERE (base.project_name) = '{}' AND titemdata.age_no = 0
GROUP BY pmlayer.layerorder, pmlayer.layerno, pmlayer.layername
--end retrieve_indexes.enterprise

--start retrieve_indexes.personal
/*
ref:https://stackoverflow.com/questions/33769143/issue-querying-from-access-database-could-not-convert-string-to-float-e6

This appears to be a compatibility issue between pypyodbc and the Access ODBC driver
when retrieving "large" or "small" numbers from a Single or Double field (column),
where "large" means  Single values with more than 6 significant digits to the left of the decimal point,
or Double values with more than 14 significant digits to the left of the decimal point
and "small" means Single values with more than 6 zeros immediately to the right of the decimal point,
or Double values with more than 14 zeros immediately to the right of the decimal point
when the numbers are represented as "normal" decimals (i.e., not in scientific notation).
Workaround 1: For Single values, using the CDbl() function can avoid the error:
Workaround 2: Use the CStr() function to return the value as a string and then convert it to a float afterwards (works for both Single and Double):
*/
SELECT
  pmlayer.layerno,
  pmlayer.layername,
  Sum(iif(titemdata.itemCode = 'PS1', titemdata.iavg, 0))      AS 'PS1',
  Sum(iif(titemdata.itemCode = 'DENSITY', titemdata.iavg, 0))  AS 'DENSITY',
  Sum(iif(titemdata.itemCode = 'CON_C', titemdata.iavg, 0))    AS 'CON_C',
  Sum(iif(titemdata.itemCode = 'CON_F', titemdata.iavg, 0))    AS 'CON_F',
  Sum(iif(titemdata.itemCode = 'QUICK_C', titemdata.iavg, 0))  AS 'QUICK_C',
  Sum(iif(titemdata.itemCode = 'QUICK_F', titemdata.iavg, 0))  AS 'QUICK_F',
  Sum(iif(titemdata.itemCode = 'SLOW_C', titemdata.iavg, 0))   AS 'SLOW_C',
  Sum(iif(titemdata.itemCode = 'SLOW_F', titemdata.iavg, 0))   AS 'SLOW_F',
  Sum(iif(titemdata.itemCode = 'CCU', titemdata.iavg, 0))      AS 'CCU',
  Sum(iif(titemdata.itemCode = 'FCU', titemdata.iavg, 0))      AS 'FCU',
  Sum(iif(titemdata.itemCode = 'CU', titemdata.iavg, 0))       AS 'CU',
  Sum(iif(titemdata.itemCode = 'FU', titemdata.iavg, 0))       AS 'FU',
  Sum(iif(titemdata.itemCode = 'KH', Cstr(titemdata.iavg), 0)) AS 'KH',
  Sum(iif(titemdata.itemCode = 'KV', Cstr(titemdata.iavg), 0)) AS 'KV',
  Sum(iif(titemdata.itemCode = 'K0', titemdata.iavg, 0))       AS 'K0'
FROM (titemdata
  INNER JOIN pmlayer ON titemdata.anumber = pmlayer.anumber)
  INNER JOIN base
    ON titemdata.project_count = base.project_count
WHERE base.project_name = '{}' AND titemdata.age_no = 0
GROUP BY pmlayer.layerorder, pmlayer.layerno, pmlayer.layername
--end retrieve_indexes.personal