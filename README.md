# Claimont

## Claim Ontology

An ontology for describing claims and their substantiation.

**Namespace**: `https://w3id.org/claimont#`

## Overview

The Claim Ontology provides a formal semantic framework for representing claims, the entities that make them, and the evidence that supports them. It is designed to model defeasible claims (which can be challenged or overturned) as well as the various forms of substantiation that support or refute them. It is meant to be used together with the Anthropogenic Impact Accounting Ontology (https://w3id.org/aiao), the Information Communication Ontology (https://w3id.org/infocomm) and the Impact Ontology (https://w3id/org/impactont).

## Core Classes

### Primary Classes

#### Claim

A claim is a defeasible statement about a thing. Claims are the central concept of the ontology and represent assertions that can be true or false, and may be supported by evidence or challenged by counter-evidence.

- **Subclasses**:
  - `IdentityClaim`: A statement made by a claimant about their identity, usually with reference to some identification system
  - `Report`: A claim made according to some specification

#### Claimant

An entity (e.g., a natural or legal person) that makes a claim. Claimants are the actors responsible for asserting claims.

#### Substantiation

A thing presented in support of the truthfulness of a claim. This represents any form of evidence, documentation, or support for a claim.

- **Subclasses**:
  - `Attestation`: An indefeasible statement, usually formal, made by an entity according to which they have witnessed or been presented with sufficient evidence to consider a specific claim made by another entity as truthful or accurate

#### Attester

An entity (e.g., a natural or legal person) that makes an attestation. Attesters provide formal statements supporting claims made by other entities.

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

#### Claim Structure Properties

- `hasSubject`: Links a Claim or Attestation to what it is about
- `hasPredicate`: Links a Claim to the characteristic, attribute or relationship being asserted
- `hasObject`: Links a Claim to the value or target of the assertion

#### Evidence and Support Properties

- `isSupportedBy`: Links a Claim to the Substantiation that backs it
- `supports`: Links a Substantiation to the Claim that it backs (inverse of `isSupportedBy`)
- `comprisesClaims`: Allows Claims to be composed of other Claims

## Logical Constraints

### Disjoint Classes

- `Claim` and `Substantiation` are disjoint - an entity cannot be both a claim and its own substantiation

### Property Hierarchies

- `supports` and `isSupportedBy` are inverse properties

## Usage Examples

The ontology supports modeling scenarios such as:

1. **Identity Claims**: A person claiming to own a particular email address, supported by email verification.
2. **Location Claims**: Someone claiming to have been in a specific location at a specific time, supported by airline tickets and witness testimony.
3. **Attestations**: Third parties providing formal statements supporting others' claims.

## File Formats

The ontology is available in multiple formats:

- **OWL/XML**: `claimont.owl` (source format)
- **JSON-LD**: `claimont.jsonld`
- **Turtle**: `claimont.ttl`
- **HTML Documentation**: `claimont.html` (human-readable)

## Examples

See `ClaimExample.owl` for concrete examples of how to use the ontology to model real-world scenarios. 

