import json
import polars as pl
COLUMNS = [
    'id',
    # 'doi',
    'title',
    # 'display_name',
    # 'relevance_score',
    'publication_year',
    # 'publication_date',
    'language',
    'type',
    # 'type_crossref',
    # 'indexed_in',
    'countries_distinct_count',
    'institutions_distinct_count',
    'corresponding_author_ids',
    # 'corresponding_institution_ids',
    # 'fwci',
    # 'has_fulltext',
    # 'fulltext_origin',
    'cited_by_count',
    # 'is_retracted',
    # 'is_paratext',
    'locations_count',
    # 'datasets',
    # 'versions',
    'referenced_works_count',
    'referenced_works',
    'related_works',
    # 'ngrams_url',
    'cited_by_api_url',
    # 'updated_date',
    # 'created_date',
    # 'ids.openalex',
    # 'ids.doi',
    # 'ids.pmid',
    # 'primary_location.is_oa',
    # 'primary_location.landing_page_url',
    # 'primary_location.pdf_url',
    # 'primary_location.source.id',
    # 'primary_location.source.display_name',
    # 'primary_location.source.issn_l',
    # 'primary_location.source.issn',
    # 'primary_location.source.is_oa',
    # 'primary_location.source.is_in_doaj',
    # 'primary_location.source.is_core',
    # 'primary_location.source.host_organization',
    # 'primary_location.source.host_organization_name',
    # 'primary_location.source.host_organization_lineage',
    # 'primary_location.source.host_organization_lineage_names',
    # 'primary_location.source.type',
    # 'primary_location.license',
    # 'primary_location.license_id',
    # 'primary_location.version',
    # 'primary_location.is_accepted',
    # 'primary_location.is_published',
    # 'open_access.is_oa',
    # 'open_access.oa_status',
    # 'open_access.oa_url',
    # 'open_access.any_repository_has_fulltext',
    # 'apc_list.value',
    # 'apc_list.currency',
    # 'apc_list.value_usd',
    # 'apc_list.provenance',
    # 'apc_paid.value',
    # 'apc_paid.currency',
    # 'apc_paid.value_usd',
    # 'apc_paid.provenance',
    'cited_by_percentile_year.min',
    'cited_by_percentile_year.max',
    # 'biblio.volume',
    # 'biblio.issue',
    # 'biblio.first_page',
    # 'biblio.last_page',
    # 'primary_topic.id',
    'primary_topic.display_name',
    # 'primary_topic.score',
    # 'primary_topic.subfield.id',
    # 'primary_topic.subfield.display_name',
    # 'primary_topic.field.id',
    # 'primary_topic.field.display_name',
    # 'primary_topic.domain.id',
    # 'primary_topic.domain.display_name',
    # 'best_oa_location.is_oa',
    # 'best_oa_location.landing_page_url',
    # 'best_oa_location.pdf_url',
    # 'best_oa_location.source.id',
    # 'best_oa_location.source.display_name',
    # 'best_oa_location.source.issn_l',
    # 'best_oa_location.source.issn',
    # 'best_oa_location.source.is_oa',
    # 'best_oa_location.source.is_in_doaj',
    # 'best_oa_location.source.is_core',
    # 'best_oa_location.source.host_organization',
    # 'best_oa_location.source.host_organization_name',
    # 'best_oa_location.source.host_organization_lineage',
    # 'best_oa_location.source.host_organization_lineage_names',
    # 'best_oa_location.source.type',
    # 'best_oa_location.license',
    # 'best_oa_location.license_id',
    # 'best_oa_location.version',
    # 'best_oa_location.is_accepted',
    # 'best_oa_location.is_published',
    # 'apc_paid',
    # 'best_oa_location',
    # 'apc_list',
    # 'ids.mag',
    # 'primary_location.source',
    'abstract',
    # 'best_oa_location.source',
    # 'primary_topic',
    'authorships.author_position',
    'authorships.institutions',
    'authorships.countries',
    # 'authorships.is_corresponding',
    # 'authorships.raw_author_name',
    # 'authorships.raw_affiliation_strings',
    # 'authorships.affiliations',
    # 'authorships.author.id',
    'authorships.author.display_name',
    # 'authorships.author.orcid',
    # 'topics.id',
    'topics.display_name',
    # 'topics.score',
    # 'topics.subfield.id',
    # 'topics.subfield.display_name',
    # 'topics.field.id',
    # 'topics.field.display_name',
    # 'topics.domain.id',
    # 'topics.domain.display_name',
    # 'keywords.id',
    'keywords.display_name',
    # 'keywords.score',
    # 'concepts.id',
    # 'concepts.wikidata',
    'concepts.display_name',
    # 'concepts.level',
    # 'concepts.score',
    # 'mesh.descriptor_ui',
    'mesh.descriptor_name',
    # 'mesh.qualifier_ui',
    'mesh.qualifier_name',
    # 'mesh.is_major_topic',
    # 'locations.is_oa',
    # 'locations.landing_page_url',
    # 'locations.pdf_url',
    # 'locations.license',
    # 'locations.license_id',
    # 'locations.version',
    # 'locations.is_accepted',
    # 'locations.is_published',
    # 'locations.source.id',
    # 'locations.source.display_name',
    # 'locations.source.issn_l',
    # 'locations.source.issn',
    # 'locations.source.is_oa',
    # 'locations.source.is_in_doaj',
    # 'locations.source.is_core',
    # 'locations.source.host_organization',
    # 'locations.source.host_organization_name',
    # 'locations.source.host_organization_lineage',
    # 'locations.source.host_organization_lineage_names',
    # 'locations.source.type',
    # 'locations.source',
    # 'sustainable_development_goals.id',
    # 'sustainable_development_goals.score',
    # 'sustainable_development_goals.display_name',
    'grants.funder',
    'grants.funder_display_name',
    'grants.award_id',
    'counts_by_year.year',
    'counts_by_year.cited_by_count'
]


def normalize_institutions_udf(records_str):
    if records_str is None:
        return []
    records = records_str.split("|")
    formated_records = []
    for record_str in records:
        try:
            record = json.loads(record_str.replace("\'", "\""))
            record_new = {}
            record_new['id'] = record['id']
            record_new['display_name'] = record['display_name']
            record_new['country_code'] = record['country_code']
            record_new['type'] = record['type']
            formated_records.append(record_new)
        except:
            # print(record_str)
            continue
    return formated_records


def str_to_lst(_str):
    if _str is None:
        return []
    return _str.split("|")


def prepare_df(path):
    works = pl.read_csv(path, ignore_errors=True)
    works = works.select(COLUMNS)
    works = works.with_columns([
        pl.col('authorships.institutions').map_elements(normalize_institutions_udf, return_dtype=pl.List(pl.Struct([
            pl.Field('id', pl.Utf8),
            pl.Field('display_name', pl.Utf8),
            pl.Field('country_code', pl.Utf8),
            pl.Field('type', pl.Utf8),
        ]))).alias('institutions')
    ])

    works = works.with_columns([
        pl.col(col).map_elements(
            str_to_lst, return_dtype=pl.List(pl.Utf8)).alias(col)

        for col in [
            'grants.funder',
            'grants.funder_display_name',
            "grants.award_id",
            'concepts.display_name',
            'keywords.display_name',
            'authorships.author_position',
            'authorships.author.display_name',
            # 'authorships.institutions.display_name',
            'authorships.countries',
            'topics.display_name',
            "referenced_works",
            "related_works"
        ]
    ])
    # add primary author
    # works = works.with_columns([
    #     pl.col('authorships.author.display_name').list.first().alias('primary_author'),
    #      pl.col("institutions").map_elements(
    #               lambda x: x[0]['display_name'], return_dtype=pl.Utf8).alias("primary_institution"),

    #     #  pl.col('institutions.display_name').list.first().alias('primary_institution')
    # ])
    return works
