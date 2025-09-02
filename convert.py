#!/usr/bin/env python3

import sys
import os
from typing import Any, Dict, List, Optional, Set, Tuple

import rdflib
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS
from jinja2 import Environment, FileSystemLoader, select_autoescape


def ensure_default_prefix(g: Graph, ontology_iri: Optional[str]) -> None:
    if not ontology_iri:
        return
    base_ns = ontology_iri
    if not base_ns.endswith(('#', '/')):
        base_ns = base_ns + '#'
    try:
        g.namespace_manager.bind('', rdflib.term.URIRef(base_ns), replace=False)
    except Exception:
        pass


def compute_used_prefixes(g: Graph) -> List[Dict[str, str]]:
    nm = g.namespace_manager
    used_prefixes: Set[str] = set()
    for s, p, o in g:
        for term in (s, p, o):
            if isinstance(term, rdflib.term.URIRef):
                try:
                    prefix, _ns, _name = nm.compute_qname(term)
                    if prefix is not None:
                        used_prefixes.add(prefix)
                except Exception:
                    continue
    prefixes: List[Dict[str, str]] = []
    for prefix, ns in nm.namespaces():
        if prefix in used_prefixes:
            prefixes.append({"prefix": prefix or ':', "ns": str(ns)})
    prefixes.sort(key=lambda x: x["prefix"])
    return prefixes


def literal_by_lang(values: List[Literal], preferred: Optional[List[str]] = None) -> Tuple[Optional[Literal], List[Literal]]:
    preferred = preferred or ["en"]
    by_lang = {v.language: v for v in values if isinstance(v, Literal)}
    for lang in preferred:
        if lang in by_lang:
            return by_lang[lang], values
    # fallback: first literal if any
    return (values[0] if values else None), values


def qname(graph: Graph, term: URIRef) -> str:
    try:
        return graph.namespace_manager.normalizeUri(term)
    except Exception:
        return str(term)


def get_labels(graph: Graph, s: URIRef) -> List[Literal]:
    return [o for o in graph.objects(s, RDFS.label) if isinstance(o, Literal)]


def get_comments(graph: Graph, s: URIRef) -> List[Literal]:
    return [o for o in graph.objects(s, RDFS.comment) if isinstance(o, Literal)]


def get_definitions(graph: Graph, s: URIRef) -> List[Literal]:
    return [o for o in graph.objects(s, SKOS.definition) if isinstance(o, Literal)]


def collect_ontology_info(g: Graph) -> Dict[str, Any]:
    info: Dict[str, Any] = {}
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    if ontologies:
        ont = ontologies[0]
        info["iri"] = str(ont)
        titles = [o for o in g.objects(ont, DCTERMS.title) if isinstance(o, Literal)]
        title, _ = literal_by_lang(titles)
        info["title"] = str(title) if title else None
        descs = [o for o in g.objects(ont, DCTERMS.description) if isinstance(o, Literal)]
        desc, _ = literal_by_lang(descs)
        info["description"] = str(desc) if desc else None
    return info


def collect_classes(g: Graph) -> List[Dict[str, Any]]:
    classes: Set[URIRef] = set(s for s in g.subjects(RDF.type, OWL.Class))
    items: List[Dict[str, Any]] = []
    for s in classes:
        labels = get_labels(g, s)
        label, _ = literal_by_lang(labels)
        item = {
            "iri": str(s),
            "qname": qname(g, s),
            "label": str(label) if label else qname(g, s),
            "labels": labels,
            "definitions": get_definitions(g, s),
            "comments": get_comments(g, s),
            "subClassOf": [qname(g, o) for o in g.objects(s, RDFS.subClassOf) if isinstance(o, URIRef)],
        }
        items.append(item)
    items.sort(key=lambda x: (x["label"].lower(), x["qname"]))
    return items


def collect_properties(g: Graph) -> List[Dict[str, Any]]:
    # Gather various property types and de-duplicate
    props: Set[URIRef] = set(s for s in g.subjects(RDF.type, OWL.ObjectProperty))
    props |= set(s for s in g.subjects(RDF.type, OWL.DatatypeProperty))
    props |= set(s for s in g.subjects(RDF.type, RDF.Property))

    items: List[Dict[str, Any]] = []
    for s in props:
        labels = get_labels(g, s)
        label, _ = literal_by_lang(labels)
        inverses: Set[URIRef] = set(o for o in g.objects(s, OWL.inverseOf) if isinstance(o, URIRef))
        inverses |= set(x for x in g.subjects(OWL.inverseOf, s) if isinstance(x, URIRef))
        item = {
            "iri": str(s),
            "qname": qname(g, s),
            "label": str(label) if label else qname(g, s),
            "labels": labels,
            "definitions": get_definitions(g, s),
            "comments": get_comments(g, s),
            "domain": [qname(g, o) for o in g.objects(s, RDFS.domain) if isinstance(o, URIRef)],
            "range": [qname(g, o) for o in g.objects(s, RDFS.range) if isinstance(o, URIRef)],
            "subPropertyOf": [qname(g, o) for o in g.objects(s, RDFS.subPropertyOf) if isinstance(o, URIRef)],
            "inverses": [qname(g, i) for i in sorted(inverses, key=lambda u: qname(g, u))],
        }
        items.append(item)
    # Remove duplicates by IRI while preferring object/datatype-typed ones
    seen: Set[str] = set()
    unique_items: List[Dict[str, Any]] = []
    for item in items:
        if item["iri"] in seen:
            continue
        seen.add(item["iri"])
        unique_items.append(item)
    unique_items.sort(key=lambda x: (x["label"].lower(), x["qname"]))
    return unique_items


def render_html(g: Graph, base_name: str, output_path: str) -> None:
    env = Environment(
        loader=FileSystemLoader("docs"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = env.get_template("template.html.j2")

    ontology = collect_ontology_info(g)
    ensure_default_prefix(g, ontology.get("iri"))
    classes = collect_classes(g)
    properties = collect_properties(g)

    # Compute used prefixes by scanning all triples (subjects, predicates, objects)
    prefixes = compute_used_prefixes(g)

    html = tmpl.render(
        ontology=ontology,
        classes=classes,
        properties=properties,
        prefixes=prefixes,
        base_name=base_name,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def convert_owl(input_path: str) -> None:
    # Load RDF/OWL file
    g = Graph()
    g.parse(input_path, format='xml')

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # JSON-LD
    jsonld_path = base_name + ".jsonld"
    g.serialize(destination=jsonld_path, format='json-ld')
    print(f"Saved JSON-LD to {jsonld_path}")

    # Turtle
    ttl_path = base_name + ".ttl"
    g.serialize(destination=ttl_path, format='turtle')
    print(f"Saved Turtle to {ttl_path}")

    # Custom HTML rendering (SKOS definitions as first-class, inverse properties visible)
    html_path = os.path.join("docs", base_name + ".html")
    render_html(g, base_name, html_path)
    print(f"Saved human-readable HTML to {html_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py your_ontology.owl")
        sys.exit(1)

    convert_owl(sys.argv[1])
