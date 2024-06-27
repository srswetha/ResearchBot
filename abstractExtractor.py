import requests
from lxml import etree

def jats_to_plain_text(jats_xml):
    wrapped_xml = f'<root xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1">{jats_xml}</root>'
    parser = etree.XMLParser(recover=True, ns_clean=True)
    root = etree.fromstring(wrapped_xml.encode('utf-8'), parser=parser)
    text_parts = []
    title = root.xpath('//*[local-name() = "title"]')
    if title:
        text_parts.append(' '.join(title[0].itertext()).strip())
    paragraphs = root.xpath('//*[local-name() = "p"]')
    for paragraph in paragraphs:
        text_parts.append(' '.join(paragraph.itertext()).strip())
    return '\n\n'.join(text_parts)

def get_paper_info(query, rows=10):
    base_url = 'https://api.crossref.org/works'
    params = {
        'query': query,
        'rows': rows,
        'filter': 'has-abstract:true',
        'order': 'desc'
    }

    params_relevance = params.copy()
    params_relevance['sort'] = 'relevance'
    response_relevance = requests.get(base_url, params=params_relevance)

    if response_relevance.status_code == 200:
        data_relevance = response_relevance.json()

        merged_abstracts = []
        for paper in data_relevance.get('message', {}).get('items', []):
            if paper.get('abstract'):
                title = paper.get('title')[0]
                abstract = jats_to_plain_text(paper.get('abstract'))
                url = paper['URL']
                citation_count = paper['is-referenced-by-count']
                merged_abstracts.append((title, abstract, url, citation_count))

        merged_abstracts.sort(key=lambda x: x[3], reverse=True)

        return merged_abstracts
    else:
        print("Failed to retrieve data for sorting by relevance.")
        return []

