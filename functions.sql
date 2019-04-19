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

create or replace function ign.f_cautonoma(geom1 geometry, field_name varchar default 'codnut2'::character varying)
 returns varchar
as $function$
/* returns the value of a varchar field content from table ccaa
   given a multipoint geometry geom1, geom1 must intersect ccaa.geom of multypoligon type
   field_name is the name of a varchar field in table ccaa
*/
declare
textgeom1 varchar;
field_value varchar;
field_value2 varchar;
begin
	textgeom1 = st_astext(geom1);
	execute format('select %i '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), ttmm.geom)', field_name)
	into field_value
	using textgeom1;

	execute format('select %i '
	'from ccaa '
	'where %i = $1', field_name, field_name)
	into field_value2
	using field_value;
	return field_value2;
end;
$function$ language plpgsql immutable strict;
----------------------------------------------------------------------------------------------------------------

create or replace function ign.f_provincia(geom1 geometry, field_name varchar default 'codnut2'::character varying)
 returns varchar
as $function$
/* returns the value of a varchar field content from table provincias
   given a multipoint geometry geom1, geom1 must intersect provincias.geom of multypoligon type
   field_name is the name of a varchar field in table provincias
*/
declare
textgeom1 varchar;
field_value varchar;
field_value2 varchar;
begin
	textgeom1 = st_astext(geom1);
	execute format('select %I '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), ttmm.geom)', field_name)
	into field_value
	using textgeom1;

	execute format('select %I '
	'from provincias '
	'where %I = $1', field_name, field_name)
	into field_value2
	using field_value;
	return field_value2;
end;
$function$ language plpgsql immutable strict;

----------------------------------------------------------------------------------------------------------------

create or replace function ign.f_tmunicipal(geom1 geometry, field_name varchar default 'codnut2') returns varchar
as $function$
/* returns the value of a varchar field content from table provincias
   given a multipoint geometry geom1, geom1 must intersect ccaa.geom of multypoligon type
   field_name is the name of a varchar field in table provincias
*/
declare
	textgeom1 varchar;
	field_value varchar;
begin
	textgeom1 = st_astext(geom1);
	execute format('select %I '
	'from ttmm '
	'where st_intersects (st_geomfromtext($1, 25830), ttmm.geom)', field_name)
	into field_value
	using textgeom1;
	return field_value;
end;
$function$ language plpgsql strict immutable;

--------------------------------------------------------------------------------------------------------------

create or replace function ign.f_provincia_name(geom1 geometry) 
returns setof character varying
language 'plpgsql'
strict immutable
as $function$ 
/*devuelve los nombres de las provincias en que se localiza una geometría geom1
  geom1 debe ser de tipo punto, en caso contrario devuelve null*/
begin
	if not st_isvalid(geom1) then
		return query select 'geom no válida';
	end if;
	if geometrytype(geom1) = 'geometrycollection' then
		return query select 'provincia no disponible para geom collection';
	end if;
	if st_dimension(geom1) = 0 then
		return query
		select provincias.nameunit
		from provincias 
		where st_intersects (geom1, provincias.geom) 
		union all 
		select 'fuera de provincias'
		where not exists (select provincias.nameunit from provincias where st_intersects (geom1, provincias.geom));
	else
		return query select 'geom debe ser tipo punto';
	end if;
end;
$function$
;
