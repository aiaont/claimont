# Claimont

## Claim Ontology

An ontology for describing claims and their substantiation.

**Namespace**: `https://w3id.org/claimont#`

## Overview

The Claimont ontology provides a formal vocabulary for representing claims, the entities that make them, and the evidence that supports them. It is designed to model both defeasible claims (which can be challenged or overturned) and the various forms of substantiation that support or refute them. It is meant to be used together with the Anthropogenic Impact Accounting Ontology (AIAO: https://w3id.org/aiao), the Information Communication Ontology (https://w3id.org/infocomm) and the Impact Ontology (https://w3id/org/impactont).

## Core Classes

### Primary Classes

#### Claim

A claim is a defeasible statement about a thing. Claims are the central concept of the ontology and represent assertions that can be true or false, and may be supported by evidence or challenged by counter-evidence.

- **Subclasses**:
  - `IdentityClaim`: A statement made by a claimant about their identity, usually with reference to some identification system
  - `Report`: A claim made according to some specification

#### Claimant

An entity (natural or legal person) that makes a claim. Claimants are the actors responsible for asserting claims.

#### Substantiation

A thing presented in support of the truthfulness of a claim. This represents any form of evidence, documentation, or support for a claim.

- **Subclasses**:
  - `Attestation`: An indefeasible statement, usually formal, made by an entity according to which they have witnessed or been presented with sufficient evidence to consider a specific claim made by another entity as truthful or accurate

#### Attester

An entity (person, organisation, system) that makes an attestation. Attesters provide formal statements supporting claims made by others.

### Supporting Classes

#### Subject

The thing about which a claim is made. This can be any entity in the domain.

#### Predicate

The characteristic, attribute, or relationship asserted about the subject of a claim.

#### Object

The target or value associated with the predicate in a claim.

## Key Relationships

### Core Properties

#### Authorship Properties

- `claimedBy`: Links a Claim to its Claimant
- `attestedBy`: Links an Attestation to its Attester
- `isMadeBy`: General parent property for authorship relationships

#### Claim Structure Properties

- `hasSubject`: Links a Claim or Attestation to what it is about
- `hasPredicate`: Links a Claim to the characteristic being asserted
- `hasObject`: Links a Claim to the value or target of the assertion

#### Evidence and Support Properties

- `isSupportedBy`: Links a Claim to Substantiation that backs it
- `supports`: Links Substantiation to the Claim it backs (inverse of `isSupportedBy`)
- `comprisesClaims`: Allows Claims to be composed of other Claims

## Logical Constraints

### Disjoint Classes

- `Claim` and `Substantiation` are disjoint - an entity cannot be both a claim and its own substantiation

### Property Hierarchies

- `claimedBy` and `attestedBy` are both subproperties of the general `isMadeBy` property
- `supports` and `isSupportedBy` are inverse properties

## Usage Examples

The ontology supports modeling scenarios such as:

1. **Identity Claims**: A person claiming to own a particular email address, supported by email verification
2. **Location Claims**: Someone claiming to be in a specific location, supported by airline tickets and witness testimony
3. **Attestations**: Third parties providing formal statements supporting others' claims

## File Formats

The ontology is available in multiple formats:

- **OWL/XML**: `claimont.owl` (source format)
- **JSON-LD**: `claimont.jsonld`
- **Turtle**: `claimont.ttl`
- **HTML Documentation**: `claimont.html` (human-readable)

## Examples

See `ClaimExample.owl` for concrete examples of how to use the ontology to model real-world scenarios. 
