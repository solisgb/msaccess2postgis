create or replace function f_is_point(geom1 geometry, verbose1 boolean default false) returns boolean as $$
/* check if geom1 is point or multipoint 
   if point or multi returns true
   else returns false
*/
declare 
	sgtype varchar()
begin
	if not st_isvalid(geom1) then
		if verbose1 then 
			raise notice 'geom not valid';
		end if;
		return false;
	end if;
	sgtype := geometrytype(geom1)
	if geometrytype(geom1) = 'geometrycollection' then
		if verbose1 then
			raise notice 'geom is ' || sgtype;
		end if;
		return false;
	end if;
	if st_dimension(geom1) = 0 then
		return true;
	else
		if verbose1 then
			raise notice 'geom is ' || geometrytype(geom1);
		end if;
		return false;
	end if;
end;
$$ language plpgsql strict immutable;

-----------------------------------------------------------------------------------------------------------

create or replace function ign.f_cautonoma(geom1 geometry, 
 field_name varchar default 'codnut1'::varchar)
 returns varchar
as $function$
/* returns the value of a varchar field content from table ccaa
   given a multipoint geometry geom1, geom1 must intersect ccaa.geom of multypoligon type
   field_name is the name of a varchar field in table ccaa
   this function uses special definition of ign tables ccaa, provincias y ttmm
*/
declare
textgeom1 varchar;
field_value varchar;
field_value1 varchar;
begin
	textgeom1 = st_astext(geom1);
	--spatial query always on table ttmm (faster) 
	execute format('select codnut1 '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), geom)')
	into field_value
	using textgeom1;

	if field_name = 'codnut1' then
		return field_value;
	end if;
	
	execute format('select %I '
	'from ccaa '
	'where codnut1 = $1', field_name)
	into field_value1
	using field_value;
	return field_value1;
end;
$function$ language plpgsql immutable strict;
----------------------------------------------------------------------------------------------------------------

create or replace function ign.f_provincia(geom1 geometry, 
 field_name varchar default 'codnut2'::varchar)
 returns varchar
as $function$
/* returns the value of a varchar field content from table provincias
   given a multipoint geometry geom1, geom1 must intersect provincias.geom of multypoligon type
   field_name is the name of a varchar field in table provincias
   this function uses special definition of ign tables ccaa, provincias y ttmm
*/
declare
textgeom1 varchar;
field_value varchar;
field_value1 varchar;
begin
	textgeom1 = st_astext(geom1);
	--spatial query always on table ttmm (faster)
	execute format('select codnut2 '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), geom)')
	into field_value
	using textgeom1;
	
	if field_name in ('codnut1', 'codnut2') then
		return field_value;
	end if;

	execute format('select %I '
	'from provincias '
	'where codnut2 = $1', field_name)
	into field_value1
	using field_value;
	return field_value1;
end;
$function$ language plpgsql immutable strict;

----------------------------------------------------------------------------------------------------------------

create or replace function ign.f_tmunicipal(geom1 geometry, 
field_name varchar default 'codnut3') returns varchar
as $function$
/* returns the value of a varchar field content from table ttmm
   given a multipoint geometry geom1, geom1 must intersect ttmm.geom of multypoligon type
   field_name is the name of a varchar field in table ttmm
*/
declare
	textgeom1 varchar;
	field_value varchar;
begin
	textgeom1 = st_astext(geom1);
	execute format('select %I '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), geom)', field_name)
	into field_value
	using textgeom1;
	return field_value;
end;
$function$ language plpgsql strict immutable;

----------------------------------------------------------------------------------------------------------------

create or replace function ign.f_mtn25(geom1 geometry, 
field_name varchar default 'mtn25_clas') returns varchar
as $function$
/* returns the value of a varchar field content from table cmtn25
   given a multipoint geometry geom1, geom1 must intersect ttmm.geom of multypoligon type
   field_name is the name of a varchar field in table ttmm
*/
declare
	textgeom1 varchar;
	field_value varchar;
begin
	textgeom1 = st_astext(geom1);
	execute format('select %I '
	'from cmtn25 '
	'where st_intersects (st_geomfromtext($1, 25830), geom)', field_name)
	into field_value
	using textgeom1;
	return field_value;
end;
$function$ language plpgsql strict immutable;

--------------------------------------------------------------------------------------------------------------


